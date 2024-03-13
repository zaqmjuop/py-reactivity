import asyncio
import nest_asyncio
nest_asyncio.apply()

async def createCoroutineByFunc(func, mesc):
    await asyncio.sleep(mesc/1000)
    func()
    return

def print_hello():
    print("Hello, world!")

async def main():
    task = asyncio.create_task(createCoroutineByFunc(print_hello, 4000))
    await task

def clearTimeout(cor):
    print(cor)
    # 怎么中断协程
    pass

if __name__ == "__main__":
    print('运行')
    # cor = main()
    # res = asyncio.run(cor)
    asyncio.run(createCoroutineByFunc(print_hello, 2000))
    print('end')
    # clearTimeout(cor)