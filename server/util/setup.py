import os
import json

# get config
with open(os.path.dirname(__file__) + '/environment.json') as f:
    config = json.load(f)

# set the environments
os.environ['FLASK_APP'] = config['FLASK_APP']
os.environ['SECRET'] = config['SECRET']
os.environ['DATABASE_URI'] = config['DATABASE_URI']
os.environ['APP_SETTINGS'] = config['APP_SETTINGS']

for key in os.environ:
    print(key, '=>', os.environ[key])