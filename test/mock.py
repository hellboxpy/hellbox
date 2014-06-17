class Mock(object):

    def __init__(self):
        self.called = False

    def __call__(self, *args):
        self.called = True
        self.args = args
