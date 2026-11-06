"""Extract native PDF text with coordinates and render evidence crops."""

import argparse
import json
import math
import sys
from pathlib import Path


def inspect_page(page, pymupdf):
    rotation = page.rotation_matrix
    flags = pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES
    blocks = []
    for block in page.get_text("dict", flags=flags, sort=False)["blocks"]:
        if block["type"] != 0:
            continue
        lines = []
        for line in block["lines"]:
            spans = [
                {
                    "text": span["text"],
                    "bbox": list(pymupdf.Rect(span["bbox"]) * rotation),
                    "size_pt": span["size"],
                    "superscript": bool(span["flags"] & pymupdf.TEXT_FONT_SUPERSCRIPT),
                }
                for span in line["spans"]
            ]
            lines.append(
                {
                    "bbox": list(pymupdf.Rect(line["bbox"]) * rotation),
                    "text": "".join(span["text"] for span in spans),
                    "spans": spans,
                }
            )
        blocks.append(
            {
                "bbox": list(pymupdf.Rect(block["bbox"]) * rotation),
                "text": "\n".join(line["text"] for line in lines),
                "lines": lines,
            }
        )
    return {
        "pdf_page": page.number + 1,
        "page_label": page.get_label() or None,
        "bounds_pt": list(page.rect),
        "blocks": blocks,
    }


def render_page(page, args, pymupdf):
    if not 36 <= args.dpi <= 600:
        raise ValueError("--dpi must be between 36 and 600.")
    if args.output.suffix.lower() != ".png":
        raise ValueError("Output must use the .png extension.")
    region = page.rect
    if args.clip:
        if not all(math.isfinite(coordinate) for coordinate in args.clip):
            raise ValueError("--clip coordinates must be finite.")
        region = pymupdf.Rect(args.clip) & region
        if region.is_empty:
            raise ValueError("--clip must cover a visible region of the page.")
    scale = args.dpi / 72
    pixel_bounds = (region * pymupdf.Matrix(scale, scale)).irect
    if pixel_bounds.width * pixel_bounds.height > 24_000_000:
        raise ValueError("The image would exceed 24 megapixels. Crop it or reduce --dpi.")
    page.get_pixmap(dpi=args.dpi, clip=region, alpha=False).save(str(args.output))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="Write page and text-block JSON.")
    inspect.add_argument("pdf", type=Path)
    inspect.add_argument("--page", type=int, action="append", help="One-based PDF position. Repeat to select more pages.")
    inspect.add_argument("--text-only", action="store_true", help="Omit geometry for a smaller, searchable page index.")
    render = commands.add_parser("render", help="Render one page or crop to PNG.")
    render.add_argument("pdf", type=Path)
    render.add_argument("page", type=int)
    render.add_argument("output", type=Path)
    render.add_argument("--dpi", type=int, default=150)
    render.add_argument("--clip", type=float, nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    args = parser.parse_args()

    try:
        import pymupdf
    except ImportError:
        parser.exit(1, "PyMuPDF is unavailable. Use another PDF reader or renderer.\n")

    try:
        with pymupdf.open(args.pdf) as doc:
            if not doc.is_pdf:
                raise ValueError("Input must be a PDF.")
            if doc.needs_pass:
                raise ValueError("The PDF requires a password.")
            selected = args.page
            if args.command == "render":
                selected = [args.page]
            if selected is None:
                selected = range(1, len(doc) + 1)
            if any(number < 1 or number > len(doc) for number in selected):
                raise ValueError(f"PDF page positions must be between 1 and {len(doc)}.")

            if args.command == "render":
                render_page(doc[args.page - 1], args, pymupdf)
            else:
                pages = []
                for number in selected:
                    page = doc[number - 1]
                    if args.text_only:
                        pages.append({
                            "pdf_page": number,
                            "page_label": page.get_label() or None,
                            "text": page.get_text(sort=False),
                        })
                    else:
                        pages.append(inspect_page(page, pymupdf))
                output = json.dumps({"pages": pages}, ensure_ascii=False) + "\n"
                sys.stdout.buffer.write(output.encode("utf-8"))
    except (OSError, RuntimeError, ValueError) as error:
        parser.exit(1, f"PDF evidence error: {error}\n")


if __name__ == "__main__":
    main()
