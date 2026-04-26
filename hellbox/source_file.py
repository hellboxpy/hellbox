from __future__ import annotations

import shlex
import shutil
import subprocess
import tempfile
from os import stat_result
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

    def copy(self, name: str | None = None) -> SourceFile:
        dest_name = name or self.name
        destination = self._make_tmp_dir() / dest_name
        if self.content_path.is_dir():
            shutil.copytree(self.content_path, destination)
        else:
            shutil.copy2(self.content_path, destination)
        return SourceFile(self.original_path, destination, self.tmp_root)

    def transform(self, command_template: str, suffix: str | None = None) -> SourceFile:
        sfx = suffix or self.suffix
        filename = f"{self.stem}{sfx}"

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
        destination = dest_dir / self.name
        if self.content_path.is_dir():
            shutil.copytree(self.content_path, destination)
        else:
            shutil.copy2(self.content_path, destination)
        return SourceFile(self.original_path, destination, self.tmp_root)

    @property
    def name(self) -> str:
        return self.content_path.name

    @property
    def stem(self) -> str:
        return self.content_path.stem

    @property
    def suffix(self) -> str:
        return self.content_path.suffix

    @property
    def suffixes(self) -> list[str]:
        return self.content_path.suffixes

    @property
    def parent(self) -> Path:
        return self.content_path.parent

    def read_text(self, encoding: str | None = None, errors: str | None = None) -> str:
        return self.content_path.read_text(encoding=encoding, errors=errors)

    def read_bytes(self) -> bytes:
        return self.content_path.read_bytes()

    def stat(self) -> stat_result:
        return self.content_path.stat()

    def exists(self) -> bool:
        return self.content_path.exists()

    def is_file(self) -> bool:
        return self.content_path.is_file()

    def is_dir(self) -> bool:
        return self.content_path.is_dir()

    def _make_tmp_dir(self) -> Path:
        return Path(tempfile.mkdtemp(dir=self.tmp_root))
