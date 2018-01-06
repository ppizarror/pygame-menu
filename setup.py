from setuptools import setup
from pygameMenu import __author__, __email__, __version__


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='pygameMenu',
    version=__version__,
    description='Menu for pygame, simple, lightweight and easy to use',
    long_description=long_description,
    license='GPLv3',
    author=__author__,
    author_email=__email__,
    url='http://ppizarror.com/pygame-menu/',
    packages=['pygameMenu'],
    install_requires=['pygame'],
    include_package_data=True
)
