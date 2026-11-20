#!/usr/bin/env python3
"""Publish the news-image entry to the make.fun output directory.

The entry artwork lives next to this script as ``entry.png``.  This program
simply stages a verified copy of it where the harness expects the output:
the directory named by ``MAKEFUN_OUTPUT_DIR`` (``/output`` when unset).

Before copying, the artwork is checked so a broken or oversized file can
never be submitted by accident:

* it must start with the eight PNG magic bytes, and
* it must be no larger than 1 MiB.
"""

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1 * 1024 * 1024
SOURCE_NAME = "entry.png"


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    if not os.path.isfile(source):
        fail(f"missing artwork: {source} not found")

    with open(source, "rb") as handle:
        data = handle.read()

    if not data.startswith(PNG_MAGIC):
        fail(f"{SOURCE_NAME} does not start with PNG magic bytes")
    if len(data) > MAX_BYTES:
        fail(f"{SOURCE_NAME} is {len(data)} bytes, over the 1 MiB limit")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE_NAME)
    shutil.copyfile(source, target)

    # Verify the copy landed intact before reporting success.
    with open(target, "rb") as handle:
        copied = handle.read()
    if hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
        fail(f"copy verification failed for {target}")

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
