from __future__ import annotations

from hellbox.chutes.chute import Chute
from hellbox.source_file import SourceFile


class CompositeChute(Chute):
    def __init__(self, *chutes: Chute) -> None:
        clones = [self.__clone(c) for c in chutes]
        self.head = self.tail = clones[0]
        for chute in clones[1:]:
            self.tail = self.tail >> chute

    def __call__(self, files: list[SourceFile] | None = None) -> None:
        self.head(files)

    def to(self, chute: Chute | type[Chute]) -> Chute:
        return self.tail.to(chute)

    def __rrshift__(self, other: Chute) -> Chute:
        other.to(self.head)
        return self.tail

    def __clone(self, chute: Chute) -> Chute:
        c = object.__new__(chute.__class__)
        c.__dict__ = chute.__dict__.copy()
        return c
