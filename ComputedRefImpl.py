
from triggerRefValue import triggerRefValue
from trackRefValue import trackRefValue
from toRaw import toRaw
from ReactiveEffect import ReactiveEffect
from rawAttr import setRawAttr


class ComputedRefImpl:
    @property
    def effect(self):
        return self._effect

    @property
    def __v_isRef(self):
        return True

    __v_isReadonly_raw = False

    @property
    def __v_isReadonly(self):
        return self.__v_isReadonly_raw

    @property
    def __v_raw(self):
        return False

    _dirty = True
    _cacheable: bool

    def __init__(self, getter, _setter, isReadonly) -> None:
        self._setter = _setter
        self.dep = None
        self._value = None
        self._effect = None

        def scheduler():
            if (not self._dirty):
                self._dirty = True
                triggerRefValue(self)
        self._effect = ReactiveEffect(getter, scheduler)
        setRawAttr(self._effect, 'computed', self)
        self._cacheable = True
        setRawAttr(self._effect, 'active', self._cacheable)
        self.__v_isReadonly_raw = isReadonly

    @property
    def value(self):
        # the computed ref may get wrapped by other proxies e.g. readonly() #3376
        rawSelf = toRaw(self)
        trackRefValue(rawSelf)
        if (rawSelf._dirty or not rawSelf._cacheable):
            rawSelf._dirty = False
            rawSelf._value = rawSelf.effect.run()
        return rawSelf._value

    @value.setter
    def value(self, newValue):
        self._setter(newValue)


if __name__ == '__main__':
    pass
