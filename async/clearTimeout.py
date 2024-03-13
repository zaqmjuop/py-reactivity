# setTimeout clearTimeout
import asyncio
import nest_asyncio
nest_asyncio.apply()


async def createCoroutineByFunc(func, mesc):
    await asyncio.sleep(mesc/1000)
    func()
    return


def setTimeout(func, mesc):
    task = asyncio.create_task(createCoroutineByFunc(func, mesc))
    return task


def clearTimeout(task):
    task.cancel()
    print('clearTimeout', task)
    return task


async def main():
    task2 = setTimeout(lambda: print('第二次测试setTimeout'), 1100)
    clearTimeout(task2)
    await task2

if __name__ == "__main__":
    asyncio.run(main())
