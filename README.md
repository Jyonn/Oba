# Oba: Converting a Python Iterable Object to an Attribute Class

![PyPI](https://img.shields.io/pypi/v/oba.svg)
![GitHub](https://img.shields.io/github/license/Jyonn/Oba.svg)

## Introduction

Converting iterable objects (such as dictionaries, tuples, lists, sets, and subclasses) to access values using class attributes instead of square brackets `[]`. Supports recursive operations and supports both getting and setting values.

## Installation

`pip install oba`

## Usage

```python
from oba import Obj

# Convert a dictionary to an attribute class
d = dict(a=[1, 2, 3], b=[4, dict(x=1)], c=dict(l='hello'))
o = Obj(d)

# Get values
print(o.a[2])  # => 3
print(o.c.l)  # => hello

# Set values
o.b[1].x = 4
print(Obj.raw(o.b[1]))  # => {'x': 4}

points = [dict(x=1, y=2), dict(x=-1, y=0), dict(x=0, y=1)]
o = Obj(points)

o[0].x += 1
print(Obj.raw(o[0]))  # => {'x': 2, 'y': 2}

o['c.l'] = 'world'
print(o.c.l)  # => world
```

## Comparison

### namedtuple (built-in module)

```python
from collections import namedtuple

o = namedtuple('Struct', d.keys())(*d.values())

print(o)  # => Struct(a=[1, 2, 3], b=[4, {'x': 1}], c={'l': 'hello'})
print(o.a)  # => [1, 2, 3]

o.x = 2  # => AttributeError
```

### bunch (package)

```python
from bunch import Bunch

o = Bunch(d)

print(o.a)  # => [1, 2, 3]
print(o.b['x'])  # => 1
print(o.b.x)  # => KeyError

o.x = 2  # OK, editable

o = Bunch(points)  # => AttributeError
```

### json (built-in module)

```python
import json

class Obj(object):
    def __init__(self, d):
        self.__dict__.update(d)

o = json.loads(json.dumps(d), object_hook=Obj)

print(o.a[2])  # => 3
print(o.c.l)  # => hello

o.x = 2  # OK, editable

o = Obj(points)

o[0].x += 1
print(o[0].x)  # => 2
```

### mock (package) 

```python
from mock import Mock

o = Mock(**d)

print(o.a)  # => [1, 2, 3]
print(o.b['x'])  # => 1
print(o.b.x)  # => KeyError

o.x = 2  # OK

o = Mock(*points)  # => TypeError
```

### Summary

| Feature       | namedtuple  | bunch (2011)              | json | mock (2020) | Oba (2022) |
|---------------|-------------|---------------------------|------|-------------|------------|
| built-in      | ✓           | ✗ 11K                     | ✓    | ✗ 28K       | ✗ 3K       |
| recursive     | ✗           | ✗                         | ✓    | ✗           | ✓          |
| revert to raw | ✗           | ✓ (with extra operations) | ✗    | ✗           | ✓          |
| editable      | ✗           | ✓                         | ✓    | ✓           | ✓          |
| iterable      | ✓ (no keys) | ✓                         | ✗    | ✗           | ✓          |
| support dict  | ✓           | ✓                         | ✓    | ✓           | ✓          |
| support list  | ✓           | ✗                         | ✓    | ✗           | ✓          |
| support tuple | ✗           | ✗                         | ✓    | ✗           | ✓          |
| _tolerable_   | ✗           | ✗                         | ✗    | ✗           | ✓          |

## Features

Additionally, `Oba` also has a unique tolerance for unknown attributes. In cases where some attributes do not exist, for example:

```python
d = dict(a=1)
print(d['b'])  # KeyError
```

Other libraries will immediately raise an error. However, in some scenarios (such as reading configuration files), the absence of sub-attributes is a common problem, and we hope to be able to tolerate and monitor the existence of such errors.

```python
from oba import Obj

d = dict(a=1)
o = Obj(d)

print('x' in o)  # => False
if not o.x.y.z:  # OK
    print('not exist')  # => not exist
print(o.x.y.z)  # => ValueError: NoneObj (x.y.z)  # locating the non-existent attribute chain
```

Its internal implementation is that when an attribute does not exist, the object automatically switches to the `NoneObj` class and records the attribute chain.

## License

MIT
