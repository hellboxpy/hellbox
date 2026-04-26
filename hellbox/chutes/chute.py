import inspect

_process_executor = None
_branch_executor = None


def _collect(result):
    if result is None:
        return []
    if isinstance(result, list):
        return result
    return [result]


class Chute(object):
    @classmethod
    def create(cls, fn):
        def process(self, file):
            return fn(file)

        new_cls = type(fn.__name__, (cls,), {"process": process})
        new_cls.__module__ = getattr(fn, "__module__", cls.__module__)
        new_cls.__qualname__ = getattr(fn, "__qualname__", fn.__name__)
        return new_cls

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init_signature = inspect.signature(cls.__init__)
        instance.__init_args = args
        instance.__init_kwargs = kwargs
        return instance

    def __call__(self, files=None):
        if files is None:
            files = []

        outputs = []
        if _process_executor is not None and files:
            futures = [_process_executor.submit(self.process, f) for f in files]
            for future in futures:
                outputs.extend(_collect(future.result()))
        else:
            for f in files:
                outputs.extend(_collect(self.process(f)))

        outputs = self.flush(outputs)

        if len(self.callbacks) > 1 and _branch_executor is not None:
            futures = [_branch_executor.submit(cb, outputs) for cb in self.callbacks]
            for future in futures:
                future.result()
        else:
            for callback in self.callbacks:
                callback(outputs)

    def __rshift__(self, other):
        if self.__class__ is other.__class__:
            return other.__rrshift__(self)
        else:
            return NotImplemented

    def __rrshift__(self, other):
        return other.to(self)

    def __eq__(self, other):
        return ChuteInspector(self) == ChuteInspector(other)

    def __str__(self):
        if self.__init_args or self.__init_kwargs:
            arguments = self.__init_signature.bind(
                self, *self.__init_args, **self.__init_kwargs
            ).arguments
            values = ", ".join(
                f"{a}={repr(b)}" for (a, b) in arguments.items() if a != "self"
            )
            return f"{self.__class__.__name__}({values})"
        else:
            return self.__class__.__name__

    def __repr__(self):
        return str(self)

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("_Chute__callbacks", None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def process(self, file):
        return file

    def flush(self, files):
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
