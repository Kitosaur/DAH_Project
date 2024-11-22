#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 15:58:33 2024

@author: meganellis
"""

from trilobot import Trilobot
import matplotlib.pyplot as plt

tbot = Trilobot()

def record_distance():
    """
    Trilobot will use the ultrasonic sensor to measure the distance to the object and return this distance.
    """
    distance = tbot.read_distance()
    return distance

def main():

    #initialising empty lists for the distances measured by the ultrasonic sensor and the distances entered by the user.
    sensor_distances = []
    user_distances = []

    #Taking 10 measurements of distance which could be in any range and interval. For this experiment a range from 0-100cm and interval of 10cm was used.
    for i in range(10):
        distance = record_distance()
        sensor_distances.append(distance)
        #lets the user know what distance the sensor measured.
        print(f"Measurement {i+1}: {distance} cm")
        #Ask the user to enter the corresponding distance they measure. 
        user_distance = float(input("Enter the distance you measured in cm: "))
        user_distances.append(user_distance)
        
    print("\nSensor Distances:")
    print(sensor_distances)
    print("\nUser Distances:")
    print(user_distances)
    
    
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 11), sensor_distances, 'o-', label="Sensor Distance")
    plt.plot(range(1, 11), user_distances, 'x-', label="User Measured Distance")

    plt.title("Sensor Distance vs User Measured Distance")
    plt.xlabel("Measurement Number")
    plt.ylabel("Distance (cm)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
