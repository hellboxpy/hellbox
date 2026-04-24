import importlib.metadata


class Autoimporter(object):
    def execute(self, globals, locals):
        for mod in self.requirements:
            try:
                imported = __import__(mod, globals, locals, ["*"])
                globals[mod] = imported
            except ImportError:
                pass

    @property
    def requirements(self):
        return [
            dist.metadata["Name"].replace("-", "_")
            for dist in importlib.metadata.distributions()
        ]
