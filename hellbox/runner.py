import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from hellbox.chutes.chute import _collect


class Runner:
    def __init__(self, process_executor, branch_executor):
        self._proc = process_executor
        self._branch = branch_executor

    @classmethod
    def create(cls):
        return cls(
            ProcessPoolExecutor(max_workers=os.cpu_count()),
            ThreadPoolExecutor(),
        )

    def run(self, chute, files):
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

    def _execute(self, chute, files):
        if files:
            futures = [self._proc.submit(chute.process, f) for f in files]
            outputs = [r for future in futures for r in _collect(future.result())]
        else:
            outputs = []
        return chute.flush(outputs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._proc.shutdown(wait=True)
        self._branch.shutdown(wait=True)
