# https://fivethirtyeight.com/features/can-you-win-the-loteria/
#
# Lotería is a traditional Mexican game of chance, akin to bingo. Each player receives a four-by-four grid of images.
# Instead of a comically large rotating bin of numbered balls, the caller randomly draws a card from a deck containing
# all 54 possible images. If a player has that image on their grid, they mark it off. The exact rules can vary, but
# in this version, the game ends when one of the players fills their entire card (and screams “¡Lotería!”). Each of
# the 54 possible images can only show up once on each card, but other than that restriction, assume that image
# selection and placement on each player’s grid is random.
#
# One beautiful day, you and your friend Christina decide to face off in a friendly game of Lotería. What is the
# probability that either of you ends the game with an empty grid, i.e. none of your images was called?
# How does this probability change if there were more or fewer unique images? Larger or smaller player grids?


import numpy as np
import math

def play(total, mine):
    neu = total - mine*2
    b = p_live_win(total, mine, neu)
    contant = card_set(total,mine)
    final = b * contant * 2
    print("Probability of zero match game with {} total cards and {} in your hand is : {}".format(total, mine, final))

def card_set(total,mine):
    f = math.factorial
    remain = total - mine
    total_sets = f(total) / f(mine) / f(total - mine)
    unique_sets = f(remain) / f(mine) / f(remain - mine)
    return unique_sets/total_sets


def p_recursive(total, mine, neu, mem):
    if not np.isnan(mem[mine, neu]):
        return mem[mine, neu]
    elif mine == 0:
        mem[mine, neu] = 1
    elif neu == 0:
        mem[mine, neu] = mine/total * p_recursive(total-1,mine-1,neu,mem)
    else:
        hit_mine = mine/total *p_recursive(total-1, mine-1, neu,mem)
        hit_neu =  neu/total * p_recursive(total-1, mine, neu - 1,mem)
        mem[mine,neu] = hit_mine + hit_neu
    return mem[mine, neu]


def p_live_win(total, mine, neu):
    mem = np.full((mine+1,neu+1), np.nan, dtype=np.float64)
    return p_recursive(total,mine,neu, mem)

def main():
    gridSize = 16
    cardsInDeck = 54
    play(cardsInDeck,gridSize)

main()