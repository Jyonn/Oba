from oba.oba import NotFound, Obj
from oba.path import Path
from oba.soba import Soba


def obj(object_):
    return Obj(object_)


def soba(object_, separator='.'):
    return Soba(object_, separator=separator)


__all__ = [NotFound, Obj, Path, Soba, obj, soba]
__version__ = '0.3.0'
