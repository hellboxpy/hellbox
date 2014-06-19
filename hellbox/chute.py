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

    def open_files(files):
        files = [f for g in globs for f in glob2.glob(g)]
        return files

    return Chute(open_files)


def WriteFiles(path):

    def write_files(files):
        return files

    return Chute(write_files)
