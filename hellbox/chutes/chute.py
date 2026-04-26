from __future__ import annotations

import inspect
from typing import Any, Self

from hellbox.source_file import SourceFile


def _collect(result: SourceFile | list[SourceFile] | None) -> list[SourceFile]:
    if result is None:
        return []
    if isinstance(result, list):
        return result
    return [result]


class Chute(object):
    __init_signature: inspect.Signature
    __init_args: tuple[Any, ...]
    __init_kwargs: dict[str, Any]

    @classmethod
    def create(cls, fn: Any) -> type[Chute]:
        def process(self: Chute, file: Any) -> Any:
            return fn(file)

        new_cls = type(fn.__name__, (cls,), {"process": process})
        new_cls.__module__ = getattr(fn, "__module__", cls.__module__)
        new_cls.__qualname__ = getattr(fn, "__qualname__", fn.__name__)
        return new_cls

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls)
        instance.__init_signature = inspect.signature(cls.__init__)
        instance.__init_args = args
        instance.__init_kwargs = kwargs
        return instance

    def __call__(self, files: list[SourceFile] | None = None) -> None:
        if files is None:
            files = []
        outputs: list[SourceFile] = []
        for f in files:
            outputs.extend(_collect(self.process(f)))
        outputs = self.flush(outputs)
        for callback in self.callbacks:
            callback(outputs)

    def __rshift__(self, other: Chute) -> Chute:
        if self.__class__ is other.__class__:
            return other.__rrshift__(self)
        return NotImplemented  # type: ignore[return-value]

    def __rrshift__(self, other: Chute) -> Chute:
        return other.to(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chute):
            return NotImplemented  # type: ignore[return-value]
        return ChuteInspector(self) == ChuteInspector(other)

    def __str__(self) -> str:
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

    def __repr__(self) -> str:
        return str(self)

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        state.pop("_Chute__callbacks", None)
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)

    def process(self, file: SourceFile) -> SourceFile | list[SourceFile] | None:
        return file

    def flush(self, files: list[SourceFile]) -> list[SourceFile]:
        return files

    def to(self, chute: Chute | type[Chute]) -> Chute:
        if inspect.isclass(chute):
            chute = chute()
        self.callbacks.append(chute)
        return chute

    @property
    def callbacks(self) -> list[Chute]:
        try:
            return self.__callbacks
        except AttributeError:
            self.__callbacks: list[Chute] = []
            return self.__callbacks


class ChuteInspector(object):
    def __init__(self, chute: Chute) -> None:
        self.chute = chute

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChuteInspector):
            return NotImplemented  # type: ignore[return-value]
        if self.chute.__class__ is not other.chute.__class__:
            return False
        return self.as_dict() == other.as_dict()

    def as_dict(self) -> dict[str, Any]:
        return {
            key: value
            for (key, value) in self.chute.__dict__.items()
            if not key.startswith("_Chute")
        }
