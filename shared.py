from typing import TypeVar
from es6.Object import Object
from es6.Symbol import Symbol
from es6.Array import Array 

T = TypeVar('T')
U = TypeVar('U')


def hasChanged(value, oldValue) -> bool:
    return not value is oldValue


def extend(target: T, source: U):
    if (isinstance(target, dict) and isinstance(source, dict)):
        for key in source:
            target[key] = source[key]
    else:
        raise TypeError('类型不对')


def isArray(arg) -> bool:
    return isinstance(arg, Array)


def isFunction(val):
    return isinstance(val, type(lambda: None))


def NOOP(): return None


def isObject(val) -> bool:
    return isinstance(val, Object)


def isIntegerKey(key) -> bool:
    return isinstance(key, str) and int(key) == key


def hasOwn(val, key):
    return key in val


def toTypeString(val):
    return val.__class__.__name__


def isMap(val):
    return toTypeString(val) == 'Map'

def isSet(val):
    return toTypeString(val) == 'Sap'

def isPlainObject(val):
    return toTypeString(val) == 'Object'


def toRawType(val):
    return toTypeString(val)


def isSymbol(val):
    return isinstance(val, Symbol)


def cacheStringFunction(fn):
    _cache = Object({})

    def func(text: str):
        nonlocal _cache
        _hit = _cache[text]
        if (not _hit):
            _cache[text] = fn(text)
        return _hit
    return func


def capitalize():
    return cacheStringFunction(lambda _str:  _str.capitalize())


def strSplit(text, separator='', limit=None):
    if (separator == None):
        return [text]
    if (separator == ''):
        return list(text[0: limit]) + [text[limit:]] if isinstance(limit, int) else list(text)
    else:
        return text.split(separator, limit) if isinstance(limit, int) else text.split(separator)

def isPromise(val) -> bool:
    return hasattr(val, 'then') and hasattr(val, 'catch')
