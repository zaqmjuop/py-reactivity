from rawAttr import getRawAttr
from isReadonly import isReadonly
from const import ReactiveFlags

##
 # Checks if an object is a proxy created by {@link reactive()} or
 # {@link shallowReactive()} (or {@link ref()} in some cases).
 #
 # @example
 # ```js
 # isReactive(reactive({}))            // => true
 # isReactive(readonly(reactive({})))  // => true
 # isReactive(ref({}).value)           // => true
 # isReactive(readonly(ref({})).value) // => true
 # isReactive(ref(true))               // => false
 # isReactive(shallowRef({}).value)    // => false
 # isReactive(shallowReactive({}))     // => true
 # ```
 #
 # @param value - The value to check.
 # @see {@link https://vuejs.org/api/reactivity-utilities.html#isreactive}
 #/
def isReactive(value) -> bool:
    if (isReadonly(value)):
        return isReactive(getRawAttr(value, ReactiveFlags.RAW))
    return bool(getRawAttr(value, ReactiveFlags.IS_REACTIVE))
