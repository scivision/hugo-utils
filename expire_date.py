#!/usr/bin/env python3
"""
append expiryDate header meta

    python expire_date.py ~/myHugoSite/content/blog
"""

import logging
import argparse
from pathlib import Path
from datetime import datetime

import hugomd


p = argparse.ArgumentParser()
p.add_argument("path", help="path of Markdown blog posts")
p.add_argument("before", help="expire dateModified before this created date  (%Y-%m-%d format)")
p.add_argument("expire_date", help="date that posts expire (%Y-%m-%d format)")
p.add_argument("-ext", help="filename suffix to sort", default=".md")
p = p.parse_args()

path = Path(p.path).expanduser()
if not path.is_dir():
    raise NotADirectoryError(path)

before = datetime.strptime(p.before, "%Y-%m-%d")
expired = datetime.strptime(p.expire_date, "%Y-%m-%d")

for f in path.rglob(f"*{p.ext}"):
    head = hugomd.get_header(f)[0]
    if head is None or "expiryDate" in head:
        continue

    create_date = datetime.strptime(head["date"][:10], "%Y-%m-%d")
    if create_date > before:
        continue

    raw = f.read_text()
    if raw[:4] != "---\n":
        logging.error(f"could not expire {f}")
        continue

    print(f"{expired:%Y-%m-%d} {f}")

    raw = (
        f"""---
expiryDate: {expired:%Y-%m-%d}
"""
        + raw[4:]
    )

    f.write_text(raw)
