"""The solution to the modified savage problem #2

This script allows the user to experiment with dinning savages
synchronization problem.
This script requires that `fei.ppds` to be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions and class:
    # SimpleBarrier
    # Shared
    * get_serving_from_pot
    * eat
    * put_servings_in_pot
    * savage
    * cook
"""

from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep

__author__ = "Juraj Budai"


M = 8
N = 4
C = 3


class SimpleBarrier:
    """
    A class to represent a barrier.
    Attributes
    ----------
    N : int
        number of threads
    M : Mutex()
        wrapper for the lock class
    C : int
         counter for blocked threads
    S : Semaphore()
        signalization util
    Methods
    -------
    wait():
        Represents the barrier's turnstile.
    """

    def __init__(self, N):
        """
        Constructs all the necessary attributes for the SimpleBarrier object.
        Parameters
        ----------
            N : int
                number of threads
        """
        self.N = N
        self.M = Mutex()
        self.C = 0
        self.S = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        """
        Locks program until all of threads complete turnstile.
        Parameters
        ----------
            print_str : string
                string for better problem visualization
            savage_id : int
                identifier of savage
            print_last_thread : boolean
                decision for better problem visualization
            print_each_thread : boolean
                decision for better problem visualization
        -------
        None
        """
        self.M.lock()
        self.C += 1
        if print_each_thread:
            print(print_str % (savage_id, self.C))
        if self.C == self.N:
            self.C = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.S.signal(self.N)
        self.M.unlock()
        self.S.wait()


class Shared:
    """
    A class to represent a shared object for servings and
    synchronisation utils.

    Attributes
    ----------
    M : Mutex()
        wrapper for the lock class
    S : int
        number of servings
    full_pot : Semaphore()
        signalization util
    empty_pot : Semaphore()
        signalization util
    B1 : SimpleBarrier()
        synchronisation util
    B2 : SimpleBarrier()
        synchronisation util
    cooking: Mutex()
        wrapper for the lock class
    finishing: Mutex()
        wrapper for the lock class
    cooks_finished: int
        number of finished cooks
    Methods
    -------
    None
    """

    def __init__(self):
        self.M = Mutex()
        self.S = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(C)
        self.B1 = SimpleBarrier(N)
        self.B2 = SimpleBarrier(N)
        self.cooking = Mutex()
        self.finishing = Mutex()
        self.cooks_finished = 0


def get_serving_from_pot(savage_id, shared):
    """
    Function represents portion taking from shared pot
            Parameters:
                    savage_id (int): variable, represents identifier of savage
                    shared (Shared): shared object, represents place
            Returns:
                    None
    """
    print("savage %2d: taking portion" % savage_id)
    shared.S -= 1


def eat(savage_id):
    """
    Function represents time of eating savage
            Parameters:
                    savage_id (int): variable, represents identifier of savage
            Returns:
                    None
    """
    print("savage %2d: eating" % savage_id)
    # portion eating time.
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared, C):
    """
    Function represents eating and waiting savages
            Parameters:
                    savage_id (int): variable, represents identifier of savage
                    shared (Shared): shared object, represents place
                    C (int): constant, represent number of cooks
            Returns:
                    None
    """
    while True:
        shared.B1.wait(
            "savage %2d: i did arrive, we are %2d",
            savage_id,
            print_each_thread=True)
        shared.B2.wait("savage %2d: we are all here, lets eat",
                       savage_id,
                       print_last_thread=True)

        #  classic solution to the problem of feasting savages
        shared.M.lock()
        print("savage %2d: serving in pot: %2d" %
              (savage_id, shared.S))
        if shared.S == 0:
            print("savage %2d: cooks wake up! %2d" % (savage_id, C))
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.M.unlock()
        eat(savage_id)


def put_servings_in_pot(cook_id, M, shared):
    """
    Function represents portion adding to shared pot
            Parameters:
                    cook_id (int): variable, represents identifier of cook
                    M (int): constant, represents number of portions
                    shared (Shared): shared object, represents place
            Returns:
                    None
    """
    while True:
        shared.cooking.lock()
        if(shared.S == M):
            shared.cooking.unlock()
            return
        # cooking time
        sleep(0.4 + randint(0, 2) / 10 / C)
        print(f'cook {cook_id} :  i am cooking')
        shared.S += 1
        shared.cooking.unlock()


def cook(cook_id, shared, C, M):
    """
    Function represents cooking of each cook together
            Parameters:
                    cook_id (int): variable, represents identifier of cook
                    shared (Shared): shared object, represents place
                    C (int): constant, represent number of cooks
                    M (int): constant, represents number of portions
            Returns:
                    None
    """
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(cook_id, M, shared)
        shared.finishing.lock()
        print(f'cook: {cook_id} finished')
        if(shared.cooks_finished == C):
            shared.cooks_finished = 0
            shared.full_pot.signal()
        shared.cooks_finished += 1
        shared.finishing.unlock()


def init_and_run(N, M, C):
    """
    Function represents experiment
            Parameters:
                    N (int): constant, represents number of savages
                    M (int): constant, represents number of portions
                    C (int): constant, represent number of cooks
            Returns:
                    None
    """
    threads = list()
    shared = Shared()
    for savage_id in range(0, N):
        threads.append(Thread(savage, savage_id, shared, C))

    for cook_id in range(0, C):
        threads.append(Thread(cook, cook_id, shared, C, M))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run(N, M, C)
