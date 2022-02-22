from fei.ppds import Thread, Mutex
from collections import Counter
import time
from random import randint


class Shared():
    """
    A class to represent a shared data.

    Attributes
    ----------
    counter : int
        counter of elements in shared data
    end : int
        size of shared data
    elms : list
        elements in shared data
    """

    def __init__(self, size):
        """
        Constructs all the necessary attributes for the shared data object.

        Parameters
        ----------
            size : int
                number of elements in shared data
        """
        self.counter = 0
        self.end = size
        self.elms = [0] * size
        self.mutex = Mutex()


def do_count(shared):
    """Takes in a class shared, wraps counter and buffer"""
    # lock the "critical part" of function
    shared.mutex.lock()
    while True:
        if shared.counter >= shared.end:
            break
        if shared.counter % 1000 == 0:
            print(shared.counter)
        shared.elms[shared.counter] += 1
        # sleep to simulate 2nd thread
        time.sleep(randint(1, 10)/10000)
        shared.counter += 1
    shared.mutex.unlock()


shared = Shared(1_000)

start = time.time()

t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)
t1.join()
t2.join()

end = time.time()

print(end - start)

counter = Counter(shared.elms)
print(counter.most_common())
