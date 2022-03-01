# Assignment 02

[![python](https://img.shields.io/badge/python%20-3.8.8-green.svg)](https://www.python.org/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![PEP8](https://img.shields.io/badge/PEP%208-green.svg)](https://www.python.org/dev/peps/pep-0008/#introduction)

More information about assignment at [2. excercise – Turnstile, barrier 🚧](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F).

# About

This assignment consist of 3 exercises. They are mostly focused on correct thinking about barriers and turnstiles and correct implementation of Mutex, Semaphore and Event classes from [fei.ppds](https://pypi.org/project/fei.ppds/).

We did 3 documented exercises. First 2 of them consist and use same object SimpleBarrier.

- The 1st exercise with ADT SimpleBarrier is in [e1.py](e1.py).
- The 2nd exercise with reusable barrier is in [e2.py](e2.py).
- The 3rd exercise with Fibonacci sequence is in [e3.py](e3.py).

## Exercise 1

We immplement ADT SimpleBarrier according to the specification from the lecture. First we used ADT Semaphore for synchronization. After successful implementation with semaphore we also did try to use event signaling to implement the turnstile. A wait method of SimpleBarrier represents that turnstile of barrier, so it locks the program until all of threads complete that turnstile. For using Event synchronization util an event is signaled using signal() and all threads that are blocked in the wait() function will be unblocked. Also, any call to wait() after set() or signal() is not blocking. Its only simple barrier with 1 execution so we dont need clear() method, thats makes it possible to "reset" the event setting using the method.

## Exercise 2

To further test the ADT SimpleBarrier we implemented a reusable barrier according to the specification from the lecture. To implement ADT SimpleBarrier and Event synchronization class from Exercise 1 we had to also implement clear() method, so it is possible to reset the event setting. This is needed condition if you want to use reusable barrier. Correct implementation also consist of using 2 barriers instead of 1 like it was in Exercise 1, because circulation of threads would be possible. And the separation of printing thread id´s is implemented in rendezvous and ko functions.

## Exercise 3

We created N threads and thread index represent the node where the element at position i+2 of the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, 13, 21...) is calculated. All threads share a list into which the computed elements of the sequence are stored sequentially during the computation. We design it with using the synchronization tool Semaphore or Event, a synchronization such that thread i+2 can perform the calculation of its Fibonacci number only after the threads that calculate the previous numbers of the sequence have stored their results in the list. We implemented Adt class wich contained Semaphore or Event object (it was a little bit of overkill but it was said, that is better to do it object oriented style). We initialized that object with N threads wich results in N + 1 synchronizations classes.

# Questions

- What is the smallest number of synchronization objects (semaphores, mutexes, events) needed to solve this problem?

> In my solution of problem the N + 1 synchronization objects was needed but that last one was not really needed so N objects. But its possible to do it with less than N but i didnt manage to solve it.

- Which of the synchronization patterns discussed (mutual exclusion, signaling, rendezvous, barrier) can be (reasonably) used to solve this problem? Specifically describe how this or that synchronization pattern is used in your solution.

> I did only used Semaphores and Events so the signaling patterns. Although i have counted with sleep and according to exercise, the calculation threads must be created right at the beginning, before the calculation of the elements of the sequence starts. So maybe reasonable solution (instead of counting with sleep function that will provide that nothing will start until...) would be to implement barrier so they are stucked at each other.

# Evaluation

The 3rd exercise was very nice example of distraction, thinking about fibonacci sequence paralelization because in
that case you have to wait until the values in front of "your position" will be computed. But in the end it was not about fibonacci sequence it was all about that, all threads must come to array (computing part) in right order.
