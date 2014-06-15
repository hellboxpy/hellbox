from .task import Task
from .autoimporter import Autoimporter

class Hellbox(object):
    __tasks = []
    default = None
    
    def __init__(self, task_name, *args, **kwargs):
        self.task = Task(task_name)

    def __enter__(self):
        return self.task

    def __exit__(self, type, value, traceback):
        self.__class__.add_task(self.task)

    @classmethod
    def add_task(cls, task):
        cls.__tasks.append(task)

    @classmethod
    def autoimport(cls):
        autoimport()

    @classmethod
    def execute(cls, name):
        if name is 'default':
            name = cls.default
        task = (t for t in cls.__tasks if t.name == name).next()
        print task.name

    @classmethod
    def write(cls, path):
        write(path)
        pass
        
def write(path):
    print "\tWrites: %s" % path

def autoimport():
    Autoimporter('requirements.txt').execute()
