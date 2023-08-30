import imrt_robot_serial
import time
import sys

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 100
TURNING_SPEED = 100
STOP_DISTANCE = 7

def stop_robot(duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)

def drive_robot(duration, dist_2, dist_1):
    iterations = int(duration * 10)
    speed_constant = 10  # Juster denne konstanten etter behov

    for i in range(iterations):
        left_speed = dist_2 * speed_constant
        right_speed = dist_2 * speed_constant
        motor_serial.send_command(int(left_speed), int(right_speed))
        time.sleep(0.10)

def turn_robot(direction):
    iterations = int(9)  # For ~90 graders sving
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.10)

execution_frequency = 50
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

    if dist_3 < 5 or dist_4 < 5 or dist_5 < 10:
        print("Obstacle in front!")
        stop_robot(1)
        
        if dist_1 > STOP_DISTANCE:
            print("Turning Right")
            turn_robot(RIGHT)
        else:
            print("Turning Left")
            turn_robot(LEFT)
    else:
        drive_robot(0.1, dist_2, dist_1)

print("Goodbye")
