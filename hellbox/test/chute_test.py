from hellbox.chute import Chute
from hellbox.test.mock import Mock


class TestChute(object):

    def test_init(self):
        f = Mock()
        chute = Chute(f)
        assert chute.func is f
        assert not chute.func.called
        assert len(chute.callbacks) is 0
    
    def test_call(self):
        f = Mock()
        f2 = Mock()
        chute = Chute(f)
        chute.to(Chute(f2))
        chute()
        assert f.called
        assert f2.called

    def test_to(self):
        chute = Chute(Mock())
        cb = Chute(Mock())
        chute.to(cb)
        assert cb in chute.callbacks
