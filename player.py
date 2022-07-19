"""
Esta classe define um jogador e suas ações

"""

from dice import Dice
from math import factorial, ceil
from itertools import islice
from random import choices

def count_dice_in_table(players_in_table=[]):
    if players_in_table == []:
        print("Error - list of players is empty")
        return ()
    count = 0
    for player in players_in_table:
        count = count + player.number_of_dice_remaining  # count the number of dice each other player has on their hands
    return (count)

def is_guess_valid(guess, previous_guess):
    if guess and previous_guess != [0, 0]:
        if guess == previous_guess:
            return False
        # quantidade igual ou menor, mas figura igual ou menor
        elif guess[0] <= previous_guess[0] and guess[1] <= previous_guess[1]:
            return False
        # figura maior, mas quantidade menor do que a metade (ou metade inteira + 1 para números ímpares) do palpite anterior
        elif guess[1] > previous_guess[1] and guess[0] < ceil(previous_guess[0] / 2):
            return False
        else:
            return True


class Player:
    def __init__(self, name="Nome", decision_method="Bernoulli", max_number_of_dice=5, type="pc",
                 vertices=((0, 0), (0, 0))):
        self.name = name
        self.__max_number_of_dice = max_number_of_dice
        self.__decision_method = decision_method
        self.__set_of_dice = Dice(self.__max_number_of_dice)
        self.number_of_dice_remaining = len(self.__set_of_dice.dice_list)
        self.type = type
        self.vertices = vertices
        self.name_coordinates = (0, 0)
        self.guess = ""
        self.remove_dice_on_next_round = False
        self.possible_guesses = {}

    def roll_dice(self):
        self.__set_of_dice.roll()

    def reveal_dice(self):
        print(self.name + ":\t", self.__set_of_dice.dice_list)

    def show_dice_hide_figures(self):
        list_hidden_dice = ["\u25A2" for i in range(self.number_of_dice_remaining)]
        print(self.name + ":\t", list_hidden_dice)

    def print_summary(self):
        print(self.name + ":\t", self.__set_of_dice.dice_list)

    def remove_dice(self, number_of_dice_to_remove=1):
        for _ in range(number_of_dice_to_remove):
            self.__set_of_dice.remove_dice()  # remove a dice from the set of dice
        self.number_of_dice_remaining = len(
            self.__set_of_dice.dice_list)  # update the number of dice after removing a dice

    def get_player_name(self):
        return self.name

    def get_set_of_dice(self):
        return self.__set_of_dice

    # conta o número de vezes que um dado número está presente nos dados do jogador
    def count_figures_on_hand(self, figure):
        count = 0
        for number in self.__set_of_dice.dice_list:
            if number == figure:
                count = count + 1
        return (count)

    # fórmula de bernoulli - calcula a probabilidade de k ocorrências em n ensaios independentes
    def bernoulli(self, k, n):
        return ((1 / 6) ** k) * ((5 / 6) ** (n - k)) * factorial(n) / (factorial(k) * factorial(
            n - k))  # TODO: generalizar fórmula para dados com um número de lados qualquer

    # calcula a probabilidade do palpite ser verdadeiro baseando-se na fórumula de Bernoulli
    def calculate_probability(self, guess=None, players_in_table=None, tipo="<="):
        if players_in_table is None:
            players_in_table = []
        if guess is None:
            guess = []
        if not guess:
            print("Error - guess is empty")
            return ()
        n_dice = count_dice_in_table(players_in_table)  # número total de dados na mesa
        n_other_dice = n_dice - self.number_of_dice_remaining  # numero de outros dados na mesa
        guess_amount = guess[0]  # numero de dados no palpite (de 1 ao máximo de dados possíveis)
        guess_figure = guess[1]  # tipo de dado no palpite (de 1 a 6)

        n_guess_at_hand = self.count_figures_on_hand(guess_figure)  # numero de dados com o valor do palpite na mão do jogador
        probability = 0
        if tipo == "<":
            # P(x<k)
            # se o jogador possuir mais (ou a mesma quantidade de) dados com a figura escolhida do que o número no palpite
            if guess_amount <= n_guess_at_hand:
                probability = 0
            # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
            elif (n_other_dice < guess_amount) and ( n_guess_at_hand == 0):
                probability = 0
            else:
                for i in range(0, guess_amount - n_guess_at_hand):
                    probability = probability + self.bernoulli(i, n_other_dice)
            # print(f"{self.__name}:\tProbabilidade de haver menos de {guess_amount} dado(s) mostrando o número {guess_figure}:\t{probability}")
            return (probability)
        elif tipo == "<=":
            # P(x<=k)
            if (guess_amount <= n_guess_at_hand):  # se o jogador possuir mais (ou a mesma quantidade de) dados com a figura escolhida do que o número no palpite
                probability = 1
            elif ((n_other_dice < guess_amount) and (
                    n_guess_at_hand == 0)):  # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 1
            else:
                for i in range(0, guess_amount - n_guess_at_hand + 1):
                    probability = probability + self.bernoulli(i, n_other_dice)
            # print(f"{self.__name}:\tProbabilidade de haver menos de (ou exatamente) {guess_amount} dado(s) mostrando o número {guess_figure}:\t{probability}")
            return (probability)
        elif tipo == ">":
            # P(x>k)
            if (guess_amount > n_dice):  # se o número de figuras no palpite for maior do que o número de dados na mesa
                probability = 0
            elif ((n_other_dice < guess_amount) and (
                    n_guess_at_hand == 0)):  # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 0
            else:
                for i in range(0, guess_amount - n_guess_at_hand + 1):
                    probability = probability + self.bernoulli(i, n_other_dice)
            # print(f"{self.__name}:\tProbabilidade de haver mais de {guess_amount} dado(s) mostrando o número {guess_figure}:\t{1-probability}")
            return (1 - probability)
        elif tipo == ">=":
            # P(x>=k)
            if (guess_amount > n_dice):  # se o número de figuras no palpite for maior do que o número de dados na mesa
                probability = 0
            elif ((n_other_dice < guess_amount) and (
                    n_guess_at_hand == 0)):  # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 0
            else:
                for i in range(0, guess_amount - n_guess_at_hand):
                    probability = probability + self.bernoulli(i, n_other_dice)
            # print(f"{self.__name}:\tProbabilidade de haver mais de (ou exatamente) {guess_amount} dado(s) mostrando o número {guess_figure}:\t{1-probability}")
            return (1 - probability)
        elif tipo == "=":
            # P(x=k)
            if (guess_amount < n_guess_at_hand):  # se o jogador possuir mais dados com a figura escolhida do que o número no palpite
                probability = 0
            elif ((n_other_dice < guess_amount) and (n_guess_at_hand == 0)):  # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 0
            elif (guess_amount > n_dice):  # se o número de dados no palpite for maior do que o número de dados na mesa
                probability = 0
            else:
                probability = self.bernoulli(guess_amount - n_guess_at_hand, n_other_dice)
            # print(f"{self.__name}:\tProbabilidade de haver exatamente {guess_amount} dado(s) mostrando o número {guess_figure}:\t{probability}")
            return (probability)

    # determina o palpite mínimo superior a um determinado palpite
    def min_next_guess(self, previous_guess):
        next_guess = previous_guess
        previous_guess_amount = previous_guess[0]
        previous_guess_figure = previous_guess[1]

        next_figure = (previous_guess_figure + 1) if (previous_guess_figure < 6) else (
            1)  # TODO: ajustar expressão para dados com um número de dados qualquer
        next_amount = previous_guess_amount

        if (next_figure == 1):  # se o palpite pulou de 6 para 1, aumentar o número de dados no palpite também
            next_amount = previous_guess_amount + 1

        next_guess = [next_amount, next_figure]
        return (next_guess)

    # calcula a probabilidade de cada decisão possível e decide a melhor jogada
    def make_guess(self, previous_guess, players_in_table=[]):
        if players_in_table == []:
            print("Error - list of players is empty")
            return ()
        previous_guess_amount = previous_guess[
            0]  # numero de dados no palpite anterior (de 1 ao máximo de dados possíveis)
        previous_guess_figure = previous_guess[1]  # tipo de dado no palpite anterior (de 1 a 6)

        if self.__decision_method == "Bernoulli":
            new_guess = self.make_bernoulli_guess(previous_guess, players_in_table)
            self.guess = " ".join(str(_) for _ in new_guess)
            return (new_guess)
        return ()

    def make_bernoulli_guess(self, previous_guess, players_in_table=[]):
        # se for o início da rodada, o palpite lido será [0,0]
        # no início, o computador sempre fará um palpite baseado nas peças que tem em mãos # TODO: implementar escolha aleatória do palpite inicial

        self.possible_guesses = {} # reinicia o dicionário de palpites possíveis
        if (previous_guess == [0, 0]):
            maximo = 1
            figure = 1
            for i in range(0, 7):  # TODO: começar de um número aleatório
                temp = self.count_figures_on_hand(i)
                if (temp >= maximo):
                    maximo = temp
                    figure = i
            amount = maximo
            initial_guess = [maximo, figure]
            p_initial_guess_most_figures_in_hand = self.calculate_probability(initial_guess, players_in_table, tipo=">")
            """print(f"{self.__name}:\tPalpite inicial: {amount} dados mostrando o número {figure}\n"
                  f"\tProbabilidade de haver mais de {amount} dado(s) "
                  f"mostrando o número {figure}:"
                  f"\t{p_initial_guess_most_figures_in_hand}\n")"""
            print(f"{self.name}:\tPalpite: {amount} dados mostrando o número {figure}")
            return (initial_guess)

        # calcula as probabilidades do palpite anterior estar correto ou incorreto
        # calcula as probabilidades do novo palpite estar correto ou incorreto
        p_previous_guess_right = self.calculate_probability(previous_guess, players_in_table, tipo=">=")
        p_previous_guess_exact = self.calculate_probability(previous_guess, players_in_table, tipo="=")
        p_previous_guess_wrong = self.calculate_probability(previous_guess, players_in_table, tipo="<")

        # busca exaustiva pelo maior palpite com maior probabilidade de acerto
        # método de cálculo da probabilidade de acerto dos palpites: binomial (Bernoulli)
        if (p_previous_guess_exact >= p_previous_guess_wrong):
            p_best_guess = p_previous_guess_exact
            best_guess = [-1, 0]
        else:
            p_best_guess = p_previous_guess_wrong
            best_guess = [-1, -1]

        self.possible_guesses[tuple(best_guess)] = p_best_guess  # add the guess to the dictionary of guesses

        new_guess = self.min_next_guess([1,1])  # determine o mínimo palpite válido, começando do menor palpite possível

        while (True):  # busca exaustiva pelo palpite com maior probabilidade de sucesso

            if not is_guess_valid(new_guess, previous_guess): # caso o palpite próximo não seja válido
                new_guess = self.min_next_guess(new_guess)  # pule este palpite
                continue # pule o palpite inválido e avalie o próximo palplite

            new_guess_amount = new_guess[0]

            if new_guess_amount > count_dice_in_table(players_in_table) - self.number_of_dice_remaining:
                break

            p_new_guess = self.calculate_probability(new_guess, players_in_table,
                                                     tipo=">=")  # calcula a probabilidade do menor próximo palpite

            self.possible_guesses[tuple(new_guess)] = p_new_guess  # add the guess to the dictionary of guesses

            if p_new_guess >= p_best_guess:  # verifica se o próximo palpite possui uma probabilidade de sucesso maior
                best_guess = new_guess  # atualiza o melhor palpite
                p_best_guess = p_new_guess

            new_guess = self.min_next_guess(new_guess)  # determine o mínimo palpite próximo


            new_guess_amount = new_guess[0]
            if (new_guess_amount > count_dice_in_table(players_in_table) - self.number_of_dice_remaining):
                break

        chosen_guess = best_guess

        # ordena o dicionário de possíveis ações por ordem decrescente de probabilidade
        self.possible_guesses = dict(sorted(self.possible_guesses.items(), key=lambda a:a[1], reverse = True))
        # retira uma amostra das possíveis ações
        self.possible_guesses = dict(islice(self.possible_guesses.items(), min(10,len(self.possible_guesses))))

        #pondera as probabilidades do conjunto amostral; as escolhas de maior probabilidade ganham um peso maior
        for key, probability in self.possible_guesses.items():
            self.possible_guesses[key] = probability
        print(self.possible_guesses)
        #sorteia uma ação dentre a amostra de ações
        # ações com maior probabilidade de acerto tem peso maior no sorteio
        chosen_guess = choices(
            list(self.possible_guesses.keys()), weights = tuple(self.possible_guesses.values()), k =1
        )[0]

        # print(best_guess)
        # a maior probabilidade de sucesso está em dizer que o palpite anterior estava exatamente correto
        if (chosen_guess == [-1, 0]):
            print(f"{self.name}:\tPalpite exato!")
            return chosen_guess

        if chosen_guess == [-1, -1]:
            print(f"{self.name}:\tPalpite incorreto!")
            return (chosen_guess)

        guess_amount = chosen_guess[0]
        guess_figure = chosen_guess[1]

        """print(f"{self.__name}:\tPalpite: {guess_amount} dados mostrando o número {guess_figure}\n"
              f"\tProbabilidade de haver mais de (ou exatamente) {guess_amount} dado(s) "
              f"mostrando o número {guess_figure}:"
              f"\t{p_best_guess}\n")"""
        print(f"{self.name}:\tPalpite: {guess_amount} dados mostrando o número {guess_figure}")
        return (chosen_guess)


