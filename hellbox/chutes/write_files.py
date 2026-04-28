from __future__ import annotations

from urllib.parse import quote

from hellbox.chutes.chute import Chute
from hellbox.source_file import SourceFile


class WriteFiles(Chute):
    def __init__(self, path: str) -> None:
        self.path = path

    def process(self, file: SourceFile) -> SourceFile:
        stage_dir = file.tmp_root / "stage" / quote(self.path, safe="")
        return file.write(stage_dir)
