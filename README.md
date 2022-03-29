# Assignment 06

[![python](https://img.shields.io/badge/python%20-3.8.8-green.svg)](https://www.python.org/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![PEP8](https://img.shields.io/badge/PEP%208-green.svg)](https://www.python.org/dev/peps/pep-0008/#introduction)

More information about assignment at [6. excercise – Less classical synchronization problems :-)](https://uim.fei.stuba.sk/i-ppds/6-cvicenie-menej-klasicke-synchronizacne-problemy/).

# About

This assignment consist of 4 exercies.
We did document and code exercise 1. which was about barber shop synchronization problem. We have implemented both solution with overtaking and no overtaking customers in waiting room of barber shop. We also wrote tools used and wrote the pseudocode for alternative implementation of no overtaking policy handling.

- The Barber shop with overtaking policy synchronization problem is in [e1_overtake.py](e1_overtake.py).
- The Barber shop with no overtaking policy synchronization problem is in [e2_no_overtake.py](e2_no_overtake.py).



# Description

According to the lecture, we did implement a solution to the problem of barber shop.

- The barber shop consists of two rooms:
    - Waiting room for N clients (N chairs)
    - Barber's room (1 chair for a client)
- If there is no client, the barber sleeps
- If a client enters
    - And all chairs are occupied, he leaves
    - And the barber is occupied, but there is a vacant chair, sits down and waits
    - And the barber is asleep, wakes him up, sits down and waits
- Coordination between clients and the barber

---
## Experiment 1 - #overtake

Scoreboard (customer thread)

2x Rendezvous (barber and customer,
barber_done and customer_done)

1. chairs - Number of clients that can sit in waiting room of barber shop
2. customer_number - number of clients actually sitting in waiting room of barber shop
3. mutex - Mutex used for wrapping the coming and leaving part of barber shop, where they are all able to access shared "chairs" counter 
4. barber - Semaphore used for arrival at the barbershop, customer actually  waits for the barber until the barber calls him to come to the chair
5. customer - Semaphore for barber that waits for customer until he comes to the barbershop
6. barber_done a customer_done - Semaphores for signalization... after the haircut, customer signals "customer_done" and waits for "barber_done"

There is no guaranteed order for customers. 
Barber uses barber.signal() to call any customer on his chair to make him a hair cut.

---

## Experiment 2 - #no overtake

Scoreboard (customer thread)

2x Rendezvous (barber and customer,
barber_done and customer_done)

1x FIFO Semaphore

1. chairs - Number of clients that can sit in waiting room of barber shop
2. customer_number - number of clients actually sitting in waiting room of barber shop
3. mutex - Mutex used for wrapping the coming and leaving part of barber shop, where they are all able to access shared "chairs" counter 
4. barber - FIFO Semaphore used for arrival at the barbershop, customer actually  waits for the barber until the barber calls him to come to the chair
5. customer - Semaphore for barber that waits for customer until he comes to the barbershop
6. barber_done a customer_done - Semaphores for signalization... after the haircut, customer signals "customer_done" and waits for "barber_done"

Now there is guaranteed order for customers.
Barber uses barber.signal() to call customer that first entered the waiting room on his chair to make him a hair cut, then he leaves, and he call the next one in line (2nd customer that entered the waiting room)
We did implement it with using FIFO Semaphore from ['fei.ppds'](https://pypi.org/project/fei.ppds/) package with synchronization objects. 
        
        barber = Semaphore(0, 'fifo')


---

### **Pseudocode - #no overtake alternative**

    CLASS BarberShop():
        chairs = N
        customers = 0
        mutex = Mutex()
        barber = Queue()
        customer = Semaphore()
        customerDone = Semaphore()
        barberDone = Semaphore()

    FUNCTION barber():
        WHILE True:
            customer.wait()
            mutex.lock()
            barberSemaphore = barber.get()
            mutex.unlock()
            barberSemaphore.signal()
            cutHair()
            customerDone.wait()
            barberDone.signal()
    END FUNCTION


    FUNCTION customer():
        WHILE True:
            mutex.lock()
            if customers == chairs:
                mutex.unlock()
            customers += 1
            barber.put(barberSemaphore)
            mutex.unlock()
            customer.signal()
            barberSemaphore.wait()
            getHaircut()
            customerDone.signal()
            barberDone.wait()
            mutex.lock()
            customers -= 1
            mutex.unlock()
    END FUNCTION

---


