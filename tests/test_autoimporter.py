from hellbox.autoimporter import Autoimporter


class TestAutoimporter(object):
    def test_init(self):
        importer = Autoimporter("./Pipfile.lock")
        assert importer.path == "./Pipfile.lock"

    def test_imports(self):
        importer = Autoimporter("./Pipfile.lock")
        importer.execute(globals(), locals())
        assert glob2
