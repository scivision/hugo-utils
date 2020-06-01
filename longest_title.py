#!/usr/bin/env python
"""
list N files from longest title to shorted

python longest_title.py ~/myHugoSite/content/blog

Michael Hirsch, Ph.D.
"""

import argparse
from pathlib import Path

import hugoutils


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to sort longest title")
    p.add_argument("-n", help="show titles of more than N characters", type=int, default=60)
    p.add_argument("-ext", help="filename suffix", default=".md")
    p = p.parse_args()

    inpath = Path(p.path).expanduser()
    if not inpath.is_dir():
        raise NotADirectoryError(inpath)

    for f in inpath.glob(f"**/*{p.ext}"):
        title = hugoutils.get_header(f)[0]["title"]
        if len(title) > p.n:
            print((f.name, title))


if __name__ == "__main__":
    main()
