"""Light switch

This script requires that fei.ppds module be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
class:

    * LighSwitch(object)
"""

from fei.ppds import Mutex


class LightSwitch(object):
    """
    A class to represent a LightSwitch.

    Attributes
    ----------
    cnt : int
        free storage space control
    mutex : Mutex
        wrapper for the lock class

    Methods
    -------
    lock(sem):
        Thread is the first to try to "get into the room"

    unlock(sem):
        Thread is the last to try to "get out of the room"
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the LightSwitch.

        Parameters
        ----------
        """
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        """
        Thread is the first to try to "get into the room"

        Parameters
        ----------
            sem : Semaphore
                semaphore for synchronization

        Returns
        -------
        None
        """
        self.mutex.lock()
        if not self.cnt:
            sem.wait()
        self.cnt += 1
        self.mutex.unlock()

    def unlock(self, sem):
        """
        Thread is the last to try to "get out of the room"

        Parameters
        ----------
            sem : Semaphore
                semaphore for synchronization

        Returns
        -------
        None
        """
        self.mutex.lock()
        self.cnt -= 1
        if not self.cnt:
            sem.signal()
        self.mutex.unlock()
