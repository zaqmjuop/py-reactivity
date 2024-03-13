from const import __DEV__
from triggerEffects import triggerEffects
from const import TriggerOpTypes
from toRaw import toRaw

def triggerRefValue(ref , newVal=None):
  ref = toRaw(ref)
  _dep = ref.dep
  if(_dep):
    if(__DEV__):
      triggerEffects(_dep, {
        "target": ref,
        "type": TriggerOpTypes.SET,
        "key": 'value',
        "newValue": newVal
      })
    else:
      triggerEffects(_dep)
