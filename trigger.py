from es6.Object import Object
from createDep import createDep
from state import effectState
from const import __DEV__, TriggerOpTypes, ITERATE_KEY, MAP_KEY_ITERATE_KEY
from shared import isArray, isMap, isIntegerKey
from triggerEffects import triggerEffects


def trigger(target: Object, triggerType, key=None, newValue=None, oldValue=None, oldTarget=None):
    _depsMap = effectState.targetMap.get(target)
    if (not _depsMap):
        # never been tracked
        return

    _deps = []
    if (triggerType == TriggerOpTypes.CLEAR):
        # collection being cleared
        # trigger all effects for target
        _deps = list(_depsMap.values())
    elif (key == 'length' and isArray(target)):
        _newLength = int(newValue)
        for key in range(0, len(_depsMap)):
            if (key == 'length' or key >= _newLength):
                _dep = _depsMap[key]
                _deps.append(_dep)
    else:
        # schedule runs for SET | ADD | DELETE
        if (key != None):
            _deps.append(_depsMap.get(key))

        # also run for iteration key on ADD | DELETE | Map.SET
        if (triggerType == TriggerOpTypes.ADD):
            if (not isArray(target)):
                _deps.append(_depsMap.get(ITERATE_KEY))
                if (isMap(target)):
                    _deps.append(_depsMap.get(MAP_KEY_ITERATE_KEY))
            elif (isIntegerKey(key)):
                # new index added to array -> length changes
                _deps.push(_depsMap.get('length'))
        elif (triggerType == TriggerOpTypes.DELETE):
            if (not isArray(target)):
                _deps.push(_depsMap.get(ITERATE_KEY))
                if (isMap(target)):
                    _deps.push(_depsMap.get(MAP_KEY_ITERATE_KEY))
        elif (triggerType == TriggerOpTypes.SET):
            if (isMap(target)):
                _deps.push(_depsMap.get(ITERATE_KEY))

    eventInfo = {
        "target": target,
        'type': triggerType,
        'key': key,
        'newValue': newValue,
        'oldValue': oldValue,
        'oldTarget': oldTarget
    } if __DEV__ else None
    if (len(_deps) == 1):
        if (_deps[0]):
            if (__DEV__):
                triggerEffects(_deps[0], eventInfo)
            else:
                triggerEffects(_deps[0])
    else:
        effects = []
        for dep in _deps:
            if (isArray(dep)):
                for item in dep:
                    effects.append(item)
        if (__DEV__):
            triggerEffects(createDep(effects), eventInfo)
        else:
            triggerEffects(createDep(effects))
