
from shared import isObject, isArray, isMap, isSet, isPlainObject
from rawAttr import getRawAttr
from es6.Set import Set
from const import ReactiveFlags
from isRef import isRef


def traverse(value, seen = None):
    if (not isObject(value) or getRawAttr(value, ReactiveFlags.SKIP)):
        return value
    seen = seen or Set()
    if (seen.has(value)):
        return value
    seen.add(value)
    if (isRef(value)):
        traverse(value.value, seen)
    elif (isArray(value)):
        for i in range(0, value.length):
            traverse(value[i], seen)
    elif (isSet(value)):
        for v in value:
            traverse(v, seen)
    elif (isMap(value)):
        for v in value:
            traverse(v, seen)
    elif (isPlainObject(value)):
        for key in value:
            traverse(value[key], seen)
    return value
