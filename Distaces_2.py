#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 15:58:33 2024

@author: meganellis
"""

from trilobot import Trilobot
import matplotlib.pyplot as plt
import numpy as np

tbot = Trilobot()

def record_distance():
    distance = tbot.read_distance()
    return distance

def main():
    
    sensor_distances = []
    user_distances = []
    
    for i in range(11):
        distance = record_distance()
        sensor_distances.append(distance)
        print(f"Measurement {i+1}: {distance} cm")
        user_distance = float(input("Enter the distance you measured in cm: "))
        user_distances.append(user_distance)
        
    print("\nSensor Distances:")
    print(sensor_distances)
    print("\nUser Distances:")
    print(user_distances)
    
    x = np.arange(1,11)
    sensor_distances_1 = np.array(sensor_distances[1:])
    user_distances_1 = np.array(user_distances[1:])
    
    sensor_fit = np.polyfit(x, sensor_distances_1, 1)
    user_fit = np.polyfit(x, user_distances_1, 1)
    
    sensor_fit_fn = np.poly1d(sensor_fit)
    user_fit_fn = np.poly1d(user_fit)
    
    y_intercept_diff = abs(sensor_fit[1]-user_fit[1])
    
    sensor_eq = f"y = {sensor_fit[0]:.2f}x + {sensor_fit[1]:.2f}"
    user_eq = f"y = {user_fit[0]:.2f}x + {user_fit[1]:.2f}"
   
    
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 11), sensor_distances[1:], 'o-', label="Sensor Distance", color = 'darkblue')
    plt.plot(range(1, 11), user_distances[1:], 'o-', label="User Measured Distance", color = 'darkgreen')
    plt.plot(x, sensor_fit_fn(x), '--' , label = ' Sensor Distance Fit' , color = 'lightblue')
    plt.plot(x, user_fit_fn(x), '--' , label = ' User Distance Fit' , color = 'lightgreen')
    plt.errorbar(range(1,11), user_distances[1:],xerr = None ,  yerr = 1, fmt = 'none', markersize = 2 , capsize = 3, barsabove = True, elinewidth =0.5, color = 'black')
    plt.text(2, max(sensor_distances_1) , sensor_eq, fontsize = 12, color = 'lightblue')
    plt.text(2, max(user_distances_1) , sensor_eq, fontsize = 12, color = 'lightgreen')
    plt.text(2, min(sensor_distances_1), f"Y-intercept Difference: {y_intercept_diff:.2f} cm", fontsize = 12, color = 'black')
    plt.title("Sensor Distance vs User Measured Distance", fontsize = 16)
    plt.xlabel("Measurement Number" , fontsize = 10)
    plt.ylabel("Distance (cm)",  fontsize = 10)
    plt.legend(loc = 'best')
    plt.savefig('Distance_Calibration_fit_5cm.png', format = 'png', dpi =300)
    plt.show()
    
    

if __name__ == "__main__":
    main()
