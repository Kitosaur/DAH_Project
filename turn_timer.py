# -*- coding: utf-8 -*-
"""
Script to calculate the time taken for one full turn
"""

from trilobot import Trilobot
import time

# Initialize the Trilobot
bot = Trilobot()

# Speed for the turn (adjust)
turn_speed = 0.6

try:
    # Record the start time
    start_time = time.time()
    
    # Start turning the Trilobot
    bot.turn_left(speed=turn_speed)
    
    # Allow time for a full turn
    time.sleep(2)  # Adjust based on Trilobot's turning speed and calibration

    # Stop the Trilobot
    bot.stop()
    
    # Record the end time
    end_time = time.time()
    
    # Calculate the time taken for one full turn
    turn_duration = end_time - start_time
    print(f"Time taken for one full turn: {turn_duration:.2f} seconds")

except KeyboardInterrupt:
    # Stop the Trilobot if interrupted
    bot.stop()
    print("Interrupted. Stopping the robot.")
