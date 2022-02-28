from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event
from fei.ppds import print

"""Program with implemented simple barrier 
    and used Event or Semaphore for synchronization
"""


class SimpleBarrier:
    """
    A class to represent a barrier.

    Attributes
    ----------
    N : int
        number of threads
    C : int
        counter for blocked threads
    M : Mutex()
        wrapper for the lock class
    T : Event()
        signalization util

    Methods
    -------
    wait():
        Represents the barrier's turnstile.

    """

    def __init__(self, N):
        """
        Constructs all the necessary attributes for the SimpleBarrier data object.

        Parameters
        ----------
            N : int
                number of threads
        """
        self.N = N
        self.C = 0
        self.M = Mutex()
        # self.T = Semaphore()
        self.T = Event()

    def wait(self):
        """
        Locks program until all of threads complete turnstile. 

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()


def barrier_simple(barrier, thread_id):
    """
    Represent a basic barrier implementation.

            Parameters:
                    barrier (SimpleBarrier): A SimpleBarrier class
                    thread_id (int): Thread indentifier

            Returns:
                    None
    """
    sleep(randint(1, 10)/10)
    print(f"Before ->barrier {thread_id}")
    barrier.wait()
    print(f"After barrier-> {thread_id}")


# THREADS number of threads
THREADS = 10

sb = SimpleBarrier(THREADS)

threads = [Thread(barrier_simple, sb, i) for i in range(THREADS)]
[t.join() for t in threads]
