import asyncio


class Timeout:
    def __init__(self):
        self._task = None

    def set(self, delay, callback):
        # Cancel the previous task if it exists
        if self._task:
            self._task.cancel()

        # Schedule the new task
        self._task = asyncio.get_event_loop().create_task(self._job(delay, callback))
        return self._task

    async def _job(self, delay, callback):
        await asyncio.sleep(delay)
        callback()

    def clear(self):
        if self._task:
            self._task.cancel()
            self._task = None


async def main():
    # Usage
    timeout = Timeout()
    task = timeout.set(1.0, lambda: print('Hello, world!'))
    timeout.clear()
    try:
        await task
    except asyncio.CancelledError:
        print('cleared')

if __name__ == "__main__":
    asyncio.run(main())
