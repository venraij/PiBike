from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
import pygame

sense = SenseHat()
event = sense.stick.wait_for_event()

def pushed_middle(event):
    if event.action != ACTION_RELEASED:
        pygame.mixer.init()
        pygame.mixer.music.load("toeter.mp3")
        pygame.mixer.music.play()

sense.stick.direction_middle = pushed_middle
