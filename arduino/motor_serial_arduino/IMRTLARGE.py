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
DRIVING_SPEED = 100
TURNING_SPEED = 100
STOP_DISTANCE = 25

def stop_robot(duration):

    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.1)

def drive_robot(direction, duration):
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        time.sleep(0.1)

def turn_robot(direction, duration):
    speed = TURNING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, -speed)
        time.sleep(0.1)

# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 10 #Hz
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


    # Get the current time
   # iteration_start_time = time.time()



    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_4()
    dist_5 = motor_serial.get_dist_5()
    print("Dist right:", dist_1, "   Dist left:", dist_2, "   Dist forwards1:", dist_3, "   Dist forwards2:", dist_4, "   Dist straigh ahead:", dist_5)

    #Check if there is a wall in front of the robot
    if dist_5 < STOP_DISTANCE and dist_3 < STOP_DISTANCE and dist_4 < STOP_DISTANCE:
        print("Wall in front of robot")
        stop_robot(1)
        turn_robot(RIGHT, 1)

    #Check if there is a wall to the right of the robot
    elif dist_1 < STOP_DISTANCE:
        print("Wall to the right of robot")
        stop_robot(1)
        turn_robot(LEFT, 1)
    #Check if there is a wall to the left of the robot
    elif dist_2 < STOP_DISTANCE:
        print("Wall to the left of robot")
        stop_robot(1)
        turn_robot(RIGHT, 1)
    #Turn to the side with the most space
    elif dist_1 < dist_2:
        print("Turning left")
        turn_robot(LEFT, 1)
    elif dist_1 > dist_2:
        print("Turning right")
        turn_robot(RIGHT, 1)
    else:
        print("Driving forwards")
        drive_robot(FORWARDS, 1)
    


    # Send commands to motor
    # Max speed is 400.
    # E.g.a command of 500 will result in the same speed as if the command was 400
   # motor_serial.send_command(speed_motor_1, speed_motor_2)



    # Here we pause the execution of the program for the apropriate amout of time
    # so that our loop executes at the frequency specified by the variable execution_frequency
   # iteration_end_time = time.time() # current time
    #iteration_duration = iteration_end_time - iteration_start_time # time spent executing code
    #if (iteration_duration < execution_period):
    #    time.sleep(execution_period - iteration_duration)



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
