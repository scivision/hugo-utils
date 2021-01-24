#!/usr/bin/env python3
"""
Count headers in file "##" "###" "####"

    python most_headers.py ~/myHugoSite/content/blog
"""

import re
import argparse
import subprocess
import shutil
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to search")
    p.add_argument(
        "-n",
        help="show pages with more than N headers / file size/80 less than",
        type=int,
        default=0.5,
    )
    p.add_argument("-ext", help="filename suffix", default=".md")
    p.add_argument("-c", help="run program for this file", choices=["gedit", "notepad++", "code"])
    p = p.parse_args()

    inpath = Path(p.path).expanduser()
    if not inpath.is_dir():
        raise NotADirectoryError(inpath)

    exe = None
    if p.c:
        exe = shutil.which(p.c)
        if not exe:
            raise FileNotFoundError(f"{p.c} not found")

    head_pats = (r"(##)\s+\w+", r"(###)\s+\w+", r"\n(####)\s+\w+")
    for f in inpath.rglob(f"*{p.ext}"):
        head_count = 0
        txt = f.read_text()
        fsize = f.stat().st_size

        for pat in head_pats:
            head_count += len(re.findall(pat, txt))

        if (head_count / (fsize / 80)) > p.n:
            print((f.name, head_count, head_count / fsize))
            if exe:
                subprocess.run([exe, str(f)])


if __name__ == "__main__":
    main()
