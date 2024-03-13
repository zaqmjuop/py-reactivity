import asyncio 

async def setTimeout(func, mesc):
    await asyncio.sleep(mesc/1000)
    func()

helloTimes = 0


def helloWorld():
    global helloTimes
    print(f'hello world {helloTimes}')
    helloTimes += 1


async def main():
   await setTimeout(helloWorld, 1000)

if __name__ == "__main__":
    asyncio.run(main())