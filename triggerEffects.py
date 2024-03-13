
from shared import isArray
from const import __DEV__
from shared import extend
from state import effectState


def _triggerEffect(effect,   debuggerEventExtraInfo=None):
    if (not (effect is effectState.activeEffect) or effect.allowRecurse):
        if (__DEV__ and effect.onTrigger):
            effect.onTrigger(
                extend({"effect": effect}, debuggerEventExtraInfo))
        if (effect.scheduler):
            effect.scheduler()
        else:
            effect.run()


def triggerEffects(dep, debuggerEventExtraInfo=None):
    # spread into array for stabilization
    _effects = dep if isArray(dep) else list(dep)
    for _effect in _effects:
        if (_effect.computed):
            _triggerEffect(_effect, debuggerEventExtraInfo)
    for _effect in _effects:
        if (not _effect.computed):
            _triggerEffect(_effect, debuggerEventExtraInfo)
