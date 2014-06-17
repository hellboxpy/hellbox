from .task import Task
from .autoimporter import Autoimporter
from .chute import WriteFiles


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
    def find_task(cls, name):
        return next((t for t in cls.__tasks if t.name == name), None)

    @classmethod
    def run_task(cls, name):
        name = cls.get_task_name(name)
        print(name)
        task = cls.find_task(name)
        print(task)
        task.run()
        
    @classmethod
    def get_task_name(cls, name):
        return cls.default if name == 'default' else name

    @classmethod
    def compose(cls, *chutes):
        chutes = list(chutes)
        chain = head = chutes.pop(0)
        for chute in chutes:
            chain = chain.to(chute)
        return head

    @classmethod
    def write(cls, *args):
        return write(*args)

    @classmethod
    def autoimport(cls, *args):
        autoimport(*args)


def write(path):
    return WriteFiles(path)


def autoimport(path='requirements.txt'):
    Autoimporter(path).execute()
