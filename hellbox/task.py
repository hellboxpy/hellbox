from __future__ import annotations

from hellbox.chutes.chute import Chute
from hellbox.chutes.read_files import ReadFiles
from hellbox.chutes.write_files import WriteFiles
from hellbox.runner import Runner


class Task:
    def __init__(self, name: str) -> None:
        self.name = name
        self.description: str | None = None
        self.requirements: tuple[str, ...] = ()
        self.chains: list[Chute] = []
        self.clean_dirs: list[str] = []

    def __lshift__(self, chute: Chute) -> Chute:
        self.chains.append(chute)
        return chute

    def read(self, *globs: str) -> Chute:
        return self << ReadFiles(*globs)

    def run(self) -> None:
        from .hellbox import Hellbox

        Hellbox.info("Running %s" % self.name)
        with Runner.create(clean_dirs=self.clean_dirs) as runner:
            for chute in self.chains:
                runner.run(chute, [])

    def write(self, path: str) -> WriteFiles:
        return WriteFiles(path)

    def describe(self, desc: str) -> None:
        self.description = desc

    def clean(self, path: str) -> None:
        self.clean_dirs.append(path)

    def requires(self, *requirements: str) -> None:
        self.requirements = requirements


class NullTask(Task):
    default_warning = "Trying to run default task but no default supplied"
    definition_warning = "Trying to run %s task but no definition found"

    def run(self) -> None:
        from .hellbox import Hellbox

        if self.name is None:
            warning = self.default_warning
        else:
            warning = self.definition_warning % self.name
        Hellbox.warn(warning)
