import weakref
__all__ = ['Object']


def copy(record):
    res = {}
    for key in record:
        res[key] = record[key]
    return res


objStateMap = weakref.WeakKeyDictionary()


class Object:

    @classmethod
    def isObject(cls, obj) -> bool:
        return isinstance(obj, cls)

    @classmethod
    def _validate(cls, obj):
        if (not cls.isObject(obj)):
            TypeError('obj except type Object')

    @classmethod
    def keys(cls, obj: 'Object'):
        return list(obj.keys())
    # 静态方法密封一个对象。密封一个对象会阻止其扩展并且使得现有属性不可配置。
    # 密封对象有一组固定的属性：不能添加新属性、不能删除现有属性或更改其可枚举性和可配置性、不能重新分配其原型。只要现有属性的值是可写的，它们仍然可以更改。
    # seal() 返回传入的同一对象。

    @classmethod
    def seal(cls, obj: 'Object') -> 'Object':
        cls._validate(obj)
        obj.__builtIn__['__sealed'] = True
        return obj

    # 静态方法可以防止新属性被添加到对象中（即防止该对象被扩展）。它还可以防止对象的原型被重新指定。
    @classmethod
    def preventExtensions(cls, obj: 'Object') -> 'Object':
        cls._validate(obj)
        obj.__builtIn__['__extensible'] = False
        return obj

    # 静态方法可以使一个对象被冻结。冻结对象可以防止扩展，并使现有的属性不可写入和不可配置。
    # 被冻结的对象不能再被更改：不能添加新的属性，不能移除现有的属性，不能更改它们的可枚举性、可配置性、可写性或值，对象的原型也不能被重新指定。
    # freeze() 返回与传入的对象相同的对象。
    # 冻结一个对象是 JavaScript 提供的最高完整性级别保护措施。
    @classmethod
    def freeze(cls, obj: 'Object') -> 'Object':
        cls._validate(obj)
        obj.__builtIn__['__frozen'] = True
        return obj

    @classmethod
    def isExtensible(cls, obj: 'Object') -> bool:
        cls._validate(obj)
        return obj.__builtIn__['__extensible']

    """
    config['configurable'] 
    config['enumerable'] 
    config['value'] 
    config['writable'] 
    config['get']  
    config['set']   
    """
    @classmethod
    def defineProperty(cls, obj, prop, config):
        if (not isinstance(obj, Object)):
            return

        if (not 'configurable' in config):
            raise ReferenceError('require configurable')
        if (config['configurable']):
            obj.__banConfigurables__.discard(prop)
        else:
            obj.__banConfigurables__.add(prop)

        if (not 'enumerable' in config):
            raise ReferenceError('require enumerable')
        if (config['enumerable']):
            obj.__banEnumerables__.discard(prop)
        else:
            obj.__banEnumerables__.add(prop)

        if ('value' in config and 'writable' in config):
            # Data Descriptor
            del obj.__customGetters__[prop]
            del obj.__customSetters__[prop]
            obj.__dict__[prop] = config['value']
            if (config['writable']):
                obj.__banWritables__.discard(prop)
            else:
                obj.__banWritables__.add(prop)
        elif ('get' in config and 'set' in config):
            # Accessor descriptor
            del obj[prop]
            obj.__banWritables__.discard(prop)
            if (not isinstance(config['get'], type(lambda: None))):
                raise TypeError(f"get should be a function")
            else:
                obj.__customGetters__[prop] = config['get']
            if (not isinstance(config['set'], type(lambda: None))):
                raise TypeError(f"set should be a function")
            else:
                obj.__customSetters__[prop] = config['set']
        else:
            raise TypeError(f"accessor descriptors err")

    def __init__(self, obj=None):
        objStateMap[self] = {
            '__dict__': {},
            '__proto__': obj,
            '__banEnumerables__': set(),
            '__banConfigurables__': set(),
            '__banWritables__': set(),
            '__customGetters__': {},
            '__customSetters__': {},
            '__builtIn__': {
                "__frozen": False,
                "__sealed": False,
                "__extensible": True
            },
        }

        if (isinstance(obj, Object)):
            for key in obj.__dict__:
                self[key] = obj.__dict__[key]
        elif (isinstance(obj, dict)):
            for key in obj:
                self[key] = obj[key]
        elif (isinstance(obj, list)):
            for i in range(0, len(obj)):
                self[i] = obj[i]

    def __getitem__(self, prop):
        return self.__getattr__(prop)

    def __setitem__(self, prop, val):
        return self.__setattr__(prop, val)

    def __delitem__(self, prop):
        if (self.__builtIn__['__frozen']):
            raise TypeError(f"{prop} is not frozen")
        if (self.__builtIn__['__sealed'] or prop in self.__banConfigurables__):
            raise TypeError(f"{prop} is not configurable")
        try:
            return self.__delattr__(prop)
        except (KeyError, AttributeError):
            pass

    def __getattr__(self, prop: str):
        state = objStateMap[self]
        className = self.__class__.__name__
        if (prop.startswith(f"_{className}")):
            prop = prop[len(className)+1:]
        if (not state):
            return None
        elif (prop in state):
            return state[prop]
        elif (prop in state['__builtIn__']):
            return state['__builtIn__'][prop]
        elif (prop in state['__customGetters__']):
            return state['__customGetters__'][prop]()
        elif prop in state['__dict__']:
            return state['__dict__'][prop]
        elif (isinstance(state['__proto__'], dict) and prop in state['__proto__']):
            return state['__proto__'][prop]
        elif (isinstance(state['__proto__'], Object) and state['__proto__'].hasattr(prop)):
            return getattr(state['__proto__'], prop)
        else:
            raise KeyError(prop)

    def __setattr__(self, prop, value):
        state = objStateMap[self]
        if (not state):
            return None
        if (prop in state['__builtIn__']):
            state['__builtIn__'][prop] = value
            return
        if (state['__builtIn__']['__sealed'] or prop in state['__banConfigurables__']):
            raise TypeError(f"{prop} is not configurable")
        if (prop in state['__banWritables__']):
            raise TypeError(f"{prop} is read-only")
        if (prop in state['__customSetters__']):
            return state['__customSetters__'][prop](value)
        if (state['__builtIn__']['__frozen']):
            raise AttributeError(f"{self} is frozen")
        if (not prop in state['__dict__'] and not state['__builtIn__']['__extensible']):
            raise AttributeError(f"{self} not extensible")
        state['__dict__'][prop] = value

    def keys(self):
        return self.__dict__.keys()

    def hasattr(self, prop) -> bool:
        state = objStateMap[self]
        if (not state):
            return False
        elif (prop in state['__dict__']):
            return True
        elif (prop in state['__customGetters__']):
            return True
        else:
            return False

    def method(self, prop, func):
        def method(*args, **kwargs):
            return func(self, *args, **kwargs)
        self.__setattr__(prop, method)

    def __keys__(self):
        return self.__map__().keys()

    def __values__(self):
        return [v for k, v in self.__items__()]

    def __iter__(self):
        canEnumerables = set(self.__dict__.keys()).difference_update(
            self.__banEnumerables__)
        return iter(canEnumerables)

    def __map__(self):
        attrs = copy(self.__dict__)
        if ('__proto__' in attrs):
            del attrs['__proto__']
        for key in self.__customGetters__:
            attrs[key] = self.__customGetters__[key]()
        return attrs

    def __items__(self):
        obj_map = self.__map__()
        return [(k, obj_map[k]) for k in obj_map.keys()]

    def __contains__(self, item):
        return item in self.__values__()

    def __str__(self):
        res = self.__map__()
        return f"Object:{res}"

    def hasOwnProperty(self, prop):
        self.hasattr(prop)

    def isPrototypeOf(self, target):
        if (not isinstance(target, Object)):
            return False
        __proto__ = target.__proto__
        while (__proto__ and not (__proto__ is Object)):
            if (self.__proto__ is __proto__):
                return True
        return False

    def propertyIsEnumerable(self, prop):
        return self.hasattr(prop) and not (prop in self.__banEnumerables__)

    def toLocaleString(self):
        return self.__str__()

    def toString(self):
        return self.__str__()

    def valueOf(self):
        id(self)


if __name__ == '__main__':
    o1 = Object()
    # print(o1)  # {}
    # o1.a = 1
    # print(o1.a)  # 1
    # print(o1['a'])  # 1
    # o1['a'] = 2
    # print(o1)  # {'a': 2}

    # bValue = 38

    # def getB():
    #     print('called getB')
    #     return bValue

    # def setB(newValue):
    #     global bValue
    #     print('called setB')
    #     bValue = newValue

    # Object.defineProperty(o1, "b", {
    #     "get": getB,
    #     "set": setB,
    #     "enumerable": True,
    #     "configurable": True,
    # })

    # print(o1.b)  # called getB \n 38
    # o1.b = 111  # called setB
    # print(o1.b)  # called getB \n 111
    # print(o1)  # called getB \n  {'a': 2, 'b': 111}
    print('------')
    # print('hasF __frozen', hasattr(o1, 'frozen'))
    # print('hasF _frozen11',   hasattr(o1, '_frozen11'))
    o1.__frozen = True
    print(o1.__frozen)  # called getB \n  {'a': 2, 'b': 111}
    print('__proto__' in o1)  # called getB \n  {'a': 2, 'b': 111}
