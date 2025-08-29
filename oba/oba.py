import abc
import warnings

from oba.path import Path


def raw(object_: 'BaseObj'):
    if isinstance(object_, NotFound):
        return object.__getattribute__(object_, '__path__')()
    if isinstance(object_, Obj):
        return object.__getattribute__(object_, '__obj__')
    return object_


def iterable(object_) -> bool:
    return isinstance(object_, dict) or isinstance(object_, list) or isinstance(object_, tuple)


def is_dict(object_: 'BaseObj') -> bool:
    return isinstance(object_, Obj) and isinstance(raw(object_), dict)


def is_list(object_: 'BaseObj') -> bool:
    return isinstance(object_, Obj) and isinstance(raw(object_), list)


def is_tuple(object_: 'BaseObj') -> bool:
    return isinstance(object_, Obj) and isinstance(raw(object_), tuple)


class BaseObj(abc.ABC):
    def __init__(self, object_=None, path=None):
        object.__setattr__(self, '__path__', path or Path())
        object.__setattr__(self, '__obj__', object_ if object_ is not None else {})

    def __iter__(self):
        raise NotImplementedError

    @classmethod
    def raw(cls, object_: 'BaseObj'):
        warnings.warn(
            'Obj.raw is deprecated, use oba.raw instead', DeprecationWarning, stacklevel=2)
        return raw(object_)

    @classmethod
    def iterable(cls, object_):
        warnings.warn(
            'Obj.iterable is deprecated, use oba.iterable instead', DeprecationWarning, stacklevel=2)
        return iterable(object_)

    def __contains__(self, item):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __getattr__(self, key):
        raise NotImplementedError

    def __setattr__(self, key, value):
        raise NotImplementedError

    def __delattr__(self, key):
        raise NotImplementedError

    def __bool__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class NotFound(BaseObj):
    def __init__(self, object_=None, path=None):
        super().__init__(object_, path)

        if not isinstance(path, Path):
            raise ValueError('path for NotFound class should be a Path object')

        if not len(path):
            raise ValueError('path should have at least one component')

        path.mark()

    def __iter__(self):
        return iter({})

    def __contains__(self, item):
        return False

    def __getitem__(self, key):
        return NotFound(path=self.__path__ / key)

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        pass

    def __delattr__(self, key):
        pass

    def __bool__(self):
        return False

    def __str__(self):
        raise ValueError(f'Path not exists: {self.__path__}')

    def __len__(self):
        return 0


NoneObj = NotFound


class Obj(BaseObj):
    def __init__(self, object_=None, path=None):
        super().__init__(object_, path)

        if not iterable(object_):
            raise TypeError('obj should be iterable (dict, list, or tuple)')

    def __getitem__(self, key):
        # noinspection PyBroadException
        try:
            value = self.__obj__.__getitem__(key)
        except Exception:
            return NotFound(path=self.__path__ / key)
        if iterable(value):
            value = Obj(value, path=self.__path__ / str(key))
        return value

    def __getattr__(self, key: str):
        return self[key]

    def __setitem__(self, key: str, value):
        if not is_dict(self):
            raise TypeError('__setitem__ and __setattr__ can only be used on a dict-like object')
        self.__obj__[key] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __contains__(self, item):
        return item in self.__obj__

    def __iter__(self):
        if isinstance(self.__obj__, dict):
            for key in self.__obj__:
                yield key
        else:
            for i, item in enumerate(self.__obj__):
                if iterable(item):
                    yield Obj(item, path=self.__path__ / str(i))
                else:
                    yield item

    def __len__(self):
        return len(self.__obj__)

    def __call__(self):
        return self.__obj__

    def __bool__(self):
        return bool(self.__obj__)

    def __str__(self):
        return 'Obj()'
