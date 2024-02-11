"""
Tela do jogo

"""

import os
import sys
from pygame import display
from pygame import Surface
from pygame import image
from pygame import mouse
from pygame import Rect
from pygame import time
from pygame import font
from pygame import transform
from pygame import draw
from pygame import MOUSEBUTTONUP
from pygame import USEREVENT
from pygame import event

from math import sin
from math import cos
from math import atan
from math import pi
from math import sqrt

from setup import START_MATCH, END_MATCH, START_ROUND, END_ROUND, DOUBT, EXACT_GUESS, GUESS, ACTION, START

font.init()

WIDTH, HEIGHT = 1000, 650

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

WINNER_FONT = font.SysFont("verdana", 40)  # font, size
PLAYER_FONT = font.SysFont("verdana", 20)  # font, size
BUTTON_FONT = font.SysFont("verdana", 20)  # font, size
SELECTION_FONT = font.SysFont("verdana", 20)  # font, size

BACKGROUND_IMAGE = transform.scale(
    image.load(os.path.join("media", "fundo.jpg")), (WIDTH, HEIGHT))

DICE_WIDTH, DICE_HEIGHT = WIDTH // 30, WIDTH // 30

DICE_1_IMAGE = transform.scale(
    image.load(os.path.join("media", "1.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_2_IMAGE = transform.scale(
    image.load(os.path.join("media", "2.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_3_IMAGE = transform.scale(
    image.load(os.path.join("media", "3.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_4_IMAGE = transform.scale(
    image.load(os.path.join("media", "4.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_5_IMAGE = transform.scale(
    image.load(os.path.join("media", "5.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_6_IMAGE = transform.scale(
    image.load(os.path.join("media", "6.png")), (DICE_WIDTH, DICE_HEIGHT))

DICE_HIDDEN_IMAGE = transform.scale(
    image.load(os.path.join("media", "hidden_dice.png")), (DICE_WIDTH, DICE_HEIGHT))

DICE_1_HIGHLIGHT_IMAGE = transform.scale(
    image.load(os.path.join("media", "1highlight.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_2_HIGHLIGHT_IMAGE = transform.scale(
    image.load(os.path.join("media", "2highlight.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_3_HIGHLIGHT_IMAGE = transform.scale(
    image.load(os.path.join("media", "3highlight.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_4_HIGHLIGHT_IMAGE = transform.scale(
    image.load(os.path.join("media", "4highlight.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_5_HIGHLIGHT_IMAGE = transform.scale(
    image.load(os.path.join("media", "5highlight.png")), (DICE_WIDTH, DICE_HEIGHT))
DICE_6_HIGHLIGHT_IMAGE = transform.scale(
    image.load(os.path.join("media", "6highlight.png")), (DICE_WIDTH, DICE_HEIGHT))

BUTTON_PLUS_IMAGE = transform.scale(
    image.load(os.path.join("media", "plus.png")), (DICE_WIDTH / 2, DICE_HEIGHT / 2))

BUTTON_MINUS_IMAGE = transform.scale(
    image.load(os.path.join("media", "minus.png")), (DICE_WIDTH / 2, DICE_HEIGHT / 2))

images_dir = os.path.join("media")


class GameWindow:

    def __init__(self, max_num_of_dice=6):
        self.SCREEN_WIDTH = WIDTH
        self.SCREEN_HEIGHT = HEIGHT
        self.caption = "Markovok"
        self.WIN = None
        self.max_num_of_dice = max_num_of_dice
        self.match_menu = PlayerActionMenu()

    def set_screen(self):
        # create display
        display.set_caption(self.caption)
        size = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.WIN = display.set_mode(size)
        mouse.set_visible(True)

    def draw_window(self, game):
        self.WIN.blit(BACKGROUND_IMAGE, (0, 0))
        self.draw_players(game.list_players, mode=game.dice_display_mode, highlight_figure=game.highlight_figure)
        self.match_menu.draw_action_menu(self.WIN, game.list_players)
        display.update()

    def draw_players(self, players, mode="HIDE", highlight_figure=-1):
        for player in players:
            if mode == "REVEAL":
                self.draw_dice(player, mode, highlight_figure=highlight_figure)
            elif mode == "HIDE_ALL":
                self.draw_dice(player, "HIDE")
            elif mode == "HIDE":
                if player.type == "pc":
                    self.draw_dice(player, mode)
                else:
                    self.draw_dice(player, "REVEAL", highlight_figure=-1)  # only reveal dice from user players
            else:
                print("Error in function draw_players. Invalid draw mode.")
            if player.number_of_dice_remaining > 0:  # if the player still has dice on their hand
                self.draw_player_name(player)

    def draw_player_name(self, player):
        x = player.name_coordinates[0]
        y = player.name_coordinates[1]
        draw_text = PLAYER_FONT.render(player.name, True, WHITE)
        self.WIN.blit(draw_text, (x, y))

    def draw_dice(self, player, mode="REVEAL", highlight_figure=-1):

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

        offset_x = (x_end - x_start) / (self.max_num_of_dice + 1)  # - (DICE_WIDTH / 2) * sin(angle * pi / 180)
        offset_y = (y_end - y_start) / (self.max_num_of_dice + 1) - (DICE_HEIGHT / 2) * cos(angle * pi / 180)

        delta_x = (x_end - x_start) / (self.max_num_of_dice + 1)
        delta_y = (y_end - y_start) / (self.max_num_of_dice + 1)

        if mode == "REVEAL":
            for dice in dice_list:
                if dice == 1:
                    if highlight_figure == dice:
                        self.WIN.blit(transform.rotate(DICE_1_HIGHLIGHT_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                    else:
                        self.WIN.blit(transform.rotate(DICE_1_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                if dice == 2:
                    if highlight_figure == dice:
                        self.WIN.blit(transform.rotate(DICE_2_HIGHLIGHT_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                    else:
                        self.WIN.blit(transform.rotate(DICE_2_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                if dice == 3:
                    if highlight_figure == dice:
                        self.WIN.blit(transform.rotate(DICE_3_HIGHLIGHT_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                    else:
                        self.WIN.blit(transform.rotate(DICE_3_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                if dice == 4:
                    if highlight_figure == dice:
                        self.WIN.blit(transform.rotate(DICE_4_HIGHLIGHT_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                    else:
                        self.WIN.blit(transform.rotate(DICE_4_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                if dice == 5:
                    if highlight_figure == dice:
                        self.WIN.blit(transform.rotate(DICE_5_HIGHLIGHT_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                    else:
                        self.WIN.blit(transform.rotate(DICE_5_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                if dice == 6:
                    if highlight_figure == dice:
                        self.WIN.blit(transform.rotate(DICE_6_HIGHLIGHT_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))
                    else:
                        self.WIN.blit(transform.rotate(DICE_6_IMAGE.convert_alpha(), angle),
                                      (x_start + offset_x, y_start + offset_y))

                offset_x += delta_x
                offset_y += delta_y
        else:
            for dice in dice_list:
                self.WIN.blit(transform.rotate(DICE_HIDDEN_IMAGE.convert_alpha(), angle),
                              (x_start + offset_x, y_start + offset_y))
                offset_x += delta_x
                offset_y += delta_y

    @staticmethod
    def set_player_coordinates(list_of_players):
        num_players = len(list_of_players)
        center_x = WIDTH // 3
        center_y = HEIGHT // 2
        radius = WIDTH // 4

        if num_players == 2:  # place the dice in two parallel lines
            delta = 0
            for player in reversed(list_of_players):
                player.vertices = ((1 * WIDTH // 10, HEIGHT // 4 + delta), (6 * WIDTH // 10, HEIGHT // 4 + delta))
                name_vertices = (
                    (1 * WIDTH // 10, 0.8 * HEIGHT // 4 + 1.3 * delta),
                    (6 * WIDTH // 10, 0.8 * HEIGHT // 4 + 1.3 * delta))
                delta += 2 * HEIGHT // 4
                player_name_vertices = (name_vertices[0], name_vertices[1])
                player.name_coordinates = ((player_name_vertices[0][0] + player_name_vertices[1][0]) / 2,
                                           (player_name_vertices[0][1] + player_name_vertices[1][1]) / 2)

        else:
            # coordinates of the vertices of the polygon on which the dice will be placed
            vertices = list((
                                (sin(i / num_players * 2 * pi + pi / num_players) * radius) + center_x,
                                (cos(i / num_players * 2 * pi + pi / num_players) * radius) + center_y)
                            for i in range(-1, num_players - 1))
            # coordinates of the vertices of the polygon on which the player names will be placed
            name_vertices = list((
                                     (sin(i / num_players * 2 * pi + pi / num_players) * 1.4 * radius) + center_x,
                                     (cos(i / num_players * 2 * pi + pi / num_players) * 1.4 * radius) + center_y)
                                 for i in range(-1, num_players - 1))

            i = 0
            for player in list_of_players:
                player.vertices = (vertices[i], vertices[i + 1 if i != num_players - 1 else 0])
                player_name_vertices = (name_vertices[i], name_vertices[i + 1 if i != num_players - 1 else 0])
                player.name_coordinates = ((player_name_vertices[0][0] + player_name_vertices[1][0]) / 2,
                                           (player_name_vertices[0][1] + player_name_vertices[1][1]) / 2)
                i += 1

    def draw_winner(self, text):
        draw_text = WINNER_FONT.render(text, True, WHITE)
        self.WIN.blit(draw_text, (
            self.SCREEN_WIDTH / 7 - draw_text.get_width() / 6, self.SCREEN_HEIGHT / 14 - draw_text.get_height() / 4))

        display.update()  # updates the screen before the pause
        time.delay(5000)  # pauses the game


class PlayerActionMenu:
    def __init__(self):
        self.buttons = []
        self.x = 7.5 * WIDTH / 10
        self.y = HEIGHT / 16
        self.guess_amount = "1"
        self.guess_figure = "6"

    @staticmethod
    def draw_dice(window, guess_figure, dice_height, x, y):
        if guess_figure == "1":
            window.blit(transform.scale(DICE_1_IMAGE, (dice_height, dice_height)), (x, y))
        elif guess_figure == "2":
            window.blit(transform.scale(DICE_2_IMAGE, (dice_height, dice_height)), (x, y))
        elif guess_figure == "3":
            window.blit(transform.scale(DICE_3_IMAGE, (dice_height, dice_height)), (x, y))
        elif guess_figure == "4":
            window.blit(transform.scale(DICE_4_IMAGE, (dice_height, dice_height)), (x, y))
        elif guess_figure == "5":
            window.blit(transform.scale(DICE_5_IMAGE, (dice_height, dice_height)), (x, y))
        elif guess_figure == "6":
            window.blit(transform.scale(DICE_6_IMAGE, (dice_height, dice_height)), (x, y))

    def draw_action_menu(self, window, player_list, erase_guesses=False):
        y_offset = 0
        h_offset = 0
        for player in player_list:
            if erase_guesses is True:
                draw_text = PLAYER_FONT.render("      ", True, WHITE)
                window.blit(draw_text, (self.x, self.y - draw_text.get_height() / 2 + y_offset))
            else:
                if player.guess.split():
                    player_guess = player.guess.split()
                    if player_guess[0] != "-1":
                        draw_text = PLAYER_FONT.render(player.name + "  " + player_guess[0] + "x ", True, WHITE)
                        window.blit(draw_text, (self.x, self.y - draw_text.get_height() / 2 + y_offset))
                        dice_height = draw_text.get_height()
                        self.draw_dice(window, player_guess[1], dice_height, self.x + draw_text.get_width(),
                                       self.y - draw_text.get_height() / 2 + y_offset)
                        y_offset = y_offset + draw_text.get_height() * 2
                    elif player_guess == ['-1', "0"]:
                        draw_text = PLAYER_FONT.render(player.name + "  " + "That's correct!", True, WHITE)
                        window.blit(draw_text, (self.x, self.y - draw_text.get_height() / 2 + y_offset))
                        y_offset = y_offset + draw_text.get_height() * 2
                    else:
                        draw_text = PLAYER_FONT.render(player.name + "  " + "Doubt!", True, WHITE)
                        window.blit(draw_text, (self.x, self.y - draw_text.get_height() / 2 + y_offset))
                        y_offset = y_offset + draw_text.get_height() * 2

                else:
                    draw_text = PLAYER_FONT.render(player.name, True, WHITE)
                    window.blit(draw_text, (self.x, self.y - draw_text.get_height() / 2 + y_offset))
                    y_offset = y_offset + draw_text.get_height() * 2

        y_offset = y_offset
        h_offset = 0

        # GUESS AMOUNT
        button_plus_guess_number = Button(x=self.x, y=self.y + y_offset,
                                          width=BUTTON_PLUS_IMAGE.get_width(),
                                          height=BUTTON_PLUS_IMAGE.get_height(),
                                          image=BUTTON_PLUS_IMAGE,
                                          name="increase_guess_amount_button")
        button_plus_guess_number.draw_button(window)
        draw_text = SELECTION_FONT.render(self.guess_amount, True, WHITE)
        h_offset = h_offset + 2 * draw_text.get_width()
        window.blit(draw_text, (button_plus_guess_number.x + h_offset, button_plus_guess_number.y - 5))
        h_offset = h_offset + 1.5 * draw_text.get_width()
        button_minus_guess_number = Button(x=self.x + h_offset, y=self.y + y_offset,
                                           width=BUTTON_MINUS_IMAGE.get_width(),
                                           height=BUTTON_MINUS_IMAGE.get_height(),
                                           image=BUTTON_MINUS_IMAGE,
                                           name="decrease_guess_amount_button")
        button_minus_guess_number.draw_button(window)

        # "X" LETTER
        h_offset = h_offset + 2 * draw_text.get_width()
        draw_text = SELECTION_FONT.render("x", True, WHITE)
        window.blit(draw_text, (button_plus_guess_number.x + h_offset, button_plus_guess_number.y - 5))
        h_offset = h_offset + 2 * draw_text.get_width()

        # GUESS FIGURE
        button_plus_guess_figure = Button(x=self.x + h_offset, y=self.y + y_offset,
                                          width=BUTTON_PLUS_IMAGE.get_width(),
                                          height=BUTTON_PLUS_IMAGE.get_height(),
                                          image=BUTTON_PLUS_IMAGE,
                                          name="increase_guess_figure_button")
        button_plus_guess_figure.draw_button(window)

        dice_height = draw_text.get_height()
        h_offset = h_offset + dice_height

        self.draw_dice(window, self.guess_figure, dice_height, button_plus_guess_number.x + h_offset + 2,
                       button_plus_guess_number.y - 5)

        h_offset = h_offset + 1.5 * dice_height

        button_minus_guess_figure = Button(x=self.x + h_offset, y=self.y + y_offset,
                                           width=BUTTON_MINUS_IMAGE.get_width(),
                                           height=BUTTON_MINUS_IMAGE.get_height(),
                                           image=BUTTON_MINUS_IMAGE,
                                           name="decrease_guess_figure_button")
        button_minus_guess_figure.draw_button(window)

        y_offset = y_offset + dice_height * 2.5

        # create and draw buttons
        # MAKE GUESS button
        button_make_guess = Button(x=self.x, y=self.y + y_offset, text="Make guess", font=BUTTON_FONT, txt_colour=BLACK,
                                   name="guess_button")
        button_make_guess.draw_button(window, border_colour=ORANGE, border_thickness=4)

        # CORRECT button
        y_offset = y_offset + button_make_guess.height * 2
        button_exact = Button(x=self.x, y=self.y + y_offset, text="That's correct!", font=BUTTON_FONT, bgn_colour=WHITE,
                              name="exact_button")
        button_exact.draw_button(window, border_colour=ORANGE, border_thickness=4)

        # DOUBT button
        y_offset = y_offset + button_exact.height * 2
        button_doubt = Button(x=self.x, y=self.y + y_offset, text="Doubt it!", font=BUTTON_FONT, bgn_colour=WHITE,
                              name="doubt_button")
        button_doubt.draw_button(window, border_colour=ORANGE, border_thickness=4)
        '''
        # START button (Debug)
        y_offset = y_offset + button_doubt.height * 2
        start_button = 
        Button(x=self.x, y= self.y + y_offset, text="START!", font=BUTTON_FONT, bgn_colour=WHITE, name = "start_button")
        start_button.draw_button(window, border_colour = GREEN, border_thickness = 4)
        '''
        self.buttons = [button_make_guess, button_exact, button_doubt,
                        button_plus_guess_number, button_minus_guess_number,
                        button_plus_guess_figure, button_minus_guess_figure]


class Button:
    def __init__(self, x, y, width=0, height=0,
                 text=None, font=BUTTON_FONT, txt_colour=BLACK,
                 bgn_colour=WHITE,
                 image=None,
                 name=None):
        self.x = x
        self.y = y
        self.text = text
        self.bgn_colour = bgn_colour
        self.txt_colour = txt_colour
        self.font = font
        self.image = image
        self.width = width
        self.height = height
        self.name = name

    def draw_button(self, win, border_colour=None, border_thickness=2):
        if self.text:
            draw_text = self.font.render(self.text, True, self.txt_colour)
            self.width = draw_text.get_width() * 1
            self.height = draw_text.get_height() * 0.8

            if border_colour:  # draw a thick border
                draw.rect(win, border_colour,
                          (self.x - border_thickness, self.y - border_thickness,
                           self.width + border_thickness * 2, self.height + border_thickness * 2), 0)

            draw.rect(win, self.bgn_colour, (self.x, self.y, self.width, self.height), 0)
            if self.text != "":
                win.blit(draw_text,
                         (self.x + (self.width / 2 - draw_text.get_width() / 2),
                          self.y + (self.height / 2 - draw_text.get_height() / 2)))

        elif self.image:
            win.blit(transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

    def is_mouse_over_button(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return (True)
        return (False)

    def handle_event(self, event, game_window):  # TODO events should not be referred to by string
        if event.type == MOUSEBUTTONUP:
            if self.is_mouse_over_button(event.pos):
                if self.name == "start_button":
                    return START
                elif self.name == "doubt_button":
                    return DOUBT
                elif self.name == "exact_button":
                    return EXACT_GUESS
                elif self.name == "guess_button":
                    return GUESS
                elif self.name == "increase_guess_amount_button":
                    game_window.match_menu.guess_amount = str(int(game_window.match_menu.guess_amount) + 1)
                elif self.name == "decrease_guess_amount_button":
                    game_window.match_menu.guess_amount = str(max(int(game_window.match_menu.guess_amount) - 1, 1))
                elif self.name == "increase_guess_figure_button":
                    game_window.match_menu.guess_figure = (str(int(game_window.match_menu.guess_figure) + 1) if int(
                        game_window.match_menu.guess_figure) < 6 else "1")
                    print(game_window.match_menu.guess_figure)
                elif self.name == "decrease_guess_figure_button":
                    game_window.match_menu.guess_figure = (str(int(game_window.match_menu.guess_figure) - 1) if int(
                        game_window.match_menu.guess_figure) > 1 else "6")
                    print(game_window.match_menu.guess_figure)
        return (None)
