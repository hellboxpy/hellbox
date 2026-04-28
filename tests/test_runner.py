from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

import pytest

from hellbox.runner import Runner


def stage_file(tmp_root: Path, dest: str, name: str, content: str = "data") -> None:
    stage_dir = tmp_root / "stage" / quote(dest, safe="")
    stage_dir.mkdir(parents=True, exist_ok=True)
    (stage_dir / name).write_text(content)


class TestCommit:
    def test_copies_staged_file_to_dest(self, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        runner = Runner.__new__(Runner)
        runner._tmp_root = tmp_path / "tmp"
        runner._tmp_root.mkdir()
        runner._clean_dirs = []
        stage_file(runner._tmp_root, str(dest), "file.txt", "hello")
        runner._commit()
        assert (dest / "file.txt").read_text() == "hello"

    def test_noop_when_stage_missing(self, tmp_path: Path) -> None:
        runner = Runner.__new__(Runner)
        runner._tmp_root = tmp_path / "tmp"
        runner._tmp_root.mkdir()
        runner._clean_dirs = []
        runner._commit()  # should not raise

    def test_does_not_overwrite_unstaged_files(self, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        dest.mkdir()
        (dest / "old.txt").write_text("old")
        runner = Runner.__new__(Runner)
        runner._tmp_root = tmp_path / "tmp"
        runner._tmp_root.mkdir()
        runner._clean_dirs = []
        stage_file(runner._tmp_root, str(dest), "new.txt", "new")
        runner._commit()
        assert (dest / "old.txt").read_text() == "old"
        assert (dest / "new.txt").read_text() == "new"

    def test_copies_staged_directory(self, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        runner = Runner.__new__(Runner)
        runner._tmp_root = tmp_path / "tmp"
        runner._tmp_root.mkdir()
        runner._clean_dirs = []
        stage_dir = runner._tmp_root / "stage" / quote(str(dest), safe="")
        stage_dir.mkdir(parents=True)
        ufo = stage_dir / "font.ufo"
        ufo.mkdir()
        (ufo / "lib.plist").write_text("data")
        runner._commit()
        assert (dest / "font.ufo" / "lib.plist").read_text() == "data"

    def test_encodes_slash_in_dest(self, tmp_path: Path) -> None:
        dest = tmp_path / "a" / "b"
        runner = Runner.__new__(Runner)
        runner._tmp_root = tmp_path / "tmp"
        runner._tmp_root.mkdir()
        runner._clean_dirs = []
        stage_file(runner._tmp_root, str(dest), "file.txt")
        runner._commit()
        assert (dest / "file.txt").exists()


class TestCleanDirs:
    def test_clean_dir_is_wiped_before_commit(self, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        dest.mkdir()
        (dest / "stale.txt").write_text("old")
        runner = Runner.__new__(Runner)
        runner._tmp_root = tmp_path / "tmp"
        runner._tmp_root.mkdir()
        runner._clean_dirs = [str(dest)]
        stage_file(runner._tmp_root, str(dest), "new.txt", "new")
        runner._commit()
        assert not (dest / "stale.txt").exists()
        assert (dest / "new.txt").read_text() == "new"

    def test_clean_dir_wiped_even_without_staged_files(self, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        dest.mkdir()
        (dest / "stale.txt").write_text("old")
        runner = Runner.__new__(Runner)
        runner._tmp_root = tmp_path / "tmp"
        runner._tmp_root.mkdir()
        runner._clean_dirs = [str(dest)]
        runner._commit()
        assert not (dest / "stale.txt").exists()

    def test_non_clean_dir_preserves_existing_files(self, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        dest.mkdir()
        (dest / "existing.txt").write_text("keep")
        runner = Runner.__new__(Runner)
        runner._tmp_root = tmp_path / "tmp"
        runner._tmp_root.mkdir()
        runner._clean_dirs = []
        stage_file(runner._tmp_root, str(dest), "new.txt")
        runner._commit()
        assert (dest / "existing.txt").read_text() == "keep"


class TestExitBehavior:
    def test_commits_on_success(self, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        os.chdir(tmp_path)
        with Runner.create() as runner:
            stage_file(runner._tmp_root, "output", "file.txt", "committed")
        assert (dest / "file.txt").read_text() == "committed"

    def test_discards_on_failure(self, tmp_path: Path) -> None:
        dest = tmp_path / "output"
        os.chdir(tmp_path)
        try:
            with Runner.create() as runner:
                stage_file(runner._tmp_root, "output", "file.txt", "should not appear")
                raise RuntimeError("simulated failure")
        except RuntimeError:
            pass
        assert not dest.exists()

    def test_cleans_tmp_root_on_success(self, tmp_path: Path) -> None:
        os.chdir(tmp_path)
        with Runner.create() as runner:
            tmp_root = runner._tmp_root
        assert not tmp_root.exists()

    def test_cleans_tmp_root_on_failure(self, tmp_path: Path) -> None:
        os.chdir(tmp_path)
        try:
            with Runner.create() as runner:
                tmp_root = runner._tmp_root
                raise RuntimeError("simulated failure")
        except RuntimeError:
            pass
        assert not tmp_root.exists()
