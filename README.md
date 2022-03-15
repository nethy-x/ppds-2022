# Assignment 04

[![python](https://img.shields.io/badge/python%20-3.8.8-green.svg)](https://www.python.org/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![PEP8](https://img.shields.io/badge/PEP%208-green.svg)](https://www.python.org/dev/peps/pep-0008/#introduction)

More information about assignment at [4. excercise – Dining philosophers, Atomic power plant 🍽️](https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/).

# About

This assignment consist of 3 exercises.
We did document 2nd exercise of type 2. We also wrote analysis of synchronization tools and wrote the pseudocode for implementation. We also constructed a model in Python language from pseudocode.

- The 1st exercise with Dining philosopers synchronization problem is in [e1.py](e1.py).
- The 2nd type 1 exercise with Atomic power plant simulation [e2_1.py](e2_1.py).
- The 2nd type 2 exercise with Atomic power plant simulation [e2_2.py](e2_2.py).

---

## Exercise 1

We didnt implement a solution to the dinner philosophers' synchronization problem using right-handed and left-handed philosophers such that the conditions are satisfied.

---

## Exercise 2 - #1

We implemented the solution for Atomic power plant simulation from lecture.

---

## Exercise 2 - #2

In a nuclear power plant we have 3 sensors:

- 1 primary circuit coolant flow sensor (sensor P): 10-20ms data update
- 1 primary coolant temperature sensor (sensor T): 10-20ms data update
- 1 control rod insertion depth sensor (sensor H): 20-25ms data update
- sensors are constantly trying to update the measured values: 50-60ms update
- they store the data in a common data storage
- each sensor has a dedicated space in the data storage where it stores the data
- 8 operators in that plant who are each constantly looking at their monitor where the sensor readings are displayed.
- the request for data updates is sent by the monitor constantly in a cycle: 40-50 ms update.

- monitors can only start working when all sensors have already supplied valid data to the storage.

### **1. Analysis of synchronization**

It is a task of mutual exclusion of processes categories. Monitors form one category, sensors form another. For both categories counts that multiple members of a category can access data at the same time.

- Monitors only read the data, they do not modify it in any way, so multiple people can access the same sensor's data at the same time.
- Each sensor has its own space where it stores data, sensors cannot overwrite each other's data this means that multiple sensors can update their data at the same time.

Interesting issue here is timing. Two type off sensors are constantly trying to update its data, and this update takes 10-20 ms and one type takes 20-25ms. And they update them in 50-60ms. The monitor tries to get an update every 40-50 ms. The times are quite balanced so it can happen that monitors can start working when sensors have not already supplied valid data to the repository.

### **2. Map the synchronization tasks**

- access_data = Semaphore(1)
  - secure synchronization for accesing data
- turnstile = Semaphore(1)
  - sensors pass through the turnstile until it is locked by the monitor
  - monitor cant work, while there is not 1 written data
- ls_monitor = LightSwitch()
  - monitor repository for their own data
- ls_sensor = LightSwitch()
  - sensor repository for their own data
- valid_data = Event()
  - secure synchronization about writing data
- barrier = SimpleBarrier(3)
  - secure that monitors can only start working when all sensors have already supplied valid data to the repository

### **3. Pseudocode**

    FUNCTION monitor(monitorId, turnstile, lsMonitor, validData, accessData):
        validData.wait()
        WHILE True:
            sleep(40-50ms)
            turnstile.wait()
            countReadMonitors = lsMonitor.lock(accessData)
            turnstile.signal()
            print("Monitor":monitorId : "Reads":countReadMonitors)
            lsMonitor.unlock(accessData)
    END FUNCTION

    FUNCTION sensor(sensorId, turnstile, lsSensor, validData, accessData, barrier):
        i = 0
        WHILE True:

            sleep(50-60ms)
            turnstile.wait()
            turnstile.signal()
            countWriteSensors = lsSensor.lock(accessData)
            IF sensorId == 2 THEN
                writeTime = random(20-25)
            ENDIF
            writeTime = random(10-20)
            print("Sensor":sensorId : "Writes":countWriteSensors : "Write time":writeTime)
            sleep(writeTime ms)
            IF x == 0 THEN
                barrier.wait()
            ENDIF
            i += 1
            validData.signal()
            lsSensor.unlock(accessData)
    END FUNCTION

    FUNCTION init():
        accessData = Semaphore(1)
        turnstile = Semaphore(1)
        lsMonitor = LightSwitch()
        lsSensor = LightSwitch()
        validData = Event()
        barrier = SimpleBarrier(SENSORS)
        FOR monitorId FROM 0 -> 8:
            createRunThread(monitor(monitorId, turnstile, lsMonitor, validData, accessData))
            ENDLOOP
        FOR sensorId FROM 0 -> 3:
            createRunThread(sensor(sensorId, turnstile, lsSensor, validData, accessData, barrier))
            ENDLOOP
    END FUNCTION

### **4. Constructed model**

- Documented code : [e2_2.py](e2_2.py).

---

# Evaluation

I dont really know, if barrier implementations is the best for this purpose, but didnt find out any other solution to this problem that should be working.
