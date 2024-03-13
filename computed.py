from ComputedRefImpl import ComputedRefImpl
from const import __DEV__
from shared import isFunction, NOOP


def computed(getterOrOptions, debugOptions=None):
    getter = None
    setter = None

    onlyGetter = isFunction(getterOrOptions)
    if (onlyGetter):
        getter = getterOrOptions

        def setter(val=None): return print(
            'Write operation failed: computed value is readonly') if __DEV__ else NOOP
    else:
        getter = getterOrOptions['get']
        setter = getterOrOptions['set']

    cRef = ComputedRefImpl(getter, setter, onlyGetter or not setter)

    if (__DEV__ and debugOptions):
        cRef.effect.onTrack = debugOptions.onTrack
        cRef.effect.onTrigger = debugOptions.onTrigger
    return cRef


if __name__ == '__main__':
    from ref import ref
    # @example

    def Creatingareadonlycomputed90ef():
        count = ref(1)
        plusOne = computed(lambda: count.value + 1)

        print(plusOne.value)  # 2
        plusOne.value += 1  # Error

    def Creatingwritablecomputedref():
        count = ref(1)
        plusOne = computed({
            "get": lambda: count.value + 1,
            "set": lambda val: setattr(count, 'value', val - 1)
        })
        plusOne.value = 1
        print(count.value)  # 0
    Creatingareadonlycomputed90ef()
    print('--')
    Creatingwritablecomputedref()
