"""
Arquivo principal do jogo
"""
from game import Game
import numpy as np

a_right = np.array([])
a_wrong = np.array([])

for _ in range(2000):
    game = Game(number_of_players_computer=5,max_number_of_dice=5,number_of_players_human=0)
    game.start_match()



    a_right = np.append(a_right,game.n_right_decisions/(game.n_wrong_decisions + game.n_right_decisions))
    a_wrong = np.append(a_wrong,game.n_wrong_decisions/(game.n_wrong_decisions + game.n_right_decisions))

    print(f"Number of rounds:\t{game.n_wrong_decisions + game.n_right_decisions}")
    print(f"Percentage of correct decisions:\t{game.n_right_decisions/(game.n_wrong_decisions + game.n_right_decisions):.2f}")
    print(f"Percentage of wrong decisions:\t{game.n_wrong_decisions/(game.n_wrong_decisions + game.n_right_decisions):.2f}")
    del game

print(np.average(a_right),np.std(a_right))
print(np.average(a_wrong),np.std(a_wrong))