from setuptools import setup, find_packages
from io import open
from os import path
from voxx import __app_name__, __description__, __author__, __voxx_version__
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if
                    ('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name=__app_name__,
    description=__description__,
    version=__voxx_version__,
    packages=find_packages(),  # list of all packages
    install_requires=install_requires,
    python_requires='>=3.7',  # any python greater than 2.7
    package_data={'voxx': ['css/*.css']},
    entry_points=f'''
        [console_scripts]
        {__app_name__}=voxx.__main__:main
    ''',
    author=__author__,
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
