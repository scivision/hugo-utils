#!/usr/bin/env python
import pytest
from pathlib import Path

import hugoutils

R = Path(__file__).parent


def test_convert(tmp_path):

    for file in R.glob("*.md"):
        new = hugoutils.post2hugo(file, tmp_path, True)
        assert " " not in new.name
        print("\n", new.name)
        print(new.read_text())


if __name__ == "__main__":
    pytest.main([__file__])
