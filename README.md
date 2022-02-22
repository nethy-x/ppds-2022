# Assignment 01

[![python](https://img.shields.io/badge/python%20-3.8.8-green.svg)](https://www.python.org/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![PEP8](https://img.shields.io/badge/PEP%208-green.svg)](https://www.python.org/dev/peps/pep-0008/#introduction)

More information about assignment at [1. excercise – Getting to know 🐍](https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/).

# About

Objective of this assignment is to implement 2 threads that use shared data. Shared index of shared array of defined size. Each thread can increment element of shared array on shared index, wich is also incremented. The function represent endless loop with condition to terminate if the index is pointing outside of the array range. Then occurance of elements are counted and printed.

We did 2 documented experiments. Both experiments consist and use same object Shared and do_count function, the diffrence is in lock usage to demonstrate paralel execution and logic behind it.

- The 1st experiment with Mutex usage is in [e1.py](e1.py).
- The 2nd experiment with Mutex usage is in [e2.py](e2.py).

## Experiment 0

This experiment is not based on the code, but on the experience we have gained in finding the right solution. We tried several variations of lock usage with diffrent outputs. Based on these experiments, we found that the critical part of the code is needed to be locked because of both Threads trying to write on same index. We also found out what is critical part and 2nd experiment is all about it. To be completly honest in those "alpha" experiments i was deadlocked with high probability every code run i did.

## Experiment 1

As mentioned [e1.py](e1.py) the usage of lock was the "most comfortable" look at problem. We evaluated that the critical part is whole endless loop and we wraped it. With that lock we secured that writing on certain index will be executed by 1 thread at the time, because other thread will be waiting for unlock. Even implemented [sleep](e1.py#L49) will not help him (as we learned from Experiment 0).

| Experiment | Sleep | Array Size |        Time        |
| :--------: | :---: | :--------: | :----------------: |
|     E1     |  ✔️   |   1_000    | 15.691299676895142 |
|     E1     |  ✔️   |   10_000   | 156.18253016471863 |
|     E1     |  ❌   |  100_000   | 0.1655588150024414 |
|     E1     |  ❌   | 1_000_000  | 1.2735166549682617 |

## Experiment 2

As mentioned [e2.py](e2.py) the usage of lock was the "most analytical" look at problem. We tryied to think "paralel" and we discoverd that, if we change the order of instructions in function do_count, we can use auxiliary variable to remember index of an array. Now we want to remember it, so we can wrap that part into lock. We wrap it with index incrementation and now we can change every writing and checking (if condition) on that index with that variable. With that we separated critical part with lock and the rest of functions instructions are not critical thanks to that variable wich is diffrent for each thread. With that lock we secured that writing on certain index will be executed by 1 thread at the time. Even implemented [sleep](e2.py#L51) will not help him (as we learned from Experiment 0).

| Experiment | Sleep | Array Size |        Time         |
| :--------: | :---: | :--------: | :-----------------: |
|     E2     |  ✔️   |   1_000    |         7.8         |
|     E2     |  ✔️   |   10_000   |  78.08997297286987  |
|     E2     |  ❌   |  100_000   | 0.25731492042541504 |
|     E2     |  ❌   | 1_000_000  | 1.5375525951385498  |

# Evaluation

Based on data from experiments we made we can see that E1 execution without [sleep](e1.py#L49) was quicker between 1.2 - 1.5x times. Also E2 exection with [sleep](e2.py#L51) was 2x - ish times quicker. It is due to diffrent lock implementation. The E2 spend less time "sleeping" because thread didnt have to wait for other sleeping thread with active lock.
