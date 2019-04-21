from tests.mock import Mock

from hellbox import Chute
from hellbox.task import Task


class TestTask(object):
    def test_init(self):
        assert Task("foo").name == "foo"

    def test_open(self):
        task = Task("foo")
        chute = task.read("*.ufo")
        assert isinstance(chute, Chute)
        assert chute in task.chains

    def test_write(self):
        task = Task("foo")
        chute = task.write("ufo")
        assert isinstance(chute, Chute)

    def test_run(self):
        f = Mock()
        task = Task("foo")
        task << Chute.create(f)()
        task.run()
        assert f.called
        assert f.args == ([],)

    def test_describe(self):
        task = Task("foo")
        task.describe("something")
        assert task.description == "something"
