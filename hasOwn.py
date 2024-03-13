from es6.Object import Object


def hasOwn(val, key: str):
    if (isinstance(val, Object)):
        return val.hasattr(key)
    return key in val
