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
        raise ValueError(f'NoneObj ({NoneObj.raw(self)})')
    
    
class Obj:
    @staticmethod
    def iterable(obj):
        types = [list, dict, tuple]
        for t in types:
            if isinstance(obj, t):
                return True
        return False

    @staticmethod
    def raw(o: 'Obj'):
        if isinstance(o, Obj):
            return object.__getattribute__(o, '__obj')
        return o

    def __init__(self, obj):
        object.__setattr__(self, '__obj', obj)

    def __getitem__(self, item):
        obj = Obj.raw(self)
        try:
            obj = obj.__getitem__(item)
        except Exception:
            return NoneObj(f'{item}')
        if Obj.iterable(obj):
            return Obj(obj)
        return obj

    def __getattr__(self, item):
        return self[item]

    def __setitem__(self, key, value):
        obj = Obj.raw(self)
        obj[key] = value

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
    o = Obj({'m': 5})
    print(o.m)
    print(o.a.b[0].x)
