import yaml
import os

class FileIO:
    def __init__(self):
        file = open(os.path.join(os.path.dirname(__file__), os.pardir, 'data.yaml'))
        self.data = yaml.safe_load(file);
        file.close()

    def get(self, key, default=None):
        val = self.data.get(key)
        if val is None and default is None:
            print('No value in data.yaml for {}. Exiting...'.format(key))
            raise SystemExit
        elif val is None:
            return default
        else:
            return val

    def set(self, key, value):
        self.data[key] = value

    def contains(self, key, value):
        if key in self.data:
            return value in self.data[key]
        else:
            return False

    def add(self, key, value):
        if not self.contains(key, value): 
            self.data.setdefault(key, []).append(value)

    def remove(self, key, value):
        if self.contains(key, value):
            self.data[key].remove(value)

    def dump(self):
        file = open(os.path.join(os.path.dirname(__file__), os.pardir, 'data.yaml'), 'w')
        yaml.safe_dump(self.data, file, default_flow_style=False)
        file.close()