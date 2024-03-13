from es6.Object import Object
from createDep import createDep
from es6.Map import Map
from state import effectState
from const import __DEV__
from trackEffects import trackEffects


def track(target: Object, trackType, key):
    global effectState
    if (effectState.shouldTrack and effectState.activeEffect):
        depsMap = effectState.targetMap.get(target)
        if (not depsMap):
            depsMap = Map()
            effectState.targetMap.set(target, depsMap)
        dep = depsMap.get(key)
        if (not dep):
            dep = createDep()
            depsMap.set(key, dep)
        eventInfo = {"effect": effectState.activeEffect, "target": target,
                     "type": trackType, "key": key} if __DEV__ else None
        trackEffects(dep, eventInfo)
