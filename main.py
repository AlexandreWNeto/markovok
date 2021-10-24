"""
Arquivo principal do jogo
"""
import pygame
from game import Game
from GameWindow import GameWindow
import numpy as np

import os


FPS = 60
MAX_NUM_OF_DICE = 6


game_window = GameWindow(MAX_NUM_OF_DICE)
game_window.set_screen()



def main():

    game = Game(number_of_players_computer=4, max_number_of_dice= MAX_NUM_OF_DICE, number_of_players_human=1)
    game.create_players()
    game.shuffle_dice()
    game_window.set_player_coordinates(game.list_players)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get(): # event QUEUE
            if event.type == pygame.QUIT: # "x" button
                run = False
                pygame.quit()

        game_window.draw_window(game)

        if (game.number_of_remaining_active_players == 1):  # se apenas um jogador tiver sobrado
            winning_player = game.list_players[0]
            winner_text = "O jogador vencedor é " + winning_player.get_player_name()
            print(f"O jogador vencedor é {winning_player.get_player_name()}!")
            game_window.draw_winner(winner_text) # SOMEONE WON
            break





def evaluate_game(game):
    a_right = np.array([])
    a_wrong = np.array([])
    a_right = np.append(a_right,game.n_right_decisions/(game.n_wrong_decisions + game.n_right_decisions))
    a_wrong = np.append(a_wrong,game.n_wrong_decisions/(game.n_wrong_decisions + game.n_right_decisions))
    print(f"Number of rounds:\t{game.n_wrong_decisions + game.n_right_decisions}")
    print(f"Percentage of correct decisions:\t{game.n_right_decisions/(game.n_wrong_decisions + game.n_right_decisions):.2f}")
    print(f"Percentage of wrong decisions:\t{game.n_wrong_decisions/(game.n_wrong_decisions + game.n_right_decisions):.2f}")
    #del game
    print(f"Média de acertos:\t{np.average(a_right)}\tDesvio padrão:{np.std(a_right)}")
    print(f"Média de erros:\t{np.average(a_wrong)}\tDesvio padrão:{np.std(a_wrong)}")


if __name__ == "__main__":
    main()
