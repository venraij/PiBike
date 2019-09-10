from sense_hat import SenseHat, ACTION_RELEASED, ACTION_HELD, ACTION_PRESSED
from time import sleep
import getpass
import time

O = (0, 0, 0)
W = (255, 255, 255)
G = (0, 255, 0)
R = (255, 0, 0)

sense = SenseHat()

    
sense.clear()

#De functies
def Yes():
    sense.clear()
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
    time.sleep(5)

    sense.clear()

    while True:
        # Code diefstalpreventie
        break

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
    time.sleep(5)
                   
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
        
        
              
for i in range(1, 4):
    x = 3 - i
    p = getpass.getpass()
    if p =='pi':
        parkeren()
        vraag = getpass.getpass(prompt='Y/n)')
        if vraag == 'Y' or vraag == 'y':
            Yes()
        else:
            No()
        break
    else:
        print("wrong, you have " + str(x) + " attempts")
