# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdfium2"]
# ///
"""Extract a PDF to per-page markdown for the deep-read text-only fast path.

Usage:
    uv run scripts/extract_text.py <input.pdf> <output.md>

Each page is written under a `## Page N` heading. No images, no figure
extraction — use this only for prose-only papers (commentary, perspective,
theory) where visual content does not matter.
"""

import argparse
import os
import sys

import pypdfium2 as pdfium


def extract_text(input_path: str, output_path: str) -> int:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    pdf = pdfium.PdfDocument(input_path)
    n = 0
    with open(output_path, "w") as f:
        for i, page in enumerate(pdf, start=1):
            textpage = page.get_textpage()
            f.write(f"\n\n## Page {i}\n\n")
            f.write(textpage.get_text_range())
            textpage.close()
            page.close()
            n = i
    pdf.close()
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_pdf")
    ap.add_argument("output_md")
    args = ap.parse_args()
    n = extract_text(args.input_pdf, args.output_md)
    print(n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
