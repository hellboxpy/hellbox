from hellbox.chutes.chute import Chute


class WriteFiles(Chute):
    def __init__(self, path):
        self.path = path

    def process(self, file):
        return file.write(self.path)
