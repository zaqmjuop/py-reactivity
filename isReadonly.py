from rawAttr import getRawAttr
from const import ReactiveFlags


def isReadonly(value) -> bool:
    try:
        return bool(getRawAttr(value, ReactiveFlags.IS_READONLY))
    except Exception as e:
        return False
