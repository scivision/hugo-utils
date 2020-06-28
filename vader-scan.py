#!/usr/bin/env python3
"""
return VADER score (tone analysis) for Hugo blog posts

pip install vaderSentiment
"""

from pathlib import Path
import argparse
import typing as T
import pandas
import logging

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import hugoutils.header


def analyze_post(text: str) -> T.Dict[str, float]:
    analyser = SentimentIntensityAnalyzer()
    return analyser.polarity_scores(text)


def cli():
    p = argparse.ArgumentParser()
    p.add_argument("blogpath", help="directory of Markdown posts to analyze")
    p.add_argument("xlsfile", help="path of .xlsx file to write")
    p.add_argument("--only", help="part of page to analyze", choices=["title", "description"])
    P = p.parse_args()

    blog_path = Path(P.blogpath).expanduser()
    xlsx = Path(P.xlsfile).expanduser()

    if blog_path.is_file():
        files = [blog_path]
    else:
        files = list(blog_path.glob("*.md"))

    cols = ["pos", "neu", "neg", "compound"]
    if P.only:
        cols.append(P.only)

    dat = pandas.DataFrame(index=[f.stem for f in files], columns=cols)

    for i, file in enumerate(files):
        print(f"{i+1} / {len(files)} {file.stem:<80}", end="\r")

        if P.only:
            header = hugoutils.header.get_header(file)[0]
            try:
                text = header[P.only]
            except KeyError:
                logging.error(f"{file.stem} does not have {P.only}")
                continue
        else:
            text = file.read_text(errors="ignore")

        s = analyze_post(text)

        if P.only:
            dat.loc[file.stem] = [s["pos"], s["neu"], s["neg"], s["compound"], text]
        else:
            dat.loc[file.stem] = [s["pos"], s["neu"], s["neg"], s["compound"]]

    if blog_path.is_file():
        print(dat)
    else:
        dat.to_excel(xlsx)


if __name__ == "__main__":
    cli()
