from __future__ import annotations

import atexit
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import NamedTuple


class SourceFile(NamedTuple):
    original_path: Path
    content_path: Path
    tmp_root: Path

    def __str__(self) -> str:
        return str(self.display_path)

    @property
    def display_path(self) -> Path:
        return self.original_path

    def copy(self, basename: str | None = None) -> SourceFile:
        name = basename or self.content_path.name
        destination = self._make_tmp_dir() / name
        if self.content_path.is_dir():
            shutil.copytree(self.content_path, destination)
        else:
            shutil.copy2(self.content_path, destination)
        return SourceFile(self.original_path, destination, self.tmp_root)

    def transform(
        self, command_template: str, extension: str | None = None
    ) -> SourceFile:
        ext = extension or self.extension
        filename = f"{self.stem}.{ext}"

        if "{output}" in command_template:
            input_path = self.content_path
            output_path = self._make_tmp_dir() / filename
        else:
            copy = self.copy()
            input_path = copy.content_path
            output_path = copy.content_path.parent / filename

        command = command_template.format(input=input_path, output=output_path)
        subprocess.run(
            shlex.split(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

        return SourceFile(self.original_path, output_path, self.tmp_root)

    def write(self, path: str | Path) -> SourceFile:
        dest_dir = Path(path)
        dest_dir.mkdir(parents=True, exist_ok=True)
        destination = dest_dir / self.content_path.name
        if self.content_path.is_dir():
            shutil.copytree(self.content_path, destination)
        else:
            shutil.copy2(self.content_path, destination)
        return SourceFile(self.original_path, destination, self.tmp_root)

    @property
    def basename(self) -> str:
        return self.content_path.name

    @property
    def stem(self) -> str:
        return self.content_path.stem

    @property
    def directory(self) -> Path:
        return self.content_path.parent

    @property
    def extension(self) -> str:
        return self.content_path.suffix.lstrip(".")

    def _make_tmp_dir(self) -> Path:
        return Path(tempfile.mkdtemp(dir=self.tmp_root))
