class Chute(object):

    def __init__(self, func):
        self.func = func
        self.callbacks = []

    def __call__(self, files=None):
        files = self.func(files)
        for callback in self.callbacks:
            callback(files)

    def to(self, chute):
        self.callbacks.append(chute)
        return chute

def OpenFiles(*globs):
    import glob2
    print("\tOpens: %s" % ', '.join(globs))

    def open_files(files):
        files = reduce(lambda f,g: f + glob2.glob(g), globs, files)
        print("Opening: %s" % ', '.join(files))
        return files

    return Chute(open_files)


def WriteFiles(path):
    print("\tWrites: %s" % path)

    def write_files(files):
        print("Writing to: %s" % path)
        return files

    return Chute(write_files)
