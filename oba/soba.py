from nestify import nestify
from oba.oba import raw, NotFound, iterable

from oba import Obj


class Soba(Obj):
    def __init__(self, object_=None, path=None, separator='.'):
        object_ = nestify(object_, separator=separator) if object_ is not None else object_
        super().__init__(object_, path)
        object.__setattr__(self, '__separator__', separator)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.split(self.__separator__, maxsplit=1)

        index = key[0] if isinstance(key, list) else key

        # noinspection PyBroadException
        try:
            value = self.__obj__.__getitem__(index)
        except Exception:
            return NotFound(path=self.__path__ / index)
        if iterable(value):
            value = Obj(value, path=self.__path__ / str(key))

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

    def __str__(self):
        return 'Soba()'
