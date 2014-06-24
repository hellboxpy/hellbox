import traceback
from .task import Task, NullTask
from .chute import WriteFiles


class Hellbox(object):
    __tasks = []
    default = None

    def __init__(self, task_name, *args, **kwargs):
        self.task = Task(task_name)

    def __enter__(self):
        return self.task

    def __exit__(self, type, value, trace):
        if type is not None:
            message = "Error when setting up %s: %s\n" % (self.task.name, value)
            message += "\n".join(traceback.format_tb(trace))
            Hellbox.warn(message)
            return True # Suppresses displaying error
        else:
            Hellbox.info("Added %s" % self.task.name)
            self.__class__.add_task(self.task)

    @classmethod
    def add_task(cls, task):
        cls.__tasks.append(task)

    @classmethod
    def find_task_by_name(cls, name):
        return next((t for t in cls.__tasks if t.name == name), NullTask(name))

    @classmethod
    def run_task(cls, name):
        name = cls.get_task_name_or_default(name)
        task = cls.find_task_by_name(name)
        task.run()

    @classmethod
    def get_task_name_or_default(cls, name):
        return cls.default if name == 'default' else name

    @classmethod
    def proxy(cls, fn):
        def proxied_method(cls, *args, **kwargs): return fn(*args, **kwargs)
        setattr(cls, fn.__name__, classmethod(proxied_method))
        return fn

    @classmethod
    def inspect(cls):
        def print_chutes(chutes, indent=0):
            for chute in chutes:
                name = chute.func.__name__
                box = u"\u2517\u2501 "
                tab = len(box) * " " * indent
                print(u"%s%s%s" % (tab, box, name))
                print_chutes(chute.callbacks, indent=indent+1)
        
        for task in cls.__tasks:
            print("Task: %s" % task.name)
            print_chutes(task.chains)
            print
