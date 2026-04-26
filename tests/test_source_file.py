from __future__ import annotations

import sys
from os import stat_result
from pathlib import Path

import pytest

from hellbox.source_file import SourceFile


@pytest.fixture
def tmp_root(tmp_path: Path) -> Path:
    return tmp_path


def make_file(directory: Path, name: str = "file.txt", content: str = "hello") -> Path:
    path = directory / name
    path.write_text(content)
    return path


def make_dir(directory: Path, name: str = "mydir") -> Path:
    d = directory / name
    d.mkdir()
    (d / "a.txt").write_text("a")
    (d / "b.txt").write_text("b")
    return d


def make_source_file(
    tmp_root: Path,
    name: str = "file.txt",
    content: str = "hello",
    original_name: str | None = None,
) -> SourceFile:
    content_path = make_file(tmp_root, name, content)
    original_path = Path(original_name or name)
    return SourceFile(original_path, content_path, tmp_root)


class TestProperties:
    def test_display_path(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        assert sf.display_path == sf.original_path

    def test_str(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, original_name="src/file.txt")
        assert str(sf) == "src/file.txt"

    def test_name(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, name="hello.txt")
        assert sf.name == "hello.txt"

    def test_stem(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, name="hello.txt")
        assert sf.stem == "hello"

    def test_suffix(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, name="hello.txt")
        assert sf.suffix == ".txt"

    def test_suffixes(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, name="archive.tar.gz")
        assert sf.suffixes == [".tar", ".gz"]

    def test_parent(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, name="hello.txt")
        assert sf.parent == tmp_root


class TestInspection:
    def test_exists_true(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        assert sf.exists() is True

    def test_exists_false(self, tmp_root: Path) -> None:
        sf = SourceFile(Path("ghost.txt"), tmp_root / "ghost.txt", tmp_root)
        assert sf.exists() is False

    def test_is_file(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        assert sf.is_file() is True
        assert sf.is_dir() is False

    def test_is_dir(self, tmp_root: Path) -> None:
        d = make_dir(tmp_root)
        sf = SourceFile(Path("mydir"), d, tmp_root)
        assert sf.is_dir() is True
        assert sf.is_file() is False

    def test_stat(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        assert isinstance(sf.stat(), stat_result)

    def test_read_text(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, content="hello world")
        assert sf.read_text() == "hello world"

    def test_read_bytes(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, content="hello world")
        assert sf.read_bytes() == b"hello world"


class TestCopy:
    def test_copy_file(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, content="original")
        copied = sf.copy()
        assert copied.content_path != sf.content_path
        assert copied.content_path.read_text() == "original"

    def test_copy_preserves_original_path(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, original_name="src/file.txt")
        copied = sf.copy()
        assert copied.original_path == Path("src/file.txt")

    def test_copy_preserves_tmp_root(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root)
        copied = sf.copy()
        assert copied.tmp_root == tmp_root

    def test_copy_with_name(self, tmp_root: Path) -> None:
        sf = make_source_file(tmp_root, name="file.txt")
        copied = sf.copy(name="renamed.txt")
        assert copied.content_path.name == "renamed.txt"
        assert copied.content_path.read_text() == "hello"

    def test_copy_directory(self, tmp_root: Path) -> None:
        d = make_dir(tmp_root)
        sf = SourceFile(Path("mydir"), d, tmp_root)
        copied = sf.copy()
        assert copied.content_path.is_dir()
        assert (copied.content_path / "a.txt").read_text() == "a"
        assert (copied.content_path / "b.txt").read_text() == "b"


class TestTransform:
    def test_transform_with_output_arg(self, tmp_root: Path) -> None:
        src = make_file(tmp_root, "input.txt", "hello")
        sf = SourceFile(Path("input.txt"), src, tmp_root)
        result = sf.transform("cp {input} {output}", suffix=".out")
        assert result.suffix == ".out"
        assert result.content_path.read_text() == "hello"

    def test_transform_without_output_arg(self, tmp_root: Path) -> None:
        # Simulate a tool that writes a sibling file next to its input (no {output}).
        script = tmp_root / "_transform.py"
        script.write_text(
            "import sys, shutil, pathlib\n"
            "p = pathlib.Path(sys.argv[1])\n"
            "shutil.copy(p, p.parent / (p.stem + '.out'))\n"
        )
        src = make_file(tmp_root, "input.txt", "hello")
        sf = SourceFile(Path("input.txt"), src, tmp_root)
        result = sf.transform(f"{sys.executable} {script} {{input}}", suffix=".out")
        assert result.suffix == ".out"
        assert result.content_path.read_text() == "hello"

    def test_transform_preserves_stem(self, tmp_root: Path) -> None:
        src = make_file(tmp_root, "hello.txt", "world")
        sf = SourceFile(Path("hello.txt"), src, tmp_root)
        result = sf.transform("cp {input} {output}", suffix=".out")
        assert result.stem == "hello"

    def test_transform_preserves_original_path(self, tmp_root: Path) -> None:
        src = make_file(tmp_root, "input.txt", "hello")
        sf = SourceFile(Path("src/input.txt"), src, tmp_root)
        result = sf.transform("cp {input} {output}", suffix=".out")
        assert result.original_path == Path("src/input.txt")

    def test_transform_default_suffix(self, tmp_root: Path) -> None:
        src = make_file(tmp_root, "file.txt", "data")
        sf = SourceFile(Path("file.txt"), src, tmp_root)
        result = sf.transform("cp {input} {output}")
        assert result.suffix == ".txt"


class TestWrite:
    def test_write_copies_file(self, tmp_root: Path, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        sf = make_source_file(tmp_root, name="file.txt", content="data")
        sf.write(dest)
        assert (dest / "file.txt").read_text() == "data"

    def test_write_creates_destination_dir(
        self, tmp_root: Path, tmp_path: Path
    ) -> None:
        dest = tmp_path / "nested" / "output"
        sf = make_source_file(tmp_root, name="file.txt")
        sf.write(dest)
        assert dest.is_dir()

    def test_write_returns_source_file_at_destination(
        self, tmp_root: Path, tmp_path: Path
    ) -> None:
        dest = tmp_path / "output"
        sf = make_source_file(tmp_root, name="file.txt", original_name="src/file.txt")
        result = sf.write(dest)
        assert result.content_path == dest / "file.txt"
        assert result.original_path == Path("src/file.txt")

    def test_write_directory(self, tmp_root: Path, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        d = make_dir(tmp_root)
        sf = SourceFile(Path("mydir"), d, tmp_root)
        result = sf.write(dest)
        assert (dest / "mydir").is_dir()
        assert (dest / "mydir" / "a.txt").read_text() == "a"
