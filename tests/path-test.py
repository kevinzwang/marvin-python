import os
file = open(os.path.join(os.path.dirname(__file__), os.pardir, 'info.yaml'))
print(file.read())