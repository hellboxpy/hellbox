class Autoimporter(object):
    def __init__(self, path):
        self.path = path

    def execute(self):
        for mod in self.requirements():
            imported = __import__(mod, globals(), locals(), ["*"])
            globals()[mod] = imported

    def requirements(self):
        reqs = []
        with open(self.path, "r") as f:
            reqs = [line.split("==")[0] for line in f]
        return reqs
