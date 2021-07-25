"""
Arquivo principal do jogo

"""
from game import Game

game = Game(number_of_players_computer=6,max_number_of_dice=10,number_of_players_human=0)
game.start_match()
print(f"Number of rounds:\t{game.n_wrong_decisions + game.n_right_decisions}")
print(f"Percentage of correct decisions:\t{game.n_right_decisions/(game.n_wrong_decisions + game.n_right_decisions):.2f}")
print(f"Percentage of wrong decisions:\t{game.n_wrong_decisions/(game.n_wrong_decisions + game.n_right_decisions):.2f}")

