from pathlib import Path

import hugoutils


def test_convert(gen_file: Path, tmp_path: Path):

    for file in gen_file.glob("*.md"):
        new = hugoutils.post2hugo(file, tmp_path, True)
        assert " " not in new.name
        print("\n", new.name)
        print(new.read_text())
