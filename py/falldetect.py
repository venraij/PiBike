# Auteur - Robin Kleinhoven ICTM1d4
# Versie 0.1
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
# lees de accel data om de zoveel seconden uit
def orientation_watchdog():
    
    # Returns Orientation - pitch , roll , yaw.
    # Only roll being relevant
    # Range left: 0° - 90°
    # Range Right: 360° - 270°
    sense_orientation = sense.get_orientation()

    # Returns accel values depending on severity of the force in x,y,z
    # Only z being relevant
    # range 0-1+ 
    sense_accel = sense.get_accelerometer_raw()

    # Debug loop to help me log measurement blocks
    global debug
    if debug == False:
        print("begin meetsessie")
        debug = True
        
    #orientation 
    #print("p: {pitch}, r: {roll}, y: {yaw}".format(**sense_orientation))
    #accelerometer
    print("x: {x}, y: {y}, z: {z}".format(**sense_accel))



# Main Loop
try:
    while True:
        orientation_watchdog()
        #print(sense.orientation)
        #print(sense.accel)
        #print(sense.accelerometer_raw)
        time.sleep(wait_interval)
except KeyboardInterrupt:
    print("eind meetsessie")
    pass


    
