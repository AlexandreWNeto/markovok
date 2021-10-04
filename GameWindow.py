"""
Tela do jogo

"""


import os, sys
from pygame import display
from pygame import Surface
from pygame import image
from pygame import mouse
from pygame import Rect
from pygame import time
from pygame import font
from pygame import transform

font.init()

WIDTH, HEIGHT = 900, 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WINNER_FONT = font.SysFont("verdana",100) # font, size

BACKGROUND_IMAGE = transform.scale(
    image.load(os.path.join("imagens","fundo.jpg")),(WIDTH, HEIGHT))

DICE_WIDTH, DICE_HEIGHT = WIDTH // 25, WIDTH // 25

DICE_1_IMAGE = transform.scale(
    image.load(os.path.join("imagens","1.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_2_IMAGE = transform.scale(
    image.load(os.path.join("imagens","2.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_3_IMAGE = transform.scale(
    image.load(os.path.join("imagens","3.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_4_IMAGE = transform.scale(
    image.load(os.path.join("imagens","4.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_5_IMAGE = transform.scale(
    image.load(os.path.join("imagens","5.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_6_IMAGE = transform.scale(
    image.load(os.path.join("imagens","6.png")), (DICE_WIDTH, DICE_HEIGHT))


images_dir = os.path.join("imagens")

class GameWindow():

    def __init__(self):
        self.SCREEN_WIDTH = WIDTH
        self.SCREEN_HEIGHT = HEIGHT
        self.caption = "Markovok"
        self.WIN = None



    def set_screen(self):
        # create display
        display.set_caption(self.caption)
        size = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.WIN = display.set_mode(size)
        mouse.set_visible(True)

    def draw_window(self, game):
        self.WIN.blit(BACKGROUND_IMAGE,(0,0))
        self.draw_players(game.list_players)
        display.update()

    def draw_winner(self, text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        self.WIN.blit(draw_text, (self.SCREEN_WIDTH / 2 - draw_text.get_width() / 2, self.SCREEN_HEIGHT / 2 - draw_text.get_height() / 2))

        display.update()  # updates the screen before the pause
        time.delay(5000)  # pauses the game

    def draw_players(self, players):
        for player in players:
            self.draw_dice(player)

    def draw_dice(self, player):
        offset = 0
        dice_list = player.get_set_of_dice().dice_list
        for dice in dice_list:
            if dice == 1:
                self.WIN.blit(DICE_1_IMAGE, (player.x + offset, player.y))
            if dice == 2:
                self.WIN.blit(DICE_2_IMAGE, (player.x + offset, player.y))
            if dice == 3:
                self.WIN.blit(DICE_3_IMAGE, (player.x + offset, player.y))
            if dice == 4:
                self.WIN.blit(DICE_4_IMAGE, (player.x + offset, player.y))
            if dice == 5:
                self.WIN.blit(DICE_5_IMAGE, (player.x + offset, player.y))
            if dice == 6:
                self.WIN.blit(DICE_6_IMAGE, (player.x + offset, player.y))

            offset += WIDTH // 25 + 10


    def set_player_coordinates(self, list_of_players):
        if len(list_of_players) == 2: # 2 jogadores
                list_of_players[0].x = WIDTH // 5
                list_of_players[1].x = WIDTH // 5
                list_of_players[0].y = HEIGHT // 5
                list_of_players[1].y = HEIGHT - HEIGHT // 5



