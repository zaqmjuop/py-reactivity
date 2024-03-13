from typing import TypeVar
from rawAttr import getRawAttr
from const import ReactiveFlags


T = TypeVar('T')


def toRaw(observed: T) -> T:
    _raw = getRawAttr(observed, ReactiveFlags.RAW)
    return toRaw(_raw) if _raw else observed
