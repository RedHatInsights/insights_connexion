from alembic import command as alembic_cmd
from alembic.config import Config as AlembicConfig
import asyncio
from ..config import config
from ..db import gino
from ..logger import log
import os
import shutil
from sqlalchemy import create_engine
import subprocess
from subprocess import CalledProcessError, Popen
from time import sleep

PORT = config.port


def _db_command(cmd):
    engine = create_engine('postgresql://{}:{}@{}:{}'.format(config.db_user, config.db_password,
                                                             config.db_host, config.db_port))
    conn = engine.connect()
    conn.execute('commit')
    conn.execute(cmd)
    conn.close()


def _create_db():
    log.info('Creating database: {}'.format(config.db_name))
    _db_command('CREATE database {};'.format(config.db_name))


def _migrate_db():
    alembic_cfg = AlembicConfig('./alembic.ini')
    alembic_cmd.upgrade(alembic_cfg, 'head')


def _drop_db():
    log.info('Dropping database: {}'.format(config.db_name))
    _db_command('ALTER DATABASE {} CONNECTION LIMIT 0;'.format(
        config.db_name))
    _db_command('SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = \'{}\';'.format(
        config.db_name))
    _db_command('DROP database {};'.format(config.db_name))


def _rm_gen_dir():
    try:
        shutil.rmtree('generated-tests')
    except(FileNotFoundError):
        pass


def _deps_installed():
    return shutil.which('oatts') is not None and shutil.which('mocha') is not None


def _run_oatts(rm_gen_dir_flag):
    log.info('Running oatts tests...')
    if not _deps_installed():
        log.error('oatts is not installed! See the README.')
        exit(0)

    _rm_gen_dir()

    try:
        subprocess.run(['oatts', 'generate',
                        '-w', 'generated-tests',
                        '-s', 'swagger/api.spec.yaml',
                        '--host', 'localhost:{}'.format(PORT),
                        '--customValuesFile', 'oatts.values.json'], check=True)
        subprocess.run(
            ['mocha', '--recursive', 'generated-tests'], check=True)
    except(CalledProcessError):
        log.error('oatts tests failed!')
    finally:
        if rm_gen_dir_flag is True:
            _rm_gen_dir()


server_process = None


def _start_server():
    global server_process
    env = os.environ.copy()
    env['INSIGHTS_CONNEXION_ENV'] = 'test'
    server_process = Popen(
        ['pipenv', 'run', 'python', 'app.py'], env=env)
    sleep(5)  # TODO: poll for GET /v1 to check if the server is started instead


def _db_init(loop):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gino.init())
    loop.close()


def _run_seed():
    log.info('Seeding...')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gino.init())
    loop.run_until_complete(asyncio.gather(seed()))
    loop.close()


# this is meant to be overridden by the consuming app
async def seed():
    log.info('Skipping seed.')
    pass


# set rm_gen_dir to False to view the generated tests
def test(rm_gen_dir=True, drop_db=True):
    try:
        log.info('Testing...')
        _create_db()
        _migrate_db()
        _run_seed()
        _start_server()
        _run_oatts(rm_gen_dir)
        log.info('Testing is done')
    except() as err:
        log.error(err)
    finally:
        if drop_db is True:
            _drop_db()
        server_process.terminate()
