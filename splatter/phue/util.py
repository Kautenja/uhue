"""Utility functions."""
import logging
import platform
import sys


if sys.version_info[0] > 2:
    PY3K = True
else:
    PY3K = False

if PY3K:
    import http.client as httplib
else:
    import httplib


logger = logging.getLogger('phue')


if platform.system() == 'Windows':
    USER_HOME = 'USERPROFILE'
else:
    USER_HOME = 'HOME'


def is_string(data):
    """Utility method to see if data is a string."""
    if PY3K:
        return isinstance(data, str)
    else:
        return isinstance(data, str) or isinstance(data, unicode)  # noqa


def encodeString(string):
    """Utility method to encode strings as utf-8."""
    if PY3K:
        return string
    else:
        return string.encode('utf-8')


def decodeString(string):
    """Utility method to decode strings as utf-8."""
    if PY3K:
        return string
    else:
        return string.decode('utf-8')

