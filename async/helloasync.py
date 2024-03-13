import asyncio
import nest_asyncio
nest_asyncio.apply()
# 解决RuntimeWarning: coroutine 'createCoroutineByFunc' was never awaited
async def createCoroutineByFunc(func, mesc):
    await asyncio.sleep(mesc/1000)
    func()
    return

# 定义一个函数
def print_hello():
    print("Hello, world!")

if __name__ == "__main__":
  # 运行createCoroutineByFunc函数
  asyncio.run(createCoroutineByFunc(print_hello, 1000))