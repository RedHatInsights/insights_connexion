from .config import config
import logging
# from pythonjsonlogger import jsonlogger

logging.basicConfig(
    level=config.log_level, format="{'timestamp': '%(asctime)s', 'level': '%(levelname)s', 'message': %(message)s}")

log = logging

# _logHandler = logging.StreamHandler()
# _formatter = jsonlogger.JsonFormatter(
# '%(message)%(levelname)%(name)%(asctime)')
# _logHandler.setFormatter(_formatter)
# _logger = logging.getLogger()
# _logger.addHandler(_logHandler)
# _logger.setLevel(config.log_level)

# log = logging
