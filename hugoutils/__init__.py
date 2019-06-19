from typing import Dict
import yaml
from pathlib import Path
from datetime import datetime, date
import re
import logging


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

    content = jfn.read_text(errors='ignore')
    pat = re.compile(r"^-{3}\s*\n([\S\s]+?)\n-{3}\s*\n([\S\s]+)")

    mat = pat.search(content)
    if not mat:
        logging.error(f'unexpected formatting-not converted: {jfn}')
        return None

    jekyll_meta = yaml.load(mat.groups()[0], Loader=yaml.BaseLoader)

    if 'date' not in jekyll_meta:
        postdate = datetime.strptime(jfn.name[:10], '%Y-%m-%d')
        jekyll_meta['date'] = postdate.strftime("%Y-%m-%d")

    write_header(hugo, jekyll_meta, fixchar)

# %% content
    content = mat.groups()[1]

    if fixchar:
        # TODO: better done with regex
        content = content.replace('```', '\n```')

    with hugo.open('a') as f:
        f.write(content)

    return hugo


def write_header(fn: Path, meta: Dict[str, str], fixchar: bool):
    """
    Parameters
    ----------
    fn: pathlib.Path
        Hugo Markdown file to write
    meta: dict of str
        Jekyll metadata to convert to Hugo metadata
    """
    with fn.open('w') as f:
        f.write('---\n')

        for key in meta:
            if not meta[key]:  # empty key
                continue

            if isinstance(meta[key], list):
                meta[key] = ' '.join(meta[key])
            elif isinstance(meta[key], bool):
                meta[key] = str(meta[key]).lower()
            elif isinstance(meta[key], (date, datetime)):
                meta[key] = meta[key].strftime("%Y-%m-%d")  # type: ignore

            if key in ('categories', 'tags'):
                f.write(f'{key}:\n')
                for v in meta[key].split(' '):
                    f.write(f'- {v}\n')
                continue

            if key == 'redirect_from':
                f.write('aliases:\n')
                for v in meta[key].split(' '):
                    f.write(f'- {v}\n')

            if key == 'published' and meta[key] == 'false':
                f.write('draft: true')
                continue

# single element keys
            if fixchar:
                line = meta[key]
                # FIXME: use str.translate
                line = line.replace(':', ' -')
                line = line.replace('(', '')
                line = line.replace(')', '')

            if key in ('summary', 'excerpt'):
                f.write(f'description: {line}\n')
            else:
                f.write(f'{key}: {line}\n')

            if not isinstance(meta[key], str):
                logging.warning(f'discarded {key} for {fn}')
                continue

        f.write('---\n\n')  # ensure blank line before content
