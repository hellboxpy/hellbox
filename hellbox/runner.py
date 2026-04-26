from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from types import TracebackType

from hellbox.chutes.chute import Chute, _collect
from hellbox.source_file import SourceFile


class Runner:
    def __init__(
        self,
        process_executor: ProcessPoolExecutor[SourceFile | list[SourceFile] | None],
        branch_executor: ThreadPoolExecutor,
    ) -> None:
        self._proc = process_executor
        self._branch = branch_executor

    @classmethod
    def create(cls) -> Runner:
        return cls(
            ProcessPoolExecutor(max_workers=os.cpu_count()),
            ThreadPoolExecutor(),
        )

    def run(self, chute: Chute, files: list[SourceFile]) -> None:
        outputs = self._execute(chute, files)
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
