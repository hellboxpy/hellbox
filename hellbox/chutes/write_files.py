from __future__ import annotations

from hellbox.chutes.chute import Chute
from hellbox.source_file import SourceFile


class WriteFiles(Chute):
    def __init__(self, path: str) -> None:
        self.path = path

    def process(self, file: SourceFile) -> SourceFile:
        return file.write(self.path)
