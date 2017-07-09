import yaml
import os
import random

class FileIO:
    def __init__(self):
        # add path of yaml files here for automatic processing
        self.paths = {
            'config': os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'config.yaml'),
            'messages': os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'messages.yaml'),
            'tord': os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'tord.yaml')
        }

        self.data = {}

        for key, value in self.paths.items():
            file = open(value)
            self.data[key] = yaml.safe_load(file)
            file.close()

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

    def add(self, *path):
        d = self.data
        for key in path[:-2]:
            d = d.setdefault(key, {})

        if path[-1] not in d.get(path[-2]):
            d.setdefault(path[-2], []).append(path[-1])

    def remove(self, *path):
        d = self.data
        for key in path[:-2]:
            d = d.setdefault(key, {})

        if path[-1] in d.get(path[-2]):
            d.setdefault(path[-2], []).remove(path[-1])

    """
    @param server - discord.Server
    @param member - discord.User

    @return - boolean, whether member is an admin of the server or not
    """
    def is_admin(self, member):
        return (str(member) in self.get('config', 'admin', 'members') or any(str(role) in self.get('config', 'admin', 'roles') for role in member.roles))

    def get_tord(self, mode):
        return random.choice(self.get('tord', mode))

    def list_tord(self, mode):
        l = self.get('tord', mode)
        sl = '```\n'
        for i in l:
            sl += i + '\n'
        sl += '```'
        return sl

    def dump(self):
        for key, value in self.paths.items():
            file = open(value, 'w')
            yaml.safe_dump(self.data[key], file, default_flow_style=False)
            file.close()

