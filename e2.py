from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event
from fei.ppds import print

"""Program with implemented cyclic barrier 
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
        # self.T = Semaphore(0)
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
        self.T.clear()
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()


def rendzevous(thread_id):
    """
    Writes out thread id before barrier.

            Parameters:
                    thread_id (int): Thread indentifier

            Returns:
                    None
    """
    # sleep to simulate threads
    sleep(randint(1, 10)/10)
    print(f"Rendezvous, ->barrier : {thread_id}")


def ko(thread_id):
    """
    Writes out thread id after barrier.

            Parameters:
                    thread_id (int): Thread indentifier 

            Returns:
                    None
    """
    print(f"Ko, barrier-> {thread_id}")
    # sleep to simulate threads
    sleep(randint(1, 10)/10)


def barrier_cycle(barrier1, barrier2, thread_id):
    """
    Represent a cyclic barrier implementation.

            Parameters:
                    barrier1 (SimpleBarrier): A SimpleBarrier class of 1st barrier
                    barrier2 (SimpleBarrier): A SimpleBarrier class of 2nd barrier
                    thread_id (int): Thread indentifier 

            Returns:
                    None
    """

    while True:
        rendzevous(thread_id)
        barrier1.wait()
        ko(thread_id)
        barrier2.wait()


# THREADS number of threads
THREADS = 10

sb1 = SimpleBarrier(THREADS)
sb2 = SimpleBarrier(THREADS)

threads = [Thread(barrier_cycle, sb1, sb2, i) for i in range(THREADS)]
[t.join() for t in threads]
