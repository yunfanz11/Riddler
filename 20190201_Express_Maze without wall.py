# https://fivethirtyeight.com/features/can-you-escape-a-maze-without-walls/
# Bad news: the enemies of Riddler Nation have forced you into a maze. And this maze is weird. The rules are as follows.
#
# You move between boxes in a grid: up, down, left or right, but never diagonally.
# Your goal is to arrive in the finish square, designated here by a “☺.”
# Your movement is dictated by the symbol inside the square you have just moved to, and each direction is relative
# to where you’d be facing if you were physically walking the maze. “S” means you continue straight, “R” means you turn
# right, “L” means you turn left, “U” means you make a U-turn, and “?” gives you the option of any of those four directions.
# An “X” ends your game in failure — think hot lava. (But hey, you can always start over!)
# If you are forced to exit the maze’s grid, you lose — more hot lava.
# Your maze is below. You may enter the maze anywhere along the perimeter, giving you 32 options. Some of these,
# however, immediately fail. If you enter at a “U” on the top of the maze, for example, you must immediately
#  U-turn out of the maze, so you lose.
#
# Can you reach the smiley face? If so, how many moves does it take?

class Location:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return ("P({},{},{})".format(self.x, self.y, self.value))


##Create GameBoard
Row1 = "LUUAULXL"
Row2 = "RLRLUGUU"
Row3 = "SLRLULXR"
Row4 = "URARSLAR"
Row5 = "RUURRRSL"
Row6 = "SASLSSLR"
Row7 = "RLRARLAL"
Row8 = "LRSRSLRL"

length = 8
GameBoard = [Row1,Row2,Row3,Row4,Row5,Row6,Row7,Row8]


print ("Game board generated :")
print (Row1)
print (Row2)
print (Row3)
print (Row4)
print (Row5)
print (Row6)
print (Row7)
print (Row8)
print ("'G' is the goal square")
print ("")

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

def entrySets(side):
    points = entryPoints(side)
    sol = []
    for i in points:
        x = i[0]
        y = i[1]
        if x == 1 and y == 1:
            a = (i,(0,1))
            b = (i,(1,0))
            sol.append(a)
            sol.append(b)
        elif x == side and y == side:
            a = (i,(side,side+1))
            b = (i,(side+1,side))
            sol.append(a)
            sol.append(b)

        elif x == 1:
            a = (i,(0,y))
            sol.append(a)

        elif y == 1:
            a = (i,(x,0))
            sol.append(a)

        elif x == side:
            a = (i,(side+1,y))
            sol.append(a)

        elif y == side:
            a = (i,(x,side+1))
            sol.append(a)

    return sol

## possible moves

def posMoves (thispath):
    thispoint = thispath[0]
    lastpoint = thispath[1]
    x0 = lastpoint[0]
    y0 = lastpoint[1]
    x1 = thispoint[0]
    y1 = thispoint[1]
    value = GameBoard[x1-1][y1-1]
    
    a = (x1-1,y1) #up
    b = (x1+1,y1) #down
    c = (x1,y1-1) #left
    d = (x1,y1+1) #right 

    frUp = False
    frDown = False
    frLeft = False
    frRight = False

    if x0 > x1:
        frDown = True
    elif x1 > x0:
        frUp = True
    elif y0 > y1:
        frRight = True
    elif y1 > y0:
        frLeft = True
    
    if value == "L":
        if frUp:
            sol = [d]
        elif frDown:
            sol = [c]
        elif frLeft:
            sol = [a]
        elif frRight:
            sol = [b]

    elif value == "R":
        if frUp:
            sol = [c]
        elif frDown:
            sol = [d]
        elif frLeft:
            sol = [b]
        elif frRight:
            sol = [a]       

    elif value == "S":
        if frUp:
            sol = [b]
        elif frDown:
            sol = [a]
        elif frLeft:
            sol = [d]
        elif frRight:
            sol = [c]

    elif value == "U":
        if frUp:
            sol = [a]
        elif frDown:
            sol = [b]
        elif frLeft:
            sol = [c]
        elif frRight:
            sol = [d]
            
    elif value == "X" or value == "G":
        sol = []
    else:
        sol = [a,b,c,d]

    #remove ilegal()
    for i in sol:
        if i[0] < 1 or i[1] < 1:
            sol.remove(i)
        elif i[0] > length or i[1] > length:
            sol.remove(i)
            
    return sol
    

def findPath(thispath, score, path, memory): #return a collection of tried paths and results
    global best
    thispoint = thispath[0]
    lastpoint = thispath[1]
    x1 = thispoint[0]
    y1 = thispoint[1]
    value = GameBoard[x1-1][y1-1]
    moves = posMoves(thispath)
    newpath = list(path)
    newpath.append(thispath)
    newscore = score + 1

    if thispath in path: #loop detection
        sol = ("L", 0, "Loop")
        memory.append(sol)
    
    elif value == "G":
        sol = ("W", newscore, newpath)
        best = newscore
        memory.append(sol)
        
    elif value == "X" or len(moves)==0:
        sol = ("L", 0, "No Moves")
        memory.append(sol)

    elif newscore > best:
        sol = ("L", 0, "Not Best")
        memory.append(sol)

    else:
        for i in moves:
            nextpath = (i,thispoint)
            findPath(nextpath, newscore, newpath, memory)
                
    return memory


def main():
    total = 0
    sol = []
    winner = []
    global length
    start = entrySets(length)
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
            
    print("Short path has {} moves".format(bestscore))
    print("Number of shortest path found: {}".format(len(bestwinner)))
    print("Best Path is: {}".format(shortestpath))

    return shortestpath

best = 100
main()

        
    
