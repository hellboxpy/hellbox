import inspect

from .source_file import SourceFile


class Chute(object):
    @classmethod
    def create(cls, fn):
        def run(self, files):
            return fn(files)

        return type(fn.__name__, (cls,), {"run": run})

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init_signature = inspect.signature(cls.__init__)
        instance.__init_args = args
        instance.__init_kwargs = kwargs
        return instance

    def __call__(self, files=None):
        files = self.run(files)
        for callback in self.callbacks:
            callback(files)

    def __rrshift__(self, other):
        return other.to(self)

    def __rlshift__(self, other):
        self.to(other)
        return self

    def __eq__(self, other):
        return ChuteInspector(self) == ChuteInspector(other)

    def __str__(self):
        if self.__init_args or self.__init_kwargs:
            arguments = self.__init_signature.bind(
                self,
                *self.__init_args,
                **self.__init_kwargs
            ).arguments
            values = ", ".join(f"{a}={repr(b)}" for (a, b) in arguments.items() if a != "self")
            return f"{self.__class__.__name__}({values})"
        else:
            return self.__class__.__name__

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


class ReadFiles(Chute):
    def __init__(self, *globs):
        self.globs = globs

    def run(self, files):
        import glob2

        return [SourceFile(path, path) for g in self.globs for path in glob2.glob(g)]


class WriteFiles(Chute):
    def __init__(self, path):
        self.path = path

    def run(self, files):
        return [file.write(self.path) for file in files]


class CompositeChute(Chute):
    def __init__(self, *chutes):
        chutes = [self.__clone(c) for c in chutes]
        self.head = self.tail = chutes[0]
        for chute in chutes[1:]:
            self.tail = self.tail.to(chute)

    def to(self, *args):
        self.tail.to(*args)

    def __rrshift__(self, other):
        other.to(self.head)
        return self.tail

    def __clone(self, chute):
        c = object.__new__(chute.__class__)
        c.__dict__ = chute.__dict__.copy()
        return c


class ChuteInspector(object):
    def __init__(self, chute):
        self.chute = chute

    def __eq__(self, other):
        if self.chute.__class__ is not other.chute.__class__:
            return False

        return self.as_dict() == other.as_dict()

    def as_dict(self):
        return {
            key: value
            for (key, value) in self.chute.__dict__.items()
            if not key.startswith("_Chute")
        }
