import os
import sys, getopt
from gps import *
from time import *
import time
import threading
import argparse
import xml.etree.ElementTree as ET

gpsd = None #seting the global variable

sensor1 = 0
sensor2 = 0
sensor3 = 0
sensor4 = 0

sensorname = ['Lengtegraad', 'Breedtegraad', 'Hoogte', 'Klim']
sensor= [sensor1, sensor2, sensor3, sensor4]

os.system('clear') #clear the terminal (optional)

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

    gpx = ET.Element('gpx')
    rte = ET.SubElement(gpx, 'rte')

    # create a new XML file with the results
    mydata = ET.ElementTree(gpx)
    mydata.write("testrit.gpx")
    
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
        timegps = gpsd.fix.time

        os.system('clear')

        print ()
        print (' GPS reading')
        print ('----------------------------------------')
        print ('latitude    ' , sensor1)
        print ('longitude   ' , sensor2)
        print ('altitude (m)' , sensor3)
        print ('climb       ' , sensor4)
        print ('time        ' , timegps)
        print ('mode        ' , gpsd.fix.mode)
        print ()

        if (gpsd.fix.mode == 2 or gpsd.fix.mode == 3):
            # create the file structure
            tree = ET.parse('testrit.gpx')
            root = tree.getroot()
        
            trkpt = ET.SubElement(rte, 'trkpt', lat=str(sensor1), lon=str(sensor2))
            ele = ET.SubElement(trkpt, 'ele')
            ele.text = str(sensor3)
            timeprint = ET.SubElement(trkpt, 'time')
            timeprint.text = str(timegps)
            root.append(trkpt)

            tree.write("testrit.gpx")
            print("Saved Coördinates")

        else:
            print("No sat fix")
            
        time.sleep(1) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print ("Done.\nExiting.")
