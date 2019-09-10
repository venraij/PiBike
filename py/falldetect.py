# Auteur - Robin Kleinhoven ICTM1d4
# Versie 0.5
# Imports
from sense_hat import SenseHat
import time

# Variables
wait_interval = 1
sense = SenseHat()
fallen = False
debug = False
# define ranges for orientation sensor that equals fall
orient_min = 85
orient_max = 285

# Booleans IMU - Compass / Gyro / Accel. More sensors = more accurate
sense.set_imu_config(True, True, True)


# Function Declerations
# lees de accel data om de zoveel seconden uit - handle val
def orientation_watchdog():
    
    # Returns Orientation - pitch , roll , yaw.
    sense_orientation = sense.get_orientation()
 
    # Returns Accelleration - x, y, z
    sense_accelleration = sense.get_accelerometer_raw()

    # First, fetch me the specific sensor values I need

    # Type Float 
    roll = sense_orientation["roll"]

    # range 1+ -0
    # type float
    z_accel = sense_accelleration["z"]

    # Variables defined up top for easy reference
    global orient_plus
    global orient_minus
    global fallen


    # Calculate whether force in Z axis sufficient enough to constitute a fall
    # Ranges defined up top
    # and (z_accel > 1 or z_accel < 0) 
    if roll > orient_min and roll < orient_max:
        fallen = True
    else:
        fallen = False

    # Debug loop to help me log measurement blocks
    global debug
    if debug == False:
        print("begin meetsessie")
        debug = True

    #debug - print sensor values       
    #orientation 
    #print("p: {pitch}, r: {roll}, y: {yaw}".format(**sense_orientation))
    #print(str(roll) + " vallen staat op " + str(fallen))
    #accelerometer
    print(str(z_accel) + " vallen staat op " + str(fallen))
    #print("x: {x}, y: {y}, z: {z}".format(**sense_accelleration))
 

# Main Loop
try:
    while True:
        orientation_watchdog()
        time.sleep(wait_interval)
except KeyboardInterrupt:
    #Debug - measurement cutoff
    print("eind meetsessie")
    pass


    
