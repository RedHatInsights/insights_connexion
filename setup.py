import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='insights-connexion',
    version='0.0.1',
    author='Chris Kyrouac',
    author_email='ckyrouac@redhat.com',
    description='Common boilerplate code to use connexion with a postgres '
                'database tested by oatts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RedHatInsights/insights-connexion',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
