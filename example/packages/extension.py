from hellbox.chute import Chute

class BuildRoboFontExtension(Chute):
    
    def __init__(self, info_format="plist"):
        self.info_format = info_format
    
    def run(self, files):
        return files
