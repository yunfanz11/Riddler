# https://fivethirtyeight.com/features/come-on-down-and-escape-the-maze/


#
# Those pesky enemies of Riddler Nation are at it again! A couple of weeks ago, they trapped you in a maze without walls.
# Most of you escaped, but the enemies remain undeterred. They’ve been hard at work building a new maze without walls, shown below.
#
# Before banishing you to the maze, they hand you a list of rules.
#
# 1. You can enter via any perimeter square. The goal is to reach the yellow star in the center with the lowest possible score,
#    which is calculated by adding up all the numbers that appeared in any squares you crossed.
# 2. You can only move horizontally or vertically (not diagonally) to bordering squares.
# 3. If you enter a square with an arrow (↑), you have to exit that square in the direction the arrow indicates. Some squares have double arrows (↔), giving you a choice of two directions.
# 4. If you enter a square with a number, you must add it to your score, but you can exit in the direction of your choice.
# 5. If an arrow leads you to a square with a skull, you die. But you knew that already.
#

import numpy as np

class Location:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return ("P({},{},{})".format(self.x, self.y, self.value))


##Create GameBoard
Row1 =[21,11,2,0,14,14,14,100,21,3,22,1,22,0,0,100,11,21,3,21]
Row2 =[14,22,12,11,14,13,2,21,100,0,1,21,2,11,1,3,21,12,14,21]
Row3 =[22,21,2,21,22,3,13,12,21,21,13,12,22,13,21,21,2,21,100,14]
Row4 =[21,22,22,22,22,13,22,14,0,21,3,21,3,21,22,1,22,22,13,1]
Row5 =[22,11,22,12,100,21,22,22,1,100,21,0,13,0,14,1,3,13,13,22]
Row6 =[1,21,21,22,21,1,21,22,22,21,3,22,12,22,13,22,21,14,22,22]
Row7 =[21,14,21,22,21,100,21,22,22,1,21,2,22,22,21,21,22,22,14,1]
Row8 =[3,2,22,22,22,21,22,3,14,21,3,21,3,11,11,22,21,21,12,11]
Row9 =[14,0,11,14,1,2,14,21,22,21,3,3,21,0,13,100,22,22,21,12]
Row10 =[21,22,12,14,13,2,21,12,22,0,21,1,22,21,11,13,22,0,21,21]
Row11 =[21,22,2,21,1,12,21,11,11,0,1000,2,22,3,21,21,22,11,22,22]
Row12 =[22,12,100,22,3,13,21,21,21,22,21,13,2,21,22,21,22,21,11,21]
Row13 =[21,100,11,13,22,21,21,11,21,21,13,22,1,0,22,3,13,12,22,21]
Row14 =[2,100,14,12,21,21,21,21,100,1,21,21,22,0,21,13,0,3,22,22]
Row15 =[100,21,2,14,14,12,22,1,11,21,0,22,3,1,13,22,100,22,22,21]
Row16 =[13,12,12,22,1,22,21,21,12,22,22,21,21,1,0,11,21,21,21,0]
Row17 =[22,12,3,22,21,22,2,12,22,11,22,13,0,100,2,22,1,22,22,21]
Row18 =[100,0,2,22,22,21,21,12,2,0,0,2,22,11,14,22,22,22,21,21]
Row19 =[22,22,1,22,21,21,3,21,22,3,21,21,2,0,11,11,22,2,14,22]
Row20 =[13,22,22,22,3,21,21,21,14,22,13,22,1,2,22,2,22,12,21,11]
length = 20
GameBoard = [Row1,Row2,Row3,Row4,Row5,Row6,Row7,Row8,Row9,Row10,
            Row11,Row12,Row13,Row14,Row15,Row16,Row17,Row18,Row19,Row20]

GameBoard_array = np.array(GameBoard)
np.set_printoptions(edgeitems=30,linewidth=200)


print("Game board generated")
print(GameBoard_array)
print("Note: Goal(1000), Landmine(100), Up(11),Down(12),Left(13),Right(14),Vertical(21),Horizontal(22),Blank(0)\n")

## starting point
def entryPoints(side):
    sol = []
    for i in range(1,side+1):
        x = (1,i)
        y = (i,1)
        w = (side,i)
        v = (i,side)
        sol.append(x)
        sol.append(y)
        sol.append(w)
        sol.append(v)
    return set(sol)


## possible moves

def posMoves (point):
    global length
    x = point[0]
    y = point[1]
    value = GameBoard[x-1][y-1]
    
    a = (x-1,y) #up
    b = (x+1,y) #down
    c = (x,y-1) #left
    d = (x,y+1) #right 
    

    if value == 11:
        sol = [a]
    elif value == 12:
        sol = [b]
    elif value == 13:
        sol = [c]
    elif value == 14:
        sol = [d]
    elif value == 21:
        sol = [a,b]
    elif value == 22:
        sol = [c,d]
    elif value == 100 or value == 1000:
        sol = []
    else:
        sol = [a,b,c,d]


    for i in sol:
        if i[0] < 1 or i[1] < 1:
            sol.remove(i)
        elif i[0] > length or i[1] > length:
            sol.remove(i)
            
    return sol


def giveScore(point):
    x = point[0]
    y = point[1]
    value = GameBoard[x-1][y-1]
    if value < 10:
        return value
    else:
        return 0
    

def findPath(point, score, path, memory): #return a collection of tried paths and results
    global best
    x = point[0]
    y = point[1]
    value = GameBoard[x-1][y-1]
    moves = posMoves(point)
    newpath = list(path)
    newpath.append(point)
    newscore = score + giveScore(point)

    if point in path: #loop detection
        sol = ("L", 0, "Loop")
        memory.append(sol)
    
    elif value == 1000:
        sol = ("W", score, newpath)
        best = score
        memory.append(sol)
        
    elif value == 100 or len(moves)==0:
        sol = ("L", 0, "No Moves")
        memory.append(sol)

    elif newscore > best:
        sol = ("L", 0, "Not Best")
        memory.append(sol)

    else:
        for i in moves:
                findPath(i, newscore, newpath, memory)
                
    return memory


def main():
    total = 0
    sol = []
    winner = []
    global length
    start = entryPoints(length)
    for x in start:
        path = []
        memory = []
        sol += findPath(x, total, path, memory)
    for y in sol:
        if y[0] == "W":
            winner.append(y)

    last = winner[len(winner)-1]
    shortestpath = last[2]
    bestscore = last[1]
    bestwinner = []
    
    for z in winner:
        if z[1] == bestscore:
            bestwinner.append(z)
            if len(z[2]) < len(shortestpath):
                shortestpath = z[2]


    print("Winning score is: {}".format(bestscore))
    print("Number of Winning Paths Found: {}".format(len(bestwinner)))
    print("Best Path is: {}".format(shortestpath))
    
    
    return bestwinner

best = 100
main()
