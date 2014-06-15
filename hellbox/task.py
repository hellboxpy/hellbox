from .chute import Chute, OpenFiles


class Task(object):

    def __init__(self, name):
        print "Setting up: %s" % name
        self.name = name
        self.chutes = []

    def source(self, *globs):
        chute = OpenFiles(*globs)
        self.chutes.append(chute)
        return chute

    def run(self):
        for chute in self.chutes:
            chute([])
