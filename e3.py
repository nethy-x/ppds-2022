"""Synchronous factorial calculation
The program is doing factorial calculation for the given numbers.
However, it’s doing so in a blocking (synchronous) manner.
This file can also be imported as a module and contains the following
functions:
    * make_fact
    * main
"""

import time


def make_fact(name, n):
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
        time.sleep(0.01)
    print(f'{name} → Factorial of {n} is: {fact}')
    yield


def main():
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
    print(f'Total elapsed time: {elapsed: .1f}')


if __name__ == "__main__":
    main()
