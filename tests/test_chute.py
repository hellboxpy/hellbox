from tests.mock import Mock

from hellbox.chute import Chute, CompositeChute


class TestChute(object):
    def test_init(self):
        f = Mock()
        chute = Chute.create(f)()
        assert not f.called
        assert len(chute.callbacks) is 0

    def test_callbacks(self):
        f = Mock()
        chute = Chute.create(f)()
        assert chute.callbacks == []
        chute.callbacks.append("foo")
        assert "foo" in chute.callbacks

    def test_call(self):
        f = Mock()
        f2 = Mock()
        chute = Chute.create(f)()
        chute.to(Chute.create(f2)())
        chute()
        assert f.called
        assert f2.called

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

    def test_lshift(self):
        chute = Chute.create(Mock())()
        cb = Chute.create(Mock())()
        result = cb << chute
        assert result is chute
        assert cb in chute.callbacks

    def test_to_with_unintialized_chute(self):
        chute = Chute.create(Mock())()
        cb = Chute.create(Mock())
        chute.to(cb)
        assert chute.callbacks
        assert isinstance(chute.callbacks[0], cb)

    def test_composite_chute(self):
        noop = lambda x: x
        foo = Chute.create(noop)()
        bar = Chute.create(noop)()
        baz = Chute.create(noop)()
        qux = Chute.create(noop)()
        composite = CompositeChute(foo, bar)
        composite >> baz
        qux >> composite
        assert baz in composite.tail.callbacks
        assert composite.head in qux.callbacks
