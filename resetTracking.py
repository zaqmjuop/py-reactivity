from state import effectState
# Resets the previous global effect tracking state.


def resetTracking():
    global effectState
    last = effectState.trackStack.pop()
    effectState.shouldTrack = True if last == None else last
