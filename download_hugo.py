#!/usr/bin/env python3
"""
Download Hugo release
"""

import sys
import platform
import json
import urllib.request
import argparse
from pathlib import Path
import tarfile
import zipfile
from io import BytesIO

p = argparse.ArgumentParser()
p.add_argument("prefix", help="install prefix for Hugo")
P = p.parse_args()

prefix = Path(P.prefix).expanduser()
prefix.mkdir(parents=True, exist_ok=True)

api = "https://api.github.com/repos/gohugoio/hugo/releases/latest"
stem = "https://github.com/gohugoio/hugo/releases/latest/download/"

# %% query API for latest release tag
with urllib.request.urlopen(api) as f:
    data = json.loads(f.read().decode())

arch = platform.machine().lower()

tag = data["tag_name"]

print("latest Hugo release:", tag)

# https://stackoverflow.com/questions/45125516/possible-values-for-uname-m
match sys.platform:
    case "darwin":
        url = stem + f"hugo_{tag[1:]}_darwin-universal.tar.gz"
    case "linux":
        match arch:
            case "aarch64":
                arch = "arm64"
            case "x86_64":
                arch = "amd64"
        url = stem + f"hugo_{tag[1:]}_linux-{arch}.tar.gz"
    case "win32":
        url = stem + f"hugo_{tag[1:]}_windows-{arch}.zip"
    case _:
        raise NotImplementedError(sys.platform)

# %% download and extract
print(f"{url} => {prefix}")

with urllib.request.urlopen(url) as f:
    if url.endswith(".zip"):
        with zipfile.ZipFile(BytesIO(f.read()), "r") as z:
            z.extractall(prefix)
    else:
        with tarfile.open(fileobj=f, mode="r:gz") as z:
            z.extractall(prefix)
