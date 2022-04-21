"""Asynchronous (Non-Blocking) HTTP Calls
This version of the program modifies the previous one to use
Python async features.
It also imports the aiohttp module, which is a library to make HTTP requests
in an asynchronous fashion using asyncio.
This file can also be imported as a module and contains the following
functions:
    * task
    * main
"""

import time
import asyncio
import aiohttp

__author__ = "Matúš Jokáy, Juraj Budai"


async def task(name, work_queue):
    """
    This function pulls work out of work_queue and processes
    the work until there is not any more to do.
            Parameters:
                    name (string): variable,
                        represents identifier of task
                    work_queue (Queue): list of URLs
                        for the tasks to access
            Returns:
                    None
    """
    if work_queue.empty():
        print(f"Task {name} nothing to do")
        return
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f"Task {name} running {url}")
            time_start = time.perf_counter()
            async with session.get(url) as response:
                await response.text()
            elapsed = time.perf_counter() - time_start
            print(f"Task {name}     elapsed time {elapsed:1f}")


async def main():
    """
    This is the main entry point for the program
    """
    work_queue = asyncio.Queue()

    for url in (
        'http://google.com',
        'http://microsoft.com',
        'https://facebook.com',
        'http://twitter.com',
        'http://stuba.sk',
        'http://uim.fei.stuba.sk',
    ):
        await work_queue.put(url)

    tasks = [
        task('One', work_queue),
        task('Two', work_queue),
    ]

    time_start = time.perf_counter()
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed: .1f}s')


if __name__ == "__main__":
    asyncio.run(main())
