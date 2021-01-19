#!/usr/bin/env python3
"""
append dateModified header meta

    python freeze_date.py ~/myHugoSite/content/blog

Need to also have Hugo config.yaml including:

frontmatter:
  lastmod:
  - lastmod
  - :default

otherwise if enableGitInfo: true, the default is that Git overrides lastmod:
"""

import logging
import argparse
from pathlib import Path
from datetime import datetime

import hugoutils


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path of Markdown blog posts")
    p.add_argument(
        "-before", help="freeze dateModified before this created date  (%Y-%m-%d format)"
    )
    p.add_argument("-ext", help="filename suffix to sort", default=".md")
    p = p.parse_args()

    path = Path(p.path).expanduser()
    if not path.is_dir():
        raise NotADirectoryError(path)

    before = datetime.strptime(p.before, "%Y-%m-%d") if p.before else None

    for f in path.glob(f"*{p.ext}"):
        head = hugoutils.get_header(f)[0]
        if "dateModified" in head:
            continue

        create_date = datetime.strptime(head["date"][:10], "%Y-%m-%d")
        if before is not None and create_date > before:
            continue

        raw = f.read_text()
        if raw[:4] != "---\n":
            logging.error(f"could not freeze {f}")
            continue

        print(f"{create_date:%Y-%m-%d} {f}")

        raw = (
            f"""---
lastmod: {create_date:%Y-%m-%d}
"""
            + raw[4:]
        )

        f.write_text(raw)


if __name__ == "__main__":
    main()
