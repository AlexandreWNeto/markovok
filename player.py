"""
Esta classe define um jogador e suas ações

"""

from dice import Dice
from math import factorial

class Player:
    def __init__(self,name = "Nome",decision_method = "Bernoulli", max_number_of_dice=5, type = "pc"):
        self.__name = name
        self.__max_number_of_dice = max_number_of_dice
        self.__decision_method = decision_method
        self.__set_of_dice = Dice(self.__max_number_of_dice)
        self.number_of_dice_remaining = len(self.__set_of_dice.dice_list)
        self.type = type


    def roll_dice(self):
        self.__set_of_dice.roll()

    def reveal_dice(self):
        print(self.__name + ":\t", self.__set_of_dice.dice_list)

    def show_dice_hide_figures(self):
        list_hidden_dice = ["\u25A2" for i in range(self.number_of_dice_remaining)]
        print(self.__name + ":\t", list_hidden_dice)



    def summary(self):
        print(self.__name + ":\t", self.__set_of_dice.dice_list)

    def remove_dice(self,number_of_dice_to_remove=1):
        for _ in range(number_of_dice_to_remove):
            self.__set_of_dice.remove_dice()  # remove a dice from the set of dice
        self.number_of_dice_remaining = len(self.__set_of_dice.dice_list) # update the number of dice after removing a dice

    def get_player_name(self):
        return(self.__name)

    def count_dice_in_table(self,players_in_table=[]):
        if players_in_table == []:
            print("Error - list of players is empty")
            return()
        count = 0
        for player in players_in_table:
            count = count + player.number_of_dice_remaining # count the number of dice each other player has on their hands
        return(count)

    # conta o número de vezes que um dado número está presente nos dados do jogador
    def count_figures_on_hand(self,figure):
        count = 0
        for number in self.__set_of_dice.dice_list:
            if number == figure:
                count = count+1
        return(count)

    # fórmula de bernoulli - calcula a probabilidade de k ocorrências em n ensaios independentes
    def bernoulli(self,k,n):
        return(  ((1/6)**k) *((5/6)**(n-k))  * factorial(n)/(factorial(k)*factorial(n-k)) ) # TODO: generalizar fórmula para dados com um número de lados qualquer

    # calcula a probabilidade do palpite ser verdadeiro baseando-se na fórumula de Bernoulli
    def calculate_probability(self,guess=[],players_in_table=[],tipo="<="):
        if guess == []:
            print("Error - guess is empty")
            return()
        n_dice = self.count_dice_in_table(players_in_table) # número total de dados na mesa
        n_other_dice = n_dice - self.number_of_dice_remaining   # numero de outros dados na mesa
        guess_amount = guess[0] # numero de dados no palpite (de 1 ao máximo de dados possíveis)
        guess_figure = guess[1] # tipo de dado no palpite (de 1 a 6)

        n_guess_at_hand = self.count_figures_on_hand(guess_figure) # numero de dados com o valor do palpite na mão do jogador
        probability = 0
        if tipo == "<":
            # P(x<k)
            if(guess_amount <= n_guess_at_hand): # se o jogador possuir mais (ou a mesma quantidade de) dados com a figura escolhida do que o número no palpite
                probability = 0
            elif((n_other_dice < guess_amount) and (n_guess_at_hand == 0)): # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 0
            else:
                for i in range(0, guess_amount-n_guess_at_hand):
                    probability = probability + self.bernoulli(i,n_other_dice)
            #print(f"{self.__name}:\tProbabilidade de haver menos de {guess_amount} dado(s) mostrando o número {guess_figure}:\t{probability}")
            return(probability)
        elif tipo == "<=":
            # P(x<=k)
            if(guess_amount <= n_guess_at_hand): # se o jogador possuir mais (ou a mesma quantidade de) dados com a figura escolhida do que o número no palpite
                probability = 1
            elif((n_other_dice < guess_amount) and (n_guess_at_hand == 0)): # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 1
            else:
                for i in range(0, guess_amount-n_guess_at_hand+1):
                    probability = probability + self.bernoulli(i,n_other_dice)
            #print(f"{self.__name}:\tProbabilidade de haver menos de (ou exatamente) {guess_amount} dado(s) mostrando o número {guess_figure}:\t{probability}")
            return(probability)
        elif tipo == ">":
            # P(x>k)
            if (guess_amount > n_dice): # se o número de figuras no palpite for maior do que o número de dados na mesa
                probability = 0
            elif((n_other_dice < guess_amount) and (n_guess_at_hand == 0)): # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 0
            else:
                for i in range(0, guess_amount-n_guess_at_hand+1):
                    probability = probability + self.bernoulli(i,n_other_dice)
            #print(f"{self.__name}:\tProbabilidade de haver mais de {guess_amount} dado(s) mostrando o número {guess_figure}:\t{1-probability}")
            return(1-probability)
        elif tipo == ">=":
            # P(x>=k)
            if (guess_amount > n_dice): # se o número de figuras no palpite for maior do que o número de dados na mesa
                probability = 0
            elif((n_other_dice < guess_amount) and (n_guess_at_hand == 0)): # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 0
            else:
                for i in range(0, guess_amount-n_guess_at_hand):
                    probability = probability + self.bernoulli(i,n_other_dice)
            #print(f"{self.__name}:\tProbabilidade de haver mais de (ou exatamente) {guess_amount} dado(s) mostrando o número {guess_figure}:\t{1-probability}")
            return(1-probability)
        elif tipo == "=":
            # P(x=k)
            if(guess_amount < n_guess_at_hand): # se o jogador possuir mais dados com a figura escolhida do que o número no palpite
                probability = 0
            elif((n_other_dice < guess_amount) and (n_guess_at_hand == 0)): # se o jogador não tiver nenhum dado com a figura do palpite e número dos outros dados for menor do que a quantidade do palpite
                probability = 0
            elif(guess_amount > n_dice): # se o número de dados no palpite for maior do que o número de dados na mesa
                probability = 0
            else:
                probability = self.bernoulli(guess_amount-n_guess_at_hand,n_other_dice)
            #print(f"{self.__name}:\tProbabilidade de haver exatamente {guess_amount} dado(s) mostrando o número {guess_figure}:\t{probability}")
            return(probability)

    # determina o palpite mínimo superior a um determinado palpite
    def min_next_guess(self,previous_guess):
        next_guess = previous_guess
        previous_guess_amount = previous_guess[0]
        previous_guess_figure = previous_guess[1]

        next_figure = (previous_guess_figure + 1) if (previous_guess_figure < 6) else (1)  # TODO: ajustar expressão para dados com um número de dados qualquer
        next_amount = previous_guess_amount

        if (next_figure == 1):  # se o palpite pulou de 6 para 1, aumentar o número de dados no palpite também
            next_amount = previous_guess_amount + 1

        next_guess = [next_amount,next_figure]
        return(next_guess)

    # calcula a probabilidade de cada decisão possível e decide a melhor jogada
    def make_guess(self,previous_guess,players_in_table=[]):
        if players_in_table == []:
            print("Error - list of players is empty")
            return()
        previous_guess_amount = previous_guess[0]  # numero de dados no palpite anterior (de 1 ao máximo de dados possíveis)
        previous_guess_figure = previous_guess[1]  # tipo de dado no palpite anterior (de 1 a 6)

        if self.__decision_method == "Bernoulli":
            # se for o início da rodada, o palpite lido será [0,0]
            # no início, o computador sempre fará um palpite baseado nas peças que tem em mãos # TODO: implementar escolha aleatória do palpite inicial
            if(previous_guess == [0,0]):
                maximo = 1
                figure=1
                for i in range(0,7): # TODO: começar de um número aleatório
                    temp = self.count_figures_on_hand(i)
                    if (temp >= maximo):
                        maximo = temp
                        figure = i
                amount = maximo
                initial_guess = [maximo,figure]
                p_initial_guess_most_figures_in_hand = self.calculate_probability(initial_guess,players_in_table,tipo = ">")
                """print(f"{self.__name}:\tPalpite inicial: {amount} dados mostrando o número {figure}\n"
                      f"\tProbabilidade de haver mais de {amount} dado(s) "
                      f"mostrando o número {figure}:"
                      f"\t{p_initial_guess_most_figures_in_hand}\n")"""
                print(f"{self.__name}:\tPalpite: {amount} dados mostrando o número {figure}")
                return(initial_guess)

            # calcula as probabilidades do palpite anterior estar correto ou incorreto
            # calcula as probabilidades do novo palpite estar correto ou incorreto
            p_previous_guess_right = self.calculate_probability(previous_guess,players_in_table,tipo = ">=")
            p_previous_guess_exact = self.calculate_probability(previous_guess,players_in_table,tipo = "=")
            p_previous_guess_wrong = self.calculate_probability(previous_guess,players_in_table,tipo = "<")

            # busca exaustiva pelo maior palpite com maior probabilidade de acerto
            # método de cálculo da probabilidade de acerto dos palpites: binomial (Bernoulli)
            if (p_previous_guess_exact >= p_previous_guess_wrong):
                p_best_guess = p_previous_guess_exact
                best_guess = [-1,0]
            else:
                p_best_guess = p_previous_guess_wrong
                best_guess = [-1,-1]

            new_guess = self.min_next_guess(previous_guess) # determine o mínimo palpite próximo

            while(True): # busca exaustiva pelo palpite com maior probabilidade de sucesso
                new_guess_amount = new_guess[0]

                if(new_guess_amount > self.count_dice_in_table(players_in_table) - self.number_of_dice_remaining):
                    break

                p_new_guess = self.calculate_probability(new_guess,players_in_table,tipo = ">=")  # calcula a probabilidade do menor próximo palpite

                if(p_new_guess >= p_best_guess):    # verifica se o próximo palpite possui uma probabilidade de sucesso maior
                    best_guess = new_guess  # atualiza o melhor palpite
                    p_best_guess = p_new_guess

                new_guess = self.min_next_guess(new_guess)  # determine o mínimo palpite próximo
                new_guess_amount = new_guess[0]
                if(new_guess_amount > self.count_dice_in_table(players_in_table) - self.number_of_dice_remaining):
                    break
            #print(best_guess)

            if(best_guess == [-1,0]): # a maior probabilidade de sucesso está em dizer que o palpite anterior estava exatamente correto
                print(f"{self.__name}:\tPalpite exato!")
                return (best_guess)
            if (best_guess == [-1, -1]):
                print(f"{self.__name}:\tPalpite incorreto!")
                return (best_guess)

            guess_amount = best_guess[0]
            guess_figure = best_guess[1]

            """print(f"{self.__name}:\tPalpite: {guess_amount} dados mostrando o número {guess_figure}\n"
                  f"\tProbabilidade de haver mais de (ou exatamente) {guess_amount} dado(s) "
                  f"mostrando o número {guess_figure}:"
                  f"\t{p_best_guess}\n")"""
            print(f"{self.__name}:\tPalpite: {guess_amount} dados mostrando o número {guess_figure}")
            return(best_guess)

"""

            same_amount = previous_guess_amount
            next_amount = previous_guess_amount + 1
            same_figure = previous_guess_figure
            next_figure = (previous_guess_figure + 1) if (previous_guess_figure < 6) else (1) # TODO: ajustar expressão para dados com um número de dados qualquer

            if(next_figure == 1):    # se o palpite pulou de 6 para 1, aumentar o número de dados no palpite também
                same_amount = next_amount
            


            next_guess_new_amount = [next_amount,same_figure]
            next_guess_new_figure = [same_amount,next_figure]


"""
"""
            p_next_guess_new_amount_right = self.calculate_probability(next_guess_new_amount,players_in_table,tipo = ">=")
            p_next_guess_new_figure_right = self.calculate_probability(next_guess_new_figure, players_in_table,tipo=">=")

            decision_dict = {"Correto": p_previous_guess_right,
                             "Exato": p_previous_guess_exact,
                             "Errado!": p_previous_guess_wrong,
                             "Novo palpite, aumento o valor.": p_next_guess_new_amount_right,
                             "Novo palpite,aumento o valor.": p_next_guess_new_figure_right}

            # decisão
            if p_previous_guess_exact == max(decision_dict.values()):
                print(f"{self.__name}:\tPalpite exato!\n"
                      f"\tProbabilidade de haver exatamente {previous_guess_amount} dado(s) "
                      f"mostrando o número {previous_guess_figure}:"
                      f"\t{p_previous_guess_exact}\n")
                return([-1,0])

            elif p_previous_guess_wrong == max(decision_dict.values()):
                print(f"{self.__name}:\tPalpite errado!\n"
                      f"\tProbabilidade de haver menos de {previous_guess_amount} dado(s) "
                      f"mostrando o número {previous_guess_figure}:"
                      f"\t{p_previous_guess_wrong}\n")
                return([-1,-1])


            elif (p_previous_guess_right >= p_next_guess_new_figure_right) and (p_next_guess_new_figure_right >= p_next_guess_new_amount_right) :
                print(f"{self.__name}:\tNovo palpite: aumento na figura: {same_amount} dados mostrando o número {next_figure}\n"
                      f"\tProbabilidade de haver menos de {same_amount} dado(s) "
                      f"mostrando o número {next_figure}:"
                      f"\t{1-p_next_guess_new_figure_right}\n")
                return(next_guess_new_figure)

            elif (p_previous_guess_right >= p_next_guess_new_amount_right) and (p_next_guess_new_amount_right >= p_next_guess_new_figure_right) :
                print(f"{self.__name}:\tNovo palpite: aumento no número de dados: {next_amount} dados mostrando o número {same_figure}\n"
                      f"\tProbabilidade de haver menos de {next_amount} dado(s) "
                      f"mostrando o número {same_figure}:"
                      f"\t{1-p_next_guess_new_amount_right}\n")
                return(next_guess_new_amount)


            elif (p_next_guess_new_amount_right>=p_next_guess_new_figure_right):
                print(f"{self.__name}:\tNovo palpite: aumento no número de dados: {next_amount} dados mostrando o número {same_figure}\n"
                      f"\tProbabilidade de haver menos de {next_amount} dado(s) "
                      f"mostrando o número {same_figure}:"
                      f"\t{1-p_next_guess_new_amount_right}\n")
                return(next_guess_new_amount)


            else:
                print(f"{self.__name}:\tNovo palpite: aumento na figura: {same_amount} dados mostrando o número {next_figure}\n"
                      f"\tProbabilidade de haver menos de {same_amount} dado(s) "
                      f"mostrando o número {next_figure}:"
                      f"\t{1-p_next_guess_new_figure_right}\n")
                return(next_guess_new_figure)


"""
