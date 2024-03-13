import asyncio
from Promise import Promise, setTimeout


async def main():
    promiseAsync = Promise(lambda resolve, reject: (
        print('beforeResolve promiseAsync'),
        setTimeout(lambda: resolve('promiseAsync'), 100)
    ))

    #  同步的promise
    promiseSync = Promise(lambda resolve, reject: (
        print('beforeResolve promiseSync'),
        resolve("promiseSync")
    ))

    #  嵌套的promise
    nestedPromise = Promise(lambda outerResolve, outerReject: (
        print('beforeResolve nestedPromise'),
        outerResolve(
            Promise(lambda innerResolve,
                    innerReject: innerResolve("nestedPromise"))
        )
    ))

    #  thenable
    thenable = {
        "then": lambda resolve, reject: (
            print('beforeResolve thenable'),
            resolve("thenable")
        )
    }

    #  嵌套的thenable
    nestedThenable = {
        "then": lambda outerResolve, outerReject: (
            print('beforeResolve nestedThenable'),
            outerResolve({
                "then": lambda innerResolve, innerReject: innerResolve("nestedThenable")
            })
        )
    }

    #  普通值
    normalValue = "normalValue"

    #  对于上面每一个变量作为`Promise`的决议值进行决议，打印决议结果
    list1 = [
        promiseAsync,
        promiseSync,
        nestedPromise,
        thenable,
        nestedThenable,
        normalValue,
    ]
    for obj in list1:
        Promise(lambda resolve, reject: resolve(obj)).then(
            lambda value: print(f"testRes1:{value}"), None)
    # 浏览器结果
    # beforeResolve promiseAsync
    # beforeResolve promiseSync
    # beforeResolve nestedPromise
    # beforeResolve thenable
    # beforeResolve nestedThenable

    # normalValue
    # thenable
    # promiseSync
    # nestedThenable
    # nestedPromise
    # promiseAsync
if __name__ == "__main__":
    asyncio.run(main())
