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
import datetime

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import hugomd


def analyze_post(text: str) -> T.Dict[str, float]:
    analyser = SentimentIntensityAnalyzer()
    return analyser.polarity_scores(text)


def cli():
    p = argparse.ArgumentParser()
    p.add_argument("blogpath", help="directory of Markdown posts to analyze")
    p.add_argument("xlsfile", help="path of .xlsx file to write")
    p.add_argument("--only", help="part of page to analyze", choices=["title", "description"])
    p.add_argument("-ext", help="filename suffix", default=".md")
    P = p.parse_args()

    blog_path = Path(P.blogpath).expanduser()
    xlsx = Path(P.xlsfile).expanduser()
    xlsx.parent.mkdir(parents=True, exist_ok=True)

    if blog_path.is_file():
        files = [blog_path]
    elif blog_path.is_dir():
        files = list(blog_path.rglob(f"*{P.ext}"))
    else:
        raise NotADirectoryError(blog_path)

    cols = ["pos", "neu", "neg", "compound"]
    if P.only:
        cols.append(P.only)

    dat = pandas.DataFrame(index=[f.stem for f in files], columns=cols)

    now = datetime.datetime.now()

    for i, file in enumerate(files):
        print(f"{i+1} / {len(files)} {file.stem:<80}", end="\r")

        header = hugomd.get_header(file)[0]
        if header is not None and "expiryDate" in header:
            if datetime.datetime.strptime(header["expiryDate"][:10], "%Y-%m-%d") < now:
                print("skip", file)
                continue

        if P.only:
            try:
                text = header[P.only]
            except TypeError:
                continue
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
