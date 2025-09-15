from oba.oba import NotFound, Obj, raw, iterable, is_dict, is_list, is_tuple, BaseObj
from oba.path import Path
from oba.soba import Soba


def obj(object_):
    return Obj(object_)


def soba(object_, separator='.'):
    return Soba(object_, separator=separator)


__all__ = [BaseObj, NotFound, Obj, Path, Soba, obj, soba, raw, iterable, is_dict, is_list, is_tuple]
__version__ = '0.3.1'
