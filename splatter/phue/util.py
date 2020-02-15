"""Utility functions."""
import logging
import os
import platform
import sys
import http.client as httplib


logger = logging.getLogger('phue')


if platform.system() == 'Windows':
    USER_HOME = 'USERPROFILE'
else:
    USER_HOME = 'HOME'


# the default name for the configuration file
CONFIG_FILE_NAME = '.python_hue'


def config_file_path(config_file_path=None):
    if config_file_path is not None:  # user specified config file
        return config_file_path
    elif os.getenv(USER_HOME) is not None and os.access(os.getenv(USER_HOME), os.W_OK):
        return os.path.join(os.getenv(USER_HOME), CONFIG_FILE_NAME)
    elif 'iPad' in platform.machine() or 'iPhone' in platform.machine():
        return os.path.join(os.getenv(USER_HOME), 'Documents', CONFIG_FILE_NAME)
    return os.path.join(os.getcwd(), CONFIG_FILE_NAME)
