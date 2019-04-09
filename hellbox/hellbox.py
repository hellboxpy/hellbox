from .task import Task, NullTask


def _print_chutes(lines, chutes, indent=""):
    for i, chute in enumerate(chutes):
        branch = "\u2523" if i+1 < len(chutes) else "\u2517"
        continuation = "\u2503" if i+1 < len(chutes) else " "
        box = f"{branch}\u2501 "
        lines.append(f"{indent}{box}{chute}")
        _print_chutes(
            lines,
            chute.callbacks,
            indent=f"{indent}{continuation}  "
        )


class Hellbox(object):
    __tasks = []
    default = None

    def __init__(self, task_name, *args, **kwargs):
        self.task = Task(task_name)

    def __enter__(self):
        return self.task

    def __exit__(self, type, value, trace):
        if type is not None:
            message = "Error when setting up %s: %s" % (self.task.name, value)
            Hellbox.error(message, trace=trace)
            return True  # Suppresses displaying error
        else:
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
        for requirement in task.requirements:
            Hellbox.run_task(requirement)
        task.run()

    @classmethod
    def get_task_name_or_default(cls, name):
        return cls.default if name == "default" else name

    @classmethod
    def proxy(cls, fn):
        def proxied_method(cls, *args, **kwargs):
            return fn(*args, **kwargs)

        setattr(cls, fn.__name__, classmethod(proxied_method))
        return fn

    @classmethod
    def inspect(cls):
        print(cls.usage())

    @classmethod
    def usage(cls):
        lines = []

        if not cls.__tasks:
            return "No tasks have been defined in Hellfile.py"

        for task in cls.__tasks:
            lines.append(f"\u2502 » {task.name}")
            if task.description:
                for line in task.description.splitlines():
                    lines.append(f"\u2502   {line}")
            lines.append("\u257D")
            _print_chutes(lines, task.chains)
            lines.append("")

        return "\n".join(lines)

    @classmethod
    def reset_tasks(cls):
        cls.__tasks = []
