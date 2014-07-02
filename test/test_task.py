from __future__ import absolute_import
from hellbox.task import Task
from hellbox.chute import Chute
from mock import Mock

class TestTask(object):

    def test_init(self):
        assert Task('foo').name is 'foo'

    def test_source(self):
        task = Task('foo')
        chute = task.source('*.ufo')
        assert type(chute) is Chute
        assert chute in task.chains

    def test_run(self):
        f = Mock()
        task = Task('foo')
        task.start_chain(Chute(f))
        task.run()
        assert f.called
        assert f.args == ([],)

    def test_describe(self):
        task = Task('foo')
        task.describe('something')
        assert task.description is 'something'
