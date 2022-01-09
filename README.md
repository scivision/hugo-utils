# Hugo Utils

![ci](https://github.com/scivision/hugo-utils/workflows/ci/badge.svg)

Utility scripts for
[converting from Jekyll to Hugo](https://www.scivision.dev/switch-jekyll-to-hugo/)
and maintaining Hugo sites.

## Convert Jekyll blog to Hugo

```sh
python -m hugotuils.jekyll2hugo -h
```

## List filenames sorted from longest to shortest

This allows shortening filename (and hence URL) of pages that may have a needlessly long filename.

```sh
python longest_filename.py -h
```
