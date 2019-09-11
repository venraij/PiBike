from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

X = [255, 0, 0]  # Red

alarm = [
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X
]

while True:
    sense.set_pixels(alarm)
    sense.clear()
    sleep(1)
