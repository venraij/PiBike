import urllib.request, json
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
import sys, getopt
import argparse
import time
import mysql.connector as mariadb
from mysql.connector import errorcode

sensor_name = "Temperatuur"
sensor_name1 = "Image"

# database connection configuration
dbconfig = {
    'user': 'sensem',
    'password': 'h@',
    'host': 'localhost',
    'database': 'pibike',
    'raise_on_warnings': True,
}

# parse arguments
verbose = True
interval = 10   # second
try:
    opts, args = getopt.getopt(sys.argv[1:], "vt:")
except getopt.GetoptError as err:
    print(str(err))
    print('measure.py -v -t <interval>')
    print('-v: be verbose')
    print('-t <interval>: measure each <interval> seconds (default: 10s)')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-v':
        verbose = True
    elif opt == '-t':
        interval = int(arg)
        
#verbinden met de database        
try:
    mariadb_connection = mariadb.connect(**dbconfig)
    if verbose:
        print("Database connected")
except mariadb.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print("Error: {}".format(err))
    sys.exit(2)
    
# create the database cursor for executing SQL queries
cursor = mariadb_connection.cursor()
# turn on autocommit
#cursor.autocommit = True

# determine the latest lat
try:
    cursor.execute('SELECT waarde FROM meting WHERE sensor_id = 1 ORDER BY id DESC LIMIT 1;')
except mariadb.Error as err:
    print("Error: {}".format(err))
    sys.exit(2)
charlie = cursor.fetchone()

# determine the latest long
try:
    cursor.execute('SELECT waarde FROM meting WHERE sensor_id = 2 ORDER BY id DESC LIMIT 1;')
except mariadb.Error as err:
    print("Error: {}".format(err))
    sys.exit(2)
delta = cursor.fetchone()

# Define some colours
Y = (255, 247, 0) # Yellow
B = (0, 0, 255) # Blue
G = (105, 105, 105) # Grey
W = (255, 255, 255) # White
E = (0, 0, 0) # Empty

sense = SenseHat()
delay_img = 2
delay_press = 1

# Demo url to test, so the key doesn't expire
demo_url = "http://weerlive.nl/api/json-data-10min.php?key=demo&locatie=Amsterdam"
basis_url = "http://weerlive.nl/api/json-data-10min.php?key="
# Key invullen
key = "27a31f3737"
rest_url = "&locatie="

# Change (demo_url) to (basis_url + key + rest_url + str(lat) + "," + str(long)) for normal code
response = urllib.request.urlopen(basis_url + key + rest_url + str(charlie[0]) + "," + str(delta[0]))
data = json.loads(response.read().decode("utf-8"))
x = data['liveweer']
y = x[0]

image = y['image']
temp = y['temp']
plaats = y['plaats']

# A def so you can call it when you press a button
def press(event):
    if event.action != ACTION_RELEASED:
        if weertype == "bewolkt" or weertype == "zwaarbewolkt" or weertype == "wolkennacht":
        # Set up where the image displays
            bewolkt = [
                G, G, E, E, E, E, E, G,
                G, G, G, E, E, E, G, G,
                E, E, E, E, E, E, E, E,
                E, E, G, G, E, G, E, E,
                E, G, G, G, G, G, G, E,
                G, G, G, G, G, G, G, G,
                G, G, G, G, G, G, G, G,
                E, E, E, E, E, E, E, E
            ]

        # Display these colours on the LED matrix
            sense.set_pixels(bewolkt)
            
        elif weertype == "halfbewolkt":
        # Set up where the image displays
            halfbewolkt = [
                G, G, E, E, E, E, E, G,
                G, G, G, E, E, E, G, G,
                E, E, E, E, E, E, E, E,
                E, E, G, G, E, Y, E, Y,
                E, G, G, G, G, G, G, E,
                G, G, G, G, Y, G, Y, Y,
                G, G, G, G, G, G, Y, Y,
                E, E, E, E, Y, E, Y, Y
            ]

        # Display these colours on the LED matrix
            sense.set_pixels(halfbewolkt)

        elif weertype == "zonnig":
        # Set up where the image displays
            zonnig = [
                Y, E, Y, E, Y, E, Y, E,
                E, E, E, E, E, E, E, Y,
                Y, E, E, Y, Y, E, E, E,
                E, E, Y, Y, Y, Y, E, Y,
                Y, E, Y, Y, Y, Y, E, E,
                E, E, E, Y, Y, E, E, Y,
                Y, E, E, E, E, E, E, E,
                E, Y, E, Y, E, Y, E, Y
            ]

        # Display these colours on the LED matrix
            sense.set_pixels(zonnig)

        elif weertype == "bliksem":
        # Set up where the image displays
            bliksem = [
                G, G, E, E, E, E, E, G,
                B, G, G, E, E, E, G, B,
                B, E, E, E, E, E, E, B,
                E, E, G, G, E, G, E, E,
                E, G, G, G, G, G, G, E,
                G, G, Y, G, G, G, Y, G,
                G, Y, Y, G, G, Y, Y, G,
                E, Y, E, E, E, Y, E, E
            ]

        # Display these colours on the LED matrix
            sense.set_pixels(bliksem)

        elif weertype == "regen" or weertype == "buien":
        # Set up where the image displays
            regen = [
                G, G, E, E, E, E, E, G,
                B, G, G, E, E, E, G, B,
                B, E, E, E, E, E, E, B,
                E, E, G, G, E, G, E, E,
                E, G, G, G, G, G, G, E,
                G, G, G, G, G, G, G, G,
                B, G, B, G, B, G, B, G,
                B, E, B, E, B, E, B, E
            ]

        # Display these colours on the LED matrix
            sense.set_pixels(regen)

        elif weertype == "hagel" or weertype == "sneeuw":
        # Set up where the image displays
            sneeuw = [
                E, E, G, G, E, G, E, E,
                E, G, G, G, G, G, G, E,
                G, G, G, G, G, G, G, G,
                E, W, E, W, E, W, E, W,
                W, E, W, E, W, E, W, E,
                E, W, E, W, E, W, E, W,
                W, E, W, E, W, E, W, E,
                E, W, E, W, E, W, E, W
            ]

        # Display these colours on the LED matrix
            sense.set_pixels(sneeuw)

        elif weertype == "mist" or weertype == "nachtmist":
        # Set up where the image displays
            mist = [
                E, E, E, E, E, E, E, E,
                E, E, E, E, E, E, E, E,
                E, E, E, E, E, E, E, E,
                E, E, E, E, E, E, E, E,
                E, E, E, E, E, E, E, E,
                E, G, G, E, G, G, G, E,
                G, G, G, G, G, G, G, G,
                G, G, G, G, G, G, G, G
            ]

        # Display these colours on the LED matrix
            sense.set_pixels(mist)

        elif weertype == "helderenacht":
        # Set up where the image displays
            nacht = [
                E, E, E, E, E, E, E, E,
                E, E, E, G, G, E, E, E,
                E, E, G, G, G, G, E, E,
                E, G, G, G, G, G, G, E,
                E, G, G, G, G, G, G, E,
                E, E, G, G, G, G, E, E,
                E, E, E, G, G, E, E, E,
                E, E, E, E, E, E, E, E,
            ]

        # Display these colours on the LED matrix
            sense.set_pixels(nacht)

        else:
        # Yeah Earth is gone...
            print("There is no weather, Earth is gone")

        sleep(delay_img)
        sense.clear()
        sense.show_message(t + "C", text_colour=[255, 255, 0])
        sleep(delay_press)

# If middle button is pressed then it will show weather and tempature
sense.stick.direction_middle = press

try:
    cursor.execute("SELECT id FROM sensor WHERE naam=%s", [sensor_name])
except mariadb.Error as err:
    print("Error: {}".format(err))
    sys.exit(2)
sensor_id = cursor.fetchone()
if sensor_id == None:
    print("Error: no sensor found with naam = %s" % sensor_name)
    sys.exit(2)
if verbose:
    print("Reading data from sensor %s with id %s" % (sensor_name, sensor_id[0]))
        
#Temperatuur
t = temp
        
# verbose
if verbose:
    print("Temperature: %s C" % t)
    # store measurement in database
    try:
        cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (t, sensor_id[0]))
    except mariadb.connector.Error as err:
        print("Error: {}".format(err))
    else:
        # commit measurements
        mariadb_connection.commit();
if verbose:
        print("Temperature committed");
            
# determine the sensor_id for image
try:
    cursor.execute("SELECT id FROM sensor WHERE naam=%s", [sensor_name1])
except mariadb.Error as err:
    print("Error: {}".format(err))
    sys.exit(2)
sensor_id = cursor.fetchone()
if sensor_id == None:
    print("Error: no sensor found with naam = %s" % sensor_name1)
    sys.exit(2)
if verbose:
    print("Reading data from sensor %s with id %s" % (sensor_name1, sensor_id[0]))
        
#weertype
weertype = image
        
# verbose
if verbose:
    print("Image: %s" % image)
    # store measurement in database
    try:
        cursor.execute('INSERT INTO meting (weertype, sensor_id) VALUES (%s, %s);', (image, sensor_id[0]))
    except mariadb.connector.Error as err:
        print("Error: {}".format(err))
    else:
        # commit measurements
        mariadb_connection.commit();
if verbose:
    print("Image committed");

# determine the latest temperature
try:
    cursor.execute('SELECT waarde FROM meting WHERE sensor_id = 3 ORDER BY id DESC LIMIT 1;')
except mariadb.Error as err:
    print("Error: {}".format(err))
    sys.exit(2)
alfa = cursor.fetchone()
print(alfa[0])

# determine the latest weertype
try:
    cursor.execute('SELECT weertype FROM meting WHERE sensor_id = 4 ORDER BY id DESC LIMIT 1;')
except mariadb.Error as err:
    print("Error: {}".format(err))
    sys.exit(2)
bravo = cursor.fetchone()
print(bravo[0])

print(plaats)

# close db connection
mariadb_connection.close()
# done

