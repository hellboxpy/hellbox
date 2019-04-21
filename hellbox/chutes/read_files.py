import glob2

from hellbox.chutes.chute import Chute
from hellbox.source_file import SourceFile


class ReadFiles(Chute):
    def __init__(self, *globs):
        self.globs = globs

    def run(self, files):
        return [SourceFile(p, p) for g in self.globs for p in glob2.glob(g)]
