import yaml
import os
import random


paths = {
    'config': os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'config.yaml'),
    'messages': os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'messages.yaml'),
    'tord': os.path.join(os.path.dirname(__file__), os.pardir, 'yaml', 'tord.yaml')
}

data = {}

def __init__():
    global data
    for key, value in paths.items():
        file = open(value)
        data[key] = yaml.safe_load(file)
        file.close()

def get(*path, default=None):
    val = data
    for key in path:
        val = val.get(key, {})

    if val != None:
        return val
    else:
        return default

def set(*path):
    d = data
    for key in path[:-2]:
        d = d.setdefault(key, {})

    d[path[-2]] = path[-1]

def add(*path):
    d = data
    for key in path[:-2]:
        d = d.setdefault(key, {})

    if path[-1] not in d.get(path[-2]):
        d.setdefault(path[-2], []).append(path[-1])

def remove(*path):
    d = data
    for key in path[:-2]:
        d = d.setdefault(key, {})

    if path[-1] in d.get(path[-2]):
        d.setdefault(path[-2], []).remove(path[-1])

"""
@param server - discord.Server
@param member - discord.User

@return - boolean, whether member is an admin of the server or not
"""
def is_admin(member):
    return (str(member) in get('config', 'admin', 'members') or any(str(role) in get('config', 'admin', 'roles') for role in member.roles))

def get_tord(mode):
    return random.choice(get('tord', mode))

def list_tord(mode):
    l = get('tord', mode)
    sl = '```\n'
    for i in l:
        sl += i + '\n'
    sl += '```'
    return sl

def dump():
    for key, value in paths.items():
        file = open(value, 'w')
        yaml.safe_dump(data[key], file, default_flow_style=False)
        file.close()

