from __future__ import absolute_import
from hellbox import Hellbox
from hellbox.chute import Chute
from hellbox.task import Task, NullTask
from mock import Mock


class TestHellbox:

    def teardown(self):
        Hellbox._Hellbox__tasks = []

    def test_init(self):
        h = Hellbox('foo')
        assert hasattr(h, 'task')
        assert type(h.task) is Task

    def test_find_task_by_name(self):
        Hellbox.add_task(Task('foo'))
        assert Hellbox.find_task_by_name('foo')

    def test_find_missing_task(self):
        task = Hellbox.find_task_by_name('bazzio')
        assert type(task) is NullTask
        Hellbox._warn = Hellbox.warn
        Hellbox.warn = Mock()
        task.run()
        assert Hellbox.warn.called
        Hellbox.warn = Hellbox._warn

    def test_with(self):
        with Hellbox('foo') as task: 
            assert task
            assert type(task) is Task
        assert Hellbox.find_task_by_name('foo')

    def test_get_default_task_name(self):
        Hellbox.default = 'bar'
        assert Hellbox.get_task_name_or_default('default') is 'bar'

    def test_get_task_name(self):
        assert Hellbox.get_task_name_or_default('bar') is 'bar'

    def test_compose_many(self):
        noop = lambda x: x
        foo = Chute.create(noop)()
        bar = Chute.create(noop)()
        baz = Chute.create(noop)()
        Composite = Hellbox.compose(foo, bar, baz)
        composed = Composite()
        assert composed.head is foo
        assert composed.tail is baz
        assert bar in foo.callbacks
        assert baz in bar.callbacks

    def test_compose(self):
        noop = lambda x: x
        foo = Chute.create(noop)()
        bar = Chute.create(noop)()
        Composite = Hellbox.compose(foo, bar)
        composed = Composite()
        assert composed.head is foo
        assert composed.tail is bar
        assert bar in foo.callbacks

    def test_multiple_compose(self):
        noop = lambda x: x
        foo = Chute.create(noop)()
        bar = Chute.create(noop)()
        Composite = Hellbox.compose(foo, bar)
        composed = Composite()
        assert composed.head is foo
        assert composed.tail is bar
        assert bar in foo.callbacks
        composed2 = Composite()
        assert composed is not composed2
        # TODO: Clone initialized chutes for each composite instance
        # assert composed.head is not composed2.head

    def test_run_task(self):
        f = Mock()
        task = Task('foobaz')
        task.start_chain(Chute.create(f)())
        Hellbox.add_task(task)
        Hellbox.run_task('foobaz')
        assert f.called

    def test_run_task_with_requirements(self):
        f = Mock()
        f2 = Mock()
        task = Task('fooqaaz')
        task.requires('foobar')
        task.start_chain(Chute.create(f)())
        task2 = Task('foobar')
        task2.start_chain(Chute.create(f2)())
        Hellbox.add_task(task)
        Hellbox.add_task(task2)
        Hellbox.run_task('fooqaaz')
        assert f2.called

    def test_proxy_decorator(self):
        @Hellbox.proxy
        def test_proxy_decorator_method(self): pass
        assert hasattr(Hellbox, 'test_proxy_decorator_method')
        assert test_proxy_decorator_method is not None
