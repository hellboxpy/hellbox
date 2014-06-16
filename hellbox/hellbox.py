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
        if name is 'default':
            name = cls.default
        task = cls.find_task(name)
        task.run()

    @classmethod
    def compose(cls, *chutes):
        chutes = list(chutes)
        head = chutes[0]
        def compose_chain(chain, chute):
            return chain.to(chute)
        reduce(compose_chain, chutes)
        return head

    @classmethod
    def write(cls, path):
        return write(path)

    @classmethod
    def autoimport(cls):
        autoimport()


def write(path):
    return WriteFiles(path)


def autoimport(path='requirements.txt'):
    Autoimporter(path).execute()