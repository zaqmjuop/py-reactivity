from rawAttr import getRawAttr
from const import ReactiveFlags


def isShallow(value) -> bool:
    getRawAttr(value, ReactiveFlags.IS_SHALLOW)
