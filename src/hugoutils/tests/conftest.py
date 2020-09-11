import pytest
from pathlib import Path


@pytest.fixture
def gen_file(tmp_path) -> Path:
    f1 = tmp_path / "2018-03-11-internal-date.md"
    f2 = tmp_path / "2018-02-14-hi-there.md"

    f1.write_text(
        """---
date: 2018-03-11
title: This has the date in meta already
---

This post has only title and internal date."""
    )

    f2.write_text(
        """---
title: This is a test post
tags: stuff fun
categories:
- new
- way
excerpt: just testing
---


This is the article body."""
    )

    return tmp_path
