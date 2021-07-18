"""
Esta classe define uma rodada do jogo


"""

from player import Player
from itertools import cycle
import secrets

class Game:
    def __init__(self,
                 number_of_players_human = 1,
                 number_of_players_computer=2,
                 decision_method = "Bernoulli",
                 max_number_of_dice=5,
                 number_of_rounds = 1):
        self.number_of_players_human = number_of_players_human
        self.number_of_players_computer = number_of_players_computer
        self.decision_method = decision_method
        self.max_number_of_dice = max_number_of_dice
        self.number_of_rounds = number_of_rounds
        self.dict_players={}
        self.list_players=[]
        self.number_of_remaining_active_players = self.number_of_players_human + self.number_of_players_computer

    def create_players(self):
        for i in range(self.number_of_players_human):
            self.dict_players["user" + str(i + 1)] = Player(name="user" + str(i + 1),
                                                            decision_method=self.decision_method,
                                                            max_number_of_dice=self.max_number_of_dice,type="user")
        for i in range(self.number_of_players_computer):
            self.dict_players["pc" + str(i + 1)] = Player(name="pc" + str(i + 1),
                                                          decision_method=self.decision_method,
                                                          max_number_of_dice=self.max_number_of_dice,type="pc")
        self.list_players=list(self.dict_players.values())

    def start_match(self):
        self.create_players()
        while(True):
            self.start_round()
            #option = input("Deseja continuar? (S/N)")
            #if (option == "N")or(option=="n"):
            if(self.number_of_remaining_active_players == 1): # se apenas um jogador tiver sobrado
                winning_player = self.list_players[0]
                print(f"O jogador vencedor é {winning_player.get_player_name()}!")
                break

        print("Partida encerrada.")

        return()

    def remove_player_from_list(self,player):
        self.list_players.remove(player)
        self.number_of_remaining_active_players = len(self.list_players)

    def show_table(self):
        for player in self.list_players:
            player.show_dice()



    def count_figure_in_table(self,figure):
        count = 0
        for player in self.list_players:
            count = count + player.count_figures_on_hand(figure)
        return(count)

    def start_round(self):
        guess = [0,0]

        # cada jogador joga os dados
        for player in self.list_players:
            player.roll_dice()

        players_iterator = cycle(self.list_players)

        # TODO: o jogador que começa deve ser aquele que fez o penúltimo palpite
        # embaralha a lista de jogadores
        for _ in range(secrets.choice(list(range(len(self.list_players))))):
            next(players_iterator)

        while(True):
            player = next(players_iterator) # é a vez de jogar do próximo jogador

            if (player.type == "user"): # só mostra os dados dos jogadores que são pessoas, mas não dos jogadores que são controlados pelo computador
                player.summary()

            while(player.number_of_dice_remaining == 0): # se um jogador tiver perdido todos os dados
                player = next(players_iterator) # passa para o próximo jogador


            previous_guess = guess

            if (player.type == "user"): # if the player is an user
                guess = list(map(int,input("\nInsira seu palpite: ").strip().split()))
                print(guess)
            else: # if the player is a computer
                guess = player.make_guess(previous_guess,self.list_players)


            if (guess[0] <= 0): # se alguém tiver julgado o palpite anterior incorreto/exato
                # a rodada acabará
                self.show_table() # revela os dados da mesa

                if(guess[1]==0): # se alguém tiver julgado o palpite anterior exato
                    if(self.evaluate_guess(guess,previous_guess) == "wrong"):
                        player.remove_dice(1)  # remove um dado do jogador que fez o julgamento errado
                        print("Julgamento incorreto.\n")
                    else:
                        for _ in range(len(self.list_players) - 1):
                            player = next(players_iterator)
                        player.remove_dice(1)  # remove um dado de todos os outros jogadores
                        print("Julgamento correto.\n")

                elif(self.evaluate_guess(guess,previous_guess) == "wrong"): # se alguém tiver julgado o palpite anterior exato
                    player.remove_dice(1) # remove um dado do jogador que fez o julgamento errado
                    print("Julgamento incorreto.\n")
                else:
                    for _ in range(len(self.list_players)-1):
                        player = next(players_iterator)
                    player.remove_dice(1) # remove um dado do jogador que fez o palpite anterior
                    print("Julgamento correto.\n")
                print("Fim da rodada.\n")
                print("--------------------")



                if(player.number_of_dice_remaining == 0):
                    self.remove_player_from_list(player)
                break

        return()


    def evaluate_guess(self,guess,previous_guess):
        previous_guess_amount = previous_guess[0]
        previous_guess_figure = previous_guess[1]

        if (guess[1]==-1): # se alguém julgou o palpite anterior como incorreto
            if (previous_guess_amount > self.count_figure_in_table(previous_guess_figure)):
                return("right")
            else:
                return("wrong")
        elif (guess[1]==0): # se alguém julgou o palpite anterior como exato
            if (previous_guess_amount == self.count_figure_in_table(previous_guess_figure)):
                return("right")
            else:
                return("wrong")


