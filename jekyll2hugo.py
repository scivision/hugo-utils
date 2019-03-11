#!/usr/bin/env python
"""
convert Jekyll posts to Hugo posts, using Python >= 3.6

This is since `hugo import jekyll` just seems broken, even for Hugo 0.54

Usage example:

python jekyll2hugo.py ~/myJekyllSite/_posts ~/myHugoSite/content/blog

Michael Hirsch, Ph.D.
"""
from argparse import ArgumentParser
from typing import Optional
import yaml
from pathlib import Path
from datetime import datetime
import re
import logging
import sys

if sys.version_info < (3, 6):
    raise RuntimeError('Python >= 3.6 required')


def post2hugo(jfn: Path, outdir: Path, fixchar: bool = True) -> Optional[Path]:
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

    postdate = datetime.strptime(jfn.name[:10], '%Y-%m-%d')

    hfn = outdir / jfn.name[11:]

    if hfn.is_file():
        return None

    with jfn.open('r') as f:
        pat = re.compile(r"^-{3}\s*\n([\S\s]+?)\n-{3}\s*\n([\S\s]+)")
        content = f.read()
        mat = pat.search(content)
        if not mat:
            logging.error(f'unexpected formatting-not converted: {jfn}')
            return None

        ydict = yaml.load(mat.groups()[0])

    with hfn.open('w') as f:
        f.write('---\n')
        if 'date' not in ydict:
            f.write(f'date: {postdate.strftime("%Y-%m-%d")}\n')

        for key in ydict:
            if not ydict[key]:  # empty key
                continue
            if not isinstance(ydict[key], str):
                logging.warning(f'discarded {key} from {jfn}')
                continue

            if key in ('categories', 'tags'):
                f.write(f'{key}:\n')
                for v in ydict[key].split(' '):
                    f.write(f'- {v}\n')
                continue

            if key == 'published' and ydict[key] == 'false':
                f.write('draft: true')
                continue

# single element keys
            if fixchar:
                line = ydict[key]
                # FIXME: use str.translate
                line = line.replace(':', ' -')
                line = line.replace('(', '')
                line = line.replace(')', '')

            if key in ('summary', 'excerpt'):
                f.write(f'description: {line}\n')
            else:
                f.write(f'{key}: {line}\n')

        f.write('---\n\n')  # ensure blank line before content
# %% content
        content = mat.groups()[1]

        if fixchar:
            # FIXME: could be better done with regex
            content = content.replace('```', '\n```')

        f.write(content)

    return hfn


def main():
    p = ArgumentParser()
    p.add_argument('jekyll_posts_dir', help='path to Jekyll _posts directory')
    p.add_argument('out_dir', help='directory to write converted Hugo posts')
    p.add_argument('-v', '--verbose', action='store_true')
    p = p.parse_args()

    inpath = Path(p.jekyll_posts_dir).expanduser()
    outdir = Path(p.out_dir).expanduser()

    jlist = inpath.glob('**/*.md')
    for jfn in jlist:
        hfn = post2hugo(jfn, outdir)
        if p.verbose and hfn:
            print(jfn, '=>', hfn)


if __name__ == '__main__':
    main()
