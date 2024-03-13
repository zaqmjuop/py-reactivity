def toTypeString(val):
    return val.__class__.__name__

def formatAttrName(target, name: str):
    res = name
    className = target.__class__.__name__
    if (name.startswith('__') and className != 'Proxy'):
        res = f"_{className}{name}"
    return res

def hasRawAttr(target, name)->bool:
    className = toTypeString(target)
    try:
        if(className == 'dict'):
            return name in target
        else:
            return hasattr(target, name)
    except Exception as e:
        return False

def getRawAttr(target, name: str):
    className = toTypeString(target)
    _attrName = formatAttrName(target, name)
    try:
        if(className == 'dict'):
            return target[_attrName]
        else:
            return getattr(target, _attrName, None)
    except Exception as e:
        return None


def setRawAttr(target, name, value):
    _attrName = formatAttrName(target, name)
    if (isinstance(target, dict)):
        target[_attrName] = value
        return
    return setattr(target, formatAttrName(target, name), value)
