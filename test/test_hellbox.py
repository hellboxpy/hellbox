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
        assert type(Hellbox.find_task_by_name('bazzio')) is NullTask

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
        head = Hellbox.compose(foo, bar, baz)
        assert head is foo
        assert bar in foo.callbacks
        assert baz in bar.callbacks

    def test_compose(self):
        noop = lambda x: x
        foo = Chute.create(noop)()
        bar = Chute.create(noop)()
        head = Hellbox.compose(foo, bar)
        assert head is foo
        assert bar in foo.callbacks

    def test_write(self):
        assert isinstance(Hellbox.write('otf'), Chute)

    def test_run_task(self):
        f = Mock()
        task = Task('foobaz')
        task.start_chain(Chute.create(f)())
        Hellbox.add_task(task)
        Hellbox.run_task('foobaz')
        assert f.called

    def test_proxy_decorator(self):
        @Hellbox.proxy
        def test_proxy_decorator_method(self): pass
        assert hasattr(Hellbox, 'test_proxy_decorator_method')
        assert test_proxy_decorator_method is not None
