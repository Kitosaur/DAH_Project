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
led_flash_duration = 0.5  # Duration of each LED flash
sensor_angle = 0  # The servo is fixed at 0° (straight ahead)

# Initialise Trilobot
tbot = Trilobot()

# Function to flash LEDs red
def flash_red(duration=led_flash_duration, times=3):
    for _ in range(times):
        tbot.set_underlight(255, 0, 0)  # Red
        time.sleep(duration)
        tbot.clear_underlight()
        time.sleep(duration)

# Function to measure distance and flash red if object is not within threshold
def measure_distance_and_flash():
    print("Measuring distance...")
    # Keep servo pointed straight ahead (0°) without rotating
    tbot.set_servo_angle(sensor_angle)  # Ensure the servo is straight ahead
    time.sleep(0.5)  # Allow time for servo to stabilize

    # Measure distance using the distance sensor
    distance = tbot.get_distance()
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

    # Create a polar plot of angle vs measured distance
    plt.figure(figsize=(8, 6))

    ax = plt.subplot(111, projection='polar')
    ax.plot(angles_radians, measured_distances, marker='o', label="Measured Distance", color='blue')
    
    ax.set_title("Polar Plot of Angle vs Distance")
    ax.set_xlabel("Angle (radians)")
    ax.set_ylabel("Distance (cm)")
    ax.grid(True)
    ax.legend()
    plt.savefig("RadialPlot.png", dpi = 300)
    plt.show()

# Function to plot the results (Measured vs. Calculated)
def plot_results(measured_distances, recorded_distances, angles):
    print("Plotting results...")

    # Create a scatter plot of measured vs recorded distances
    plt.figure(figsize=(8, 6))

    # Scatter plot of measured vs recorded distances
    plt.scatter(measured_distances, recorded_distances, color='blue', label="Measured vs Recorded", marker='o')
    
    # Line of best fit (using numpy polyfit)
    #p = np.polyfit(measured_distances, recorded_distances, 1)  # Linear fit
    #plt.plot(measured_distances, np.polyval(p, measured_distances), color='red', label="Line of Best Fit")

    # Display the equation of the line of best fit
    #equation = f"y = {p[0]:.2f}x + {p[1]:.2f}"
    #plt.text(0.5, 0.9, equation, transform=plt.gca().transAxes, color='red', fontsize=12)

    # Labels and title
    plt.title("Measured vs Recorded Distance")
    plt.xlabel("Measured Distance (cm)")
    plt.ylabel("Recorded Distance (cm)")
    plt.grid(True)
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
        for _ in range(5):  # Ask for 5 test cases (you can adjust this number)
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
        tbot.clear_underlight()  # Turn off LEDs
        print("Measurement complete.")

# Run the main function
if __name__ == "__main__":
    main()
