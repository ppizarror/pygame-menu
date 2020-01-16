# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SETUP DISTRIBUTION
Create setup for PyPi.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

# Library imports
from setuptools import setup, find_packages
import pygameMenu

# Load readme
with open('README.rst') as f:
    long_description = f.read()

# Load requirements
with open('requirements.txt') as f:
    requirements = []
    for line in f:
        requirements.append(line.strip())

# Setup library
setup(
    author=pygameMenu.__author__,
    author_email=pygameMenu.__email__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia',
        'Topic :: Software Development :: Libraries :: pygame',
        'Topic :: Text Processing',
    ],
    description=pygameMenu.__description__,
    include_package_data=True,
    install_requires=requirements,
    keywords=pygameMenu.__keywords__,
    license=pygameMenu.__license__,
    long_description=long_description,
    name='pygame-menu',
    packages=find_packages(exclude=["test"]),
    platforms=['any'],
    project_urls={
        'Bug Tracker': pygameMenu.__url_bug_tracker__,
        'Documentation': pygameMenu.__url_documentation__,
        'Source Code': pygameMenu.__url_source_code__,
    },
    python_requires='>=2.7',
    url=pygameMenu.__url__,
    version=pygameMenu.__version__
)
