# https://fivethirtyeight.com/features/can-you-win-a-spelling-bee-if-you-know-99-percent-of-the-words/
"""
You are competing in a spelling bee alongside nine other contestants. You can each spell words perfectly from a certain
portion of the dictionary but will misspell any word not in that portion of the book. Specifically, you have 99 percent
of the dictionary down cold, and your opponents have 98 percent, 97 percent, 96 percent, and so on down to 90 percent
memorized. The bee’s rules are simple: The contestants take turns spelling in some fixed order, which then restarts
with the first surviving speller at the end of a round. Miss a word and you’re out, and the last speller standing wins.
The bee words are chosen randomly from the dictionary.

First, say the contestants go in decreasing order of their knowledge, so that you go first. What are your chances of
winning the spelling bee? Second, say the contestants go in increasing order of knowledge, so that you go last.
What are your chances of winning now?

"""

import numpy as np
from itertools import combinations
import pdb

def spelling_fast(player_count, win_prob, my_pos = 0):  # [0 = first, 1 = last]
    players = dict(zip(range(1,player_count+1),win_prob))
    if my_pos == 0:
        my_id = 1
    elif my_pos == 1:
        my_id = player_count
    mem = {(my_id,):1}
    if my_pos == 0:
        return spelling_going_first(players, mem)
    else:
        return spelling_going_last(players, mem, my_id)

def spelling_going_first (players, mem):
    player_count = len(players)
    players_id = players.keys()
    players_key = tuple(players_id)
    if players_key in mem:
        return mem[players_key]

    elif player_count == 2:
        my_win_prob = players[1]
        this_round_lose = (1-my_win_prob)
        this_round_cont = np.prod(list(players.values()))
        winrate = 1 - (this_round_lose/(1-this_round_cont))
        mem[tuple(players_id)] = winrate
        return winrate
    else:
        winrate = 0
        opp_id = [x for x in players_id if x != 1]
        this_round_cont = np.prod(list(players.values()))
        l_factor = 1-this_round_cont

        # Generate all possible loser in this round
        event_outcome = []
        for i in range(1,len(opp_id)+1):
            for x in combinations(opp_id,i):
                event_outcome.append(x)

        # add up all the winrate of each loser combination
        for event in event_outcome:
            cum_prob = 1
            survivors = dict(players)
            for each_loser in event:
                each_loser_prob = 1 - players[each_loser]
                cum_prob *= each_loser_prob
                del survivors[each_loser]
            for each_winner_prob in survivors.values():
                cum_prob *= each_winner_prob
            nextround_winrate = spelling_going_first(survivors,mem)
            this_prob = (cum_prob * nextround_winrate)/l_factor
            winrate += this_prob
        mem[tuple(players_id)] = winrate
        return winrate


def spelling_going_last(players, mem, my_id):
    player_count = len(players)
    players_id = players.keys()
    players_key = tuple(players_id)
    if players_key in mem:
        return mem[players_key]

    elif player_count == 2:
        my_win_prob = players[my_id]
        opp_id = [x for x in players_id if x != my_id][0]
        opp_win_prob = players[opp_id]
        this_round_win = (1 - opp_win_prob)
        this_round_cont = my_win_prob * opp_win_prob
        l_factor = 1-this_round_cont
        winrate = this_round_win/l_factor
        mem[tuple(players_id)] = winrate
        return winrate

    else:

        # in the event that at least 1 person before me surives
        opp_id = [x for x in players_id if x != my_id]
        this_round_cont = np.prod(list(players.values()))
        l_factor = 1-this_round_cont

        # in the event that everyone before me loses
        opp_win_prob = [players[x] for x in players_id if x != my_id]
        opp_lose_prob = list(map(lambda x: 1 - x, opp_win_prob))
        winrate = np.prod(opp_lose_prob) / l_factor

        # Generate all possible loser in this round
        event_outcome = []
        for i in range(1,len(opp_id)):
            for x in combinations(opp_id,i):
                event_outcome.append(x)

        # add up all the winrate of each loser combination
        for event in event_outcome:
            cum_prob = 1
            survivors = dict(players)
            for each_loser in event:
                each_loser_prob = 1 - players[each_loser]
                cum_prob *= each_loser_prob
                del survivors[each_loser]
            for each_winner_prob in survivors.values():
                cum_prob *= each_winner_prob
            nextround_winrate = spelling_going_last(survivors,mem,my_id)
            this_prob = (cum_prob * nextround_winrate)/l_factor
            winrate += this_prob
            # pdb.set_trace()
        mem[tuple(players_id)] = winrate
        return winrate

def main():
    my_win = 0.99
    print("Your chance of survival is :{}".format(round(my_win,4)))
    competitors = [0.98,0.97,0.96,0.95,0.94,0.93,0.92,0.91,0.90]
    print("Your competitiors' chances of survival are %s" % competitors)
    print("There is total %s players" % (len(competitors)+1))
    #going first
    win_prob = [my_win]+competitors
    playercount = len(win_prob)
    first = spelling_fast(playercount, win_prob, 0)
    print("\nChance of winning if going first: {}".format(round(first,4)))
    #going last
    win_prob = competitors+[my_win]
    playercount = len(win_prob)
    last = spelling_fast(playercount, win_prob, 1)
    print("Chance of winning if going last: {}".format(round(last,4)))
    print("Your chance of winning will increase by {} if you go last rather than first".format(round(last-first,4)))


main()