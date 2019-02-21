"""
Python 3 compatibility tools.
"""
import sys

try:
    from pathlib import Path, PurePath
except ImportError:
    try:
        from pathlib2 import Path, PurePath
    except ImportError:
        Path = PurePath = None

if sys.version_info[0] >= 3:
    basestring = str
else:
    basestring = basestring


def is_pathlib_path(obj):
    """
    Check whether obj is a pathlib.Path object.
    Prefer using `isinstance(obj, os_PathLike)` instead of this function.
    """
    return Path is not None and isinstance(obj, Path)
