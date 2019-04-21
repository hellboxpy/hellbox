from hellbox.chutes.chute import Chute


class WriteFiles(Chute):
    def __init__(self, path):
        self.path = path

    def run(self, files):
        return [file.write(self.path) for file in files]
