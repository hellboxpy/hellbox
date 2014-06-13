class Hellbox(object):
    __tasks = []

    def __init__(self, arg):
        self.arg = arg

    @classmethod
    def autoimport(cls):
        for mod in Hellbox.requirements():
            globals()[mod] = __import__(mod, globals(), locals(), ['*'])

    @classmethod
    def requirements(cls):
        return []

    @classmethod
    def execute(cls, task):
        print task
