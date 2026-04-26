import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import hellbox.chutes.chute as _chute_module
from hellbox.chutes.read_files import ReadFiles
from hellbox.chutes.write_files import WriteFiles


class Task(object):
    def __init__(self, name):
        self.name = name
        self.description = None
        self.requirements = []
        self.chains = []

    def __lshift__(self, chute):
        self.chains.append(chute)
        return chute

    def read(self, *globs):
        return self << ReadFiles(*globs)

    def run(self):
        from .hellbox import Hellbox

        Hellbox.info("Running %s" % self.name)
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as proc_exec:
            with ThreadPoolExecutor() as branch_exec:
                _chute_module._process_executor = proc_exec
                _chute_module._branch_executor = branch_exec
                try:
                    for chute in self.chains:
                        chute([])
                finally:
                    _chute_module._process_executor = None
                    _chute_module._branch_executor = None

    def write(self, path):
        return WriteFiles(path)

    def describe(self, desc):
        self.description = desc

    def requires(self, *requirements):
        self.requirements = requirements


class NullTask(Task):
    default_warning = "Trying to run default task but no default supplied"
    definition_warning = "Trying to run %s task but no definition found"

    def run(self):
        from .hellbox import Hellbox

        if self.name is None:
            warning = self.default_warning
        else:
            warning = self.definition_warning % self.name
        Hellbox.warn(warning)
