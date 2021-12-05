from pygame import USEREVENT
from pygame import mixer
from os import path

FPS = 60

MAX_NUM_OF_DICE = 5
NUM_PC_PLAYERS = 4
NUM_USER_PLAYERS = 1
# USER EVENTS
START_MATCH = USEREVENT + 1
END_MATCH = USEREVENT + 2
START_ROUND = USEREVENT + 3
END_ROUND = USEREVENT + 4
DOUBT = USEREVENT + 5
EXACT_GUESS = USEREVENT + 6
GUESS = USEREVENT + 7
ACTION = USEREVENT + 8
START = USEREVENT + 9

CLICK_SOUND = mixer.Sound(path.join("media","click.mp3"))
DOUBT_SOUND = mixer.Sound(path.join("media","doubt.mp3"))

