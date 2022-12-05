"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SETUP DISTRIBUTION
Create setup for PyPi.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017 Pablo Pizarro R. @ppizarror

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

from setuptools import setup, find_packages
import pygame_menu

# Load readme
with open('README.rst') as f:
    long_description = f.read()

# Load requirements
with open('requirements.txt') as f:
    requirements = []
    for line in f:
        requirements.append(line.strip())

requirements_docs = requirements.copy()
requirements_docs.extend([
    'sphinx',
    'sphinx-autodoc-typehints>=1.2.0',
    'sphinx-rtd-theme'
])

requirements_tests = requirements.copy()
requirements_tests.extend([
    'codecov',
    'nose2',
    # 'pyautogui'
])

# Setup library
setup(
    name=pygame_menu.__module_name__,
    version=pygame_menu.__version__,
    author=pygame_menu.__author__,
    author_email=pygame_menu.__email__,
    description=pygame_menu.__description__,
    long_description=long_description,
    url=pygame_menu.__url__,
    project_urls={
        'Bug Tracker': pygame_menu.__url_bug_tracker__,
        'Documentation': pygame_menu.__url_documentation__,
        'Source Code': pygame_menu.__url_source_code__
    },
    license=pygame_menu.__license__,
    platforms=['any'],
    keywords=pygame_menu.__keywords__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia',
        'Topic :: Software Development :: Libraries :: pygame',
        'Topic :: Text Processing'
    ],
    include_package_data=True,
    packages=find_packages(exclude=['test']),
    python_requires='>=3.7, <4',
    install_requires=requirements,
    extras_require={
        'docs': requirements_docs,
        'test': requirements_tests
    },
    setup_requires=[
        'setuptools',
    ],
    options={
        'bdist_wheel': {'universal': False}
    },
    entry_points={
        'pyinstaller40': ['hook-dirs = pygame_menu.__pyinstaller:get_hook_dirs']
    }
)
