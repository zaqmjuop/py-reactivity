import asyncio
from watch import watch
from reactive import reactive
from es6.Array import Array
from es6.Object import Object


async def main():
    try:
        obj1 = reactive(Object({
            'count': 1,
            'arr': Array([1, 2, 3])
        }))

        def getter():
            return obj1.count

        def onChange(newValue, oldValue):
            print(f"触发watch")
            print(f"newValue", newValue)
            print(f"oldValue", oldValue)
        watch(getter, onChange)
        obj1.count = 3
    except asyncio.CancelledError:
        print('CancelledError')

if __name__ == "__main__":
    asyncio.run(main())
