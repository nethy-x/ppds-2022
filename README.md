# Assignment 05

[![python](https://img.shields.io/badge/python%20-3.8.8-green.svg)](https://www.python.org/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![PEP8](https://img.shields.io/badge/PEP%208-green.svg)](https://www.python.org/dev/peps/pep-0008/#introduction)

More information about assignment at [5. excercise – Smokers problem, savages problem 🚬](https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/).

# About

This assignment consist of 3 exercises.
We did document 2nd exercise of type 2. We also wrote thoughts about synchronization problems and tools usage and wrote the pseudocode for implementation. We also constructed a model in Python language from pseudocode.

- The 1st exercise with Smokers synchronization problem is in [e1.py](e1.py).
- The 2nd type 1 exercise with Dinning savages simulation [e2_1.py](e2_1.py).
- The 2nd type 2 exercise with Dinning savages simulation [e2_2.py](e2_2.py).

---

## Exercise 1

According to the lecture, we did implement a solution to the problem of smokers. For the modification in which the agent does not wait for resource allocation signaling, we didnt solve the smoker preference problem.

---

## Exercise 2 - #1

Program that solves the modified synchronization problem of Dinning Savages #1.

Savages always START having dinner all together. When they all get together, they gradually start taking from the pot (and possibly waking up the cook). The cook puts the portions in the pot, not the savage!

According to the lecture, we did implement a solution to the dinning savages problem.

---

## Exercise 2 - #2

Program that solves the modified synchronization problem of Dinning Savages #2.

There are several cooks in a tribe. When a savage discovers that the pot is empty, he wakes up ALL the cooks, who can help each other in cooking and cook together. JUST ONE cook tells the waiting savage that it is done. The cook puts the portions in the pot, not the savage!

### **1. Analysis of synchronization**

This problem is based on the idea of Producers-consumers and Readers-writers synchronization problem , augmented by tracking the state of the "store" (how many portions are in the pot). We also user barrier so savages are eating together wich was not necessary. And also Semaphore(N) as a classic solution to prevent race conditions and the problem of hungry philosophers.

However, the standard solution of the Feasting Savages needs to be extended even further to accomplish task assignment with a combination of locks, counter and condition. 

My adaptation of the solution is based on Locks to secure both critical part and ensure integrity. Also counter that increment cooks that finished their cooking and Semaphore reinitialization for N signalization. 

0. Semaphore(C) to signalize empty pot with number of cooks
1. Mutex used for wrapping the cooking part when they are all adding servings to pot.
2. Condition used for checking how many servings were made so they dont exceed the number of desired servings that pot can handle
3. Mutex used when they are finishing cooking and letting each other know that they finished, so 
last cook can give signal to savages that they can come to eat
4. Counter used for checking that the last cook is actually last cook finishing cooking. Comparing to number of cooks


### **2. Pseudocode**

    FUNCTION putServingsInPot(shared, cookNumber, servingsNumber):
        WHILE True:
            shared.cooking.lock()
            # cook checks if he is needed to cook another portion
            IF(shared.servings == servingsNumber) THEN
                shared.cooking.unlock()
                # if not he can leave serving part
                return
            ENDIF
            # cooking time
            sleep(time / cookNumber)
            # cook adds the portion to servings in pot
            shared.servings += 1
            shared.cooking.unlock()
    END FUNCTION


    FUNCTION cook(shared, cookNumber, servingsNumber):
        while True:
            # cooks wait for pot to be empty
            shared.emptyPot.wait()
            # cooks enter the space
            putServingsInPot(servingsNumber, shared)
            shared.finishing.lock()
            # cook checks if he is the last finished cooking
            IF(shared.cooksFinished == cookNumber) THEN
                # cook emptied the counter
                shared.cooksFinished = 0
                # cook giving signal to savages that pot is full
                shared.fullPot.signal()
            ENDIF
            # cook escaped the space and added himself as finished
            shared.cooksFinished += 1
            shared.finishing.unlock()
    END FUNCTION


### **3. Documented code and prints**

- Documented code : [e2_2.py](e2_2.py).

---



