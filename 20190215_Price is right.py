# https://fivethirtyeight.com/features/come-on-down-and-escape-the-maze/
# You’re playing a “Price Is Right” game called Cover Up, which has contestants try to guess all five digits of the
# price of a brand new car. You have two numbers to choose from for the first digit, three numbers to choose from for
# the second digit, and so on, ending with six options for the fifth and final digit. You’re not winning any $100,000
# cars in this game.
#
# First, you lock in a guess at the entire price of the car. If you get at least one digit correct on the first guess,
# the correct digit(s) are highlighted and you get to replace incorrect digits on a second guess. This continues on
# subsequent guesses until the price is guessed correctly. But if none of the new numbers you swapped in are correct,
# you lose. A contestant could conceivably win the car on the first guess or with five guesses, getting one additional
# correct digit highlighted on each guess.
#
# First question: If you’re guessing entirely by chance, what’s the likelihood of winning the car?
#
# Second question: Suppose you know a little bit about cars. Specifically, you are 100 percent certain about the digit
# in the ten-thousands place, but have to guess the remaining four digits by chance. What’s the best strategy, and
# what’s the likelihood of winning the car now?

import itertools

# Code Strategy
##1. Input: optionlist (2,3,4,5,6)
##2. Generate possible guesses
##3. For each guess
##    If no right guess, gamestate = Over, winrate = 0%
##    If all right guess, gamestate = Over, winrate = 100%
##    If at least one right guess, gamestate = Continue, winrate = Resurve
##    new optionlist (all wrong guess reduce 1, all right guess remove element, all 1 change to 0)
##4. Masterwinrate = each guess prob * each guess winrate


def winratespecial(options):  # a = winrate using lifelife

    a = 0
    outcomes = possibleOutcome(options)
    for x in outcomes:
        chance = prob(options,x)
        if (gameResult(x) == "W"):
            a += chance
        else:
            newoptions = newState(options,x)
            a += winrate(newoptions)* chance

    b = 0
    outcomes = possibleOutcome(options)
    for x in outcomes:
        chance = prob(options, x)
        if gameResult(x) == "W":
            b += chance
        elif gameResult(x) == "L":
            b = b
        else:
            newoptions = newState(options, x)
            b += winratespecial(newoptions) * chance

    if a > b:
        return a
    else:
        return b


def winrate(options):
    sol = 0
    outcomes = possibleOutcome(options)
    for x in outcomes:
        chance = prob(options,x)
        if (gameResult(x) == "W"):
            sol += chance
        elif (gameResult(x) == "L"):
            sol = sol
        else:
            newoptions = newState(options,x)
            sol += winrate(newoptions)* chance
    return sol


def prob(options, outcome):
    sol = 1
    for i in range(0,len(outcome)):
        chance = 1/(options[i])
        if outcome[i]:
            sol *= chance
        else:
            sol *= (1-chance)

    return sol

def possibleOutcome(options):
    sol = []
    normal = [True, False]
    special = [True]
    for x in options:
        if x == 1:
            sol.append(special)
        else:
            sol.append(normal)

    sol = list(itertools.product(*sol))
    return sol

#generate new optionlist based on the guess result
def newState(options, guess):
    newoption = []
    for i in range(0,len(options)):
        if (not(guess[i])):
            b = options[i]
            newoption.append(b-1)
    return (newoption)

#determine if game is over, win, loss or notover

def gameResult(guess):
    winflag = "W"
    loseflag = "L"
    notoverflag = "N"
    if sum(guess) == len(guess):
        return winflag
    elif sum(guess) == 0:
        return loseflag
    else:
        return notoverflag


def main():
    optionlist1 = [2,3,4,5,6]
    sol = round(winrate(optionlist1),5)
    print("Win prob_entirely by luck: {}%".format(round(sol*100,2)))

    optionlist2 = [3,4,5,6]
    sol = round(winratespecial(optionlist2),5)
    print("Win_prob_knowing first digit: {}%".format(round(sol*100,2)))

main()
