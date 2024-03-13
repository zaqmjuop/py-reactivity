from typing import TypeVar, Generic, Any
from shared import hasChanged
from isRef import isRef
from trackRefValue import trackRefValue
from triggerRefValue import triggerRefValue
from toRaw import toRaw
from isShallow import isShallow
from isReadonly import isReadonly

T = TypeVar('T')


class _RefImpl(Generic[T]):

    @property
    def __v_isRef(self):
        return True

    @property
    def __v_isShallow(self):
        return self.__dict__['__v_isShallow']

    def __init__(self, value: T, __v_isShallow: bool) -> None:
        super().__init__()
        self.__dict__ = {}
        self._value = value
        self.dep = None
        self._rawValue = value
        self.__dict__['__v_isShallow'] = __v_isShallow

    @property
    def value(self):
        trackRefValue(self)
        return self._value

    @value.setter
    def value(self, newVal):
        _useDirectValue = self.__v_isShallow or isShallow(
            newVal) or isReadonly(newVal)
        newVal = newVal if _useDirectValue else toRaw(newVal)
        if (hasChanged(newVal, self._rawValue)):
            self._rawValue = newVal
            self._value = newVal
            triggerRefValue(self, newVal)


def _createRef(rawValue: Any, shallow: bool):
    if (isRef(rawValue)):
        return rawValue
    return _RefImpl(rawValue, shallow)


def ref(value: Any = None):
    return _createRef(value, False)


if __name__ == '__main__':
    count = ref(0)
    print(count.value)

    count.value += 1
    print(count.value)
    pass
