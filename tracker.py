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

gpsd = None #seting the global variable

sensor1 = 0
sensor2 = 0
sensor3 = 0
sensor4 = 0

sensorname = ['Lengtegraad', 'Breedtegraad', 'Hoogte', 'Klim']
sensor= [sensor1, sensor2, sensor3, sensor4]

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
        sensor1 = gpsd.fix.latitude
        sensor2 = gpsd.fix.longitude
        sensor3 = gpsd.fix.altitude
        sensor4 = gpsd.fix.climb

        os.system('clear')

        print ()
        print (' GPS reading')
        print ('----------------------------------------')
        print ('latitude    ' , sensor1)
        print ('longitude   ' , sensor2)
        print ('altitude (m)' , sensor3)
        print ('climb       ' , sensor4)
        print ('mode        ' , gpsd.fix.mode)
        print ()

        x = 0
        
        while (x <= 3):
            ############################
            # Determine the sensor_id's#
            ############################

            sensor_name = sensorname[x]
            
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
                cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (sensor[x], sensor_id[0]))
            except mysql.connector.Error as err:
                print("Error: {}".format(err))
            else:
                # commit measurements
                mariadb_connection.commit();
            if verbose:
                print(str(sensor_name) + " committed");
                x += 1

            time.sleep(5) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    mariadb_connection.close()
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print ("Done.\nExiting.")
