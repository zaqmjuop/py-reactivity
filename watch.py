from shared import isFunction
from const import __DEV__
from doWatch import doWatch


def watch(source, cb, options=None):
    if (__DEV__ and not isFunction(cb)):
        print("\"watch(fn, options?)\" signature has been moved to a separate API. " +
              "Use \"watchEffect(fn, options?)\" instead. \"watch\" now only " +
              "supports \"watch(source, cb, options?) signature.")
    return doWatch(source, cb, options) if options else doWatch(source, cb)


if __name__ == '__main__':
    pass
    from reactive import reactive
    from es6.Array import Array
    from es6.Object import Object
    obj1 = reactive(Object({
        'count': 1,
        'arr': Array([1, 2, 3])
    }))
    print('before watch')
    def getter():
        print('run source getter')
        return obj1.count
    watch(getter, lambda: print(f"watch成功！！！")) 
    print('after watch')
    obj1.count = 3
