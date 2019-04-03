class Mock(object):
    def __init__(self, returns=None):
        self.called = False
        self.returns = returns

    def __call__(self, *args):
        self.called = True
        self.args = args
        return self.returns

    @property
    def __name__(self):
        return "Mock"
