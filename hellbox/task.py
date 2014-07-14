from .chute import Chute, ReadFiles


class Task(object):

    def __init__(self, name):
        self.name = name
        self.description = None
        self.requirements = []
        self.chains = []

    def read(self, *globs):
        return self.start_chain(ReadFiles(*globs))

    def start_chain(self, chute):
        self.chains.append(chute)
        return chute

    def run(self):
        from .hellbox import Hellbox
        Hellbox.info("Running %s" % self.name)
        for chute in self.chains:
            chute([])

    def describe(self, desc):
        self.description = desc

    def requires(self, *requirements):
        self.requirements = requirements


class NullTask(Task):

    def run(self):
        from .hellbox import Hellbox
        if self.name is None:
            warning = "Trying to run default task but no default supplied"
        else:
            warning = "Trying to run task %s but no definition found" % self.name
        Hellbox.warn(warning)