#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:14:22 2024

@author: meganellis
"""

import time
from trilobot import Trilobot, NUM_BUTTONS, BUTTON_X
from datetime import datetime
from time import sleep

tbot = Trilobot()

def check_button_press(button):
    """
    Check if a specified button is pressed.
    """
    return tbot.read_button(button)
            

def obstacles():

    #turn distance is the buffer distance
    turn_distance = 30
    wait_time = 2
    speed = 0.9
    #calibrated for a 90-degree turn 
    quarter_turn_time = 0.35 
    #calibrated for a 180-degree turn 
    half_turn_time = 0.7 
    
    while True:
        distance = tbot.read_distance()
        
        if distance < turn_distance:
            
            tbot.coast()
            time.sleep(wait_time)
            tbot.turn_right(speed)
            time.sleep(quarter_turn_time) #Trilobot is facing right
            tbot.coast()
            distance = tbot.read_distance()
            
            if distance < turn_distance:
                time.sleep(wait_time)
                tbot.turn_left(speed)
                time.sleep(half_turn_time) #Trilobot is facing left
                tbot.coast()
                distance = tbot.read_distance()
                
                if distance < turn_distance:
                    tbot.turn_left(speed)
                    time.sleep(quarter_turn_time) #Trilobot is facing backwards
                    tbot.coast()
                    tbot.forward(speed)
                    time.sleep(2)
                    tbot.coast()
                    return
        else:
            tbot.forward(speed)
            time.sleep(0.1)
            
                   
    
def wandering():
    
    start_time = time.time()
    #the Trilobot will 'wander' while avoiding obstacles for 500 seconds
    duration = 500  

    while time.time() - start_time < duration:
        obstacles()
        time.sleep(0.1)

    tbot.coast()


def main():
    """
    Main function to check for button presses and trigger corresponding actions.
    """
    
    last_state_X = False
  
    while not tbot.read_button(BUTTON_X):
        pass

    while True:
        #Check button state
        button_X_state = check_button_press(BUTTON_X)
 
        if button_X_state and not last_state_X:
            wandering()

        #Update the last states of the button
        last_state_X = button_X_state

if __name__ == "__main__":
    main()
