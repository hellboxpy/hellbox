from hellbox import Hellbox, Task
from hellbox.chute import Chute


class TestHellbox:

    def test_init(self):
        h = Hellbox('foo')
        assert hasattr(h, 'task')
        assert type(h.task) is Task

    def test_find_task(self):
        Hellbox.add_task(Task('foo'))
        assert Hellbox.find_task('foo')

    def test_find_missing_task(self):
        assert Hellbox.find_task('bazzio') is None

    def test_with(self):
        with Hellbox('foo') as task: 
            assert task
            assert type(task) is Task
        assert Hellbox.find_task('foo')

    def test_get_default_task_name(self):
        Hellbox('bar')
        Hellbox.default = 'bar'
        assert Hellbox.get_task_name('default') is 'bar'

    def test_get_task_name(self):
        Hellbox('bar')
        assert Hellbox.get_task_name('bar') is 'bar'

    def test_compose_many(self):
        noop = lambda x: x
        foo = Chute(noop)
        bar = Chute(noop)
        baz = Chute(noop)
        head = Hellbox.compose(foo, bar, baz)
        assert head is foo
        assert bar in foo.callbacks
        assert baz in bar.callbacks

    def test_compose(self):
        noop = lambda x: x
        foo = Chute(noop)
        bar = Chute(noop)
        head = Hellbox.compose(foo, bar)
        assert head is foo
        assert bar in foo.callbacks

    def test_write(self):
        assert type(Hellbox.write('otf')) is Chute
