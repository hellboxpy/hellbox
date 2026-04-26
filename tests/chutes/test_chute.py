from tests.mock import Mock

from hellbox.chutes.chute import Chute
from hellbox.chutes.composite import CompositeChute


@Chute.create
def Noop(x):
    return x


@Chute.create
def Add2(x):
    return x + 2


@Chute.create
def Multiply2(x):
    return x * 2


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
        assert chute.process("input") == "path/to/file.ufo"

    def test_callbacks(self):
        f = Mock()
        chute = Chute.create(f)()
        assert chute.callbacks == []
        chute.callbacks.append("foo")
        assert "foo" in chute.callbacks

    def test_call(self):
        f = Mock(returns=2)
        f2 = Mock()
        chute = Chute.create(f)()
        chute.to(Chute.create(f2)())
        chute([1])
        assert f.called
        assert f2.called

    def test_call_filters_none(self):
        f = Mock(returns=None)
        downstream = Mock()
        chute = Chute.create(f)()
        chute.to(Chute.create(downstream)())
        chute([1])
        assert not downstream.called

    def test_call_flattens_list(self):
        f = Mock(returns=[10, 20])
        received = {}
        chute = Chute.create(f)()
        chute.to(Record("out", received))
        chute([1])
        assert received["out"] == [10, 20]

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
        CompositeChute(Add2(), Multiply2(), Record("value", output))([1])
        assert output["value"] == [6]

    def test_composite_nested_run(self):
        output = {}
        CompositeChute(
            Add2(), CompositeChute(Add2(), Multiply2()), Record("value", output)
        )([1])
        assert output["value"] == [10]

    def test_composite_prepend(self):
        foo = Add2()
        bar = Multiply2()
        qux = Noop()
        composite = CompositeChute(foo, bar)
        qux >> composite
        assert composite.head in qux.callbacks

    def test_composite_apprend(self):
        foo = Add2()
        bar = Multiply2()
        baz = Noop()
        composite = CompositeChute(foo, bar)
        composite >> baz
        assert baz in composite.tail.callbacks
