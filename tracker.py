import os
import sys, getopt
from gps import *
from time import *
import time
import threading
import argparse
import mysql.connector as mariadb
from mysql.connector import errorcode
import mysql.connector

sensor_name = 'Lengtegraad';
sensor_name1 = 'Breedtegraad';
sensor_name2 = 'Hoogte';
sensor_name3 = 'Snelheid';
sensor_name4 = 'Klim';

gpsd = None #seting the global variable

os.system('clear') #clear the terminal (optional)

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

try:
    mariadb_connection = mariadb.connect(**dbconfig)
    if verbose:
        print("Database connected")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print("Error: {}".format(err))
    sys.exit(2)

# create the database cursor for executing SQL queries
cursor = mariadb_connection.cursor()

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
        #It may take a second or two to get good data
        #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc      
        
        
        #######################
        # Getting GPS readings#
        #######################

        os.system('clear')

        breedtegraad = gpsd.fix.latitude
        lengtegraad = gpsd.fix.longitude
        hoogte = gpsd.fix.altitude
        snelheid = gpsd.fix.speed
        klim = gpsd.fix.climb

        print ()
        print (' GPS reading')
        print ('----------------------------------------')
        print ('latitude    ' , breedtegraad)
        print ('longitude   ' , lengtegraad)
        print ('time utc    ' , gpsd.utc,' + ', gpsd.fix.time)
        print ('altitude (m)' , hoogte)
        print ('speed (m/s) ' , snelheid)
        print ('climb       ' , klim)
        print ('track       ' , gpsd.fix.track)
        print ('mode        ' , gpsd.fix.mode)
        print ()

        ########################################
        # Determine the sensor_id for Longitude#
        ########################################
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

        # store measurement in database
        try:
            cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (lengtegraad, sensor_id[0]))
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
        else:
            # commit measurements
            mariadb_connection.commit();
        if verbose:
            print("Longitude committed");

        #######################################
        # Determine the sensor_id for Latitude#
        #######################################
        try:
            cursor.execute("SELECT id FROM sensor WHERE naam=%s", [sensor_name1])
        except mysql.Error as err:
            print("Error: {}".format(err))
            sys.exit(2)
        sensor_id = cursor.fetchone()
        if sensor_id == None:
            print("Error: no sensor found with naam = %s" % sensor_name1)
            sys.exit(2)
        if verbose:
            print("Reading data from sensor %s with id %s" % (sensor_name1, sensor_id[0]))

        # store measurement in database
        try:
            cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (breedtegraad, sensor_id[0]))
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
        else:
            # commit measurements
            mariadb_connection.commit();
        if verbose:
            print("Latitude committed");

        #####################################
        # Determine the sensor_id for Height#
        #####################################
        try:
            cursor.execute("SELECT id FROM sensor WHERE naam=%s", [sensor_name2])
        except mariadb.Error as err:
            print("Error: {}".format(err))
            sys.exit(2)
        sensor_id = cursor.fetchone()
        if sensor_id == None:
            print("Error: no sensor found with naam = %s" % sensor_name2)
            sys.exit(2)
        if verbose:
            print("Reading data from sensor %s with id %s" % (sensor_name2, sensor_id[0]))

        # store measurement in database
        try:
            cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (hoogte, sensor_id[0]))
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
        else:
            # commit measurements
            mariadb_connection.commit();
        if verbose:
            print("Height committed");

        #####################################
        # Determine the sensor_id for Speed#
        #####################################
        try:
            cursor.execute("SELECT id FROM sensor WHERE naam=%s", [sensor_name3])
        except mariadb.Error as err:
            print("Error: {}".format(err))
            sys.exit(2)
        sensor_id = cursor.fetchone()
        if sensor_id == None:
            print("Error: no sensor found with naam = %s" % sensor_name3)
            sys.exit(2)
        if verbose:
            print("Reading data from sensor %s with id %s" % (sensor_name3, sensor_id[0]))

        # store measurement in database
        try:
            cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (snelheid, sensor_id[0]))
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
        else:
            # commit measurements
            mariadb_connection.commit();
        if verbose:
            print("Speed committed");

        ####################################
        # Determine the sensor_id for Climb#
        ####################################
        try:
            cursor.execute("SELECT id FROM sensor WHERE naam=%s", [sensor_name4])
        except mysql.Error as err:
            print("Error: {}".format(err))
            sys.exit(2)
        sensor_id = cursor.fetchone()
        if sensor_id == None:
            print("Error: no sensor found with naam = %s" % sensor_name4)
            sys.exit(2)
        if verbose:
            print("Reading data from sensor %s with id %s" % (sensor_name4, sensor_id[0]))

        # store measurement in database
        try:
            cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (klim, sensor_id[0]))
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
        else:
            # commit measurements
            mariadb_connection.commit();
        if verbose:
            print("Climb committed");


        time.sleep(5) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    mariadb_connection.close()
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print ("Done.\nExiting.")
