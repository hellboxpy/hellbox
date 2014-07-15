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

    default_warning = "Trying to run default task but no default supplied"
    definition_warning = "Trying to run %s task but no definition found"

    def run(self):
        from .hellbox import Hellbox
        if self.name is None:
            warning = self.default_warning
        else:
            warning = self.definition_warning % self.name
        Hellbox.warn(warning)
