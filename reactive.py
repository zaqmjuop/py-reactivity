from rawAttr import getRawAttr
from const import ReactiveFlags, TriggerOpTypes, TrackOpTypes
from es6.Map import Map
from es6.Object import Object
from es6.Reflect import Reflect
from es6.Proxy import Proxy
from shared import isArray, isObject, isIntegerKey, hasChanged, toRawType, isMap, isSymbol, capitalize
from isRef import isRef
from isShallow import isShallow
from toRaw import toRaw
from hasOwn import hasOwn
from const import ITERATE_KEY, __DEV__, reactiveMap, shallowReactiveMap, readonlyMap, shallowReadonlyMap, TargetType
from track import track
from trigger import trigger
from pauseTracking import pauseTracking
from resetTracking import resetTracking
from isNonTrackableKeys import isNonTrackableKeys
from state import effectState

# ios10.x Object.getOwnPropertyNames(Symbol) can enumerate 'arguments' and 'caller'
# but accessing them on Symbol leads to TypeError because Symbol is a strict mode
# function
builtInSymbols = set(['length', 'name', 'prototype', 'for', 'keyFor', 'asyncIterator', 'hasInstance', 'isConcatSpreadable', 'iterator', 'match',
                      'matchAll', 'replace', 'search', 'species', 'split', 'toPrimitive', 'toStringTag', 'unscopables', 'useSetter', 'useSimple'])


def targetTypeMap(rawType: str):
    if (rawType in set(['Object', 'Array'])):
        return TargetType.COMMON
    elif (rawType in set(['Map', 'Set', 'WeakMap', 'WeakSet'])):
        return TargetType.COLLECTION
    return TargetType.INVALID


def getTargetType(value: Object):
    if (getRawAttr(value, ReactiveFlags.SKIP) or not Object.isExtensible(value)):
        return TargetType.INVALID
    return targetTypeMap(toRawType(value))


def createArrayInstrumentations():
    instrumentations = {}
    # instrument identity-sensitive Array methods to account for possible reactive
    # values

    def _createFinder(key: str):
        def _func(this, *args):
            _arr = toRaw(this)
            for i in range(0, len(this)):
                track(_arr, TrackOpTypes.GET, str(i))
            # we run the method using the original args first (which may be reactive)
            _res = _arr[key](*args)
            if (_res != -1 or _res == False):
                # if that didn't work, run it again using raw values.
                return _arr[key](*args.map(toRaw))
            else:
                return _res
        return _func
    for key in ['includes', 'indexOf', 'lastIndexOf']:
        instrumentations[key] = _createFinder(key)
    # instrument length-altering mutation methods to avoid length being tracked
    # which leads to infinite loops in some cases (#2137)

    def _createAlter(key: str):
        def _func(this, *args):
            pauseTracking()
            res = toRaw(this)[key].apply(this, args)
            resetTracking()
            return res
        return _func
    for key in ['push', 'pop', 'shift', 'unshift', 'splice']:
        instrumentations[key] = _createAlter(key)


arrayInstrumentations = createArrayInstrumentations()


def createReadonlyMethod(triggerType):
    def func(self, *args: list):
        if (__DEV__):
            _key = f"on key '{args[0]}' " if args[0] else ''
            print(
                f"{capitalize(triggerType)} operation {_key}failed: target is readonly.", toRaw(self))
        return False if triggerType is TriggerOpTypes.DELETE else self
    return func


def toReactive(value):
    return reactive(value) if isObject(value) else value


def toShallow(value):
    return value


def _checkIdentityKeys(target, has, key):
    _rawKey = toRaw(key)
    if (not (_rawKey is key) and has.call(target, _rawKey)):
        _type = toRawType(target)
        _minStr = " as keys" if _type == "Map" else ""
        print(f"Reactive ${_type} contains both the raw and reactive " +
              f"versions of the same object {_minStr}, " +
              "which can lead to inconsistencies. " +
              "Avoid differentiating between the raw and reactive versions " +
              "of an object and only use the reactive version if possible.")


def _getProto(v):
    return Reflect.getPrototypeOf(v)


def _get(target, key, isReadonly=False, isShallow=False):
    # #1772: readonly(reactive(Map)) should return readonly + reactive version
    # of the value
    target = getRawAttr(target, ReactiveFlags.RAW)
    _rawTarget = toRaw(target)
    _rawKey = toRaw(key)
    if (not isReadonly):
        if (hasChanged(key, _rawKey)):
            track(_rawTarget, TrackOpTypes.GET, key)
        track(_rawTarget, TrackOpTypes.GET, _rawKey)
    _has = _getProto(_rawTarget).has
    _wrap = toShallow if isShallow else (
        toReadonly if isReadonly else toReactive)
    if (_has.call(_rawTarget, key)):
        return _wrap(target.get(key))
    elif (_has.call(_rawTarget, _rawKey)):
        return _wrap(target.get(_rawKey))
    elif (not (target is _rawTarget)):
        # #3602 readonly(reactive(Map))
        # ensure that the nested reactive `Map` can do tracking for itself
        target.get(key)


def _has(self, key, isReadonly=False) -> bool:
    target = getRawAttr(self, ReactiveFlags.RAW)
    _rawTarget = toRaw(target)
    _rawKey = toRaw(key)
    if (not isReadonly):
        if (hasChanged(key, _rawKey)):
            track(_rawTarget, TrackOpTypes.HAS, key)
        track(_rawTarget, TrackOpTypes.HAS, _rawKey)
    return target.has(key) if key is _rawKey else (target.has(key) or target.has(_rawKey))


def _size(target, isReadonly=False):
    target = getRawAttr(target, ReactiveFlags.RAW)
    not isReadonly and track(toRaw(target), TrackOpTypes.ITERATE, ITERATE_KEY)
    return Reflect.get(target, 'size', target)


def _add(self, value):
    value = toRaw(value)
    _target = toRaw(self)
    _proto = _getProto(_target)
    _hadKey = _proto.has.call(_target, value)
    if (not _hadKey):
        _target.add(value)
        trigger(_target, TriggerOpTypes.ADD, value, value)
    return self


def _set(self, key, value):
    value = toRaw(value)
    _target = toRaw(self)
    _has = _getProto(_target).has
    _get = _getProto(_target).get

    _hadKey = _has.call(_target, key)
    if (not _hadKey):
        key = toRaw(key)
        _hadKey = _has.call(_target, key)
    elif (__DEV__):
        _checkIdentityKeys(_target, _has, key)

    _oldValue = _get.call(_target, key)
    _target.set(key, value)
    if (not _hadKey):
        trigger(_target, TriggerOpTypes.ADD, key, value)
    elif (hasChanged(value, _oldValue)):
        trigger(_target, TriggerOpTypes.SET, key, value, _oldValue)
    return self


def _deleteEntry(self, key):
    _target = toRaw(self)
    _has = _getProto(_target).has
    _get = _getProto(_target).get
    _hadKey = _has.call(_target, key)
    if (not _hadKey):
        key = toRaw(key)
        _hadKey = _has.call(_target, key)
    elif (__DEV__):
        _checkIdentityKeys(_target, _has, key)

    _oldValue = _get.call(_target, key) if _get else None
    # forward the operation before queueing reactions
    _result = _target.delete(key)
    if (_hadKey):
        trigger(_target, TriggerOpTypes.DELETE, key, None, _oldValue)
    return _result


def _clear(self):
    _target = toRaw(self)
    _hadItems = _target.size != 0
    _oldTarget = (Map(_target) if isMap(_target)
                  else set(_target)) if __DEV__ else None
    # forward the operation before queueing reactions
    _result = _target.clear()
    if (_hadItems):
        trigger(_target, TriggerOpTypes.CLEAR, None, None, _oldTarget)
    return _result


def hasOwnProperty(self:  object, key: str):
    obj = toRaw(self)
    track(obj, TrackOpTypes.HAS, key)
    return obj.hasOwnProperty(key)


class BaseReactiveHandler():
    @property
    def _isReadonly(self):
        return self.__isReadonly

    @property
    def _shallow(self):
        return self.__shallow

    def __init__(self, _isReadonly=False, _shallow=False) -> None:
        self.__isReadonly = _isReadonly
        self.__shallow = _shallow
        pass

    def get(self, target, key, receiver):
        _isReadonly = self._isReadonly
        _shallow = self._shallow

        def _getTargetMap():
            nonlocal _isReadonly
            nonlocal _shallow
            if (_isReadonly):
                return shallowReadonlyMap if _shallow else readonlyMap
            else:
                return shallowReactiveMap if _shallow else reactiveMap
        if (key is ReactiveFlags.IS_REACTIVE):
            return not _isReadonly
        elif (key is ReactiveFlags.IS_READONLY):
            return _isReadonly
        elif (key is ReactiveFlags.IS_SHALLOW):
            return _shallow
        elif (key is ReactiveFlags.RAW and receiver is _getTargetMap().get(target)):
            return target
        targetIsArray = isArray(target)
        if (not _isReadonly):
            if (targetIsArray and hasOwn(arrayInstrumentations, key)):
                return Reflect.get(arrayInstrumentations, key, receiver)
            if (key == 'hasOwnProperty'):
                return hasOwnProperty
        res = Reflect.get(target, key, receiver)
        if (builtInSymbols.has(key) if isSymbol(key) else isNonTrackableKeys(key)):
            return res
        if (not _isReadonly):
            track(target, TrackOpTypes.GET, key)
        if (_shallow):
            return res
        if (isRef(res)):
            # ref unwrapping - skip unwrap for Array + integer key.
            return targetIsArray and (res if isIntegerKey(key) else res.value)
        if (isObject(res)):
            # Convert returned value into a proxy as well. we do the isObject check
            # here to avoid invalid value warning. Also need to lazy access readonly
            # and reactive here to avoid circular dependency.
            return readonly(res) if _isReadonly else reactive(res)
        return res


class ReadonlyReactiveHandler(BaseReactiveHandler):
    def __init__(self, shallow=False) -> None:
        super().__init__(True, shallow)
        pass

    def set(self, target, key):
        if (__DEV__):
            print(
                f"Set operation on key '{str(key)}' failed: target is readonly.", target)
        return True

    def deleteProperty(self, target, key):
        if (__DEV__):
            print(
                f"Delete operation on key '{str(key)}' failed: target is readonly.", target)
        return True


readonlyHandlers = ReadonlyReactiveHandler()


def readonly(target):
    return createReactiveObject(
        target,
        True,
        readonlyHandlers,
        readonlyCollectionHandlers,
        readonlyMap)


def toReadonly(value):
    readonly(value) if isObject(value) else value


class MutableReactiveHandler(BaseReactiveHandler):
    def __init__(self, shallow=False) -> None:
        super().__init__(False, shallow)
        pass

    def __getitem__(self, prop: str):
        return getattr(self, prop)

    def set(self, target, key, value, receiver) -> bool:
        oldValue = target[key]
        if (isReadonly(oldValue) and isRef(oldValue) and not isRef(value)):
            return False
        if (not self._shallow):
            if (not isShallow(value) and isReadonly(value)):
                oldValue = toRaw(oldValue)
                value = toRaw(value)
            if (not isArray(target) and isRef(oldValue) and not isRef(value)):
                oldValue.value = value
                return True
        else:
            pass
            # in shallow mode, objects are set as-is regardless of reactive or not
        hadKey = int(key) < len(target) if isArray(
            target) and isIntegerKey(key) else hasOwn(target, key)
        result = Reflect.set(target, key, value, receiver)
        # don't trigger if target is something up in the prototype chain of original
        if (target is toRaw(receiver)):
            if (not hadKey):
                trigger(target, TriggerOpTypes.ADD, key, value)
            elif (hasChanged(value, oldValue)):
                trigger(target, TriggerOpTypes.SET, key, value, oldValue)
        return result

    def deleteProperty(self, target: Object, key: str) -> bool:
        _hadKey = hasOwn(target, key)
        _oldValue = getRawAttr(target, key)
        _result = Reflect.deleteProperty(target, key)
        if (_result and _hadKey):
            trigger(target, TriggerOpTypes.DELETE, key, None, _oldValue)
        return _result

    def has(self, target: Object, key: str) -> bool:
        _result = Reflect.has(target, key)
        if (not isSymbol or not key in builtInSymbols):
            track(target, TrackOpTypes.HAS, key)
        return _result

    def ownKeys(self, target: Object):
        track(target, TrackOpTypes.ITERATE,
              'length' if isArray(target) else ITERATE_KEY)
        return Reflect.ownKeys(target)


mutableHandlers = MutableReactiveHandler()


def createForEach(isReadonly: bool, isShallow: bool):
    def forEach(this, callback, thisArg=None):
        _observed = this
        _target = getRawAttr(_observed, ReactiveFlags.RAW)
        _rawTarget = toRaw(_target)
        _wrap = toShallow if isShallow else (
            toReadonly if isReadonly else toReactive)
        not isReadonly and track(_rawTarget, TrackOpTypes.ITERATE, ITERATE_KEY)

        def _handler(value, key):
            # important: make sure the callback is
            # 1. invoked with the reactive map as `this` and 3rd arg
            # 2. the value received should be a corresponding reactive/readonly.
            return callback.call(thisArg, _wrap(value), _wrap(key), _observed)
        return _target.forEach(_handler)
    return forEach


mutableInstrumentations = Object({})
mutableInstrumentations['get'] = lambda this, key: _get(this, key)
mutableInstrumentations['size'] = lambda: _size(mutableInstrumentations)
mutableInstrumentations['has'] = _has
mutableInstrumentations['add'] = _add
mutableInstrumentations['set'] = _set
mutableInstrumentations['delete'] = _deleteEntry
mutableInstrumentations['clear'] = _clear
mutableInstrumentations['forEach'] = createForEach(False, False)

shallowInstrumentations = Object({})
shallowInstrumentations['get'] = lambda this, key: _get(this, key, False, True)
shallowInstrumentations['size'] = lambda: _size(shallowInstrumentations)
shallowInstrumentations['has'] = _has
shallowInstrumentations['add'] = _add
shallowInstrumentations['set'] = _set
shallowInstrumentations['delete'] = _deleteEntry
shallowInstrumentations['clear'] = _clear
shallowInstrumentations['forEach'] = createForEach(False, True)


shallowReadonlyInstrumentations = Object({})
shallowReadonlyInstrumentations['get'] = lambda this, key: _get(
    this, key, True, True)
shallowReadonlyInstrumentations['size'] = lambda: _size(
    shallowReadonlyInstrumentations, True)
shallowReadonlyInstrumentations['has'] = lambda this, key: _has.call(
    this, key, True)
shallowReadonlyInstrumentations['add'] = createReadonlyMethod(
    TriggerOpTypes.ADD)
shallowReadonlyInstrumentations['set'] = createReadonlyMethod(
    TriggerOpTypes.SET)
shallowReadonlyInstrumentations['delete'] = createReadonlyMethod(
    TriggerOpTypes.DELETE)
shallowReadonlyInstrumentations['clear'] = createReadonlyMethod(
    TriggerOpTypes.CLEAR)
shallowReadonlyInstrumentations['forEach'] = createForEach(True, True)


readonlyInstrumentations = Object({})
readonlyInstrumentations['get'] = lambda self, key: _get(self, key, True)
readonlyInstrumentations['size'] = lambda: _size(
    readonlyInstrumentations,   True)
readonlyInstrumentations['has'] = lambda this, key: _has.call(this, key, True)
readonlyInstrumentations['add'] = createReadonlyMethod(TriggerOpTypes.ADD)
readonlyInstrumentations['set'] = createReadonlyMethod(TriggerOpTypes.SET)
readonlyInstrumentations['delete'] = createReadonlyMethod(
    TriggerOpTypes.DELETE)
readonlyInstrumentations['clear'] = createReadonlyMethod(TriggerOpTypes.CLEAR)
readonlyInstrumentations['forEach'] = createForEach(True, False)


def createInstrumentationGetter(isReadonly: bool, shallow: bool):
    instrumentations = None
    if (shallow):
        instrumentations = shallowReadonlyInstrumentations if isReadonly else shallowInstrumentations
    else:
        instrumentations = readonlyInstrumentations if isReadonly else mutableInstrumentations

    def res(target, key, receiver):
        nonlocal isReadonly
        nonlocal shallow
        if (key is ReactiveFlags.IS_REACTIVE):
            return not isReadonly
        elif (key is ReactiveFlags.IS_READONLY):
            return isReadonly
        elif (key is ReactiveFlags.RAW):
            return target
        _target = instrumentations if hasOwn(
            instrumentations, key) and key in target else target
        return Reflect.get(_target, key, receiver)
    return res


readonlyCollectionHandlers = createInstrumentationGetter(True, False)

mutableCollectionHandlers = {
    "get": createInstrumentationGetter(False, False)
}


def isReadonly(value):
    return bool(getRawAttr(value, ReactiveFlags.IS_READONLY))


def createReactiveObject(
    target: Object,
    isReadonly: bool,
    baseHandlers,
    collectionHandlers,
    proxyMap
):
    if (not Object.isObject(target)):
        if (__DEV__):
            print(f"value cannot be made reactive: {str(target)}")
        return target
    # target is already a Proxy, return it.
    # exception: calling readonly() on a reactive object
    if (getRawAttr(target, ReactiveFlags.RAW) and not (isReadonly and getRawAttr(target, ReactiveFlags.IS_REACTIVE))):
        return target
    # target already has corresponding Proxy
    existingProxy = proxyMap.get(target)
    if (existingProxy):
        return existingProxy
    # only specific value types can be observed.
    targetType = getTargetType(target)
    if (targetType == TargetType.INVALID):
        return target
    proxy = Proxy(
        target,
        collectionHandlers if targetType is TargetType.COLLECTION else baseHandlers
    )
    proxyMap.set(target, proxy)
    return proxy


def reactive(target: Object):
    # if trying to observe a readonly proxy, return the readonly version.
    if (isReadonly(target)):
        return target
    return createReactiveObject(
        target,
        False,
        mutableHandlers,
        mutableCollectionHandlers,
        reactiveMap
    )


if __name__ == '__main__':
    # obj = reactive(Object({"count": 0}))
    # print(obj.count)
    # obj.count += 1
    # print(obj.count)
    from computed import computed
    # plusOne = computed(lambda: obj.count + 1)
    # print(plusOne.value)

    def Creatingareadonlycomputed90ef():
        obj = reactive(Object({"count": 0}))
        plusOne = computed(lambda: obj.count + 1)

        print(plusOne.value)  # 2
        plusOne.value += 1  # Error

    def Creatingwritablecomputedref():
        obj = reactive(Object({"count": 0}))
        plusOne = computed({
            "get": lambda: obj.count + 1,
            "set": lambda val: setattr(obj, 'value', val - 1)
        })
        plusOne.value = 1
        print(obj.count)  # 0
    # Creatingareadonlycomputed90ef()
    print('--')
    # Creatingwritablecomputedref()

    def testIsReactive():
        obj = reactive(Object({"count": 0}))
        print(obj)
        print(obj[ReactiveFlags.IS_REACTIVE])
        print(getRawAttr(obj, ReactiveFlags.IS_REACTIVE))
    testIsReactive()
