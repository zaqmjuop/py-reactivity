import weakref

"""
WeakKeyDictionary的键必须是弱引用可接受的对象。这通常意味着该对象必须是可变的，并且必须是可散列的。

在Python中，大多数自定义类的实例都可以作为WeakKeyDictionary的键。例如：

然而，一些内置类型的实例，如列表和字典，不能作为WeakKeyDictionary的键，因为它们是不可散列的。尝试使用这些类型的实例作为键会引发TypeError。

此外，不可变的对象，如字符串和整数，也不能作为WeakKeyDictionary的键，即使它们是可散列的。这是因为不可变对象的生命周期通常由Python解释器管理，而不是由引用计数管理。

总的来说，WeakKeyDictionary的键的类型可以是大多数自定义类的实例，但不能是列表、字典、字符串、整数等内置类型的实例。


hash() 可以获取的就是可散列的
"""


class WeakMap:

    def __init__(self, kvList=[]) -> None:
        self.__weakMap__ = weakref.WeakKeyDictionary()
        if (isinstance(kvList, list)):
            for kv in kvList:
                self.set(kv[0], kv[1])
        pass

    def set(self, key, value):
        self.__weakMap__[key] = value

    def has(self, key):
        return key in self.__weakMap__

    def get(self, key):
        return self.__weakMap__[key] if self.has(key) else None

    def delete(self, key):
        del self.__weakMap__[key]

    @property
    def size(self):
        return len(self.__weakMap__)

    def clear(self):
        self.__weakMap__.clear()

    def keys(self):
        return iter(self.__weakMap__.keys())

    def values(self):
        return iter(self.__weakMap__.values())

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
    class MyClass:
        pass
    m1 = MyClass()
    w1 = WeakMap()
    w1.set(m1, 'ddd')
    print(w1.get(m1))
    print(list(w1.keys()))
    print(list(w1.values()))
# WeakKeyDictionary和WeakValueDictionary
