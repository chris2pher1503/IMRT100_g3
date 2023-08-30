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
        time.sleep(0.10)

def drive_robot(direction, duration):
    gain = 8
    speed_motor_1 = dist_1 * gain *direction
    speed_motor_2 = dist_2 * gain *direction

    time.sleep(0.10)

def turn_robot(direction):
    iterations = int(9)  
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.10)

execution_frequency = 10
execution_period = 1. / execution_frequency

motor_serial = imrt_robot_serial.IMRTRobotSerial()

try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

motor_serial.run()
print("Entering loop. Ctrl+c to terminate")

while not motor_serial.shutdown_now:

    dist_1 = motor_serial.get_dist_4()  # Right Sensor
    dist_2 = motor_serial.get_dist_2()  # Left Sensor
    dist_3 = motor_serial.get_dist_3()  # Front Right Sensor
    dist_4 = motor_serial.get_dist_1()  # Front Center Sensor
    dist_5 = motor_serial.get_dist_5()  # Front Left Sensor

    # Correct robot position if it's not centered between the walls
    if dist_1 > dist_2 + 5:
        turn_robot(LEFT)
    elif dist_2 > dist_1 + 5:
        turn_robot(RIGHT)

    # If an obstacle is detected in front of the robot
    if dist_3 < STOP_DISTANCE or dist_4 < STOP_DISTANCE or dist_5 < STOP_DISTANCE:
        print("Obstacle in front!")
        stop_robot(1)
        
        # Turn right if no obstacle to the right
        if dist_1 > STOP_DISTANCE:
            print("Turning Right")
            turn_robot(RIGHT)
        else:
            # Else, turn left
            print("Turning Left")
            turn_robot(LEFT)

    else:
        # Drive forwards
        drive_robot(FORWARDS, 0.1)

print("Goodbye")
