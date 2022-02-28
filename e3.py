from fei.ppds import Thread, Mutex, Event, Semaphore
from random import randint
from time import sleep
from fei.ppds import print

"""Program with implemented function compute fibonacci  
    sequence and used Semaphore or Event for synchronization
"""


class Adt:
    """
    A class to represent a Semaphore.

    Attributes
    ----------
    N : int
        number of threads
    T : array of Semaphore/Event
        signalization util

    Methods
    -------
    wait(i):
        Waits for i-th index to signal.

    signal(i):
        Starts the i+1-th index.

    """

    def __init__(self, N):
        """
        Constructs all the necessary attributes for the Adt data object.

        Parameters
        ----------
            N : int
                number of threads
        """
        self.N = N
        self.T = [Semaphore(0) for _ in range(N + 1)]

    def wait(self, i):
        """
        Waits for i-th index of semaphore/event to signal. 

        Parameters
        ----------
            i : int
                index of thread

        Returns
        -------
        None
        """
        self.T[i].wait()

    def signal(self, i):
        """
        Starts the i+1-th index of semaphore.

        Parameters
        ----------
            i : int
                index of thread

        Returns
        -------
        None
        """
        self.T[i+1].signal()


def compute_fibonacci(sem, i):
    """
    Computes the fibonacci sequence paralel and writes the id before and after wait.

            Parameters:
                    i (int): index to sequence, thread indentifier

            Returns:
                    None
    """
    # could create barrier but sleep is good enough, all threads will exist
    sleep(randint(1, 10))
    print(f"Before wait {i}")
    sem.wait(i)
    print(f"After wait {i}")
    fib_seq[i+2] = fib_seq[i] + fib_seq[i+1]
    sem.signal(i)


# THREADS number of threads
THREADS = 10

sem = Adt(THREADS)
sem.T[0].signal()

fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1

threads = [Thread(compute_fibonacci, sem, i) for i in range(THREADS)]

[t.join() for t in threads]

print(fib_seq)
