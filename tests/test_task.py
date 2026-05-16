from hellbox import Chute
from hellbox.task import Task
from tests.mock import SentinelFlush


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

    def test_run(self, tmp_path):
        sentinel = tmp_path / "ran.txt"
        task = Task("foo")
        task << SentinelFlush(sentinel)
        task.run()
        assert sentinel.exists()

    def test_describe(self):
        task = Task("foo")
        task.describe("something")
        assert task.description == "something"

    def test_clean(self):
        task = Task("foo")
        task.clean("output")
        assert "output" in task.clean_dirs

    def test_clean_multiple(self):
        task = Task("foo")
        task.clean("output")
        task.clean("dist")
        assert task.clean_dirs == ["output", "dist"]
