from pathlib import Path

import hugomd


def test_convert(gen_file: Path, tmp_path: Path):
    for file in gen_file.glob("*.md"):
        new = hugomd.post2hugo(file, tmp_path, True)
        assert " " not in new.name
        print("\n", new.name)
        print(new.read_text())
