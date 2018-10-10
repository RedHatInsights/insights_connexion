from alembic import command as alembic_cmd
from alembic.config import Config as AlembicConfig
from ..config import config
import logging
import os
import shutil
from sqlalchemy import create_engine
import subprocess
from subprocess import CalledProcessError, Popen
from time import sleep

logging.basicConfig(
    level=config.log_level, format='%(asctime)s | %(levelname)s | %(message)s')

PORT = config.port


def _db_command(cmd):
    engine = create_engine('postgresql://{}:{}@{}:{}'.format(config.db_user, config.db_password,
                                                             config.db_host, config.db_port))
    conn = engine.connect()
    conn.execute('commit')
    conn.execute(cmd)
    conn.close()


def _create_db():
    logging.info('Creating database: {}'.format(config.db_name))
    _db_command('CREATE database {};'.format(config.db_name))


def _migrate_db():
    alembic_cfg = AlembicConfig('./alembic.ini')
    alembic_cfg.set_main_option(
        'sqlalchemy.url',
        'postgresql://{}:{}@{}:{}/{}'.format(config.db_user,
                                             config.db_password,
                                             config.db_host,
                                             config.db_port,
                                             config.db_name))
    alembic_cmd.upgrade(alembic_cfg, 'head')


def _drop_db():
    logging.info('Dropping database: {}'.format(config.db_name))
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


def _run_oatts():
    logging.info('Running oatts tests...')
    if not _deps_installed():
        logging.error('oatts is not installed! See the README.')
        exit(0)

    _rm_gen_dir()

    try:
        subprocess.run(['oatts', 'generate',
                        '-w', 'generated-tests',
                        '-s', 'swagger/api.spec.yaml',
                        '--host', 'localhost:{}'.format(PORT),
                        '--customValuesFile', 'test/values.json'], check=True)
        subprocess.run(
            ['mocha', '--recursive', 'generated-tests'], check=True)
    except(CalledProcessError):
        logging.error('oatts tests failed!')
    finally:
        _rm_gen_dir()


server_process = None


def _start_server():
    global server_process
    env = os.environ.copy()
    env['INSIGHTS_CONNEXION_ENV'] = 'test'
    server_process = Popen(['pipenv', 'run', 'server'], env=env)
    sleep(5)


def test():
    try:
        logging.info('Testing...')
        _create_db()
        _migrate_db()
        _start_server()
        _run_oatts()
        logging.info('Testing is done')
    except() as err:
        logging.error(err)
    finally:
        _drop_db()
        server_process.terminate()
