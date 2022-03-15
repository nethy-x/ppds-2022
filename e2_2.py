"""Nuclear Power Plant #2

This script allows the user to experiment with specific alternative excercise
about modelled processes in a nuclear power plant

This script requires that `fei.ppds` to be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions and class:
    # LightSwitch
    * monitor
    * sensor
"""

from fei.ppds import Semaphore, Mutex, Thread, Event, print
from time import sleep
from random import randint

__author__ = "Juraj Budai"


class LightSwitch:
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
        self.mutex = Mutex()
        self.cnt = 0

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
        cnt = self.cnt
        self.cnt += 1
        if self.cnt == 1:
            sem.wait()
        self.mutex.unlock()
        return cnt

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
        if self.cnt == 0:
            sem.signal()
        self.mutex.unlock()


class SimpleBarrier:
    """
    A class to represent a barrier.
    Attributes
    ----------
    N : int
        number of threads
    C : int
         counter for blocked threads
    M : Mutex()
        wrapper for the lock class
    T : Event()
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
        self.C = 0
        self.M = Mutex()
        # self.T = Semaphore(0)
        self.T = Event()

    def wait(self):
        """
        Locks program until all of threads complete turnstile.
        Parameters
        ----------
        None
        Returns
        -------
        None
        """

        self.M.lock()
        self.T.clear()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()


def monitor(monitor_id, turnstile, ls_monitor, valid_data, access_data):
    """
    Function represents monitors of nuclear plant operators
            Parameters:
                    monitor_id (): variable, represents identifier of monitor
                    turnstile (Semaphore): semaphore, represents turnstile
                    ls_monitor (LightSwitch): light switch, represents light
                        switch for monitor
                    valid_data (Event): event, represents validation data
                    access_data (Semaphore): semaphore, represents data
                        to work with
            Returns:
                    None
    """
    # monitor cant work, while there is not 1 written data
    valid_data.wait()
    while True:
        # the monitor has a pause of 400 - 500ms from start or last update
        sleep(randint(40, 50) / 1000)

        # we block the turnstile to throw the sensors out of the KO
        turnstile.wait()
        # we get access to the "storage"
        count_read_monitors = ls_monitor.lock(access_data)
        turnstile.signal()

        # data access simulated by the following statement
        print(
            f'Monitor : {monitor_id:02d} - '
            f'count_read_monitors={count_read_monitors:02d}')
        # we have updated the data, we are leaving the repository
        ls_monitor.unlock(access_data)


def sensor(sensor_id, turnstile, ls_sensor, valid_data, access_data, barrier):
    """
    Function represents sensors of nuclear plant
            Parameters:
                    sensor_id (): variable, represents identifier of sensor
                    turnstile (Semaphore): semaphore, represents turnstile
                    ls_sensor (LightSwitch): light switch, represents
                        light switch for sensor
                    valid_data (Event): event, represents validation data
                    access_data (Semaphore): semaphore, represents data
                        to work with
            Returns:
                    None
    """
    i = 0
    while True:
        # sensor update
        sleep(randint(50, 60) / 1000)

        # sensors pass through the turnstile until it is locked by the monitor
        turnstile.wait()
        turnstile.signal()

        # getting access to "storage"
        count_write_sensors = ls_sensor.lock(access_data)

        # data access simulated by waiting at intervals,
        # data update itself takes 10-20 ms for sensor_id 0 and
        # sensor_id 1, but 20-25 ms for sensor_id 2.
        write_time = randint(10, 20) / 1000
        if sensor_id == 2:
            write_time = randint(20, 25) / 1000

        # according to the task specification
        # we inform about the sensor and the entry to be made
        print(
            f'Sensor {sensor_id:02d} : '
            f'count_write_sensors={count_write_sensors:02d}, '
            f'write_time={write_time:5.3f}')
        # write time sleep
        sleep(write_time)

        # implement barrier so they all enter data by writing
        if i == 0:
            barrier.wait()
        i += 1
        # after entering the data, we signal that the data is valid
        valid_data.signal()
        # we're leaving the "storage" away
        ls_sensor.unlock(access_data)


def init():
    SENSORS = 3
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = LightSwitch()
    ls_sensor = LightSwitch()
    valid_data = Event()
    barrier = SimpleBarrier(SENSORS)

    for monitor_id in range(8):
        Thread(monitor, monitor_id,
               turnstile, ls_monitor, valid_data, access_data)
    for sensor_id in range(SENSORS):
        Thread(sensor, sensor_id,
               turnstile, ls_sensor, valid_data, access_data, barrier)


if __name__ == '__main__':
    init()
