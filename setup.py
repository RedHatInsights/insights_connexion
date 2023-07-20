import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='insights_connexion',
    version='0.0.1',
    author='Chris Kyrouac',
    author_email='ckyrouac@redhat.com',
    description='Common boilerplate code to use connexion with a postgres '
                'database tested by oatts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RedHatInsights/insights_connexion',
    packages=setuptools.find_packages(),
    install_requires=['aiohttp==3.8.5',
                      'aiohttp-jinja2==1.1.0',
                      'alembic==1.0.1',
                      'connexion==2.3.0',
                      'factory-boy==2.11.1',
                      'gino==0.8.0',
                      'gunicorn==19.9.0',
                      'psycopg2-binary==2.7.5',
                      'python-json-logger==0.1.9',
                      'sqlalchemy==1.3.10'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
