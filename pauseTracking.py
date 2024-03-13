from state import effectState
# Temporarily pauses tracking.
def pauseTracking():
  global effectState
  effectState.trackStack.append(effectState.shouldTrack)
  effectState.shouldTrack = False