#!/usr/bin/env python3
"""
list N files from longest title to shortest

    python longest_title.py ~/myHugoSite/content/blog
"""

import argparse
import subprocess
import shutil
from pathlib import Path

import hugoutils


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to sort longest title")
    p.add_argument("-n", help="show titles of more than N characters", type=int, default=60)
    p.add_argument("-ext", help="filename suffix", default=".md")
    p.add_argument("-c", help="run program for this file", choices=["gedit", "notepad++", "code"])
    p = p.parse_args()

    inpath = Path(p.path).expanduser()
    if not inpath.is_dir():
        raise NotADirectoryError(inpath)

    if p.c:
        exe = shutil.which(p.c)
        if not exe:
            raise FileNotFoundError(f"{p.c} not found")

    for f in inpath.rglob(f"*{p.ext}"):
        title = hugoutils.get_header(f)[0]["title"]
        if len(title) > p.n:
            print((f.name, title))
            if p.c:
                subprocess.run([exe, str(f)])


if __name__ == "__main__":
    main()
