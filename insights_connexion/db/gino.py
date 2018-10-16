from ..config import config
from gino import Gino

db = Gino()


async def init():
    await db.set_bind('postgresql://{}:{}@{}:{}/{}'.format(config.db_user,
                                                           config.db_password,
                                                           config.db_host,
                                                           config.db_port,
                                                           config.db_name))


async def disconnect():
    db.pop_bind().close()
