"""Cooperative Concurrency With Non-Blocking Calls
This file can also be imported as a module and contains the following
functions:
    * task
    * main
"""

import asyncio
import time

__author__ = "Matúš Jokáy, Juraj Budai"


async def task(name, work_queue):
    """
    This function pulls work out of work_queue and processes
    the work until there is not any more to do.
            Parameters:
                    name (string): variable,
                        represents identifier of task
                    work_queue (Queue): count of values
                        for the tasks to process
            Returns:
                    None
    """
    if work_queue.empty():
        print(f"Task {name} nothing to do")
        return

    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running {delay}")
        time_start = time.perf_counter()
        await asyncio.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time {elapsed:1f}")


async def main():
    work_queue = asyncio.Queue()

    for work in (5, 3, 4, 1):
        await work_queue.put(work)

    tasks = [
        task("One", work_queue),
        task("Two", work_queue),
    ]

    time_start = time.perf_counter()
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed}')


if __name__ == "__main__":
    asyncio.run(main())
