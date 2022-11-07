# Oba

![PyPI](https://img.shields.io/pypi/v/oba.svg)
![GitHub](https://img.shields.io/github/license/Jyonn/Oba.svg)

## Usage

- Convert iterative object to attribute-accessible object

## Install 

`pip install oba`

## Description

```python
from oba import Obj

o = Obj(dict(a=[1, 2, 3], b=[4, dict(x=1)], c=dict(l='hello')))

print(o.a[2])  # => 3
print(o.c.l)  # => hello

o.b[1].x = 4
print(Obj.raw(o.b[1]))  # => {'x': 4}

print(bool(o.xxx))  # => False, accessible as NoneObj()
```
