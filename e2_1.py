"""Nuclear Power Plant #1

This script allows the user to experiment with specific excercise about
modelled processes in a nuclear power plant

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

__author__ = "Juraj Budai, Matúš Jókay"


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


def init():
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = LightSwitch()
    ls_sensor = LightSwitch()
    valid_data = Event()

    for monitor_id in range(2):
        Thread(monitor, monitor_id,
               turnstile, ls_monitor, valid_data, access_data)
    for sensor_id in range(11):
        Thread(sensor, sensor_id,
               turnstile, ls_sensor, valid_data, access_data)


def monitor(monitor_id, turnstile, ls_monitor, valid_data, access_data):
    """
    Function represents monitors of nuclear plant operators
            Parameters:
                    monitor_id (): variable, represents identifier of monitor
                    turnstile (Semaphore): semaphore, represents turnstile
                    ls_monitor (LightSwitch): light switch, represents light
                        switch for monitor
                    valid_data (Event): event, represents validation data
                    access_data (Semaphore): semaphore, represents data to
                        work with
            Returns:
                    None
    """
    # monitor cant work, while there is not 1 written data
    valid_data.wait()
    while True:
        # the monitor has a pause 500ms from start or last update
        sleep(.5)

        # we block the turnstile to throw the sensors out of the KO
        turnstile.wait()
        # we get access to the "storage"
        count_read_monitors = ls_monitor.lock(access_data)
        turnstile.signal()

        # data access simulated by the following statement
        print(
            f'Monitor {monitor_id:02d} :'
            f'count_read_monitors={count_read_monitors: 02d}')
        # we have updated the data, we are leaving the repository
        ls_monitor.unlock(access_data)


def sensor(sensor_id, turnstile, ls_sensor, valid_data, access_data):
    """
    Function represents sensors of nuclear plant
            Parameters:
                    sensor_id (): variable, represents identifier of sensor
                    turnstile (Semaphore): semaphore, represents turnstile
                    ls_sensor (LightSwitch): light switch, represents light
                        switch for sensor
                    valid_data (Event): event, represents validation data
                    access_data (Semaphore): semaphore, represents data to
                        work with
            Returns:
                    None
    """

    while True:
        # sensors pass through the turnstile until it is locked by the monitor
        turnstile.wait()
        turnstile.signal()

        # gettig access to "storage"
        count_write_sensors = ls_sensor.lock(access_data)
        # data access simulated by waiting at interval 10 - 15 ms
        write_time = randint(10, 15) / 1000

        # according to the task specification, we inform about the sensor
        # and the entry to be made
        print(
            f'Sensor {sensor_id:02d} : '
            f'count_write_sensors={count_write_sensors:02d}, '
            f'write_time={write_time:5.3f}')
        sleep(write_time)
        # after entering the data, we signal that the data is valid
        valid_data.signal()
        # we're leaving the "storage" away
        ls_sensor.unlock(access_data)


if __name__ == '__main__':
    init()
