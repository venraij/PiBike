# Auteur - Robin Kleinhoven ICTM1d4
# Versie 1.0
# TODO - Implement yaw / roll / pitch choice - Mount is now static!
# Mount with either the USB or the SD side toword the front of the bike

# Imports
from sense_hat import SenseHat
import time

# Variables
measurement_interval = 1
sense = SenseHat()
# define ranges for orientation sensor that equals fall
# 60 degree offset both clockwise and counter-clockwise 360 - 60 AND 0 + 60
range_cw = 60
range_ccw = 300
debug = False

# Booleans IMU - Compass / Gyro / Accel. Enable more sensors = more accurate
sense.set_imu_config(True, True, True)


# Function Declerations

# Check's whether the bike is at a fallen angle
# Returns Bool
def orientation_watchdog():

    # Returns Orientation - pitch , roll , yaw.
    sense_orientation = sense.get_orientation()
 
    # Returns Accelleration - x, y, z
    sense_accelleration = sense.get_accelerometer_raw()

    # First, fetch me the specific sensor values I need

    # Type Float 
    roll = sense_orientation["roll"]

    # Type Float - Implement this at some point
    yaw = sense_orientation["yaw"]

    # range 1+ -0
    # Type float
    z_accel = sense_accelleration["z"]



    # Variables defined up top for easy reference
    global range_cw
    global range_ccw

    # Calculate whether force in Z axis sufficient enough to constitute a fall
    # Ranges defined up top
    # and (z_accel > 1 or z_accel < 0) - logic not sound
    if roll > range_cw and roll < range_ccw:
       return True
    else:
        return False

# Check orientation_watchdog()'s bool for fall.
def fallen_watchdog():
    # Debug loop to help me log measurement blocks
    global debug
    if debug == False:
        print("begin meetsessie")
        debug = True

    #debug - print sensor values       
    #orientation 
    #print("p: {pitch}, r: {roll}, y: {yaw}".format(**sense_orientation))
    #print(str(roll) + " vallen staat op " + str(fallen))
    #print(str(roll))
    #accelerometer
    #print(str(z_accel) + " vallen staat op " + str(fallen))
    #print("x: {x}, y: {y}, z: {z}".format(**sense_accelleration))
        
    # Grab return bool
    fallen = orientation_watchdog()

    # Check return bool
    if fallen == True:
        print(str(fallen))
        sense.show_message("VAL")
    else:
        print(str(fallen))
        sense.clear()
        


# Main Loop
try:
    while True:
        orientation_watchdog()
        fallen_watchdog()
        time.sleep(measurement_interval)
except KeyboardInterrupt:
    #Debug - measurement cutoff
    print("eind meetsessie")
    pass

 




