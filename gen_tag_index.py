#!/usr/bin/env python3
"""
This generates _index.md for each Hugo tag.

If you haven't already, make a directory like content/tags
to hold the _index.md for each tag.

While it's better for SEO to write a paragraph or two for each tag,
if desired, you can fill with a "noindex" meta header tag with -noindex
and the appropriate hugo partial.
"""

from __future__ import annotations
import argparse
from pathlib import Path

import hugoutils


def get_tags(path: Path, taxonomy_type: str) -> set[str]:
    files = list(path.glob("*.md"))
    dat: set[str] = set()

    for f in files:
        header = hugoutils.get_header(f)[0]
        try:
            tags = header[taxonomy_type]
        except KeyError:
            continue

        for tag in tags:
            dat.add(tag)

    return dat


def main():
    p = argparse.ArgumentParser(description="generate _index.md for taxonomies")
    p.add_argument("path", help="Hugo content path e.g. ~/site/content")
    p.add_argument("taxonomy_type", help="tags categories or similar")
    p.add_argument("-noindex", help="add noindex,noarchive meta to tag", action="store_true")
    p = p.parse_args()

    inpath = Path(p.path).expanduser()
    if not inpath.is_dir():
        raise NotADirectoryError(inpath)

    tags = get_tags(inpath, p.taxonomy_type)

    i = inpath.parts[::-1].index("content") - 1
    tag_root = inpath if i < 0 else inpath.parents[i]

    for tag in tags:
        res_index = tag_root / p.taxonomy_type / tag / "_index.md"
        if res_index.is_file():
            continue

        res_index.parent.mkdir(exist_ok=True)

        hdr = f"""---
title: {tag}
description: {tag} {p.taxonomy_type} taxonomy
"""

        if p.noindex:
            hdr += "noindex: true\n"
        hdr += "---\n"

        print("write", res_index)
        res_index.write_text(hdr)


if __name__ == "__main__":
    main()
