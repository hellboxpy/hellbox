from pathlib import Path

from hellbox import Chute


class SentinelFlush(Chute):
    """Module-level chute that writes a sentinel file when flush is called.

    Using a file rather than an instance attribute means the side effect
    crosses the subprocess boundary and is visible in the test process.
    """

    def __init__(self, path):
        self.path = str(path)

    def flush(self, files):
        Path(self.path).write_text("called")
        return files


class Mock(object):
    def __init__(self, returns=None):
        self.called = False
        self.returns = returns

    def __call__(self, *args):
        self.called = True
        self.args = args
        return self.returns

    @property
    def __name__(self):
        return "Mock"
