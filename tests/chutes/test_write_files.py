from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

import pytest

from hellbox.chutes.write_files import WriteFiles
from hellbox.source_file import SourceFile


@pytest.fixture
def tmp_root(tmp_path: Path) -> Path:
    return tmp_path


def make_source_file(
    tmp_root: Path, name: str = "file.txt", content: str = "hello"
) -> SourceFile:
    content_path = tmp_root / name
    content_path.write_text(content)
    return SourceFile(Path(name), content_path, tmp_root)


class TestWriteFiles:
    def test_writes_to_stage_dir(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        WriteFiles("output").process(sf)
        stage_dir = tmp_root / "stage" / quote("output", safe="")
        assert (stage_dir / "file.txt").exists()

    def test_does_not_write_to_final_dest(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        WriteFiles("output").process(sf)
        assert not (Path("output") / "file.txt").exists()

    def test_stage_dir_encodes_slashes(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        WriteFiles("path/to/output").process(sf)
        stage_dir = tmp_root / "stage" / quote("path/to/output", safe="")
        assert (stage_dir / "file.txt").exists()

    def test_returns_source_file_in_stage(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        result = WriteFiles("output").process(sf)
        assert str(tmp_root / "stage") in str(result.content_path)

    def test_preserves_original_path(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        result = WriteFiles("output").process(sf)
        assert result.original_path == Path("file.txt")

    def test_multiple_files_same_dest(self, tmp_root: Path) -> None:
        sf1 = make_source_file(tmp_root, "a.txt", "aaa")
        sf2 = make_source_file(tmp_root, "b.txt", "bbb")
        WriteFiles("output").process(sf1)
        WriteFiles("output").process(sf2)
        stage_dir = tmp_root / "stage" / quote("output", safe="")
        assert (stage_dir / "a.txt").exists()
        assert (stage_dir / "b.txt").exists()

    def test_writes_directory_to_stage(self, tmp_root: Path) -> None:
        d = tmp_root / "myfont.ufo"
        d.mkdir()
        (d / "lib.plist").write_text("data")
        sf = SourceFile(Path("myfont.ufo"), d, tmp_root)
        WriteFiles("output").process(sf)
        stage_dir = tmp_root / "stage" / quote("output", safe="")
        assert (stage_dir / "myfont.ufo" / "lib.plist").read_text() == "data"
