#!/usr/bin/env python3
"""
list N files from longest filename (longest URL) to shortest

    python longest_filename.py ~/myHugoSite/content/blog
"""

import argparse
from pathlib import Path


p = argparse.ArgumentParser()
p.add_argument("path", help="path to sort longest filename")
p.add_argument("-n", help="show filenames of more than N characters", type=int, default=70)
p.add_argument("-ext", help="filename suffix to sort", default=".md")
p = p.parse_args()

inpath = Path(p.path).expanduser()
if not inpath.is_dir():
    raise NotADirectoryError(inpath)

by_len = sorted((f.name for f in inpath.rglob(f"*{p.ext}") if len(f.stem) > p.n), key=len)[::-1]
for f in by_len:
    print(f)
