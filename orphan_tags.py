#!/usr/bin/env python3
"""
Find singleton (orphan) tags

    python orphan_tags.py ~/myHugoSite/content/blog tags.xlsx
"""

from __future__ import annotations
import logging
import argparse
from pathlib import Path
import pandas

import hugoutils


p = argparse.ArgumentParser()
p.add_argument("path", help="path to read Markdown blog files")
p.add_argument("xlsx", help="excel filename to write")
p.add_argument("-ext", help="filename suffix", default=".md")
p = p.parse_args()

inpath = Path(p.path).expanduser()
if not inpath.is_dir():
    raise NotADirectoryError(inpath)

xlsx = Path(p.xlsx).expanduser()

files = list(inpath.rglob(f"*{p.ext}"))
dat: dict[str, int] = {}

for f in files:
    header = hugoutils.get_header(f)[0]
    try:
        tags = header["tags"]
    except (TypeError, KeyError):
        continue
    except Exception as e:
        logging.error(f"{e}: {f.stem}")

    for tag in tags:
        try:
            dat[tag] += 1
        except KeyError:
            dat[tag] = 1

pandas.DataFrame(index=dat.keys(), data=dat.values(), columns=["count"]).to_excel(xlsx)
