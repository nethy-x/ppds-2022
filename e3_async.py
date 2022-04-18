"""Asynchronous factorial calculation
The program is doing factorial calculation for the given numbers.
However, it is doing so in asynchronous manner.
This file can also be imported as a module and contains the following
functions:
    * make_fact
    * main
"""

import time
import asyncio
import sys

__author__ = "Juraj Budai"


async def make_fact(name, n):
    """
    This function calculate the factorial of given value 
            Parameters:
                    name (string): variable,
                        represents identifier of task
                    n (int): variable,
                        value for calculation
            Returns:
                    None
    """
    fact = 1
    for i in range(1, n+1):
        fact = fact * i
        await asyncio.sleep(0.01)
    print(f'{name} → Factorial of {n} is: {fact}')


async def main():
    """
    This is the main entry point for the program
    """
    tasks = [
        make_fact('One', 100),
        make_fact('Two', 4),
        make_fact('Three', 7),
        make_fact('Four', 22),
        make_fact('Five', 77),
    ]

    time_start = time.perf_counter()
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed: .1f}')


if __name__ == "__main__":
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 \
            and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
