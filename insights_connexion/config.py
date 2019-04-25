from ConfigParser import SafeConfigParser
import os
from types import SimpleNamespace
import sys


config_parser = SafeConfigParser(os.environ)
config_parser.read('config.ini')

if 'test' in sys.argv[0]:
    env = 'test'
else:
    env = os.environ.get('INSIGHTS_CONNEXION_ENV', 'dev')

config = config_parser[env]

for key in config:
    try:
        config[key] = os.getenv(key)
    except:
        pass

config = SimpleNamespace(**config)
