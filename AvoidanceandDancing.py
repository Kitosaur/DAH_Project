#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:14:22 2024

@author: meganellis
"""

import time
from trilobot import Trilobot, NUM_BUTTONS, BUTTON_A, BUTTON_C
from datetime import datetime
from time import sleep

tbot = Trilobot()

def check_button_press(button):
    """
    Check if a specified button is pressed.
    """
    return tbot.read_button(button)


def flash_lights_dance():
    """
    Flashes lights on the Trilobot with a multicoloured pattern and performs a dance routine for 30 seconds.
    """
    duration = 30
    flashes = 10
    flash_interval = 0.3
    slow_interval = 0.5
    end_time = time.time() + duration

    while time.time() < end_time:
        
        for i in range(flashes):
            # Turn on LEDs with a cycling colour pattern
            for led in range(NUM_BUTTONS):
                colour = (i * 25 % 255, (i * 50) % 255, (i * 75) % 255)
                tbot.set_button_led(led, True, colour=colour)
            
            time.sleep(flash_interval)
            
            # Dance moves with varied speeds
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

            # Turn LEDs off after each flash cycle
            for led in range(NUM_BUTTONS):
                tbot.set_button_led(led, False)
            time.sleep(flash_interval)
            

def obstacles(): 
    """
    Makes the robot wander around, avoiding obstacles and making turns when necessary
    it encounters an object closer than 20cm, the trilobot will turn.
    Continually checks for obstacles.
    """
    Turn_Distance = 20
    Turn_Duration = 1.0
    Speed = 0.7
    Forward_Duration = 0.5
    
    while True:
        distance = tbot.read_distance()
        if distance < Turn_Distance:
          
            sleep(2) 
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"/home/pi/trilobot_image_{timestamp}.jpg"
     
            print(f"Image captured and saved as {filename}")
          
            tbot.turn_right(Speed)
            time.sleep(Turn_Duration)
        
            distance = tbot.read_distance()
            if distance < Turn_Distance:
                tbot.turn_right(Speed)
                time.sleep(Turn_Duration*2)
                distance = tbot.read_distance()
            
                if distance < Turn_Distance:
                    tbot.turn_left(Speed)
                    time.sleep(Turn_Duration)
                    return

            tbot.forward(Speed)
            time.sleep(Forward_Duration)
    
            tbot.turn_left(Speed)
            time.sleep(Turn_Duration)
    
            distance = tbot.read_distance()
            if distance >= Turn_Distance:
                tbot.forward(Speed)
            else:
                obstacles()
        else:
           tbot.forward(Speed)
            
    
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
  
    last_state_C = False
  
    
    while not tbot.read_button(BUTTON_C):
        pass

    while True:
        # Check button states
        button_A_state = check_button_press(BUTTON_A)
       
        button_C_state = check_button_press(BUTTON_C)

        # If Button A is pressed, start the light and dance routine
        if button_A_state and not last_state_A:
            flash_lights_dance()  
            
       
        
        if button_C_state and not last_state_C:
            wandering()

        # Update the last states of the buttons
        last_state_A = button_A_state
      
        last_state_C = button_C_state

if __name__ == "__main__":
    main()