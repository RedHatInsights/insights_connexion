import configparser
import os
from types import SimpleNamespace
import sys


config_parser = configparser.ConfigParser()
config_parser.read('config.ini')

if sys.argv[0] == 'test/test.py':
    tag_env = 'test'
else:
    tag_env = os.environ.get('INSIGHTS_CONNEXION_ENV', 'dev')

config = config_parser[tag_env]

for key in config:
    try:
        config[key] = os.getenv(key)
    except:
        pass

config = SimpleNamespace(**config)
