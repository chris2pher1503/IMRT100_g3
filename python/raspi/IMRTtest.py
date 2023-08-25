#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Example code for IMRT100 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 150
TURNING_SPEED = 150
STOP_DISTANCE = 15

def stop_robot(duration):
    motor_serial.send_command(0, 0)
    time.sleep(duration)



def drive_robot(dist_1, dist_2,dist_3,dist_4, duration):
        gain = 10
        speed_motor_1 = dist_1 * gain
        speed_motor_2 = dist_2 * gain
        min_distance = min(dist_3, dist_4)
        if min_distance < STOP_DISTANCE:
            speed_motor_1 = min(speed_motor_1, DRIVING_SPEED * (min_distance / STOP_DISTANCE))
            speed_motor_2 = min(speed_motor_2, DRIVING_SPEED * (min_distance / STOP_DISTANCE))
    
        motor_serial.send_command(speed_motor_1, speed_motor_2)
        time.sleep(duration)
      
        
def drive_turn(direction,duration):
    speed = DRIVING_SPEED * direction
    motor_serial.send_command(speed, speed)
    time.sleep(duration)



def turn_robot(direction, duration):
    iteration=int(duration*10)
    for i in range(iteration):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.1)

        
        
        

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

    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_4()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_1()
    print("Dist hoyre:", dist_1, "   Dist venstre:", dist_2, "   Dist foran1:", dist_3, "   Dist foran2:", dist_4)

    # Check if there is an obstacle in the way
    if dist_1>100 and dist_2>100 and dist_3>100:
        stop_robot(60)
        
        
    
    elif dist_1>70: 
        if dist_3>40 or dist_4>40: 
            drive_turn(FORWARDS,0.5)
        if dist_3<40 or dist_4<40: 
            drive_turn(FORWARDS,0.25)
        turn_robot(RIGHT,0.6)
        if dist_3>40 or dist_4>40: 
            drive_turn(FORWARDS,0.8)
        if dist_3<40 or dist_4<40: 
            drive_turn(FORWARDS,0.4)
    
    elif dist_1<15 and dist_3<15:
        turn_robot(LEFT,0.6)
        
    elif dist_1<15 and dist_3<15 and dist_2<15: 
        turn_robot(RIGHT,0.6)
        turn_robot(RIGHT,0.6)
    elif dist_3<15 or dist_4<15:
        turn_robot(RIGHT,0.6)
        
    
        

    else:
        # If there is nothing in front of the robot it continus driving forwards
        drive_robot(dist_1,dist_2, 0.0005)
        
    ##############################################    

print("Goodbye")


# In[2]:





# In[ ]:
