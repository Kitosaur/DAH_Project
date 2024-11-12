#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 14:24:20 2024

@author: meganellis
"""
        
from trilobot import Trilobot, BUTTON_A
import matplotlib.pyplot as plt
import time

tbot = Trilobot()


def main():

    speeds = [0.3, 0.5, 0.7, 0.9, 1.1] 
    stop_distance = 5  # Distance from wall in cm to stop


    intended_speeds = []
    measured_speeds = []
    
    user_distance = float(input("Enter the distance from the wall in cm: "))
    
    for speed in speeds:
        input("Press Enter to start measuring at speed {}...".format(speed))  # Wait for user input to start
        tbot.forward(speed) 
        start_time = time.time()  # Record start time
    
        # Move until the bot is 5 cm from the wall
        while tbot.read_distance() > stop_distance:
            pass  # Keep moving forward until within stop distance
    
        end_time = time.time()  # Record end time when bot stops
        tbot.stop()  # Stop the bot
        
        # Calculate the time taken and human-measured speed
        time_taken = end_time - start_time
        measured_speed = user_distance / time_taken  
    
        # Store the intended and measured speeds for plotting
        intended_speeds.append(speed)
        measured_speeds.append(measured_speed)
        print(f"Intended speed: {speed}, Measured speed: {measured_speed:.2f} cm/s")
        
    measurement_number = range(1, len(speeds) + 1)
    
    # Plotting the results
    plt.figure(figsize=(8, 6))
    plt.plot(measurement_number, measured_speeds, 'o-', label="Measured Speed", color = 'lightblue')
    plt.plot(measurement_number, intended_speeds, 'r--', label="Set Speed", color = 'darkblue')
    plt.xlabel("Set Speed (cm/s)")
    plt.ylabel("Measured Speed (cm/s)")
    plt.title("Trilobot's Set Speed vs Measured Speed")
    plt.legend()
    plt.savefig("Speed_Calibration.png", format = 'png', dpi = 300)
    plt.show()

if __name__ == "__main__":
    main()