import configparser
import os
from types import SimpleNamespace
import sys


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)


config_parser = configparser.ConfigParser(interpolation=EnvInterpolation())
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
