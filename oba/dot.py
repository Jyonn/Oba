from oba.oba import raw, NotFound, _get_path, iterable

from oba import Obj


def check_compatible(obj: dict | list | tuple):
    if isinstance(obj, dict):
        for k in obj:
            if '.' in k:
                raise ValueError(f"Key '{k}' contains a dot, which is not allowed to be wrapped by DotObj")
            check_compatible(obj[k])

    if isinstance(obj, (list, tuple)):
        for i in obj:
            check_compatible(i)


class DotObj(Obj):
    __separator__ = '.'

    def __init__(self, obj=None, path=None):
        check_compatible(obj)
        super().__init__(obj, path)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.split(self.__separator__, maxsplit=1)

        index = key[0] if isinstance(key, list) else key
        obj = raw(self)

        # noinspection PyBroadException
        try:
            value = obj.__getitem__(index)
        except Exception:
            return NotFound(path=_get_path(self) / index)
        if iterable(value):
            value = Obj(value, path=_get_path(self) / str(key))

        if isinstance(key, list) and len(key) > 1:
            value = value[key[1]]
        return value

    def __setitem__(self, key: str, value):
        key = key.split(self.__separator__, maxsplit=1)

        if len(key) == 1:
            obj = raw(self)
            obj[key[0]] = value
        else:
            self[key[0]][key[1]] = value
