"""
Arquivo principal do jogo
"""

import pygame

from game import Game

from GameWindow import GameWindow
import numpy as np

import os

from setup import FPS, MAX_NUM_OF_DICE, NUM_PC_PLAYERS, NUM_USER_PLAYERS
from setup import START_MATCH, END_MATCH, START_ROUND, END_ROUND, DOUBT, EXACT_GUESS, GUESS, ACTION, START
from setup import DELAY_BETWEEN_GUESSES, DELAY_BETWEEN_ROUNDS

game_window = GameWindow(MAX_NUM_OF_DICE)
game_window.set_screen()


icon = pygame.image.load(os.path.join("media", "hidden_dice.jpg"))
pygame.display.set_icon(icon)

width = game_window.WIN.get_width()
height = game_window.WIN.get_height()


def main():
    game = Game(number_of_players_computer=NUM_PC_PLAYERS, number_of_players_human=NUM_USER_PLAYERS,
                max_number_of_dice=MAX_NUM_OF_DICE)
    game.create_players()
    game.shuffle_dice()
    game_window.set_player_coordinates(game.list_players)

    clock = pygame.time.Clock()
    pygame.event.post(pygame.event.Event(START))
    run = True
    while run:
        clock.tick(FPS)

        if game.number_of_remaining_active_players == 1:  # se apenas um jogador tiver sobrado
            winning_player = game.list_players[0]
            winner_text = winning_player.get_player_name() + " wins!"
            print(f"O jogador vencedor é {winning_player.get_player_name()}!")
            game_window.draw_winner(winner_text)  # SOMEONE WON
            break

        for event in pygame.event.get():  # event QUEUE
            handle_event(game, event)
        game_window.draw_window(game)




def evaluate_game(game):
    a_right = np.array([])
    a_wrong = np.array([])
    a_right = np.append(a_right, game.n_right_decisions / (game.n_wrong_decisions + game.n_right_decisions))
    a_wrong = np.append(a_wrong, game.n_wrong_decisions / (game.n_wrong_decisions + game.n_right_decisions))
    print(f"Number of rounds:\t{game.n_wrong_decisions + game.n_right_decisions}")
    print(f"Percentage of correct decisions:\t{game.n_right_decisions / (game.n_wrong_decisions + game.n_right_decisions):.2f}")
    print(f"Percentage of wrong decisions:\t{game.n_wrong_decisions / (game.n_wrong_decisions + game.n_right_decisions):.2f}")
    # del game
    print(f"Média de acertos:\t{np.average(a_right)}\tDesvio padrão:{np.std(a_right)}")
    print(f"Média de erros:\t{np.average(a_wrong)}\tDesvio padrão:{np.std(a_wrong)}")


def handle_event(game, event):
    if event.type == pygame.QUIT:  # "x" button
        pygame.quit()

    elif event.type == pygame.MOUSEBUTTONUP:  # todo only handle click events for non-computer players
        for button in game_window.match_menu.buttons:
            button_event = button.handle_event(event, game_window)
            if button_event:
                pygame.event.post(pygame.event.Event(button_event))

    elif event.type == START_MATCH and game.has_started is False:
        game.has_started = True
        game.start_new_round()

    if event.type == START and game.has_started is False:
        pygame.event.post(pygame.event.Event(START_MATCH))

    if event.type == ACTION or event.type == GUESS or event.type == EXACT_GUESS or event.type == DOUBT:
        if game.has_started is True:
            game.handle_event(event, game_window)
            game.handle_round()
            if not game.has_started:  # the round has finished
                pygame.event.post(pygame.event.Event(END_ROUND))

    elif event.type == END_ROUND:
        # erasing guesses from screen
        pygame.time.delay(DELAY_BETWEEN_ROUNDS)
        game.clear_guesses()
        pygame.event.post(pygame.event.Event(START))


if __name__ == "__main__":
    main()
