"""Barber shop problem without overtaking
This script allows the user to experiment with less classical 
synchronization problems,
This script requires that `fei.ppds` to be installed within the Python
environment you are running this script in.
This file can also be imported as a module and contains the following
functions and class:
    # BarberShop
    * barber
    * cut_hair
    * get_hair_cut
    * customer
"""

from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, Event, print

__author__ = "Juraj Budai"


N_CHAIRS = 5


class BarberShop:
    """
    A class to represent a Barber shop.

    Attributes
    ----------
    chairs : int
        number of threads
    customer_number : int
        number of customers in barber shop
    mutex : Mutex()
        wrapper for the lock class
    barber : Semaphore(0)
        fifo semaphore
    customer : Semaphore(0)
        signalization util
    barber_done : Semaphore(0)
        signalization util for rendezvous
    customer_done : Semaphore(0)
        signalization util for rendezvous

    Methods
    -------
    None

    """

    def __init__(self, chairs):
        """
        Constructs all the necessary attributes for the BarberShop object.

        Parameters
        ----------
            chairs : int
                number of threads
        """
        self.chairs = chairs
        self.customers_number = 0
        self.mutex = Mutex()
        self.barber = Semaphore(0, 'fifo')
        self.customer = Semaphore(0)
        self.barber_done = Semaphore(0)  # Event()
        self.customer_done = Semaphore(0)  # Event()


def barber(barber_shop):
    """
    Function represents barber cutting hair and calling for next customer
            Parameters:
                    barber_shop (BarberShop): shared object, represents barber shop
            Returns:
                    None
    """
    while True:
        barber_shop.customer.wait()
        barber_shop.mutex.lock()
        print("✂ Barber: Next one please...")
        barber_shop.mutex.unlock()
        barber_shop.barber.signal()
        cut_hair()
        barber_shop.customer_done.wait()
        print("✂ Barber: Haircut is finished!")
        barber_shop.barber_done.signal()


def cut_hair():
    """
    Function represents barbers time consuption of cutting hair
            Parameters:
                    None
            Returns:
                    None
    """
    print("✂ Barber: I am cutting customer's hair")
    sleep(randint(1, 10) / 10)


def get_hair_cut(custom_id):
    """
    Function represents customers time consuption of getting haircut
            Parameters:
                    custom_id (int): variable, represents identifier of customer
            Returns:
                    None
    """
    sleep(randint(1, 10) / 100)
    print(f"🧑 Customer {custom_id}: I am getting my hair cut.")


def customer(barber_shop, customer_id):
    """
    Function represents customer coming to shop, getting haircut and leaving barber shop
            Parameters:
                    barber_shop (BarberShop): shared object, represents barber shop
            Returns:
                    None
    """
    while True:
        sleep(randint(5, 10) / 100)
        barber_shop.mutex.lock()
        if barber_shop.customers_number == barber_shop.chairs:
            print(f"🧒 Customer {customer_id}: Barber shop is full!")
            barber_shop.mutex.unlock()
            continue
        barber_shop.customers_number += 1
        print(
            f"🧒 Customer {customer_id}: Hello gentlemen.")
        print(
            f"💈 Barber shop has {barber_shop.chairs - barber_shop.customers_number} chairs left.")
        barber_shop.mutex.unlock()

        barber_shop.customer.signal()
        barber_shop.barber.wait()

        get_hair_cut(customer_id)

        barber_shop.customer_done.signal()
        barber_shop.barber_done.wait()

        barber_shop.mutex.lock()
        barber_shop.customers_number -= 1
        print(
            f"👦 Customer {customer_id}: Hair cut is good. Goodbye! ")
        print(
            f"💈 Barber shop has {barber_shop.chairs - barber_shop.customers_number} chairs left.")
        barber_shop.mutex.unlock()


def init():
    """
    Function represents initialization of an experiment
            Parameters:
                    None
            Returns:
                    None
    """
    barber_shop = BarberShop(N_CHAIRS)

    b = Thread(barber, barber_shop)
    customers = [Thread(customer, barber_shop, customer_id)
                 for customer_id in range(10)]

    b.join()
    [c.join() for c in customers]


if __name__ == '__main__':
    init()
