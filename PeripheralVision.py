#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:10:06 2024

@author: jessicakitchen
"""
import time
import numpy as np
import matplotlib.pyplot as plt
from trilobot import Trilobot

# Constants
distance_threshold = 30  # Distance in cm to trigger the red flash
led_flash_duration = 0.3  # Duration of each LED flash
sensor_angle = 0  # The servo is fixed at 0° (straight ahead)

# Initialise Trilobot
tbot = Trilobot()

# Function to flash LEDs red
def flash_red(duration=led_flash_duration, times=3):
    for _ in range(times):
        tbot.fill_underlighting(255, 0, 0)  # Red
        time.sleep(duration)
        tbot.clear_underlighting()
        time.sleep(duration)

# Function to measure distance and flash red if object is not within threshold
def measure_distance_and_flash():
    print("Measuring distance...")
    # Keep servo pointed straight ahead (0°) without rotating
    tbot.set_servo_angle(sensor_angle)  # Ensure the servo is straight ahead
    time.sleep(0.5)  # Allow time for servo to stabilize

    # Measure distance using the distance sensor
    distance = tbot.read_distance()
    print(f"Measured distance to object: {distance} cm")

    # Flash red if no object is detected within 50 cm
    if distance > distance_threshold:
        print("No object detected within 50 cm. Flashing red...")
        flash_red()

    return distance

# Function to ask user for the relative angle of the object
def get_relative_angle():
    while True:
        try:
            angle = float(input("Enter the relative angle of the object in degrees (from -90 to 90): "))
            if -90 <= angle <= 90:
                return angle
            else:
                print("Please enter an angle between -90° and 90°.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to calculate the distance (simulated, since the robot only measures directly ahead)
def calculate_distance(angle, measured_distance):
    # The distance remains the same because we're only measuring straight ahead, but this
    # function can be expanded if you want to simulate distance based on angle for a wider field of view.
    return measured_distance  # No change for simplicity in this example

# Function to plot the Polar plot (angle vs. distance)
def plot_polar_results(measured_distances, angles):
    print("Plotting polar results...")

    # Convert angles to radians for polar plot
    angles_radians = np.radians(angles)
    
    #filter the data
    filtered_angles = [angle for angle, dist in zip(angles_radians, measured_distances) if dist <= 50]
    filtered_distances = [dist for dist in measured_distances if dist <50]

    # Create a polar plot of angle vs measured distance
    plt.figure(figsize=(8, 6))

    
    ax = plt.subplot(111, projection='polar')
    ax.yaxis.set_label_coords(-0.1, 0.5)
    ax.plot(filtered_angles[1:], filtered_distances[1:], marker='o', label="Measured Distance", color='darkblue')
    ax.set_yticklabels([])
    
    ax.set_title("Polar Plot of Angle vs Distance")
    ax.set_xlabel("Angle /radians")
    ax.set_ylabel("Distance /cm")
    ax.grid(True)
    ax.legend()
    plt.savefig("RadialPlot.png", dpi = 300)
    plt.show()

# Function to plot the results (Measured vs. Calculated)
def plot_results(measured_distances, recorded_distances, angles):
    print("Plotting results...")
    angles_radians = np.radians(angles)
    
    # Create a scatter plot of measured vs recorded distances
    plt.figure(figsize=(8, 6))
    plt.errorbar(angles_radians[1:], measured_distances[1:], xerr = 0.083, capsize = 3)
    filtered_angles = [angles for angles, dist in zip(angles_radians, measured_distances) if dist <= 40]
    filtered_distances = [dist for dist in measured_distances if dist <=40]
    # Scatter plot of measured vs recorded distances
    #plt.scatter(angles_radians[1:], recorded_distances[1:], color='darkblue', label="Recorded Distances", marker='o')
    #plt.scatter(angles_radians[1:], measured_distances[1:], color = 'lightblue', label = "Measured Distances", marker = 'o')
    plt.scatter(filtered_angles, filtered_distances, color = 'lightblue', label = "Measured Distances", marker = 'o')
    plt.fill_between([0, 3], 29.5, 30.5, color = 'lightgray', alpha = 0.3, label ='Recorded Distance')
    
    # Line of best fit (using numpy polyfit)
    #p = np.polyfit(measured_distances, recorded_distances, 1)  # Linear fit
    #plt.plot(measured_distances, np.polyval(p, measured_distances), color='red', label="Line of Best Fit")

    # Display the equation of the line of best fit
    #equation = f"y = {p[0]:.2f}x + {p[1]:.2f}"
    #plt.text(0.5, 0.9, equation, transform=plt.gca().transAxes, color='red', fontsize=12)

    plt.gca().invert_yaxis()
    # Labels and title
    plt.title("Measured vs Recorded Distance")
    plt.xlabel("Angle /radians")
    plt.ylabel("Distance /cm")
    plt.ylim(0, 50)
    plt.legend()
    plt.savefig("UservsBotPeripheralDistances.png", dpi = 300)
    plt.show()

# Main function
def main():
    try:
        # Lists to store angles, measured distances, and recorded distances
        angles = []
        measured_distances = []
        recorded_distances = []

        # Ask the user for the relative angle and measure the distance
        for _ in range(18):  # Ask for 5 test cases (you can adjust this number)
            angle = get_relative_angle()
            angles.append(angle)

            # Measure the distance at the fixed forward angle
            measured_distance = measure_distance_and_flash()
            measured_distances.append(measured_distance)

            # Calculate the distance (we can simulate here as no angle-based calculation is available)
            recorded_distance = calculate_distance(angle, measured_distance)
            recorded_distances.append(recorded_distance)
             

            print(f"Recorded distance at {angle}°: {recorded_distance} cm\n")

        # Plot the polar results (angle vs. distance)
        plot_polar_results(measured_distances, angles)

        # Plot the results (Measured vs Recorded with line of best fit)
        plot_results(measured_distances, recorded_distances, angles)

    finally:
        tbot.stop()  # Stop the robot
        tbot.clear_underlighting()  # Turn off LEDs
        print("Measurement complete.")

# Run the main function
if __name__ == "__main__":
    main()
