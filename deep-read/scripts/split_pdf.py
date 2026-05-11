# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf"]
# ///
"""Split a PDF into N-page chunks. Used by the deep-read skill.

Usage:
    uv run scripts/split_pdf.py <input.pdf> <output_dir> [--pages-per-chunk 4]

Writes chunks named `<basename>_pp<start>-<end>.pdf` into <output_dir>.
Prints the chunk count to stdout.
"""

import argparse
import os
import sys

import pypdf


def split_pdf(input_path: str, output_dir: str, pages_per_chunk: int = 4) -> int:
    os.makedirs(output_dir, exist_ok=True)
    reader = pypdf.PdfReader(input_path)
    n = len(reader.pages)
    prefix = os.path.splitext(os.path.basename(input_path))[0]
    for start in range(0, n, pages_per_chunk):
        end = min(start + pages_per_chunk, n)
        writer = pypdf.PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])
        out_path = os.path.join(output_dir, f"{prefix}_pp{start + 1}-{end}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
    return -(-n // pages_per_chunk)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_pdf")
    ap.add_argument("output_dir")
    ap.add_argument("--pages-per-chunk", type=int, default=4)
    args = ap.parse_args()
    n_chunks = split_pdf(args.input_pdf, args.output_dir, args.pages_per_chunk)
    print(n_chunks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
