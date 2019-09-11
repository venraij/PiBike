from sense_hat import SenseHat, ACTION_RELEASED, ACTION_HELD, ACTION_PRESSED
from time import sleep
import getpass
import time
import pygame
import sys
import os

O = (0, 0, 0)
W = (255, 255, 255)
G = (0, 255, 0)
R = (255, 0, 0)
red = (255, 0, 0)

sense = SenseHat()
delay = 0.1
Parked = None
    
sense.clear()

#De functies
def Yes():
    sense.clear()
    global Parked
    vink = [
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,G,
        O,O,O,O,O,O,G,G,
        G,O,O,O,O,G,G,O, 
        G,G,O,O,G,G,O,O,
        O,G,G,G,G,O,O,O,
        O,O,G,G,O,O,O,O
    ]

                  
    sense.set_pixels(vink)
    Parked = True
    if Parked is True:
        print('Je fiets is geparkeerd')
    time.sleep(1)
    sense.clear()
    
def No():
    sense.clear()
    kruis = [
        R,O,O,O,O,O,O,R,
        O,R,O,O,O,O,R,O,
        O,O,R,O,O,R,O,O,
        O,O,O,R,R,O,O,O,
        O,O,O,R,R,O,O,O,
        O,O,R,O,O,R,O,O,
        O,R,O,O,O,O,R,O,
        R,O,O,O,O,O,O,R
    ]

                    
    sense.set_pixels(kruis)
    time.sleep(1)
    Parked = False
                   
    sense.clear()            

def parkeren():
    park = [
        O,O,O,O,O,G,O,G,
        W,W,W,O,O,G,G,G,
        W,O,O,W,O,O,G,O,
        W,O,O,W,O,G,O,O,
        W,W,W,O,O,O,O,O,
        W,O,O,O,O,R,R,R,
        W,O,O,O,O,R,O,R,
        W,O,O,O,O,R,O,R
    ]
    print('Parkeren?')
    sense.set_pixels(park)

def stolen():
    alarm = [
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R,
        R, R, R, R, R, R, R, R
    ]

    empty = [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O
    ]

    sense.set_pixels(alarm)
    sleep(delay)
    sense.set_pixels(empty)
    sleep(delay)

def geluid():
    pygame.mixer.init()
    pygame.mixer.music.load("geluid.mp3")
    pygame.mixer.music.play()

def wrong():
    geluid()
    for q in range(50):
        stolen()
    charlie = getpass.getpass(prompt='Password: ')
    if charlie == 'pi':
        sys.exit()
    else:
        wrong()
                
for i in range(1, 4):
    x = 3 - i
    p = getpass.getpass(prompt= 'Password: ')
    if p =='pi':
        parkeren()
        vraag = getpass.getpass(prompt='Y/n)')
        if vraag == 'Y' or vraag == 'y':
            Yes()
        else:
            No()
        break
    else:
        print("Wrong, you have " + str(x) + " attempts")

while Parked is True:
    codes = sense.get_accelerometer_raw()
    x = codes['x']
    y = codes['y']
    z = codes['z']

    x = abs(x)
    y = abs(y)
    z = abs(z)

    for event in sense.stick.get_events():
        if event.action != ACTION_RELEASED and event.direction == "down" and event.action == ACTION_HELD:
            delta = getpass.getpass(prompt='Password: ')
            if delta == 'pi':
                sys.exit() 
            else:
                wrong()
    
    if x > 1.25 or y > 1.25 or z > 1.25:
        wrong()
    else:
        sense.clear()



