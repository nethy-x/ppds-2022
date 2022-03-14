"""Dining philosophers

This script allows the user to experiment with dining philosophers synchronization 
problem.
 
This script requires that `fei.ppds` to be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:
    * phil
    * think 
    * eat
    * get_forks
    * put_forks
"""

from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, print

__author__ = "Juraj Budai, Matúš Jókay"


PHIL_NUM = 5


def phil(forks, footman, p_id):
    """
    Function represents philosophers that thinks, gets forks, eats and puts forks
            Parameters:
                    forks (Array(Semaphore)): array of semaphores, represents forks
                    footman (Semaphore): semaphore, represents footman
                    p_id (int): variable, represents identifier of philosopher
            Returns:
                    None
    """
    sleep(randint(40, 100)/1000)
    while True:
        think(p_id)
        get_forks(forks, footman, p_id)
        eat(p_id)
        put_forks(forks, footman, p_id)


def think(p_id):
    """
    Function represents philosophers thinking time
            Parameters:
                    p_id (int): variable, represents identifier of philosopher
            Returns:
                    None
    """
    print(f'{p_id:02d}: thinking')
    sleep(randint(40, 50)/1000)


def eat(p_id):
    """
    Function represents philosophers eating time
            Parameters:
                    p_id (int): variable, represents identifier of philosopher
            Returns:
                    None
    """
    print(f'{p_id:02d}: eating')
    sleep(randint(40, 50)/1000)


def get_forks(forks, footman, p_id):
    """
    Function represents philosophers getting up the forks
            Parameters:
                    forks (Array(Semaphore)): array of semaphores, represents forks
                    footman (Semaphore): semaphore, represents footman
                    p_id (int): variable, represents identifier of philosopher
            Returns:
                    None
    """
    footman.wait()
    print(f'{p_id:02d}: try to get forks')
    forks[p_id].wait()
    forks[(p_id+1) % PHIL_NUM].wait()
    print(f'{p_id:02d}: taken forks')


def put_forks(forks, footman, p_id):
    """
    Function represents philosophers putting down the forks
            Parameters:
                    forks (Array(Semaphore)): array of semaphores, represents forks
                    footman (Semaphore): semaphore, represents footman
                    p_id (int): variable, represents identifier of philosopher
            Returns:
                    None
    """
    forks[p_id].signal()
    forks[(p_id+1) % PHIL_NUM].signal()
    print(f'{p_id:02d}: put forks')
    footman.signal()


def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    footman = Semaphore(PHIL_NUM - 1)

    phils = [Thread(phil, forks, footman, p_id) for p_id in range(PHIL_NUM)]
    for p in phils:
        p.join()


if __name__ == '__main__':
    main()
