from tests.mock import Mock

from hellbox import Hellbox
from hellbox.chute import Chute
from hellbox.task import Task


USAGE = """\
│ » build
│   Does the building
╽
┣━ Bar(level=2, grade=3)
┃  ┗━ Foo
┗━ Foo
   ┗━ Bar(level=2)

│ » package
│   Does the packaging
│   Zips and tars
╽
┗━ Foo
"""


Noop = Chute.create(lambda x: x)


class Foo(Chute):
    pass


class Bar(Chute):
    def __init__(self, level, grade=1):
        pass


class TestHellbox:
    def teardown(self):
        Hellbox.reset_tasks()

    def test_init(self):
        h = Hellbox("foo")
        assert hasattr(h, "task")
        assert type(h.task) is Task

    def test_find_task_by_name(self):
        Hellbox.add_task(Task("foo"))
        assert Hellbox.find_task_by_name("foo")

    def test_find_missing_task(self):
        task = Hellbox.find_task_by_name("bazzio")
        Hellbox._warn = Hellbox.warn
        Hellbox.warn = Mock()
        task.run()
        assert Hellbox.warn.called
        Hellbox.warn = Hellbox._warn

    def test_with(self):
        with Hellbox("foo") as task:
            assert task
            assert type(task) is Task
        assert Hellbox.find_task_by_name("foo")

    def test_get_default_task_name(self):
        Hellbox.default = "bar"
        assert Hellbox.get_task_name_or_default("default") == "bar"

    def test_get_task_name(self):
        assert Hellbox.get_task_name_or_default("bar") == "bar"

    def test_compose(self):
        foo = Noop()
        bar = Noop()
        composed = Hellbox.compose(foo, bar)()
        assert composed.head == foo
        assert composed.head is not foo
        assert composed.tail == bar
        assert composed.tail is not bar
        assert bar in composed.head.callbacks

    def test_compose_many(self):
        foo = Noop()
        bar = Noop()
        baz = Noop()
        composed = Hellbox.compose(foo, bar, baz)()
        assert composed.head == foo
        assert composed.tail == baz

    def test_multiple_compose(self):
        foo = Noop()
        bar = Noop()
        Composite = Hellbox.compose(foo, bar)
        composed = Composite()
        assert composed.head == foo
        assert composed.tail == bar
        composed2 = Composite()
        assert composed is not composed2
        assert composed.head is not composed2.head

    def test_run_task(self):
        f = Mock()
        task = Task("foobaz")
        task << Chute.create(f)()
        Hellbox.add_task(task)
        Hellbox.run_task("foobaz")
        assert f.called

    def test_run_task_with_requirements(self):
        f = Mock()
        f2 = Mock()
        task = Task("fooqaaz")
        task.requires("foobar")
        task << Chute.create(f)()
        task2 = Task("foobar")
        task2 << Chute.create(f2)()
        Hellbox.add_task(task)
        Hellbox.add_task(task2)
        Hellbox.run_task("fooqaaz")
        assert f2.called

    def test_proxy_decorator(self):
        @Hellbox.proxy
        def test_proxy_decorator_method(self):
            pass

        assert hasattr(Hellbox, "test_proxy_decorator_method")
        assert test_proxy_decorator_method is not None

    def test_usage(self):
        task = Task("build")
        task.describe("Does the building")
        task << (Foo() << Bar(2, grade=3))
        task << (Bar(level=2) << Foo())
        Hellbox.add_task(task)

        task = Task("package")
        task.describe("Does the packaging\nZips and tars")
        task << Foo()
        Hellbox.add_task(task)

        assert Hellbox.usage() == USAGE
