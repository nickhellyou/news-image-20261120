#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120.

The front page image (1024x1024, 40 stories from Friday 20 November
2026, drawn with PIL in the work session) is baked into the repository
as entry.png. This program only copies those exact bytes to the output
path, so both sandbox runs write byte-identical files. Standard library
only; no network, no clock, no randomness.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target = out_dir / "entry.png"

    data = source.read_bytes()
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1
    if not data.startswith(PNG_MAGIC):
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) < 1000:
        print("entry.png looks truncated", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
