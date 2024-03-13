import asyncio
import nest_asyncio
nest_asyncio.apply()

async def createCoroutineByFunc(func, mesc):
    await asyncio.sleep(mesc/1000)
    func()
    return

def setTimeout(func, mesc = 0):
    task = asyncio.create_task(createCoroutineByFunc(func, mesc))
    return task

def clearTimeout(task):
    task.cancel()
    return task

def setInterval(func, mesc = 0):
    taskList = []
    def interval():
        nonlocal taskList
        task = asyncio.create_task(createCoroutineByFunc(lambda: (
            interval(),
            func()
        ), mesc))
        taskList.append(task)
        if(len(taskList) > 2):
            del taskList[0]

    def cancel():
        for task in taskList:
            task and task.cancel()
        taskList.clear()
            
    interval()
    return {
        "cancel": cancel
    }

def clearInterval(task):
    task and task["cancel"]()
    return task

import types

State = types.MappingProxyType({
  "PENDING": "pending",
  "FULFILLED": "fulfilled",
  "REJECTED": "rejected",
})

class PromiseValueResolveHandler:
    @classmethod
    def canResolve(self, resolveValue):
        return isinstance(resolveValue, Promise)
    
    def tryToResolve(self, resolveValue, changeState, resolve, reject):
        resolveValue.then(lambda value: resolve(value), lambda reason: reject(reason))
        return True
    
class ThenableValueResolveHandler:
    @classmethod
    def canResolve(self, resolveValue):
        try:
            then = getattr(resolveValue, 'then') if(hasattr(resolveValue, "then")) else resolveValue["then"]
            return isinstance(then, type(lambda:None))
        except Exception as e:
            return False
    def tryToResolve(self, resolveValue, changeState, resolve, reject):
        try:
            then = getattr(resolveValue, 'then') if(hasattr(resolveValue, "then")) else resolveValue["then"]
            then(lambda y: resolve(y), lambda y: reject(y))
            return True
        except Exception as e:
            reject(e)
            return True
               
class DefaultResolveValueHandler:
    @classmethod
    def canResolve(self, resolveValue):
        return True
    def tryToResolve(self, resolveValue, changeState, resolve, reject):
        changeState(State['FULFILLED'], resolveValue)
        return True

               
resolveValueHandlerChain = (
    # Promise类型决议值处理器
    PromiseValueResolveHandler(),
    # Thenable决议值处理器
    ThenableValueResolveHandler(),
    # 其他类型决议值处理器
    DefaultResolveValueHandler()
)

def bind(fn, instance):
    def resFunc(*args):
        return fn(instance, *args)
    return resFunc
    
class Promise:
    """
    value: any => Promise
    """
    @classmethod
    def resolve(cls, value):
        return Promise(lambda resolve, _: resolve(value))

    """
    reason: any => Promise
    """
    @classmethod
    def reject(cls, reason):
        return Promise(lambda _, reject: reject(reason))

    """
    promises: Promise[] => Promise
    """
    @classmethod
    def all(cls, promises):
        def __innerTask(resolve, reject):
            fulfilledCnt = 0
            fulfilledValues = []
            for i in range(0, len(promises)):
                p = promises[i]
                def __onFulfilled(value):
                    fulfilledValues.insert(i, value)
                    fulfilledCnt+=1
                    if(fulfilledCnt == len(promises)):
                        resolve(fulfilledValues)
                def __onRejected(reason):
                    reject(reason)
                def __callback():
                    p.then(__onFulfilled, __onRejected)
                setTimeout(__callback)
        return Promise(__innerTask)
    
    """
    promises: Promise[] => Promise
    """
    @classmethod
    def race(promises):
        def __innerTask(resolve, reject):
            for p in promises:
                setTimeout(lambda: p.then(
                    lambda value: resolve(value),
                    lambda reason: reject(reason)
                ))
        return Promise(__innerTask)
    
    """
    promises: Promise[] => Promise
    """
    @classmethod
    def allSettled(promises):
        def __innerTask(resolve, reject):
            result = []
            for i in range(0, len(promises)):
                p = promises[i]
                def __onFulfilled(value):
                    result.append({"status": "fulfilled", "value": value})
                    if(i == len(promises) - 1):
                        resolve(result)
                def __onRejected(reason):
                    result.append({"status": "rejected", "reason": reason})
                    if(i == len(promises) - 1):
                        resolve(result)
                p.then(__onFulfilled, __onRejected)
        return Promise(__innerTask)
        
    """
    promises: Promise[] => Promise
    """
    @classmethod
    def any(promises):
        def __innerTask(resolve, reject):
            rejectedReasons = []
            rejectedCnt = 0
            for i in range(0, len(promises)):
                p = promises[i]
                def __onFulfilled(value):
                    resolve(value)
                def __onRejected(reason):
                    rejectedReasons.insert(i, reason)
                    rejectedCnt+=1
                if(rejectedCnt == len(rejectedReasons)):
                    reject(rejectedReasons)
                setTimeout(lambda: p.then(__onFulfilled, __onRejected))
        return Promise(__innerTask)
        
    """
    @param {Function} initialTask   Called as handler(resolve: Function, reject: Function)
    """
    def __init__(self, initialTask, promise = None):
        self.state = State['PENDING']
        self.value = None
        self.reason = None
        self.onPromiseResolvedListeners = []
        
        def __resolve(resolveValue):
            return self.__resolve(resolveValue)
        def __reject(reason):
            return self.__reject(reason)
        def __runInitTask():
            try:
                initialTask(__resolve, __reject)
            except Exception as e:
                self.__reject(e)
        if(isinstance(promise, Promise)): 
            if(promise.state == State['PENDING']):
                promise.onPromiseResolvedListeners.append(__runInitTask)
            else:
                setTimeout(__runInitTask)
        else:
            __runInitTask()
    """
  * 修改当前Promise的状态
  * @param state 要进入的状态
  * @param valueOrReason 如果要进入fulfilled状态，那么需要一个Promise成功后的结果，如果要进入rejected状态，那么需要一个拒绝的原因
  * @returns 修改是否成功
    """
    def __changeState(self, state, valueOrReason):
        # 如果当前状态已经不是Pending了，或者尝试转移状态到pending，直接失败
        if(self.state != State['PENDING'] or state == State['PENDING']):
            return False
        self.state = state
        if(self.state == State['FULFILLED']):
            self.value = valueOrReason
        else:
            self.reason = valueOrReason
        # 执行回调
        for fn in self.onPromiseResolvedListeners:
            fn()
        return True
    
    def __resolve(self, resolveValue):
        for handler in resolveValueHandlerChain:
            if(handler.canResolve(resolveValue)):
                resolved = handler.tryToResolve(
                    resolveValue,
                    self.__changeState,
                    self.__resolve,
                    self.__reject  
                )
                if(resolved):
                    break
        
    def __reject(self, reason):
        self.__changeState(State['REJECTED'], reason)
    """
    onFulfilled: (value: any) => void
    onRejected: (reason: any) => void
    """
    def then(self, onFulfilled, onRejected):  
        """
        onFulfilled: value => {}
        onRejected: reason => {}
        self.value
        self.reason
        """
        def innerInitTask(resolve, reject):
            if(self.state == State["FULFILLED"]):
                if(not isinstance(onFulfilled, type(lambda: None))):
                    resolve(self.value)
                    return
                try:
                    result = onFulfilled(self.value)
                    resolve(result)
                except Exception as e:
                    reject(e)
            elif(self.state == State["REJECTED"]):
                if(not isinstance(onRejected, type(lambda: None))):
                    reject(self.reason)
                    return
                try:
                    result = onRejected(self.reason)
                    resolve(result)
                except Exception as e:
                    reject(e)
        p1 = Promise(innerInitTask, self)
        return p1
    
    """
    onRejected: any => Promise
    """
    def catch(self, onRejected):
        return self.then(None, onRejected)
    
    """
    callback: any => Promise
    """
    def do_finally(self, callback):
        def __onFulfilled(value):
            if(isinstance(callback, type(lambda: None))):
                callback()
            return value
        def __onRejected(reason):
            if(isinstance(callback, type(lambda: None))):
                callback()
            return reason
        return self.then(__onFulfilled, __onRejected)

if __name__ == "__main__":
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
    nestedPromise = Promise(lambda outerResolve, outerReject:(
        print('beforeResolve nestedPromise'),
        outerResolve(
            Promise(lambda innerResolve, innerReject: innerResolve("nestedPromise"))
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
    "then": lambda outerResolve, outerReject:(
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
        Promise(lambda resolve, reject: resolve(obj)).then(lambda value: print(f"testRes1:{value}"), None)
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