import os
import sys


DEFAULT_EXTENSION = '.txt'


def my_remove(filename):
    if '.' not in filename:
        filename += DEFAULT_EXTENSION
    os.remove(filename)
