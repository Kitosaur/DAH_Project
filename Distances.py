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
    #measure distance using ultrasonic distance sensor
    distance = tbot.read_distance()
    return distance

def main():
    
    sensor_distances = []
    user_distances = []
    
    for i in range(10):
        #measure distance to the object
        distance = record_distance()
        sensor_distances.append(distance)
        #print this value
        print(f"Measurement {i+1}: {distance} cm")
        #ask the user to input the corresponding distance they measure
        user_distance = float(input("Enter the distance you measured in cm: "))
        user_distances.append(user_distance)
        
    print("\nSensor Distances:")
    print(sensor_distances)
    print("\nUser Distances:")
    print(user_distances)
    
    #Plot a graph of the two data series against measurement number to compare the variation.
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
