from collections.abc import Mapping


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

    def __setitem__(self, key, value):
        pass

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        pass

    def __bool__(self):
        return False

    def __str__(self):
        raise ValueError(f'Path {NoneObj.raw(self)} not exists')
    
    
class Obj:
    @staticmethod
    def iterable(obj):
        return isinstance(obj, Mapping)

    @staticmethod
    def raw(o: 'Obj'):
        if isinstance(o, Obj):
            return object.__getattribute__(o, '__obj')
        return o

    def __init__(self, obj=None):
        if obj is None:
            obj = {}
        if not Obj.iterable(obj):
            raise TypeError('Obj input should be iterable')
        object.__setattr__(self, '__obj', obj)

    def __getitem__(self, item):
        if isinstance(item, str):
            item = item.split('.', maxsplit=1)
            indexer = item[0]
        else:
            indexer = item

        obj = Obj.raw(self)
        try:
            obj = obj.__getitem__(indexer)
        except Exception:
            return NoneObj(indexer)
        if Obj.iterable(obj):
            obj = Obj(obj)
        if isinstance(item, list) and len(item) > 1:
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

    def __call__(self):
        return Obj.raw(self)


if __name__ == '__main__':
    o = Obj({'a': {'b': {'c': {'d': 1}}}})
    print(o['a']['b.c']['e.f.g'])
