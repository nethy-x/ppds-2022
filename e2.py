"""Synchronous (Blocking) HTTP Calls
The program is doing some actual work with real IO by making HTTP requests
to a list of URLs and getting the page contents.
However, it’s doing so in a blocking (synchronous) manner.
This file can also be imported as a module and contains the following
functions:
    * task
    * main
"""

import queue
import time
import urllib.request

__author__ = "Matúš Jokáy, Juraj Budai"


def task(name, work_queue):
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

    while not work_queue.empty():
        url = work_queue.get()
        print(f"Task {name} running {url}")
        time_start = time.perf_counter()
        urllib.request.urlopen(url)
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time {elapsed:1f}")
        yield


def main():
    """
    This is the main entry point for the program
    """
    work_queue = queue.Queue()

    for url in (
        'http://google.com',
        'http://microsoft.com',
        'https://facebook.com',
        'http://twitter.com',
        'http://stuba.sk',
        'http://uim.fei.stuba.sk',
    ):
        work_queue.put(url)

    tasks = [
        task('One', work_queue),
        task('Two', work_queue),
    ]

    done = False
    time_start = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)

            if not tasks:
                done = True
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed}')


if __name__ == "__main__":
    main()
