class Mock(object):
    called = False

    def __call__(self, *args):
        self.called = True
        self.args = args
