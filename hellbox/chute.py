class Chute(object):

    def __init__(self, func):
        self.func = func
        self.callbacks = []

    def __call__(self, files=None):
        files = self.func(files)
        for callback in self.callbacks:
            callback(files)

    def __repr__(self):
        return '<Chute %s>' % self.func.__name__

    def to(self, chute):
        self.callbacks.append(chute)
        return chute


def OpenFiles(*globs):
    print "\tOpens: %s" % ', '.join(globs)

    def open_files(files):
        print "Opening: %s" % ', '.join(globs)
        return []

    return Chute(open_files)


def WriteFiles(path):
    print "\tWrites: %s" % path

    def write_files(files):
        print "Writing to: %s" % path
        return files

    return Chute(write_files)
