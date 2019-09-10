from sense_hat import SenseHat, ACTION_RELEASED
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
  for event in sense.stick.get_events():
    if event.action != ACTION_RELEASED:
      if event.action == "pressed":
          if event.direction == "middle":
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

def keuze(event):
  for event in sense.stick.get_events():
    if event.action != ACTION_RELEASED:
      if event.action == "pressed":
          if event.direction == "up":
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
              
          if event.direction == "down":
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
try:
  while True:
    parkeren()
    keuze()

except KeyboardInterrupt:
    pass
sense.clear()

print("Einde script")
    
  
