from state import effectState
from const import __DEV__, maxMarkerBits
from shared import extend
from newTracked import newTracked
from wasTracked import wasTracked
from createDep import Dep


def trackEffects(dep: Dep,  debuggerEventExtraInfo=None):
    _shouldTrack = False
    
    if (effectState.effectTrackDepth <= maxMarkerBits):
        if (not newTracked(dep)):
            dep.n |= effectState.trackOpBit  # set newly tracked
            _shouldTrack = not wasTracked(dep)
    else:
        # Full cleanup mode.
        _shouldTrack = not effectState.activeEffect in dep
    if (_shouldTrack):
        dep.add(effectState.activeEffect)
        effectState.activeEffect.deps.append(dep)
        if (__DEV__ and effectState.activeEffect.onTrack):
            extend({'effect': effectState.activeEffect},
                   debuggerEventExtraInfo)
