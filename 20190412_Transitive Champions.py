#https://fivethirtyeight.com/features/how-many-times-a-day-is-a-broken-clock-right/
"""
On Sunday, the Baylor Lady Bears won the 2019 NCAA women’s basketball championship, and on Monday, the Virginia Cavaliers did the same on the men’s side.

But what about all of the unsung transitive champions? For example, earlier in the season, Florida State beat Virginia,
thereby laying claim to a transitive championship for the Seminoles. And Boston College beat Florida State, claiming
one for the Eagles. And IUPUI beat Boston College, and Ball State beat IUPUI, and so on and so on.

Baylor, meanwhile, only lost once, to Stanford, who lost to five teams, and so on.

How many transitive national champions were there this season in the women’s and men’s games?
Or, maybe more descriptively, how many teams weren’t transitive national champions? You should include tournament
losses in your calculations. All of this season’s women’s results are here and all of the men’s results are here.
"""

import pandas as pd


# Women Section

file_path = "NCAA.xlsx"
df_women = pd.read_excel(file_path, sheet_name='Sheet2')
df_men = pd.read_excel(file_path, sheet_name='Sheet3')


#NCAA Women

win_teams = list(df_women["Winning Team"])
lose_teams = list(df_women["Losing Team"])
game_results = list(zip(win_teams, lose_teams))
my_teams = win_teams + lose_teams
teams = list(set(my_teams))
champ = ["Baylor"]


def find_teams(seed, remain_teams):
    global game_results
    sol = []
    if remain_teams == [] or seed == []:
        return sol

    else:
        for x in seed:
            # pdb.set_trace()
            for y in game_results:
                if y[1] == x and y[0] in remain_teams:
                    sol.append(y[0])
    return list(set(sol))


def main():
    global champ
    global teams
    remain = list(set(teams) - set(champ))
    this_tier = find_teams(champ, remain)

    tier_list = []
    tier_count = []

    while this_tier != []:
        #pdb.set_trace()
        tier_list.append(this_tier)
        tier_count.append(len(this_tier))
        remain = list(set(remain) - set(this_tier))
        this_tier = find_teams(this_tier, remain)


    print(tier_count)
    print("Number of transitive champions: {}".format(sum(tier_count)))
    return tier_list

print("NCAA Women")
women = main()

#NCAA Men

win_teams = list(df_men["Winning Team"])
lose_teams = list(df_men["Losing Team"])
game_results = list(zip(win_teams, lose_teams))
my_teams = win_teams + lose_teams
teams = list(set(my_teams))
champ = ["Virginia"]

print("\nNCAA Men")
men = main()

