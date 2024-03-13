import asyncio

async def my_coroutine():
    while True:
        print("Coroutine is running")
        await asyncio.sleep(1)

# 创建一个任务
task = asyncio.create_task(my_coroutine())

# 等待一段时间
await asyncio.sleep(5)

# 取消任务
task.cancel()

# 等待任务被取消
try:
    await task
except asyncio.CancelledError:
    print("The coroutine has been cancelled.")