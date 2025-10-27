import argparse
from pathlib import Path
from PIL import Image, ImageOps
from .core import resize_image, place_image

VALID_EXTENSIONS = (".apng", ".png", ".avif", ".jpeg", ".jpg", ".jfif", ".pjpeg", ".pjp", ".svg", ".webp")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="imgfmt",
        description="Format images to a 1000x1000 white canvas"
    )

    p.add_argument("--input-dir", help="Folder with source images")
    p.add_argument("--output-dir", help="Folder to write results")
    p.add_argument("--demo", action="store_true",
                   help="Run in demo mode using internal sample directories and images")

    return p

def process_dir(input_dir: Path, output_dir: Path) -> None:

    for p in input_dir.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in VALID_EXTENSIONS:
            print(f"[SKIP] unsupported: {p.name}")
            continue
        try:
            with Image.open(p) as img:
                stem = p.stem
                img = ImageOps.exif_transpose(img)
                if img.mode in {"RGBA", "LA"} or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

                img = resize_image(img)
                result = place_image(img)

                out_path = output_dir / f"{stem}.jpg"
                result.save(out_path, "JPEG", quality=90)
                print(f"[SUCCESS] {p.name} -> {out_path.name}")
        except Exception as e:
            print(f"[ERROR] {p.name}: {e}")

def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.demo:
        root = Path(__file__).resolve().parents[2]
        input_dir = root / "samples" / "input"
        output_dir = root / "samples" / "output"
        print(f"[DEMO] Using sample folders in: \n [IN]: {input_dir}\n [OUT]: {output_dir}")

    else:
        if not args.input_dir or not args.output_dir:
            print("[ERROR]: must supply --input-dir and --output-dir (or use another valid flag such as --demo)")
            return
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
    process_dir(input_dir, output_dir)

if __name__ == "__main__":
    main()