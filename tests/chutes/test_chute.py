from pathlib import Path

from tests.mock import Mock

from hellbox.chutes.chute import Chute
from hellbox.chutes.composite import CompositeChute
from hellbox.source_file import SourceFile


@Chute.create
def Noop(x):
    return x


@Chute.create
def StepA(x):
    return SourceFile(x.original_path, Path(str(x.content_path) + ".a"), x.tmp_root)


@Chute.create
def StepB(x):
    return SourceFile(x.original_path, Path(str(x.content_path) + ".b"), x.tmp_root)


class Record(Chute):
    def __init__(self, name, env):
        self.name = name
        self.env = env

    def flush(self, files):
        self.env[self.name] = files
        return files


class TestChute(object):
    def test_init(self):
        f = Mock()
        chute = Chute.create(f)()
        assert not f.called
        assert len(chute.callbacks) == 0

    def test_process(self):
        f = Mock(returns="path/to/file.ufo")
        chute = Chute.create(f)()
        file = SourceFile(Path("input.ttf"), Path("input.ttf"), Path("/tmp"))
        assert chute.process(file) == "path/to/file.ufo"

    def test_callbacks(self):
        f = Mock()
        chute = Chute.create(f)()
        assert chute.callbacks == []
        other = Chute.create(Mock())()
        chute.callbacks.append(other)
        assert other in chute.callbacks

    def test_call(self):
        f = Mock(returns=2)
        f2 = Mock()
        chute = Chute.create(f)()
        chute.to(Chute.create(f2)())
        chute([SourceFile(Path("input.ttf"), Path("input.ttf"), Path("/tmp"))])
        assert f.called
        assert f2.called

    def test_call_filters_none(self):
        f = Mock(returns=None)
        downstream = Mock()
        chute = Chute.create(f)()
        chute.to(Chute.create(downstream)())
        chute([SourceFile(Path("input.ttf"), Path("input.ttf"), Path("/tmp"))])
        assert not downstream.called

    def test_call_flattens_list(self):
        file1 = SourceFile(Path("a.ttf"), Path("a.ttf"), Path("/tmp"))
        file2 = SourceFile(Path("b.ttf"), Path("b.ttf"), Path("/tmp"))
        f = Mock(returns=[file1, file2])
        received = {}
        chute = Chute.create(f)()
        chute.to(Record("out", received))
        chute([SourceFile(Path("input.ttf"), Path("input.ttf"), Path("/tmp"))])
        assert received["out"] == [file1, file2]

    def test_to(self):
        chute = Chute.create(Mock())()
        cb = Chute.create(Mock())()
        result = chute.to(cb)
        assert result is cb
        assert cb in chute.callbacks

    def test_rshift(self):
        chute = Chute.create(Mock())()
        cb = Chute.create(Mock())()
        result = chute >> cb
        assert result is cb
        assert cb in chute.callbacks

    def test_rshift_to_same_class(self):
        chute = Noop()
        cb = Noop()
        result = chute >> cb
        assert result is cb
        assert cb in chute.callbacks

    def test_to_with_unintialized_chute(self):
        chute = Chute.create(Mock())()
        cb = Chute.create(Mock())
        chute.to(cb)
        assert chute.callbacks
        assert isinstance(chute.callbacks[0], cb)

    def test_composite_run(self):
        output = {}
        file = SourceFile(Path("input"), Path("input"), Path("/tmp"))
        CompositeChute(StepA(), StepB(), Record("value", output))([file])
        assert output["value"][0].content_path == Path("input.a.b")

    def test_composite_nested_run(self):
        output = {}
        file = SourceFile(Path("input"), Path("input"), Path("/tmp"))
        CompositeChute(
            StepA(), CompositeChute(StepA(), StepB()), Record("value", output)
        )([file])
        assert output["value"][0].content_path == Path("input.a.a.b")

    def test_composite_prepend(self):
        foo = StepA()
        bar = StepB()
        qux = Noop()
        composite = CompositeChute(foo, bar)
        qux >> composite
        assert composite.head in qux.callbacks

    def test_composite_apprend(self):
        foo = StepA()
        bar = StepB()
        baz = Noop()
        composite = CompositeChute(foo, bar)
        composite >> baz
        assert baz in composite.tail.callbacks
