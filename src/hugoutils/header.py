from __future__ import annotations
from pathlib import Path
import re
from datetime import date, datetime
import logging

import yaml


def get_header(fn: Path) -> tuple[dict[str, str], str]:

    if not fn.is_file():
        raise FileNotFoundError(fn)

    pat = re.compile(r"^-{3}\s*\n([\S\s]+?)\n-{3}\s*\n([\S\s]+)")

    raw = fn.read_text(errors="ignore")

    mat = pat.search(raw)
    if not mat:
        return (None, None)

    header = yaml.load(mat.group(1), Loader=yaml.BaseLoader)

    if "date" not in header:
        try:
            postdate = datetime.strptime(fn.name[:10], "%Y-%m-%d")
            header["date"] = postdate.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return header, mat.group(2)


def write_header(fn: Path, meta: dict[str, str], fixchar: bool):
    """
    Parameters
    ----------
    fn: pathlib.Path
        Hugo Markdown file to write
    meta: dict of str
        Jekyll metadata to convert to Hugo metadata
    fixchar: bool
        fix bad characters
    """
    with fn.open("w") as f:
        f.write("---\n")

        for key in meta:
            if not meta[key]:  # empty key
                continue

            if isinstance(meta[key], list):
                meta[key] = " ".join(meta[key])
            elif isinstance(meta[key], bool):
                meta[key] = str(meta[key]).lower()
            elif isinstance(meta[key], (date, datetime)):
                meta[key] = meta[key].strftime("%Y-%m-%d")  # type: ignore

            if key in ("categories", "tags"):
                f.write(f"{key}:\n")
                for v in meta[key].split(" "):
                    f.write(f"- {v}\n")
                continue

            if key == "redirect_from":
                f.write("aliases:\n")
                for v in meta[key].split(" "):
                    f.write(f"- {v}\n")

            if key == "published" and meta[key] == "false":
                f.write("draft: true")
                continue

            # single element keys
            if fixchar:
                line = meta[key]
                # FIXME: use str.translate
                line = line.replace(":", " -")
                line = line.replace("(", "")
                line = line.replace(")", "")

            if key in ("summary", "excerpt"):
                f.write(f"description: {line}\n")
            else:
                f.write(f"{key}: {line}\n")

            if not isinstance(meta[key], str):
                logging.warning(f"discarded {key} for {fn}")
                continue

        f.write("---\n\n")  # ensure blank line before content
