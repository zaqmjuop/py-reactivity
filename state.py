from es6.Object import Object
from es6.Map import Map
from es6.Array import Array
from es6.Promise import Promise
from es6.Map import Map
from weakref import WeakKeyDictionary

effectState = Object({
    "activeEffect": None,
    "shouldTrack": True,
    "effectTrackDepth": 0,
    "trackOpBit": 1,
    "targetMap": Map(),
    "trackStack": [],  # boolean[]
    'activeEffectScope': None,
})

schedulerState = Object({
    'isFlushing': False,
    'isFlushPending': False,

    'queue':  Array(),
    'flushIndex': 0,

    'pendingPostFlushCbs': Array(),
    'activePostFlushCbs': None,
    'postFlushIndex': 0,

    'resolvedPromise': Promise.resolve(None),
    'currentFlushPromise': None,

    'jobPreMap': WeakKeyDictionary(),
    'jobIdMap': WeakKeyDictionary(),
    'jobAttrMap': WeakKeyDictionary(),
    'allowRecurseMap': WeakKeyDictionary()
})
