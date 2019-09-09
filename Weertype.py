import urllib.request, json
from sense_hat import SenseHat
from time import sleep

# Define some colours
Y = (255, 247, 0) # Yellow
B = (0, 0, 255) # Blue
G = (105, 105, 105) # Grey
W = (255, 255, 255) # White
E = (0, 0, 0) # Empty

sense = SenseHat()
delay = 5

# Demo url to test, so the key doesn't expire
demo_url = "http://weerlive.nl/api/json-data-10min.php?key=demo&locatie=Amsterdam"
basis_url = "http://weerlive.nl/api/json-data-10min.php?"
# Key invullen
key = "key=27a31f3737"
rest_url = "&locatie="
# Stad variabele
stad = "Zwolle"

# Change (demo_url) to (basis url + key + rest_url + stad) for normal code
response = urllib.request.urlopen(demo_url)
data = json.loads(response.read().decode("utf-8"))
x = data['liveweer']
y = x[0]

weertype = y['image']
temp = y['temp']

if weertype == "bewolkt" or weertype == "halfbewolkt" or weertype == "zwaarbewolkt" or weertype == "wolkennacht":
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
        E, Y, Y, G, G, Y, Y, G,
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

sleep(delay)
sense.clear()

# Shows tempature
sense.show_message(temp)
