from pathlib import Path
import typing as T
import re
from datetime import date, datetime
import logging

import yaml


def get_header(jfn: Path) -> T.Tuple[T.Dict[str, str], str]:

    pat = re.compile(r"^-{3}\s*\n([\S\s]+?)\n-{3}\s*\n([\S\s]+)")

    raw = jfn.read_text(errors="ignore")

    mat = pat.search(raw)
    if not mat:
        return (None, None)

    jekyll_header = yaml.load(mat.groups()[0], Loader=yaml.BaseLoader)

    if "date" not in jekyll_header:
        try:
            postdate = datetime.strptime(jfn.name[:10], "%Y-%m-%d")
            jekyll_header["date"] = postdate.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return jekyll_header, mat.groups()[1]


def write_header(fn: Path, meta: T.Dict[str, str], fixchar: bool):
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
