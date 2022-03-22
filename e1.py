"""The smokers problem
This script allows the user to experiment with smokers
synchronization problem.
This script requires that `fei.ppds` to be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions and class:
    # Shared
    * agent_1
    * agent_2
    * agent_3
    * make_cigarette
    * smoke
    * smoker_tobacco
    * smoker_paper
    * smoker_match
    * pusher_tobacco
    * pusher_paper
    * pusher_match
"""

from random import randint
from time import sleep
from fei.ppds import Thread, Mutex, Semaphore, print

__author__ = "Matúš Jókay, Juraj Budai"


class Shared(object):
    """
    A class to represent a shared object for smokers and
    agents and pushers.

    Attributes
    ----------
    tobacco : Semaphore()
        signalization util
    paper : Semaphore()
        signalization util
    match : Semaphore()
        signalization util
    agentSem : Semaphore()
        signalization util
    pusherTobacco : Semaphore()
        signalization util
    pusherPaper : Semaphore()
        signalization util
    pusherMatch : Semaphore()
        signalization util
    mutex: Mutex()
        wrapper for the lock class
    isTobacco: boolean
        boolean for decisions
    isPaper: boolean
        boolean for decisions
    isMatch: boolean
        boolean for decisions
    Methods
    -------
    None
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the SimpleBarrier object.
        Parameters
        ----------
        None
        """
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)
        self.agentSem = Semaphore(1)

        self.pusherTobacco = Semaphore(0)
        self.pusherPaper = Semaphore(0)
        self.pusherMatch = Semaphore(0)

        self.mutex = Mutex()
        self.isTobacco = False
        self.isPaper = False
        self.isMatch = False


def agent_1(shared):
    """
    Function represents agent 1
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.agentSem.wait()
        print('\nagent: tobacco, paper')
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    """
    Function represents agent 2
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.agentSem.wait()
        print('\nagent: paper, match')
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    """
    Function represents agent 3
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.agentSem.wait()
        print('\nagent: tobacco, match')
        shared.tobacco.signal()
        shared.match.signal()


def make_cigarette(name):
    """
    Function represents rolling cigarette
            Parameters:
                    name (string): smoker identifier
            Returns:
                    None
    """
    print(f"Smoker : {name} rolling")
    sleep(randint(0, 10)/100)


def smoke(name):
    """
    Function represents smoking cigarette
            Parameters:
                    name (string): smoker identifier
            Returns:
                    None
    """
    print(f"Smoker: {name} smoking")
    sleep(randint(0, 10)/100)


def smoker_tobacco(shared):
    """
    Function represents smoker need tobacco
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.pusherTobacco.wait()
        make_cigarette("tobacco")
        shared.agentSem.signal()
        smoke("tobacco")


def smoker_paper(shared):
    """
    Function represents smoker need paper
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.pusherPaper.wait()
        make_cigarette("paper")
        shared.agentSem.signal()
        smoke("paper")


def smoker_match(shared):
    """
    Function represents smoker need match
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        sleep(randint(0, 10)/100)
        shared.pusherMatch.wait()
        make_cigarette("match")
        shared.agentSem.signal()
        smoke("match")


def pusher_tobacco(shared):
    """
    Function represents pusher with tobacco
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper = False
            shared.pusherMatch.signal()
        elif shared.isMatch:
            shared.isMatch = False
            shared.pusherPaper.signal()
        else:
            shared.isTobacco = True
        shared.mutex.unlock()


def pusher_paper(shared):
    """
    Function represents pusher with paper
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        shared.paper.wait()
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco = False
            shared.pusherMatch.signal()
        elif shared.isMatch:
            shared.isMatch = False
            shared.pusherTobacco.signal()
        else:
            shared.isPaper = True
        shared.mutex.unlock()


def pusher_match(shared):
    """
    Function represents pusher with match
            Parameters:
                    shared (Shared): shared data for synchronization
            Returns:
                    None
    """
    while True:
        shared.match.wait()
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco = False
            shared.pusherPaper.signal()
        elif shared.isPaper:
            shared.isPaper = False
            shared.pusherTobacco.signal()
        else:
            shared.isMatch = True
        shared.mutex.unlock()


def run_experiment():
    """
    Function represents experiment
            Parameters:
                    None
            Returns:
                    None
    """
    shared = Shared()

    smokers = []
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))
    smokers.append(Thread(smoker_match, shared))

    pushers = []
    pushers.append(Thread(pusher_tobacco, shared))
    pushers.append(Thread(pusher_paper, shared))
    pushers.append(Thread(pusher_match, shared))

    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in smokers+agents+pushers:
        t.join()


if __name__ == "__main__":
    run_experiment()
