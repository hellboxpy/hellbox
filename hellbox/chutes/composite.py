from hellbox.chute import Chute


class CompositeChute(Chute):
    def __init__(self, *chutes):
        chutes = [self.__clone(c) for c in chutes]
        self.head = self.tail = chutes[0]
        for chute in chutes[1:]:
            self.tail = self.tail >> chute

    def __call__(self, *args):
        self.head(*args)

    def to(self, *args):
        self.tail.to(*args)

    def __rrshift__(self, other):
        other.to(self.head)
        return self.tail

    def __clone(self, chute):
        c = object.__new__(chute.__class__)
        c.__dict__ = chute.__dict__.copy()
        return c
