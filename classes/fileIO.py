import yaml
import os

class FileIO:
    def __init__(self):
        f = open(os.path.join(os.path.dirname(__file__), os.pardir, 'data.yaml'))
        self.data = yaml.safe_load(f);
        f.close()
    def getToken(self):
        return self.data['token']
