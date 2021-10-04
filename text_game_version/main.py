"""
Arquivo principal do jogo
"""
from game import Game
import numpy as np
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from background import Background

def main():

  #  pygame.init()
#    background = Background()
 #   background.set_screen()
    run_bool = True
    game = Game(number_of_players_computer=5, max_number_of_dice=5, number_of_players_human=0)

    #while run_bool:
     #   for event in pygame.event.get():
      #      if event.type == KEYDOWN:
       #         if event.key == K_ESCAPE:
        #            run_bool = False
         #   elif event.type == QUIT:
          #      run_bool = False
    game.start_match()
    #background.draw()

    evaluate_game(game)


    pygame.quit()





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