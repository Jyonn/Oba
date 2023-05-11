from collections.abc import Iterable


class NoneObj:
    __obj = dict()

    @staticmethod
    def raw(o: 'NoneObj'):
        return object.__getattribute__(o, '__path')

    def __init__(self, path=''):
        object.__setattr__(self, '__path', path)

    def __iter__(self):
        return iter(NoneObj.__obj)

    def __contains__(self, item):
        return False

    def __getitem__(self, item):
        p = NoneObj.raw(self)
        return NoneObj(f'{p}.{item}')

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        return

    def __bool__(self):
        return False

    def __str__(self):
        raise ValueError(f'Path {NoneObj.raw(self)} not exists')
    
    
class Obj:
    @staticmethod
    def iterable(obj):
        return isinstance(obj, Iterable)

    @staticmethod
    def raw(o: 'Obj'):
        if isinstance(o, Obj):
            return object.__getattribute__(o, '__obj')
        return o

    def __init__(self, obj=None):
        if obj is None:
            obj = {}
        assert Obj.iterable(obj), TypeError('Obj input should be iterable')
        object.__setattr__(self, '__obj', obj)

    def __getitem__(self, item):
        item = item.split('.', maxsplit=1)

        obj = Obj.raw(self)
        try:
            obj = obj.__getitem__(item[0])
        except Exception:
            return NoneObj(f'{item[0]}')
        if Obj.iterable(obj):
            obj = Obj(obj)
        if len(item) > 1:
            obj = obj[item[1]]
        return obj

    def __getattr__(self, item: str):
        return self[item]

    def __setitem__(self, key: str, value):
        key = key.split('.', maxsplit=1)
        if len(key) == 1:
            obj = Obj.raw(self)
            obj[key[0]] = value
        else:
            self[key[0]][key[1]] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __contains__(self, item):
        obj = Obj.raw(self)
        return item in obj

    def __iter__(self):
        obj = Obj.raw(self)
        for item in obj:
            if Obj.iterable(item):
                item = Obj(item)
            yield item

    def __len__(self):
        return len(Obj.raw(self))


if __name__ == '__main__':
    o = Obj({'a': {'b': {'c': {'d': 1}}}})
    print(o['a']['b.c']['e.f.g'])
