from shared import isFunction, isPromise
from es6.Array import Array
from callWithErrorHandling import callWithErrorHandling, handleError


def callWithAsyncErrorHandling(fn,  errType, args=[]):
    if (isFunction(fn)):
        res = callWithErrorHandling(fn,  errType, args)
        if (res and isPromise(res)):
            res.catch(lambda err: handleError(err,  errType))
        return res
    values = Array()
    for i in range(0, len(fn)):
        values.push(callWithAsyncErrorHandling(fn[i], errType, args))
    return values
