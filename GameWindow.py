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


from math import sin
from math import cos
from math import atan
from math import pi
from math import sqrt




font.init()

WIDTH, HEIGHT = 900, 650

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

DICE_HIDDEN_IMAGE = transform.scale(
    image.load(os.path.join("imagens","hidden_dice.png")), (DICE_WIDTH, DICE_HEIGHT))


images_dir = os.path.join("imagens")

class GameWindow:

    def __init__(self, max_num_of_dice = 6):
        self.SCREEN_WIDTH = WIDTH
        self.SCREEN_HEIGHT = HEIGHT
        self.caption = "Markovok"
        self.WIN = None
        self.max_num_of_dice = max_num_of_dice



    def set_screen(self):
        # create display
        display.set_caption(self.caption)
        size = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.WIN = display.set_mode(size)
        mouse.set_visible(True)

    def draw_window(self, game):
        self.WIN.blit(BACKGROUND_IMAGE,(0,0))
        self.draw_players(game.list_players, mode = "HIDE")
        display.update()

    def draw_winner(self, text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        self.WIN.blit(draw_text, (self.SCREEN_WIDTH / 2 - draw_text.get_width() / 2, self.SCREEN_HEIGHT / 2 - draw_text.get_height() / 2))

        display.update()  # updates the screen before the pause
        time.delay(5000)  # pauses the game

    def draw_players(self, players, mode = "HIDE"):
        if mode == "REVEAL":
            for player in players:
                self.draw_dice(player, mode)
        elif mode == "HIDE":
            for player in players:
                if player.type == "pc":
                    self.draw_dice(player, mode)
                else:
                    self.draw_dice(player, "REVEAL")    # only reveal dice from user players
        else:
            print("Error in function draw_players. Invalid draw mode.")

    def draw_dice(self, player, mode = "REVEAL"):

        dice_list = player.get_set_of_dice().dice_list

        x_start = player.vertices[0][0]
        y_start = player.vertices[0][1]
        x_end = player.vertices[1][0]
        y_end = player.vertices[1][1]


        if x_end != x_start:
            angle = -atan((y_end - y_start) / (x_end - x_start)) * 180 / pi
        else:
            angle = 90 if y_end < y_start else -90

        if y_end == y_start:
            angle = 180 if x_end > x_start else 0

        offset_x = (x_end - x_start) / (self.max_num_of_dice + 1) #- (DICE_WIDTH / 2) * sin(angle * pi / 180)
        offset_y = (y_end - y_start) / (self.max_num_of_dice + 1) - (DICE_HEIGHT / 2) * cos(angle * pi / 180)

        delta_x = (x_end - x_start) / (self.max_num_of_dice + 1)
        delta_y = (y_end - y_start) / (self.max_num_of_dice + 1)

        if mode == "REVEAL":
            for dice in dice_list:
                if dice == 1:
                    self.WIN.blit(transform.rotate(DICE_1_IMAGE.convert_alpha(), angle), (x_start + offset_x, y_start + offset_y))
                if dice == 2:
                    self.WIN.blit(transform.rotate(DICE_2_IMAGE.convert_alpha(), angle), (x_start + offset_x, y_start + offset_y))
                if dice == 3:
                    self.WIN.blit(transform.rotate(DICE_3_IMAGE.convert_alpha(), angle), (x_start + offset_x, y_start + offset_y))
                if dice == 4:
                    self.WIN.blit(transform.rotate(DICE_4_IMAGE.convert_alpha(), angle), (x_start + offset_x, y_start + offset_y))
                if dice == 5:
                    self.WIN.blit(transform.rotate(DICE_5_IMAGE.convert_alpha(), angle), (x_start + offset_x, y_start + offset_y))
                if dice == 6:
                    self.WIN.blit(transform.rotate(DICE_6_IMAGE.convert_alpha(), angle), (x_start + offset_x, y_start + offset_y))

                offset_x += delta_x
                offset_y += delta_y
        else:
            for dice in dice_list:
                self.WIN.blit(transform.rotate(DICE_HIDDEN_IMAGE.convert_alpha(), angle), (x_start + offset_x, y_start + offset_y))
                offset_x += delta_x
                offset_y += delta_y


    def set_player_coordinates(self, list_of_players):
        num_players = len(list_of_players)
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        radius = WIDTH // 3

        if num_players == 2: # place the dice in two parallel lines
            delta = 0
            for player in list_of_players:
                player.vertices = ((WIDTH // 5, HEIGHT // 4 + delta), (4 * WIDTH // 5, HEIGHT // 4 + delta))
                delta += 2 * HEIGHT // 4


        else:
            # coordinates of the vertices of the polygon on which the dice will be placed
            vertices = list((
                               (sin(i / num_players * 2 * pi + pi/num_players) * radius) + center_x,
                               (cos(i / num_players * 2 * pi + pi/num_players) * radius) + center_y)
                            for i in range(-1, num_players -1))

            i = 0
            for player in list_of_players:
                player.vertices = (vertices[i], vertices[i+1 if i != num_players - 1 else 0])
                i += 1


