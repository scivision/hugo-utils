#!/usr/bin/env python3
"""
Find singleton (orphan) categories

    python orphan_categories.py ~/myHugoSite/content/blog cats.xlsx
"""

import logging
import argparse
from pathlib import Path
import pandas

import hugoutils


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to read Markdown blog files")
    p.add_argument("xlsx", help="excel filename to write")
    p.add_argument("-n", help="show titles of more than N characters", type=int, default=60)
    p.add_argument("-ext", help="filename suffix", default=".md")
    p = p.parse_args()

    inpath = Path(p.path).expanduser()
    if not inpath.is_dir():
        raise NotADirectoryError(inpath)

    xlsx = Path(p.xlsx).expanduser()

    files = list(inpath.rglob(f"*{p.ext}"))
    dat = {}

    for f in files:
        header = hugoutils.get_header(f)[0]
        try:
            tags = header["categories"]
        except KeyError:
            continue
        except Exception as e:
            logging.error(f"{e}: {f.stem}")

        for tag in tags:
            try:
                dat[tag] += 1
            except KeyError:
                dat[tag] = 1

    pandas.DataFrame(index=dat.keys(), data=dat.values(), columns=["count"]).to_excel(xlsx)


if __name__ == "__main__":
    main()
