"""Cooperative Concurrency With Blocking Calls
This file can also be imported as a module and contains the following
functions:
    * task
    * main
"""

import queue
import time

__author__ = "Matúš Jokáy, Juraj Budai"


def task(name, work_queue):
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
        delay = work_queue.get()
        print(f"Task {name} running {delay}")
        time_start = time.perf_counter()
        time.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time {elapsed:1f}")
        yield


def main():
    work_queue = queue.Queue()

    for work in (5, 3, 4, 1):
        work_queue.put(work)

    tasks = [
        task("One", work_queue),
        task("Two", work_queue),
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
