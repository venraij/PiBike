# Auteur - Robin Kleinhoven ICTM1d4
# Versie 0.5
# Imports
from sense_hat import SenseHat
import time
# debug

# Variables
wait_interval = 0.5

# Declare sense hat 
sense = SenseHat()
fallen = False
debug = False

# Booleans IMU Compass / Gyro / Accel. More sensors = more accurate
sense.set_imu_config(True, True, True)

# Redundant, formatting use only
#accel_data = sense.get_accelerometer()
#accel_data_raw = sense.get_accelerometer_raw()


# Function Declerations
# lees de accel data om de zoveel seconden uit - handle val
def orientation_watchdog():
    
    # Returns Orientation - pitch , roll , yaw.
    # Only roll being relevant
    # Range left: 0° - 90°
    # Range Right: 360° - 270°
    # Difference 90°!
    # type float
    sense_orientation = sense.get_orientation()

    # Returns accel values depending on severity of the force in x,y,z
    # Only z being relevant
    # range 1+
    # type float
    sense_accelleration = sense.get_accelerometer_raw()

    # TODO
    # if range outside values Left or Right - throw "fallen" else - False.
    # Also , show message as feedback on Sense HAT LED

    # First, fetch me the specific sensor values I need
    roll = sense_orientation["roll"]
    z_accel = sense_accelleration["z"]



    # Calculate whether roll between 90 - 270
    # Calculate whether force in Z axis sufficient enough to constitute a fall
    if roll > 90 and roll < 270 and z_accel > 1 or z_accel < 0:
        print("fall value")
        print(roll)
    
    

    # Debug loop to help me log measurement blocks
    global debug
    if debug == False:
        print("begin meetsessie")
        debug = True

    #debug - print sensor values    
    #orientation 
    #print("p: {pitch}, r: {roll}, y: {yaw}".format(**sense_orientation))
    #accelerometer
    print(z_accel)
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


    
