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
    distance = tbot.read_distance()
    return distance

def main():
    
    sensor_distances = []
    user_distances = []
    
    for i in range(10):
        distance = record_distance()
        sensor_distances.append(distance)
        print(f"Measurement {i+1}: {distance} cm")
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
