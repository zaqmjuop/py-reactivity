def markToKey(key) -> str:
    return str(id(key))


class Map:
    def __init__(self, kvList=[]) -> None:
        self.__keys__ = {}
        self.__values__ = {}
        if (isinstance(kvList, list)):
            for kv in kvList:
                self.set(kv[0], kv[1])
        pass

    def set(self, key, value):
        keyId = markToKey(key)
        self.__keys__[keyId] = key
        self.__values__[keyId] = value

    def get(self, key):
        if (self.has(key)):
            keyId = markToKey(key)
            return self.__values__[keyId]
        else:
            return None

    def has(self, key):
        keyId = markToKey(key)
        return keyId in self.__values__

    def delete(self, key):
        if (self.has(key)):
            keyId = markToKey(key)
            del self.__values__[keyId]

    @property
    def size(self):
        return len(self.__values__)

    def clear(self):
        self.__values__.clear()

    def keys(self):
        return iter(self.__keys__.values())

    def values(self):
        return iter(self.__values__.values())

    def __iter__(self):
        res = []
        for key in self.keys():
            res.append([key, self.get(key)])
        return iter(res)

    def entries(self):
        return self.__iter__()

    def forEach(self, handler):
        for key in self.keys():
            handler(self.get(key), key, self)


if __name__ == '__main__':
    map = Map([
        ['F', 'no'],
        ['T',  'yes'],
    ])

    class MyClass:
        pass
    m1 = MyClass()
    map.set(m1, 'm1')

    for key in map.keys():
        print(key)
    # F
    # T
    # <__main__.MyClass object at 0x7fa4f2f2fc10>

    for value in map.values():
        print(value)
    # no
    # yes
    # m1

    for item in map.entries():
        print(item[0], item[1])
    # F no
    # T yes
    # <__main__.MyClass object at 0x7fa4f2f2fc10> m1

    map.forEach(lambda value, key, map: print(f"Key: {key}, Value: {value}, "))
    # Key: F, Value: no,
    # Key: T, Value: yes,
    # Key: <__main__.MyClass object at 0x7fa4f2f2fc10>, Value: m1,
