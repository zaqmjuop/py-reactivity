from rawAttr import getRawAttr


def isRef(r):
    return getRawAttr(r, '__v_isRef') is True
