from state import effectState

def recordEffectScope(effect, scope = effectState.activeEffectScope):
  if(scope and scope.active):
    scope.effects.append(effect)
