from setuptools import setup


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='pygameMenu',
    version='1.7',
    description='Menu for pygame, simple, lightweight and easy to use',
    license='GPLv3',
    author='Pablo Pizarro R.',
    author_email='pablo.pizarro@ing.uchile.cl',
    url='http://ppizarror.com/pygame-menu/',
    packages=['pygameMenu'],
    install_requires=['pygame'],
    include_package_data=True
)
