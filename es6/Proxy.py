
from rawAttr import getRawAttr
from .Object import Object
import sys
sys.path.append('../')


def assign(target: dict, source: dict):
    for key in source:
        target[key] = source[key]


class Proxy:
    def __init__(self, target: Object, handler: dict) -> None:
        if (not isinstance(target, Object)):
            raise TypeError('target except Object')
        self.__dict__ = {}
        self.__dict__['origin'] = target
        self.__dict__['get'] = getRawAttr(handler, 'get')
        self.__dict__['set'] = getRawAttr(handler, 'set')
        pass

    def __getitem__(self, prop):
        return self.__getattr__(prop)

    def __setitem__(self, prop, val):
        return self.__setattr__(prop, val)

    def __delitem__(self, prop):
        try:
            return self.__delattr__(prop)
        except (KeyError, AttributeError):
            pass

    def __getattr__(self, propKey):
        if (propKey.startswith('__dict__')):
            return None
        try:
            _get = self.__dict__['get']
            if (_get):
                return self.__dict__['get'](self.__dict__['origin'], propKey, self)
            else:
                return self.__dict__[propKey]
        except (KeyError, AttributeError):
            return None

    def __setattr__(self, propKey, value):
        if (propKey == '__dict__'):
            return
        try:
            _set = self.__dict__['set']
            if (_set):
                _set(self.__dict__['origin'], propKey, value, self)
        except (KeyError, AttributeError):
            return None

    def hasattr(self, prop):
        return prop in self.__dict__


if __name__ == '__main__':
    def objGetter(target, propKey, receiver):
        print(f"getting ${propKey}!", target)
        return target[propKey]

    def objSetter(target, propKey, value, receiver):
        print(f"setting ${propKey}!")
        target[propKey] = value
    _target = Object({})
    obj = Proxy(_target, {
        "get": objGetter,
        "set": objSetter
    })
    obj.count = 1
    obj.count += 1
    print(obj.count)

    p2 = Proxy(Object({}), {
        "get": lambda target, propKey, receiver: 35
    })
    print(p2.time)
    print(p2.name)
    print(p2.title)
    # o1 = Object()
    # o1.count = 1
