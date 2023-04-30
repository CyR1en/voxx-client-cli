from setuptools import setup, find_packages
from io import open
from os import path

import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if
                    ('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name='voxx-cli',
    description='A command line interface client for Voxx',
    version='1.0.2',
    packages=find_packages(),  # list of all packages
    install_requires=install_requires,
    python_requires='>=3.7',  # any python greater than 2.7
    package_data={'voxx': ['css/*.css']},
    entry_points='''
        [console_scripts]
        voxx-cli=voxx.__main__:main
    ''',
    author="CyR1en",
    keyword="voxx",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/CyR1en/voxx-client-cli',
    download_url='https://github.com/CyR1en/voxx-client-cli',
    dependency_links=dependency_links,
    author_email='ethan.bacurio@ucdenver.edu',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ]
)
