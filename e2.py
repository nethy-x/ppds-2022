"""Producer - consumer 

This script allows the user to experiment with producer - consumer synchronization 
problem. 

This script requires that `fei.ppds` and `matplotlib` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions and class:
    # Shared(object)
    * producer 
    * consumer
    * plot
"""

from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print
import matplotlib.pyplot as plt


class Shared(object):
    """
    A class to represent a Shared c component of storage.

    Attributes
    ----------
    finished : boolean
        free storage space control
    mutex : Mutex
        wrapper for the lock class
    free : Semaphore
        number of free items 
    items: Semaphore
        signalization util
    produced: int
        number of items in storage
    consumed: int
        number of items in storage

    Methods
    -------
    produce(count):
        Adds number to storage of produced items.

    consume(count):
        Takes number from storage of consumed items.
    """

    def __init__(self, N):
        """
        Constructs all the necessary attributes for the Shared data object.
        Parameters
        ----------
            N : int
                storage size
        """
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(N)
        self.items = Semaphore(0)
        self.produced = 0
        self.consumed = 0


def producer(shared, t):
    """
    Produce the item, checks the free space in storage, gains acces, adds the item and leaves the storage.

            Parameters:
                    shared (Shared): shared object, represents storage
                    t (int): variable, represents task execution time

            Returns:
                    None
    """
    while True:
        # production time
        sleep(t)
        # check of free space in storage
        shared.free.wait()
        if shared.finished:
            break
        # gain acces to storage room
        shared.mutex.lock()
        # storage the item

        shared.produced += 1
        # leave the storage room
        shared.mutex.unlock()
        # signalize + in storage
        shared.items.signal()


def consumer(shared, t):
    """
    Checks the items in storage, gains the acces, gains the item, leaves storage, consume item.

            Parameters:
                    shared (Shared): shared object, represents storage
                    t (int): variable, represents task execution time

            Returns:
                    None
    """
    while True:
        # check of items in storage room
        shared.items.wait()
        if shared.finished:
            break
        # gain access to storage room
        shared.mutex.lock()
        # gain item from storage
        shared.consumed += 1
        # leave the storage room
        shared.mutex.unlock()
        # process time
        shared.free.signal()
        sleep(t)


def plot(result: list):
    """
    Plots the 3D graph, sets the axes and labels them. 

            Parameters:
                    result (List): data to be visualized

            Returns:
                    None
    """
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x = [a[0] for a in result]
    y = [a[1] for a in result]
    z = [a[2] for a in result]
    ax.set_xlabel('Production time')
    ax.set_ylabel('Producers')
    ax.set_zlabel('Consumed items')
    ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
    plt.show()


storage_size = 10
results = []
sleep_time = 0.05
progress = 0
production_time = [0.01, 0.02, 0.04, 0.08, 0.1]
for p_t in production_time:
    for c_count in range(1, 11):
        items_per_sec_sum = 0
        n = 10
        for j in range(n):
            s = Shared(storage_size)
            c = [Thread(consumer, s, 0.04)
                 for _ in range(10)]
            p = [Thread(producer, s, p_t) for _ in range(c_count)]
            sleep(sleep_time)
            s.finished = True
            s.items.signal(100)
            s.free.signal(100)
            [t.join() for t in c + p]
            items = s.consumed
            items_per_sec = items / sleep_time
            items_per_sec_sum += items_per_sec
        average_per_sec = items_per_sec_sum / n
        results.append(
            (p_t, c_count, average_per_sec))
        progress += 1
        print(f'...{progress}%')
plot(results)
