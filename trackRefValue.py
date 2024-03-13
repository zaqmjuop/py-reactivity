from createDep import createDep
from const import TrackOpTypes, __DEV__
from toRaw import toRaw
from trackEffects import trackEffects
from state import effectState


def _getDep(ref):
    if (not getattr(ref, 'dep', None)):
        setattr(ref, 'dep', createDep())
    return getattr(ref, 'dep', None)


def trackRefValue(ref):
    if (effectState.shouldTrack and effectState.activeEffect):
        ref = toRaw(ref)
        if (__DEV__):
            trackEffects(_getDep(ref), {
                'target': ref,
                'type': TrackOpTypes.GET,
                'key': 'value'
            })
        else:
            trackEffects(_getDep(ref))
