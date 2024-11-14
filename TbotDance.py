#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 14:13:53 2024

@author: meganellis

Uses button A to begin dancing with a multicoloured light show for 30 seconds.
Uses button B to toggle following a user/object and stops after the button is pressed a second time.
"""

import time
from trilobot import Trilobot, NUM_BUTTONS, BUTTON_A, BUTTON_B, BUTTON_C
from picamera import PiCamera
from datetime import datetime
from time import sleep

# Initialise the Trilobot
tbot = Trilobot()
camera = PiCamera()

max_speed = 1         
goal_distance = 20.0 #The distance the trilobot will stay away from an object when following it
speed_range = 5.0  # The distance an object is from the goal that will have the robot drive at full speed
SPEED = 0.7  # The speed the trilobot will move with 
TURN_DISTANCE = 20  # How close an object needs to be before the robot turns
FORWARD_DISTANCE = 5  # The distance to move forward before checking for an object again
TURN_DURATION = 1.0 #Time taken for the trilobot to do a full turn
FORWARD_DURATION = 0.5 #Time the trilobot will move forwards for 

def check_button_press(button):
    """
    Check if a specified button is pressed.
    """
    return tbot.read_button(button)

def flash_lights_dance():
    """
    Flashes lights on the Trilobot with a multicoloured pattern and performs a dance routine for 30 seconds.
    """
    duration = 30 #number of seconds the trilobot will preform for
    flashes = 10 #number of flashes
    flash_interval = 0.3 #time between flashes
    slow_interval = 0.5 #time duration for slower movements
    end_time = time.time() + duration 

    while time.time() < end_time:
        
        for i in range(flashes):
            # Turn on LEDs with a cycling colour pattern
            for led in range(NUM_BUTTONS):
                #for each flash, a color value (RGB tuple), is calculated by multiplying i by a different factor (25, 50, 75)
                #and taking the remainder when divided by 255.
                colour = (i * 25 % 255, (i * 50) % 255, (i * 75) % 255)
                tbot.set_button_led(led, True, colour=colour)
            #pauses for the flash interval between flashes
            time.sleep(flash_interval)
            
            #The dancing
            tbot.forward()          
            time.sleep(flash_interval)
            tbot.backward()          
            time.sleep(slow_interval)
            tbot.turn_left()         
            time.sleep(flash_interval / 2)
            tbot.turn_right()        
            time.sleep(flash_interval / 2)
            tbot.spin()              
            time.sleep(slow_interval)
            tbot.forward()          
            time.sleep(flash_interval / 1.5)
            tbot.backward()         
            time.sleep(flash_interval)
            tbot.coast()

            #Turn LEDs off after each flash cycle
            for led in range(NUM_BUTTONS):
                tbot.set_button_led(led, False)
            time.sleep(flash_interval)
            
def follow_person():
    """
    Follow a person/object by maintaining a set distance using the ultrasonic sensor on the Trilobot.
    """
    while True:
        # Check if Button B is pressed again to stop following
        if check_button_press(BUTTON_B):
            tbot.disable_motors()
            break
        
        # Measure distance and adjust speed to maintain goal distance
        distance = tbot.read_distance()
        if distance >= 0.0:  #Valid distance reading
            #this line finds the difference between the distance from the object and the ideal distance and normalises it
            scale = (distance - goal_distance) / speed_range
            speed = max(min(scale, 1.0), -1.0) * max_speed
            tbot.set_motor_speeds(speed, speed)
        else:
            tbot.disable_motors()

        time.sleep(0.01)

def obstacles():
    """
    Makes the robot wander around, avoiding obstacles and making turns when necessary
    it encounters an object closer than 20cm, the trilobot will turn.
    Continually checks for obstacles.
    """
    while True:
        distance = tbot.read_distance()
        if distance < TURN_DISTANCE:
            camera.start_preview()
            sleep(2) 
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"/home/pi/trilobot_image_{timestamp}.jpg"
            camera.capture(filename)
            print(f"Image captured and saved as {filename}")
            camera.stop_preview()
            tbot.turn_right(SPEED)
            time.sleep(TURN_DURATION)
        
            distance = tbot.read_distance()
            if distance < TURN_DISTANCE:
                tbot.turn_right(SPEED)
                time.sleep(TURN_DURATION*2)
                distance = tbot.read_distance()
            
                if distance < TURN_DISTANCE:
                    tbot.turn_left(SPEED)
                    time.sleep(TURN_DURATION)
                    return

            tbot.forward(SPEED)
            time.sleep(FORWARD_DURATION)
    
            tbot.turn_left(SPEED)
            time.sleep(TURN_DURATION)
    
            distance = tbot.read_distance()
            if distance >= TURN_DISTANCE:
                tbot.forward(SPEED)
            else:
                obstacles()
        else:
           tbot.forward(SPEED)
            
    
def wandering():
    
    start_time = time.time()
    duration = 60  

    while time.time() - start_time < duration:
        obstacles()
        time.sleep(0.1)

    tbot.coast()


def main():
    """Main function to check for button presses and trigger corresponding actions."""
    last_state_A = False
    last_state_B = False
    last_state_C = False
    following_mode = False
    
    while not tbot.read_button(BUTTON_C):
        pass

    while True:
        # Check button states
        button_A_state = check_button_press(BUTTON_A)
        button_B_state = check_button_press(BUTTON_B)
        button_C_state = check_button_press(BUTTON_C)

        # If Button A is pressed, start the light and dance routine
        if button_A_state and not last_state_A:
            flash_lights_dance()  
            
        # Toggle following mode on each Button B press
        if button_B_state and not last_state_B:
            if following_mode:
                
                tbot.disable_motors()
                following_mode = False
            else:
         
                following_mode = True
                follow_person()  
        
        if button_C_state and not last_state_C:
            wandering()

        # Update the last states of the buttons
        last_state_A = button_A_state
        last_state_B = button_B_state
        last_state_C = button_C_state

if __name__ == "__main__":
    main()
