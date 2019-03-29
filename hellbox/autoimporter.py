import json


class Autoimporter(object):
    def __init__(self, path):
        self.path = path

    def execute(self, globals, locals):
        for mod in self.requirements:
            imported = __import__(mod, globals, locals, ["*"])
            globals[mod] = imported

    @property
    def requirements(self):
        with open(self.path, "r") as f:
            body = json.load(f)
            packages = body["default"].keys()
        return packages
