"""
Esta classe define os dados e seus métodos

"""

import secrets
class Dice:
    def __init__(self,number_of_dice=5):

        self.numbers = list(range(1,7))

        self.number_of_dice = number_of_dice
        self.dice_list = [secrets.choice(self.numbers) for _ in list(range(self.number_of_dice))]

    def roll(self):
        self.dice_list = [secrets.choice(self.numbers) for _ in self.dice_list]

    def remove_dice(self):
        self.dice_list.pop()

    def restart(self):
        self.dice_list = [secrets.choice(self.numbers) for _ in list(range(self.number_of_dice))]

