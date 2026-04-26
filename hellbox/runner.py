from __future__ import annotations

import os
import shutil
import tempfile
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from contextvars import ContextVar
from pathlib import Path
from types import TracebackType

from hellbox.chutes.chute import Chute, _collect
from hellbox.source_file import SourceFile

# Set by Runner before firing chains; read by ReadFiles.flush() in the main process.
run_tmp_root: ContextVar[Path] = ContextVar("run_tmp_root")


class Runner:
    def __init__(
        self,
        process_executor: ProcessPoolExecutor[SourceFile | list[SourceFile] | None],
        branch_executor: ThreadPoolExecutor,
        tmp_root: Path,
    ) -> None:
        self._proc = process_executor
        self._branch = branch_executor
        self._tmp_root = tmp_root

    @classmethod
    def create(cls) -> Runner:
        return cls(
            ProcessPoolExecutor(max_workers=os.cpu_count()),
            ThreadPoolExecutor(),
            Path(tempfile.mkdtemp(prefix="hellbox-")),
        )

    def run(self, chute: Chute, files: list[SourceFile]) -> None:
        token = run_tmp_root.set(self._tmp_root)
        try:
            outputs = self._execute(chute, files)
        finally:
            run_tmp_root.reset(token)

        if len(chute.callbacks) > 1:
            futures = [
                self._branch.submit(self.run, cb, outputs) for cb in chute.callbacks
            ]
            for future in futures:
                future.result()
        else:
            for cb in chute.callbacks:
                self.run(cb, outputs)

    def _execute(self, chute: Chute, files: list[SourceFile]) -> list[SourceFile]:
        if files:
            futures = [self._proc.submit(chute.process, f) for f in files]
            outputs = [r for future in futures for r in _collect(future.result())]
        else:
            outputs = []
        return chute.flush(outputs)

    def __enter__(self) -> Runner:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._proc.shutdown(wait=True)
        self._branch.shutdown(wait=True)
        shutil.rmtree(self._tmp_root)
