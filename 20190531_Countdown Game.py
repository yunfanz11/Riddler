"Note: This module will take one hour to run for each question, it will evaluate 113,554,259 combination"
#https://fivethirtyeight.com/features/can-you-win-the-loteria/
# Riddler Classic 2019.05.37

# My favorite game show is “Countdown” on Channel 4 in the UK. I particularly enjoy its Numbers Game.
# Here is the premise: There are 20 “small” cards, two of each numbered 1 through 10.
# There are also four “large” cards numbered 25, 50, 75 and 100.
# The player asks for six cards in total: zero, one, two, three or four “large” numbers, and the rest in “small” numbers.
# The hostess selects that chosen number of “large” and “small” at random from the deck. A random-number generator
# then selects a three-digit number, and the players have 30 seconds to use addition, subtraction, multiplication
# and division to combine the six numbers on their cards into a total as close to the selected three-digit number as
# they can.

#This riddle is two fold.
# One: What number of “large” cards is most likely to produce a solvable game and what number of “large” cards is least likely to be solvable?
# Two: What three-digit numbers are most or least likely to be solvable?

import itertools as it
import time
from collections import Counter

def solve_single_set(first_set): #turn all
    key = len(first_set)
    temp_list,sol = gsets_recur([first_set],key,set(first_set))
    for set_of_two in temp_list:
        x = set_of_two[0]
        y = set_of_two[1]
        single_set = set(combine(x, y))
        sol.add(x)
        sol.add(y)
        sol.update(single_set)
    answer = [x for x in sol if x > 99 if x <1000]
    return answer

def gsets_recur(num_set,key,sol):
    if key == 2:
        return num_set, sol
    else:
        this_tier = []
        for each_set in num_set:
            combo_list = it.combinations(each_set, 2)
            combo_set = set(tuple(x) for x in combo_list)
            for combo in combo_set:
                x = combo[0]
                y = combo[1]
                temp_sets = set(combine(x, y))
                sol.update(temp_sets)
                newset = each_set[:]
                newset.remove(x)
                newset.remove(y)
                new_tier = [newset+[i] for i in temp_sets]
                this_tier += new_tier
        num_set = [list(k) for k in (set(tuple(x) for x in this_tier))]
        return gsets_recur(num_set,key-1,sol)

def combine(x,y):
    if x > y:
        large = x
        small = y
    else:
        large = y
        small = x
    a = large + small
    b = large - small
    c = large * small
    path = [a,b,c]
    if small != 0 and large % small == 0:
        d = large//small
        path.append(d)
    return path

def all_sets(num_of_large):
    total_cards = 6
    large = [25, 50, 75, 100]
    small = [*range(1, 11),*range(1, 11)]
    a_list = it.combinations(large, num_of_large)
    b_list = tuple(it.combinations(small, total_cards - num_of_large))
    start = []
    for x in a_list:
        for y in b_list:
            # pdb.set_trace()
            new = list(x) + list(y)
            start.append(new)
    return start

def solve_fast(num_of_large):
    start = all_sets(num_of_large)
    dict = {}
    sum = 0
    for x in start:
        key = tuple(sorted(x))
        if key in dict:
            sum += dict.get(key)
        else:
            coverage = len(solve_single_set(x))
            dict[key] = coverage
            sum += coverage
    avg = sum/len(start)
    return avg


def solve_frq_fast(num_of_large):
    start = all_sets(num_of_large)
    mem = {}
    frq_dict = Counter({x:0 for x in range(100,1000)})
    for x in start:
        key = tuple(sorted(x))
        if key in mem:
            frq_dict.update(mem.get(key))
        else:
            this_count =Counter(solve_single_set(x))
            mem[key] = this_count
            frq_dict.update(this_count)
    return frq_dict

def tally():
    frq = Counter()
    for x in range(5):
        start_time = time.time()
        frq.update(solve_frq_fast(x))
        print("--- %s seconds ---" % (time.time() - start_time))
    return frq

def play (num_set,target):
    operator = ["+","-","x","/"]
    sol = []
    if target in num_set:
        return [target]

    elif len(num_set) < 2:
        return sol

    elif len(num_set) == 2:
        x = num_set[0]
        y = num_set[1]
        if x > y:
            large = x
            small = y
        else:
            large = y
            small = x

        temp_sets = combine(x,y)
        if target in temp_sets:
            pos = temp_sets.index(target)
            sol += [str(large),operator[pos],str(small)]
        return sol

    else:
        combo_list = it.combinations(num_set, 2)
        combo_set = set(tuple(x) for x in combo_list)
        #pdb.set_trace()
        for combo in combo_set:
            x = combo[0]
            y = combo[1]
            temp_sets = combine(x, y)
            if x > y:
                large = x
                small = y
            else:
                large = y
                small = x
            if target in temp_sets:
                pos = temp_sets.index(target)
                sol += [str(large), operator[pos], str(small)]
                # pdb.set_trace()
                return sol
            else:
                newset = num_set.copy()
                newset.remove(x)
                newset.remove(y)
                for i in range(len(temp_sets)):
                    a = [temp_sets[i]] + newset
                    b = play(a,target)
                    if b != []:
                        sol+= [str(large), operator[i], str(small)] + b
                        return sol
        return sol

def solve_reverse(target): # find out which sets can not play the number
    sol = []
    count = 1
    for i in range(5):
        start = all_sets(i)
        for x in start:
            if play(x,target) == []:
                sol.append(x)
            print(count)
            count += 1
    return sol


def unique_sets():
    for i in range(5):
        e_set = all_sets(i)
        e_uni = set(tuple(sorted(x)) for x in e_set)
        print (len(e_uni))

def main():
    print("Average Solve Probability - approx 66min runtime")
    for i in reversed(range(5)):
        start_time = time.time()
        sol = solve_fast(i)
        b = round(sol/900*100,2)
        print("Solvability for {} large cards and {} small cards combinations is {}%".format(i,6-i,b))
        print("---{} mins ---".format(round(time.time() - start_time)/60,2))

    a = tally()
    top = 3
    most = (a.most_common(top))
    least = a.most_common()[:-top-1:-1]

    print("\nMost solvable (Top 3)/Least Solvable (Bottome 3) - approx 50min runtime")
    print(most)
    print(least)

main()