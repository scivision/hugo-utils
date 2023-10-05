#!/usr/bin/env python3
"""
Download Hugo release, if newer exists
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
import shutil
import subprocess
import re
from packaging import version

p = argparse.ArgumentParser()
p.add_argument("prefix", help="install prefix for Hugo")
P = p.parse_args()

prefix = Path(P.prefix).expanduser()

exist_version = None
hugo = shutil.which("hugo", path=prefix)
if hugo:
    out = subprocess.check_output([hugo, "version"], text=True)
    exist_version = out.split()[1]
    re.compile("$v([0-9.]+)")
    mat = re.match(r"^v(\d+\.\d+\.\d+)", exist_version)
    if mat:
        exist_version = mat.group(1)
    else:
        exist_version = None

prefix.mkdir(parents=True, exist_ok=True)

api = "https://api.github.com/repos/gohugoio/hugo/releases/latest"
stem = "https://github.com/gohugoio/hugo/releases/latest/download/"

# %% query API for latest release tag
with urllib.request.urlopen(api) as f:
    data = json.loads(f.read().decode())

arch = platform.machine().lower()

tag = data["tag_name"]

print("latest Hugo release:", tag[1:])
if exist_version:
    print("existing Hugo version: ", exist_version)
    if version.parse(exist_version) >= version.parse(tag[1:]):
        print("No newer version available")
        raise SystemExit
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
