#!/usr/bin/env python3
"""Copy the front-page image to the output directory.

The entry is the pre-drawn image entry.png sitting next to this script.
This program only checks that it is a real JPEG and copies it, so two
runs always produce exactly the same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    with open(SOURCE, "rb") as handle:
        head = handle.read(2)
    if head != b"\xff\xd8":
        print("entry.png is not a JPEG (missing SOI marker)", file=sys.stderr)
        sys.exit(1)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    # Confirm the copy landed intact: same size and still a JPEG.
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        print("copy size mismatch", file=sys.stderr)
        sys.exit(1)
    with open(target, "rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            print("copied file lost its JPEG marker", file=sys.stderr)
            sys.exit(1)
    print("wrote %s (%d bytes)" % (target, os.path.getsize(target)))


if __name__ == "__main__":
    main()
