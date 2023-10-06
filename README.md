# markovok🥕
A Liar's dice game.

# How to access the game

1- Download the executable files from the .exe folder.
2- Download the media folder.
3- Extract the compressed files into a single executable file
4 -Run the executable file markovok.exe.

Note: please save the executable file and the media folder to the same folder.

## Rules of the game

The main goal of the game is to be the last player with dice in their hands.
You can make your opponents lose dice by:
+ catching an opponent in a bluff;
+ catching your opponent making an exact guess.

The game is played in rounds. Each player starts with a given number of dice. The dice figures in a player's hand are hidden to the other players. In a given round, each player has to guess the total number of dice of a given figure on the table. Each player makes one guess at a time.

After a player makes a guess, the next player can take three actions:
+ challenge the guess
+ affirm that the guess was exactly correct
+ make another guess

If a player challenges a guess, all players must reveal their dice. There can be two outcomes to this action, depending on whether the guess was correct or not:
+ if the guess was wrong, the player that made the guess loses one dice
+ if the guess wasn't wrong, the player that challenged the guess loses one dice instead

A guess is only wrong if, on the table, there are less dice of the figure from the guess then indicated on the guess.

```
For example, the following guess would not be considered to be wrong:
- guess: 4 x four
- number of fours on the table: 5

However, the following guess would be deemed wrong:
- guess: 4 x four
- number of fours on the table: 3
```

Similarly, if a player affirms that the guess is **exactly** correct, all players must reveal their dice. There can be two outcomes to this action:
+ if the guess did not match the dice on the table **exactly**, the player that made the guess loses one dice
+ if, however, the guess was, indeed, exactly correct, all other players lose one dice (that is, except the player that affirmed that the guess was correct).

```
From the previous example, the following guess would not be considered to be **exact**:
- guess: 4 x four
- number of fours on the table: 3

However, the following guess would be considered to be **exact**:
- guess: 4 x four
- number of fours on the table: 4
```

Alternatively, if a player wants to a make another guess, the following rules apply:
+ the amount in the new guess must be higher than the number on the previous guess
**or**
+ the figure in the new guess must be higher than the figure on the previous guess, provided that the amount in the new guess is at least half (rounded up) of the amount of the previous guess

```
For example:
- previous guess: 4 x four
- valid guess: 5 x four
- valid guess: 6 x four
- invalid guess: 4 x four (guess is equal to the previous guess)
- invalid guess: 4 x 3 (figure is lower than the figrue on the previous guess)
- valid guess: 2 x 5
- invalid guess: 1 x 5 (amount is less than half (rounded up) the amount of the previous guess)
- valid guess: 5 x 3
```



