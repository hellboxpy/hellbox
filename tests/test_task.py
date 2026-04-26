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
        received = {}

        class Recorder(Chute):
            def flush(self, files):
                received["files"] = files
                return files

        task = Task("foo")
        task << Recorder()
        task.run()
        assert received["files"] == []

    def test_describe(self):
        task = Task("foo")
        task.describe("something")
        assert task.description == "something"
