"""
Esta classe define uma rodada do jogo
"""

from player import Player
from itertools import cycle

import secrets
from collections import deque

from pygame import USEREVENT
from pygame import event
from pygame import time
from pygame import mixer

from setup import START_MATCH, END_MATCH, START_ROUND, END_ROUND, DOUBT, EXACT_GUESS, GUESS, ACTION, START
from setup import CLICK_SOUND, DICE_ROLL_SOUND, DOUBT_SOUND, WRONG_SOUND, CORRECT_SOUND, INVALID_ACTION_SOUND
from setup import DELAY_BETWEEN_GUESSES, DELAY_BETWEEN_ROUNDS

from time import sleep


mixer.init()


def check_guess_validity(guess, previous_guess):
    print(guess)
    print(previous_guess) # previous guess starts as [0,0] at the beginning of the round
    if guess and previous_guess != [0,0]:
        if guess[0] == -1: # se o jogador julgou o palpite anterior como EXATO ou INCORRETO
            return guess
        elif guess == previous_guess:
            INVALID_ACTION_SOUND.play()
            print("Palpite inválido!")

            return None
        # quantidade igual ou menor, mas figura igual ou menor
        elif guess[0] <= previous_guess[0] and guess[1] <= previous_guess[1]:
            INVALID_ACTION_SOUND.play()
            print("Palpite inválido!")
            return None
        else:
            return guess
    elif guess and previous_guess == [0,0] and guess[0] == -1:    # usuário tentou julgar o palpite anterior, mas não há palpite anterior (i.e. o usuário é o primeiro a jogar)
        print("Palpite inválido!")
        return None
    else:
        return guess


class Game:
    def __init__(self,
                 number_of_players_human=1,
                 number_of_players_computer=2,
                 decision_method="Bernoulli",
                 max_number_of_dice=5,
                 number_of_rounds=1):
        self.has_started = False
        self.number_of_players_human = number_of_players_human
        self.number_of_players_computer = number_of_players_computer
        self.decision_method = decision_method
        self.max_number_of_dice = max_number_of_dice
        self.number_of_rounds = number_of_rounds
        self.dict_players = {}
        self.list_players = []
        self.players_iterator = cycle(self.list_players)
        self.number_of_remaining_active_players = self.number_of_players_human + self.number_of_players_computer
        self.n_right_decisions = 0
        self.n_wrong_decisions = 0
        self.guess_queue = deque([[0,0], [0,0]])
        self.current_guess = None
        self.current_player = None
        self.dice_display_mode = "HIDE_ALL"
        self.highlight_figure = -1 # dice type to be highlighted at the end of the round

    def create_players(self):
        for i in range(self.number_of_players_human):
            self.dict_players["user" + str(i + 1)] = Player(name="user" + str(i + 1),
                                                            decision_method=self.decision_method,
                                                            max_number_of_dice=self.max_number_of_dice,
                                                            type="user",
                                                            vertices=((0, 0), (0, 0)))

        for i in range(self.number_of_players_computer):
            self.dict_players["pc" + str(i + 1)] = Player(name="pc" + str(i + 1),
                                                          decision_method=self.decision_method,
                                                          max_number_of_dice=self.max_number_of_dice,
                                                          type="pc",
                                                          vertices=((0, 0), (0, 0)))

        self.list_players = list(self.dict_players.values())

    def remove_player_from_list(self, player):
        self.list_players.remove(player)
        self.number_of_remaining_active_players = len(self.list_players)

    def reveal_table(self):
        for player in self.list_players:
            player.reveal_dice()
        print("\n")

    def show_table_dice_hidden(self):
        for player in self.list_players:
            if player.type == "user":
                player.reveal_dice()
            else:
                player.show_dice_hide_figures()
        print("\n")

    def count_figure_in_table(self, figure):
        count = 0
        for player in self.list_players:
            count = count + player.count_figures_on_hand(figure)
        return count

    def get_player_guess(self, player, previous_guess=None):
        if player.type == "user":  # if the player is an user
            '''  guess = list(map(int, input(
                "Escreva seu palpite\nFormatos de palpite possíveis:\n"
                "\tnúmero_de_dados figura, separados por um espaço (ex.: 1 2)\n"
                "\t0  (caso ache que o palpite anterior esteja exatamente correto)\n"
                "\t-1 (caso ache que o palpite anterior esteja incorreto)\n").strip().split()))'''
            guess = self.current_guess
            guess = check_guess_validity(guess, previous_guess)
            if guess is not None:
                if guess[1] == 0:  # palpite exato
                    print(f"{player.get_player_name()}:\tPalpite exato!")
                elif guess[1] == -1:  # palpite incorreto
                    print(f"{player.get_player_name()}:\tPalpite incorreto!")
                else:
                    print(f"{player.get_player_name()}:\tPalpite: {guess[0]} dados mostrando o número {guess[1]}")
                player.guess = " ".join(str(_) for _ in guess)  # registra o palpite
                print(f"Palpite do usuário:{player.guess}")
        else:  # if the player is a computer
            guess = player.make_guess(previous_guess, self.list_players)
            self.current_guess = guess
        if guess:
            if guess[1] > 0:
                self.highlight_figure = guess[1]  # guarda a figura a ser destacada para o caso dos dados serem revelados na próxima rodada

        return guess

    def shuffle_dice(self):
        for player in self.list_players:
            player.roll_dice()

    def start_new_round(self):
        self.players_iterator = cycle(self.list_players)

        # verifica se o jogador precisa descartar um dado
        for _ in self.list_players:
            player = next(self.players_iterator)
            if player.remove_dice_on_next_round:
                player.remove_dice(1) # remove um dado do jogador
                player.remove_dice_on_next_round = False


        self.highlight_figure = -1 # no início do jogo, nenhum dado deve ser destacado

        # cada jogador joga os dados
        self.shuffle_dice()
        DICE_ROLL_SOUND.play()
        time.delay(DELAY_BETWEEN_GUESSES)  # set minimum time between player actions

        self.show_table_dice_hidden()

        # TODO: o jogador que começa deve ser aquele que fez o penúltimo palpite
        # embaralha a lista de jogadores
        for _ in range(secrets.choice(list(range(len(self.list_players))))):
            self.current_player = next(self.players_iterator)

        self.dice_display_mode = "HIDE"  # hide the non-user dice
        event.post(event.Event(ACTION))  # trigger next action

    def handle_round(self):
        guess = None
        previous_guess = None
        print(f"\n Jogador da vez: {self.current_player.name}")
        if self.current_player is None:
            return ()
        if self.current_player.type == "pc":
            # moving the guess queue
            self.guess_queue.popleft()  # remove the oldest guess from the guess queue
            # (there should only be two guesses at the guess queue at any given time)
            previous_guess = self.guess_queue[0]  # get the previous guess
            guess = self.get_player_guess(self.current_player, previous_guess)  # determine the new guess
            self.guess_queue.append(guess)  # add the new guess to the guess queue
            event.post(event.Event(ACTION))  # trigger next action
            time.delay(DELAY_BETWEEN_GUESSES)  # set minimum time between player actions

        elif self.current_player.type == "user":
            if self.current_guess == self.guess_queue[1]:  # if the player hasn't guessed yet
                self.current_guess = None
            previous_guess = self.guess_queue[1]  # get the previous guess
            guess = self.get_player_guess(self.current_player, previous_guess)  # determine the new guess
            if guess:
                self.guess_queue.popleft()  # remove the oldest guess from the guess queue
                previous_guess = self.guess_queue[0]  # get the previous guess
                self.guess_queue.append(guess)  # add the new guess to the guess queue
                event.post(event.Event(ACTION))  # trigger next action
                # time.delay(DELAY_BETWEEN_GUESSES)  # set minimum time between player actions

        if guess and (guess[0] <= 0):  # se alguém tiver julgado o palpite anterior incorreto/exato
            self.do_end_of_round(guess, previous_guess)
            return ()
        print(self.current_player.name, self.current_guess)
        # if guess:
        #   self.advance_to_next_player()  # move the turn to the next player
        return ()

    def do_end_of_round(self, guess, previous_guess):
        self.reveal_table()  # revela os dados da mesa
        self.dice_display_mode = "REVEAL"  # reveal all dice
        DOUBT_SOUND.play() #plays the sound indicating someone has made a call
        time.delay(DELAY_BETWEEN_GUESSES)
        if guess[1] == 0:  # se alguém tiver julgado o palpite anterior exato
            if self.evaluate_guess(guess, previous_guess) == "wrong":
                WRONG_SOUND.play()
                self.current_player.remove_dice_on_next_round = True  # no início da próxima rodada, remove um dado do jogador que fez o julgamento errado
                print("Julgamento incorreto.\n")
            else:
                CORRECT_SOUND.play()
                for _ in range(len(self.list_players) - 1): # remove um dado de todos os outros jogadores na próxima rodada
                    self.current_player = next(self.players_iterator)
                    self.current_player.remove_dice_on_next_round = True  # no início da próxima rodada, remove um dado do jogador que fez o julgamento errado
                print("Julgamento correto.\n")

        # se alguém tiver julgado o palpite anterior errado
        else:
            if self.evaluate_guess(guess, previous_guess) == "wrong":
                WRONG_SOUND.play()
                self.current_player.remove_dice_on_next_round = True  # no início da próxima rodada, remove um dado do jogador que fez o julgamento errado
                print("Julgamento incorreto.\n")
                self.n_wrong_decisions = self.n_wrong_decisions + 1
            else:
                CORRECT_SOUND.play()
                for _ in range(len(self.list_players) - 1):
                    self.current_player = next(self.players_iterator)
                self.current_player.remove_dice_on_next_round = True  # no início da próxima rodada, remove um dado do jogador que fez o palpite anterior
                print("Julgamento correto.\n")
                self.n_right_decisions = self.n_right_decisions + 1
        # sleep(1)
        print("Fim da rodada.")
        print("--------------------\n")
        # sleep(1.5)

        if self.current_player.number_of_dice_remaining == 0:
            self.remove_player_from_list(self.current_player)
        self.has_started = False
        self.guess_queue = deque([[0,0], [0,0]])  # clear the guess queue for the next round
        # sleep(1)

    def evaluate_guess(self, guess, previous_guess):
        previous_guess_amount = previous_guess[0]
        previous_guess_figure = previous_guess[1]

        if guess[1] == -1:  # se alguém julgou o palpite anterior como incorreto
            if previous_guess_amount > self.count_figure_in_table(previous_guess_figure):
                return "right"
            else:
                return "wrong"
        elif guess[1] == 0:  # se alguém julgou o palpite anterior como exato
            if previous_guess_amount == self.count_figure_in_table(previous_guess_figure):
                return "right"
            else:
                return "wrong"

    def clear_guesses(self):
        for player in self.list_players:
            player.guess = " "
        self.current_guess = None

    def handle_event(self, event, game_window):
        if event.type == DOUBT:
            self.current_guess = [-1, -1]
            print(self.current_guess)
            self.dice_display_mode = "REVEAL"
        elif event.type == EXACT_GUESS:
            self.current_guess = [-1, 0]
            print(self.current_guess)
            self.dice_display_mode = "REVEAL"
        elif event.type == GUESS:
            self.current_guess = [int(game_window.match_menu.guess_amount), int(game_window.match_menu.guess_figure)]
            print(f"Botão clicado. Palpite do usuário: {self.current_guess}")
        elif event.type == ACTION:
            if self.current_player and self.current_guess:
                print(self.current_player.name, self.current_guess)
            self.advance_to_next_player()  # move the turn to the next player
            CLICK_SOUND.play()

    def advance_to_next_player(self):
        self.current_player = next(self.players_iterator)  # é a vez de jogar do próximo jogador

        if self.current_player.type == "user":  # só mostra os dados dos jogadores que são pessoas, mas não dos jogadores que são controlados pelo computador
            self.current_player.print_summary()
            pass

        while self.current_player.number_of_dice_remaining == 0:  # se um jogador tiver perdido todos os dados
            self.current_player = next(self.players_iterator)  # passa para o próximo jogador

