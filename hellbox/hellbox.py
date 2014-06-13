class Hellbox(object):
    __tasks = []

    def __init__(self, task_name, *args, **kwargs):
        self.task = Hellbox.Task(task_name)

    def __enter__(self):
        return self.task

    def __exit__(self, type, value, traceback):
        pass

    @classmethod
    def autoimport(cls):
        for mod in Hellbox.requirements():
            globals()[mod] = __import__(mod, globals(), locals(), ['*'])

    @classmethod
    def requirements(cls):
        reqs = []
        with open('requirements.txt', 'r') as f:
            reqs = [line.split('==')[0] for line in f]
        return reqs

    @classmethod
    def execute(cls, task):
        print task

    @classmethod
    def write(cls, path):
        print "\tWrites: %s" % path
        pass
        
    @classmethod
    def default(cls, tasks):
        print "Default: %s" % tasks
        pass

    class Task(object):

        def __init__(self, name):
            print "Setting up: %s" % name
            self.name = name

        def source(self, glob):
            print "\tSource: %s" % glob
            return self
            
        def to(self, chute):
            print "\tChute: %s" % chute
            return self
