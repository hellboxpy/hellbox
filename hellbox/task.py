from .chute import Chute, OpenFiles


class Task(object):

    def __init__(self, name):
        self.name = name
        self.chains = []

    def source(self, *globs):
        return self.start_chain(OpenFiles(*globs))

    def start_chain(self, chute):
        self.chains.append(chute)
        return chute

    def run(self):
        for chute in self.chains:
            chute([])
