import abc
import warnings

from oba.path import Path


def raw(obj: 'BaseObj'):
    if isinstance(obj, NotFound):
        return object.__getattribute__(obj, '__path')()
    if isinstance(obj, Obj):
        return object.__getattribute__(obj, '__obj')
    return obj


def _get_path(obj: 'BaseObj') -> Path:
    return object.__getattribute__(obj, '__path')


def iterable(obj) -> bool:
    return isinstance(obj, dict) or isinstance(obj, list) or isinstance(obj, tuple)


def is_dict(obj: 'BaseObj') -> bool:
    return isinstance(obj, Obj) and isinstance(raw(obj), dict)


def is_list(obj: 'BaseObj') -> bool:
    return isinstance(obj, Obj) and isinstance(raw(obj), list)


def is_tuple(obj: 'BaseObj') -> bool:
    return isinstance(obj, Obj) and isinstance(raw(obj), tuple)


class BaseObj(abc.ABC):
    def __init__(self, obj=None, path=None):
        object.__setattr__(self, '__path', path or Path())
        object.__setattr__(self, '__obj', obj if obj is not None else {})

    def __iter__(self):
        raise NotImplementedError

    @classmethod
    def raw(cls, obj: 'BaseObj'):
        warnings.warn(
            'Obj.raw is deprecated, use oba.raw instead', DeprecationWarning, stacklevel=2)
        return raw(obj)

    @classmethod
    def iterable(cls, obj):
        warnings.warn(
            'Obj.iterable is deprecated, use oba.iterable instead', DeprecationWarning, stacklevel=2)
        return iterable(obj)

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
    def __init__(self, obj=None, path=None):
        super().__init__(obj, path)

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
        return NotFound(path=_get_path(self) / key)

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
        path = _get_path(self)
        raise ValueError(f'Path not exists: {path}')

    def __len__(self):
        return 0


NoneObj = NotFound


class Obj(BaseObj):
    def __init__(self, obj=None, path=None):
        super().__init__(obj, path)

        if not iterable(obj):
            raise TypeError('obj should be iterable (dict, list, or tuple)')

    def __getitem__(self, key):
        obj = raw(self)
        # noinspection PyBroadException
        try:
            value = obj.__getitem__(key)
        except Exception:
            return NotFound(path=_get_path(self) / key)
        if iterable(value):
            value = Obj(value, path=_get_path(self) / str(key))
        return value

    def __getattr__(self, key: str):
        return self[key]

    def __setitem__(self, key: str, value):
        if not is_dict(self):
            raise TypeError('__setitem__ and __setattr__ can only be used on a dict-like object')
        obj = raw(self)
        obj[key] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __contains__(self, item):
        obj = raw(self)
        return item in obj

    def __iter__(self):
        obj = raw(self)
        if isinstance(obj, dict):
            for key in obj:
                yield key
        else:
            for i, item in enumerate(obj):
                if iterable(item):
                    yield Obj(item, path=_get_path(self) / str(i))
                else:
                    yield item

    def __len__(self):
        return len(raw(self))

    def __call__(self):
        return raw(self)

    def __bool__(self):
        return bool(raw(self))

    def __str__(self):
        return 'Obj()'


if __name__ == '__main__':
    o = Obj({'a': {'b': {'c': {'d': 1}}}})
    print(o['a'].b.c['e·f·g'])
