from pathlib import Path
import logging

from .header import get_header, write_header


def post2hugo(jfn: Path, outdir: Path, fixchar: bool) -> Path:
    """
    Converts Jekyll posts to Hugo format.
    Hugo's Markdown parser is significantly stricter than Jekyll's, so you will
    likely have to do some manual fixes to the Markdown syntax here and there.

    Parameters
    ----------
    jfn : Path
        Jekyll post filename--assumes date in filename
    outdir : Path
        path to write converted post to.
    fixchar : bool
        if true, fix common metadata illegal characters such as  :=>-

    Results
    -------

    outfn : Path
        filename that was converted

    outputs converted Hugo post

    only converts front matter, does not look at content at all.
    """

    hugo = outdir / jfn.name[11:]

    if hugo.is_file():
        return None

    jekyll_header, body = get_header(jfn)
    if not jekyll_header:
        logging.error(f"not converted: {jfn}")
        return None

    write_header(hugo, jekyll_header, fixchar)

    with hugo.open("a") as f:
        f.write(body)

    return hugo
