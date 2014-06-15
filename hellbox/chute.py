class Chute(object):

    def __init__(self, func):
        self.func = func
        self.callbacks = []

    def to(self, chute):
        print "\tChute: %s" % chute
        self.callbacks.append(chute)
        return chute

def OpenFiles(*globs):

    def open_files():
        print globs
        return []

    return Chute(open_files)
