import sys, getopt
import argparse
import time
import mysql.connector as mariadb
from mysql.connector import errorcode

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


# infinite loop
try:
    while True:
        # determine the sensor_id for temperature sensor
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
        
        # measure temperature, humidity and pressure
        t = round(sh.get_temperature(),1)
        t_corr = round(t - 25.5, 1)
        
        # verbose
        if verbose:
            print("Temperature: %s C" % t_corr)
        # store measurement in database
        try:
            cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (t_corr, sensor_id[0]))
        except mariadb.connector.Error as err:
            print("Error: {}".format(err))
        else:
            # commit measurements
            mariadb_connection.commit();
        if verbose:
            print("Temperature committed");

        time.sleep(interval)
 
except KeyboardInterrupt:
    pass
# close db connection
mariadb_connection.close()
# done






