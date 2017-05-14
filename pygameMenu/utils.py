# coding=utf-8
"""
Some utilitary functions.

"""

# Import libraries
import sys


def check_python_version():
    """
    Check if python version is lower than 3
    
    :return: 
    """
    if sys.version_info >= (3, 0):
        sys.stdout.write("Sorry, requires Python 2.x, not Python 3.x\n")
        sys.exit(1)
