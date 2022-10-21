class NoneObj:
    __obj = dict()

    def __iter__(self):
        return iter(NoneObj.__obj)

    def __contains__(self, item):
        return False

    def __getitem__(self, item):
        return self

    def __getattr__(self, item):
        return self

    def __setattr__(self, key, value):
        return

    def __bool__(self):
        return False

    def __str__(self):
        raise ValueError('NoneObj')
    
    
class Obj:
    none = NoneObj()

    @staticmethod
    def iterable(obj):
        types = [list, dict, tuple]
        for t in types:
            if isinstance(obj, t):
                return True
        return False

    @staticmethod
    def raw(o: 'Obj'):
        return object.__getattribute__(o, '__obj')

    def __init__(self, obj):
        object.__setattr__(self, '__obj', obj)

    def __getitem__(self, item):
        obj = Obj.raw(self)
        try:
            obj = obj.__getitem__(item)
        except Exception:
            return Obj.none
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
        return iter(obj)
