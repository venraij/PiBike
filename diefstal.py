from sense_hat import SenseHat, ACTION_RELEASED, ACTION_HELD, ACTION_PRESSED
from time import sleep
sense = SenseHat()

import time

O = (0, 0, 0)
W = (255, 255, 255)
G = (0, 255, 0)
R = (255, 0, 0)

    
sense.clear()

#De functies

def parkeren(event):
    if event.action != ACTION_RELEASED:
      park = [
        O,O,O,O,O,O,G,O,
        W,W,W,W,O,G,G,G,
        W,O,O,O,W,O,G,O,
        W,O,O,O,W,O,G,O,
        W,W,W,W,O,O,R,O,
        W,O,O,O,O,O,R,O,
        W,O,O,O,O,R,R,R,
        W,O,O,O,O,O,R,O
      ]
      print('Parkeren?')
      sense.set_pixels(park)

def keuze_up(event2):
    if event2.action != ACTION_RELEASED:
      sense.clear()
      vink = [
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,G,
        O,O,O,O,O,O,G,O,
        O,O,O,O,O,G,O,O,
        G,O,O,O,G,O,O,O, 
        O,G,O,G,O,O,O,O,
        O,O,G,O,O,O,O,O,
        O,O,O,O,O,O,O,O
      ]

              
      sense.set_pixels(vink)
      time.sleep(5)

      sense.clear()

def keuze_down(event3):
    if event3.action != ACTION_RELEASED:              
      sense.clear()
      kruis = [
        O,O,O,O,O,O,O,O,
        R,O,O,O,O,O,R,O,
        O,R,O,O,O,R,O,O,
        O,O,R,O,R,O,O,O,
        O,O,O,R,O,O,O,O,
        O,O,R,O,R,O,O,O,
        O,R,O,O,O,R,O,O,
        R,O,O,O,O,O,R,O
      ]

                
      sense.set_pixels(kruis)
      time.sleep(5)
               
      sense.clear()

sense.stick.direction_middle = parkeren
sense.stick.direction_up = keuze_up
sense.stick.direction_down = keuze_down
    
  
