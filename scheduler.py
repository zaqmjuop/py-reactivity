from es6.Array import Array
from const import __DEV__, ErrorCodes
from es6.Map import Map
from es6.Set import Set
from shared import NOOP
from shared import isArray
from es6.Array import Array
from state import schedulerState
from callWithErrorHandling import callWithErrorHandling


RECURSION_LIMIT = 100


def unsigned_right_shift(n, m):
    return (n % 0x100000000) >> m


def getId(job) -> int:
    id = schedulerState.jobIdMap[job]
    return float('inf')


# #2768
# Use binary-search to find a suitable position in the queue,
# so that the queue maintains the increasing order of job's id,
# which can prevent the job from being skipped and also can avoid repeated patching.
def findInsertionIndex(id: int):
    # the start index should be `flushIndex + 1`
    start = schedulerState.flushIndex + 1
    end = schedulerState.queue.length

    while (start < end):
        middle = unsigned_right_shift(start + end, 1)
        middleJobId = getId(schedulerState.queue[middle])
        if (middleJobId < id):
            start = middle + 1
        else:
            end = middle

    return start


def comparator(a, b) -> int:
    preA = schedulerState.jobPreMap[a]
    preB = schedulerState.jobPreMap[b]
    if (preA and not preB):
        return -1
    if (preB and not preA):
        return 1
    return 0


def checkRecursiveUpdates(seen, fn):
    if (not seen.has(fn)):
        seen.set(fn, 1)
    else:
        count = seen.get(fn)
        if (count > RECURSION_LIMIT):
            return True
        else:
            seen.set(fn, count + 1)


"""
@param seen? {CountMap}
"""


def flushPostFlushCbs(seen=None):
    global schedulerState
    if (schedulerState.pendingPostFlushCbs.length):
        deduped = Array(Set(schedulerState.pendingPostFlushCbs))
        schedulerState.pendingPostFlushCbs.length = 0

        # #1947 already has active queue, nested flushPostFlushCbs call
        if (activePostFlushCbs):
            activePostFlushCbs.push(*deduped)
            return

        activePostFlushCbs = deduped
        if (__DEV__):
            seen = seen or Map()

        activePostFlushCbs.sort(lambda a, b: getId(a) - getId(b))

        for postFlushIndex in range(0, activePostFlushCbs.length):
            if (__DEV__ and checkRecursiveUpdates(seen, activePostFlushCbs[postFlushIndex])):
                continue
            activePostFlushCbs[postFlushIndex]()
        activePostFlushCbs = None
        postFlushIndex = 0


def flushJobs(seen=None):
    global schedulerState
    schedulerState.isFlushPending = False
    schedulerState.isFlushing = True
    if (__DEV__):
        seen = seen or Map()

    # Sort queue before flush.
    # This ensures that:
    # 1. Components are updated from parent to child. (because parent is always
    #    created before the child so its render effect will have smaller
    #    priority number)
    # 2. If a component is unmounted during a parent component's update,
    #    its update can be skipped.
    schedulerState.queue.sort(comparator)

    # conditional usage of checkRecursiveUpdate must be determined out of
    # try ... catch block since Rollup by default de-optimizes treeshaking
    # inside try-catch. This can leave all warning code unshaked. Although
    # they would get eventually shaken by a minifier like terser, some minifiers
    # would fail to do that (e.g. https:#github.com/evanw/esbuild/issues/1610)
    def check(job):
        if (__DEV__):
            return checkRecursiveUpdates(seen, job)
        else:
            return

    try:
        for flushIndex in range(0, schedulerState.queue.length):
            job = schedulerState.queue[flushIndex]
            # job and job.active != False
            if (job):
                if (__DEV__ and check(job)):
                    continue
                callWithErrorHandling(job, ErrorCodes.SCHEDULER)
    finally:
        schedulerState.flushIndex = 0
        schedulerState.queue.length = 0

        flushPostFlushCbs(seen)

        schedulerState.isFlushing = False
        schedulerState.currentFlushPromise = None
        # some postFlushCb queued jobs!
        # keep flushing until it drains.
        if (schedulerState.queue.length or schedulerState.pendingPostFlushCbs.length):
            flushJobs(seen)


def queueFlush():
    global schedulerState
    if (not schedulerState.isFlushing and not schedulerState.isFlushPending):
        schedulerState.isFlushPending = True
        try:
            schedulerState.currentFlushPromise = schedulerState.resolvedPromise.then(
                flushJobs, NOOP)
        except Exception as e:
            print('queueFlush', e)


def queueJob(job):
    # the dedupe search uses the startIndex argument of Array.includes()
    # by default the search index includes the current job that is being run
    # so it cannot recursively trigger itself again.
    # if the job is a watch() callback, the search will start with a +1 index to
    # allow it recursively trigger itself - it is the user's responsibility to
    # ensure it doesn't end up in an infinite loop.
    if (not schedulerState.queue.length or not schedulerState.queue.includes(
        job,
        schedulerState.flushIndex +
            1 if schedulerState.isFlushing and schedulerState.allowRecurseMap[
                job] else schedulerState.flushIndex
    )
    ):
        schedulerState.queue.push(job)
        queueFlush()


def queuePostFlushCb(cb):
    global schedulerState
    if (not isArray(cb)):
        if (not schedulerState.activePostFlushCbs or
                not schedulerState.activePostFlushCbs.includes(
                    cb, schedulerState.postFlushIndex + 1 if schedulerState.allowRecurseMap[cb] else schedulerState.postFlushIndex)
            ):
            schedulerState.pendingPostFlushCbs.push(cb)
    else:
        # if cb is an array, it is a component lifecycle hook which can only be
        # triggered by a job, which is already deduped in the main queue, so
        # we can skip duplicate check here to improve perf
        schedulerState.pendingPostFlushCbs.push(*cb)
    queueFlush()


queuePostRenderEffect = queuePostFlushCb
