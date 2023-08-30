import imrt_robot_serial
import signal
import time
import sys
import random

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 70
TURNING_SPEED = 200
STOP_DISTANCE = 25

def stop_robot(duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.1)

def drive_robot(dist_1, dist_5, duration):
    error = dist_1 - 10
    angle_error = dist_1 - dist_5
    speed_adjustment = 8 * error + 2 * angle_error
    speed_motor_1 = 250 + speed_adjustment
    speed_motor_2 = 250 - speed_adjustment
    motor_serial.send_command(speed_motor_1, speed_motor_2)
    time.sleep(duration)

def drive_turn(direction, duration):
    speed = DRIVING_SPEED * direction
    motor_serial.send_command(speed, speed)
    time.sleep(duration)

def turn_robot(direction, duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.1)

try:
    motor_serial = imrt_robot_serial.IMRTRobotSerial()
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

motor_serial.run()

print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now:
    dist_1 = motor_serial.get_dist_4()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_1()
    dist_5 = motor_serial.get_dist_5()
    print("Dist 1:", dist_1, "Dist 2:", dist_2, "Dist 3:", dist_3, "Dist 4:", dist_4, "Dist 5:", dist_5)

    if dist_1 > 50 or dist_5 > 50:
        drive_turn(FORWARDS, 0.15)
        turn_robot(RIGHT, 0.7)
        drive_turn(FORWARDS, 0.25)
    elif dist_1 < 10 and dist_3 < 10:
        turn_robot(LEFT, 0.7)
    elif dist_3 < 10 or dist_4 < 10:
        turn_robot(RIGHT, 0.7)
    else:
        drive_robot(dist_1, dist_5, 0.005)

print("Goodbye")