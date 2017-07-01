import yaml
import os
import random

class FileIO:
    def __init__(self):
        dataFile = open(os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'data.yaml'))
        self.data = yaml.safe_load(dataFile);
        dataFile.close()

        tordFile = open(os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'tord.yaml'))
        self.tord = yaml.safe_load(tordFile);
        tordFile.close()

    def get(self, *path, default=None):
        val = self.data
        for key in path:
            val = val.get(key, {})

        if val != None:
            return val
        else:
            return default

    def set(self, *path):
        d = self.data
        for key in path[:-2]:
            d = d.setdefault(key, {})

        d[path[-2]] = path[-1]

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

    """
    @param server - discord.Server
    @param member - discord.User

    @return - boolean, whether member is an admin of the server or not
    """
    def is_admin(self, member):
        return (str(member) in self.get('admin', 'members') or any(str(role) in self.get('admin', 'roles') for role in member.roles))

    def get_tord(self, mode):
        return random.choice(self.tord.get(mode))

    def list_tord(self, mode):
        l = self.tord.get(mode)
        sl = '```\n'
        for i in l:
            sl += i + '\n'
        sl += '```'
        return sl

    def dump(self):
        file = open(os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'data.yaml'), 'w')
        yaml.safe_dump(self.data, file, default_flow_style=False)
        file.close()
