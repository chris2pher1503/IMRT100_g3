#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Example code for IMRT100 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys
import random


import pygame
import threading
image_path='MyMans.jpg'
mp3_file_path='under.mp3'

def display_image(image_path, screen):
    image = pygame.image.load(image_path)
    image_width, image_height = image.get_rect().size

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))
        screen.blit(image, ((screen_width - image_width) // 2, (screen_height - image_height) // 2))
        pygame.display.flip()

def play_music(mp3_file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file_path)
    pygame.mixer.music.play()
    time.sleep(30)  # Adjust the duration as needed
    pygame.mixer.music.stop()

# Initialize pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the path to your MP3 file and image
mp3_file_path = 'Barbiesong.mp3'
image_path = 'MyMans.jpg'

# Start playing the music in a separate thread
music_thread = threading.Thread(target=play_music, args=(mp3_file_path,))
music_thread.start()

# Display the image
display_image(image_path, screen)

# Wait for the music thread to finish before quitting
music_thread.join()



LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 50
TURNING_SPEED = 150
STOP_DISTANCE = 10
sving=1.25

def stop_robot(duration):
    motor_serial.send_command(0, 0)
    time.sleep(duration)



def drive_robot(dist_1, dist_2, duration):
        gain = 10
        speed_motor_1 = dist_1 * gain
        speed_motor_2 = dist_2 * gain
        motor_serial.send_command(speed_motor_1, speed_motor_2)
        time.sleep(duration)
        
def drive_turn(direction,duration):
    speed = DRIVING_SPEED * direction
        motor_serial.send_command(speed, speed)
        time.sleep(duration)

#        
        

def turn_robot(direction, duration):
    motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
    time.sleep(duration)

        
        
        



# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 100 #Hz
execution_period = 1. / execution_frequency #seconds


# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

    
# Start serial receive thread
motor_serial.run()


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :


    ###############################################################
    # This is the start of our loop. Your code goes below.        #
    #                                                             #
    # An example is provided to give you a starting point         #
    # In this example we get the distance readings from each of   #
    # the two distance sensors. Then we multiply each reading     #
    # with a constant gain and use the two resulting numbers      #
    # as commands for each of the two motors.                     #
    #  ________________________________________________________   #
    # |                                                        |  #
    # V                                                           #
    # V                                                           #
    ###############################################################




    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_4()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_1()
    print("Dist hoyre:", dist_1, "   Dist venstre:", dist_2, "   Dist foran1:", dist_3, "   Dist foran2:", dist_4 ,)

    # Check if there is an obstacle in the way
    if dist_1>100 and dist_2>100 and dist_3>100: 
        stop_robot(10)
        #play song
        
    
    elif dist_1>70: 
        drive_turn(FORWARDS,0.1)
        turn_robot(RIGHT,sving)
        drive_turn(FORWARDS,0.4)
    
    elif dist_1<15 and dist_3<15:
        turn_robot(LEFT,sving)
        
    elif dist_1<15 and dist_3<15 and dist_2<15: 
        turn_robot(RIGHT,sving)
        turn_robot(RIGHT,sving)
    elif dist_3<10 or dist_4<10:
        turn_robot(RIGHT,sving)
        
    
        

    else:
        # If there is nothing in front of the robot it continus driving forwards
        drive_robot(dist_1,dist_2, 0.0005)
        
        
        
        
        


                

#k

    ###############################################################
    #                                                           A #
    #                                                           A #
    # |_________________________________________________________| #
    #                                                             #
    # This is the end of our loop,                                #
    # execution continus at the start of our loop                 #
    ###############################################################
    ###############################################################





# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("Goodbye")


# Quit pygame
pygame.quit()
sys.exit()



