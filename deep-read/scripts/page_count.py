# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf"]
# ///
"""Print a PDF's page count. Used by deep-read to decide short vs. split path.

Usage:
    uv run scripts/page_count.py <input.pdf>
"""

import argparse
import sys

import pypdf


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_pdf")
    args = ap.parse_args()
    print(len(pypdf.PdfReader(args.input_pdf).pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
