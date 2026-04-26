from __future__ import annotations

import glob
from pathlib import Path

from hellbox.chutes.chute import Chute
from hellbox.runner import run_tmp_root
from hellbox.source_file import SourceFile


class ReadFiles(Chute):
    def __init__(self, *globs: str) -> None:
        self.globs = globs

    def flush(self, files: list[SourceFile]) -> list[SourceFile]:
        tmp_root = run_tmp_root.get()
        return [
            SourceFile(Path(p), Path(p), tmp_root)
            for g in self.globs
            for p in glob.glob(g, recursive=True)
        ]
