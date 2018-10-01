import configparser
import os
from types import SimpleNamespace


config_parser = configparser.ConfigParser()
config_parser.read('config.ini')

tag_env = os.environ.get('INSIGHTS_CONNEXION_ENV', 'dev')
config = config_parser[tag_env]

for key in config:
    try:
        config[key] = os.getenv(key)
    except:
        pass

config = SimpleNamespace(**config)
