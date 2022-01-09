"""
convert Jekyll posts to Hugo posts

This is since `hugo import jekyll` just seems broken, even for Hugo 0.54

Usage example:

    python jekyll2hugo.py ~/myJekyllSite/_posts ~/myHugoSite/content/blog
"""
from argparse import ArgumentParser
from pathlib import Path
import hugoutils


p = ArgumentParser()
p.add_argument("jekyll_posts_dir", help="path to Jekyll _posts directory")
p.add_argument("out_dir", help="directory to write converted Hugo posts")
p.add_argument("-nofix", help="do not fix bad characters (Hugo might fail)", action="store_true")
p.add_argument("-v", "--verbose", action="store_true")
p = p.parse_args()

inpath = Path(p.jekyll_posts_dir).expanduser()
if not inpath.is_dir():
    raise NotADirectoryError(inpath)

outdir = Path(p.out_dir).expanduser()
outdir.mkdir(parents=True, exist_ok=True)

jlist = inpath.rglob("*.md")
for jfn in jlist:
    hfn = hugoutils.post2hugo(jfn, outdir, not p.nofix)
    if p.verbose and hfn:
        print(jfn, "=>", hfn)
