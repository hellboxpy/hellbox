from hellbox.autoimporter import Autoimporter


class TestAutoimporter(object):
    def test_requirements(self):
        importer = Autoimporter()
        assert isinstance(importer.requirements, list)
        assert len(importer.requirements) > 0

    def test_imports(self):
        importer = Autoimporter()
        importer.execute(globals(), locals())
        assert globals()["pytest"]
