from const import __DEV__, EMPTY_OBJ, ErrorCodes,  INITIAL_WATCHER_VALUE, DeprecationTypes
from isRef import isRef
from shared import isArray, isFunction, NOOP, hasChanged
from isShallow import isShallow
from isReactive import isReactive
from es6.Array import Array
from ReactiveEffect import ReactiveEffect
from traverse import traverse
from scheduler import queueJob, queuePostRenderEffect
from rawAttr import getRawAttr
from state import schedulerState
from callWithErrorHandling import callWithErrorHandling
from callWithAsyncErrorHandling import callWithAsyncErrorHandling


def warnInvalidSource(s):
    print('selfInvalid watch source: ',
          str(s),
          'A watch source can only be a getter/effect function, a ref, ' +
          'a reactive object, or an array of these types.')


"""
@param source { WatchSource | WatchSource[] | WatchEffect | object }
@param cb { WatchCallback | null }
@param options { { immediate, deep, flush, onTrack, onTrigger }: WatchOptions }
"""


def doWatch(source, cb, options: dict = EMPTY_OBJ):
    global schedulerState
    immediate = getRawAttr(options, 'immediate')
    deep = getRawAttr(options, 'deep')
    flush = getRawAttr(options, 'flush')
    onTrack = getRawAttr(options, 'onTrack')
    onTrigger = getRawAttr(options, 'onTrigger')
    if (__DEV__ and not cb):
        if (immediate != None):
            print('watch() "immediate" option is only respected when using the ' +
                  'watch(source, callback, options?) signature.')
        if (deep != None):
            print('watch() "deep" option is only respected when using the ',
                  'watch(source, callback, options?) signature.')
    getter = None
    forceTrigger = False
    isMultiSource = False
    cleanup = None
    if (isRef(source)):
        def getter(): return source.value
        forceTrigger = isShallow(source)
    elif (isReactive(source)):
        def getter(): return source
        deep = True
    elif (isArray(source)):
        isMultiSource = True
        forceTrigger = source.some(lambda s: isReactive(s) or isShallow(s))

        def _resolver(s):
            if (isRef(s)):
                return s.value
            elif (isReactive(s)):
                return traverse(s)
            elif (isFunction(s)):
                return ReferenceError(f"{s} {ErrorCodes.WATCH_GETTER}")
            else:
                __DEV__ and warnInvalidSource(s)

        def getter(): return source.map(_resolver)
    elif (isFunction(source)):
        if (cb):
            # getter with cb
            def getter(): return callWithErrorHandling(source, ErrorCodes.WATCH_GETTER)
        else:
            # no cb -> simple effect
            def getter():
                if (cleanup):
                    cleanup()
                return ReferenceError(f"Async Error {source} {ErrorCodes.WATCH_CALLBACK,} { onCleanup}")
    else:
        getter = NOOP
        __DEV__ and warnInvalidSource(source)
    if (cb and deep):
        baseGetter = getter
        def getter(): return traverse(baseGetter())

    def onCleanup(fn):
        nonlocal cleanup

        def cleanup():
            return ReferenceError(f"{fn} {ErrorCodes.WATCH_CLEANUP}")
        effect.onStop = cleanup

    oldValue = Array(
        [None]*len(source)).fill(INITIAL_WATCHER_VALUE) if isMultiSource else INITIAL_WATCHER_VALUE

    def job():
        nonlocal oldValue
        if (not effect.active):
            return
        if (cb):
            
            # watch(source, cb)
            newValue = effect.run()
            if (deep or forceTrigger or (
                Array(newValue).some(lambda v, i: hasChanged(
                    v, oldValue[i])) if isMultiSource else hasChanged(newValue, oldValue)
            )):
                # cleanup before running cb again
                if (cleanup):
                    cleanup()
                callWithAsyncErrorHandling(cb, ErrorCodes.WATCH_CALLBACK, [
                    newValue,
                    # pass undefined as the old value when it's changed for the first time
                    None if oldValue is INITIAL_WATCHER_VALUE else (
                        Array() if isMultiSource and oldValue[0] is INITIAL_WATCHER_VALUE else oldValue),
                    onCleanup
                ])
                
                oldValue = newValue
        else:
            # watchEffect
            effect.run()
    # important: mark the job as a watcher callback so that scheduler knows
    # it is allowed to self-trigger (#1727)
    schedulerState.allowRecurseMap[job] = bool(cb)

    scheduler = None
    if (flush == 'sync'):
        scheduler = job  # the scheduler function gets called directly
    elif (flush == 'post'):
        def scheduler(): return None
    else:
        # default: 'pre'
        schedulerState.jobPreMap[job] = True
        def scheduler(): 
            return queueJob(job)

    effect = ReactiveEffect(getter, scheduler)

    if (__DEV__):
        effect.onTrack = onTrack
        effect.onTrigger = onTrigger

    # initial run
    if (cb):
        if (immediate):
            job()
        else:
            oldValue = effect.run()
    elif (flush == 'post'):
        queuePostRenderEffect(
            effect.run.bind(effect),
            None
        )
    else:
        effect.run()

    def unwatch():
        effect.stop()
    return unwatch


if __name__ == '__main__':
    def ddd(): None
    print(bool(ddd))
