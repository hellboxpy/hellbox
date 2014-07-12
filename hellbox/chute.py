import inspect

class Chute(object):

    @classmethod
    def create(cls, fn):
        def run(self, files): fn(files)
        return type(fn.__name__, (cls,), { 'run': run })

    def __call__(self, files=None):
        files = self.run(files)
        for callback in self.callbacks:
            callback(files)

    def __rrshift__(self, other):
        return other.to(self)

    def __rlshift__(self, other):
        self.to(other)
        return self

    def run(self, files):
        return files

    def to(self, chute):
        if inspect.isclass(chute):
            chute = chute()
        self.callbacks.append(chute)
        return chute

    @property
    def callbacks(self):
        try:
            return self.__callbacks
        except AttributeError:
            self.__callbacks = []
            return self.__callbacks


class OpenFiles(Chute):

    def __init__(self, *globs):
        self.globs = globs

    def run(self, files):
        import glob2
        files = [f for g in self.globs for f in glob2.glob(g)]
        return files


class WriteFiles(Chute):

    def __init__(self, path):
        self.path = path

    def write_files(files):
        return files
