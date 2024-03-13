from const import __DEV__, ErrorCodes
import inspect

ErrorTypeStrings = {}
ErrorTypeStrings[ErrorCodes.SETUP_FUNCTION] = 'setup function'
ErrorTypeStrings[ErrorCodes.RENDER_FUNCTION] = 'render function'
ErrorTypeStrings[ErrorCodes.WATCH_GETTER] = 'watcher getter'
ErrorTypeStrings[ErrorCodes.WATCH_CALLBACK] = 'watcher callback'
ErrorTypeStrings[ErrorCodes.WATCH_CLEANUP] = 'watcher cleanup function'
ErrorTypeStrings[ErrorCodes.NATIVE_EVENT_HANDLER] = 'native event handler'
ErrorTypeStrings[ErrorCodes.COMPONENT_EVENT_HANDLER] = 'component event handler'
ErrorTypeStrings[ErrorCodes.VNODE_HOOK] = 'vnode hook'
ErrorTypeStrings[ErrorCodes.DIRECTIVE_HOOK] = 'directive hook'
ErrorTypeStrings[ErrorCodes.TRANSITION_HOOK] = 'transition hook'
ErrorTypeStrings[ErrorCodes.APP_ERROR_HANDLER] = 'app errorHandler'
ErrorTypeStrings[ErrorCodes.APP_WARN_HANDLER] = 'app warnHandler'
ErrorTypeStrings[ErrorCodes.FUNCTION_REF] = 'ref function'
ErrorTypeStrings[ErrorCodes.ASYNC_COMPONENT_LOADER] = 'async component loader'
ErrorTypeStrings[ErrorCodes.SCHEDULER] = 'scheduler flush. This is likely a Vue internals bug. ' + \
    'Please open an issue at https://new-issue.vuejs.org/?repo=vuejs/core'


def logError(err, errType, throwInDev=True):
    if (__DEV__):
        info = ErrorTypeStrings[errType]
        print("Unhandled error" +
              f" during execution of ${info}" if info else "}")
        # crash in dev by default so it's more noticeable
        if (throwInDev):
            raise err
    else:
        # recover in prod to reduce the impact on end-user
        print(err)


def handleError(err, errType, throwInDev=True):
    logError(err, errType, throwInDev)


def callWithErrorHandling(fn, errType, args=[]):
    res = None
    acceptArgLength = len(inspect.signature(fn).parameters)
    if (acceptArgLength < len(args)):
        args = args[0:acceptArgLength]
    try:
        res = fn(*args)
    except Exception as err:
        if(__DEV__):
            funcStr = inspect.getsource(fn) 
            print(f"Unhandled error during execution of run" + funcStr + f"with arguments: {args}")
        else:
            handleError(err, errType)
    return res
