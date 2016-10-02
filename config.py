import json

def load_config(fname):
	with open(fname, 'r') as f:
		data = json.load(f)
	return data