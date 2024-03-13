from recordEffectScope import recordEffectScope
from state import effectState
from const import maxMarkerBits
from wasTracked import wasTracked
from newTracked import newTracked


def _cleanupEffect(effect):
    deps = effect.deps
    if (len(deps)):
        for item in deps:
            item.delete(effect)
        deps.clear()


def _finalizeDepMarkers(effect):
    deps = effect.deps
    if (len(deps)):
        ptr = 0
        for dep in deps:
            if (wasTracked(dep) and not newTracked(dep)):
                dep.delete(effect)
            else:
                deps[ptr] = dep
                ptr += 1
            # clear bits
            dep.w &= ~effectState.trackOpBit
            dep.n &= ~effectState.trackOpBit
        for i in range(ptr, len(deps)):
            deps.pop()


def _initDepMarkers(effect):
    deps = effect.deps
    if (len(deps)):
        for item in deps:
            item.w |= effectState.trackOpBit  # set was tracked


class ReactiveEffect:
    def __init__(self, fn, scheduler=None, scope=None) -> None:
        self.active = True
        self.deps = []
        self.parent = None

        self.computed = None
        self.allowRecurse = None
        self.deferStop = None
        self.onStop = None
        # dev only
        self.onTrack = None
        # dev only
        self.onTrigger = None
        self.fn = fn
        self.scheduler = scheduler
        recordEffectScope(self, scope)

    def run(self):
        global effectState
        if (not self.active):
            return self.fn()
        parent = effectState.activeEffect
        lastShouldTrack = effectState.shouldTrack
        while (parent):
            if (parent is self):
                return
            parent = parent.parent
        try:
            self.parent = effectState.activeEffect
            effectState.activeEffect = self
            effectState.shouldTrack = True

            effectState.effectTrackDepth += 1
            effectState.trackOpBit = 1 << effectState.effectTrackDepth
            if (effectState.effectTrackDepth <= maxMarkerBits):
                _initDepMarkers(self)
            else:
                _cleanupEffect(self)
            return self.fn()
        finally:
            if (effectState.effectTrackDepth <= maxMarkerBits):
                _finalizeDepMarkers(self)

            effectState.effectTrackDepth -= 1
            effectState.trackOpBit = 1 << effectState.effectTrackDepth

            effectState.activeEffect = self.parent
            effectState.shouldTrack = lastShouldTrack
            self.parent = None

            if (self.deferStop):
                self.stop()

    def stop(self):
        # stopped while running itself - defer the cleanup
        if (effectState.activeEffect == self):
            self.deferStop = True
        elif (self.active):
            _cleanupEffect(self)
            if (self.onStop):
                self.onStop()
            self.active = False
