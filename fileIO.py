import yaml
import os

def getToken():
	f = open(os.path.join(os.path.dirname(__file__), 'info.yaml'))
	data = yaml.safe_load(f)
	f.close()
	return data['token']
