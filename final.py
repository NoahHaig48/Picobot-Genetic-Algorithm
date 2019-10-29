#Picobot Final Project

#Noah Haig

import random

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5

class Program(object):
    """
    the class which writes and edits picobot programs
    """
    def __init__(self):
        """
        initializes the rule list for picobot
        """
        self.rules = {}
    
    def __repr__(self):
        """
        prints the list of rules in order 
        in a format that picobot can directly interpret
        """
        Keys = list( self.rules.keys() )   
        sortedKeys = sorted(Keys)
        s = ""
        for i in range(len(sortedKeys)):
            s += str(sortedKeys[i][0]) + " " + str(sortedKeys[i][1]) + " "+"->" +" "+ str(self.rules[sortedKeys[i]][0])+ " " + str(self.rules[sortedKeys[i]][1])
            s += "\n"    
        return s

    def randomize(self):
        """
        creates a random list of valid rules for picobot
        """
        L = ["xxxx","Nxxx","NExx","NxWx","xxxS","xExS","xxWS","xExx","xxWx"]
        for i in range(len(L)):
            for x in range(NUMSTATES):
                newstate = random.choice(range(NUMSTATES))
                movedir = random.choice(["N","E","W","S"])
                while movedir in L[i]:
                    movedir = random.choice(["N","E","W","S"])
                self.rules[(x,L[i])] = (movedir,newstate)
        
    def getMove(self,state,surroundings):
        """
        returns the next move based on the rules, state and surroundings
        """
        return self.rules[(state,surroundings)[0]]
    
    def mutate(self):
        """
        changes the move and new state for a random rule
        """
        L = ["xxxx","Nxxx","NExx","NxWx","xxxS","xExS","xxWS","xExx","xxWx"]
        y = random.choice(L)
        x = random.choice(range(NUMSTATES))
        newstate = random.choice(range(NUMSTATES))
        while newstate == x:
            newstate = random.choice(range(NUMSTATES))
        movedir = random.choice(["N","E","W","S"])
        while movedir in y:
            movedir = random.choice(["N","E","W","S"])
        self.rules[(x,y)] = (movedir,newstate)
    
    def crossover(self,other):
        """
        creates a new ruleset based on parent rulesets
        """
        x = Program()
        for i in self.rules:
            if i[0] in [0,1,2]:
                x.rules = dict(list(x.rules.items())+list({i:self.rules[i]}.items()))
        for i in other.rules:
            if i[0] in [3,4]:
                x.rules = dict(list(x.rules.items())+list({i:other.rules[i]}.items()))
        return x
    
    def __gt__(self, other):
            """Greater-than operator -- works randomly, but works!"""
            return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])
    
    def __eq__(self,other):
        """
        defines equality for the program class
        """
        L = ["xxxx","Nxxx","NExx","NxWx","xxxS","xExS","xxWS","xExx","xxWx"]
        for i in range(NUMSTATES):
            for x in L:
                if self.rules[(i,x)] != other.rules[(i,x)]:
                    return False
        return True
        
        
p = Program()
p.randomize()
d = Program()
d.randomize()

class World(object):
    """
    the class which creates the picobot map
    """
    def __init__(self, initial_row, initial_col, program):
        """
        creates the data for world
        """
        self.prow = initial_row
        self.pcol = initial_col
        self.state = 0
        self.prog = program
        self.room = [[" "]*WIDTH for row in range(HEIGHT)]
        for col in range(WIDTH):
              self.room[0][col] = "+"
              self.room[HEIGHT-1][col] = "+"
        for row in range(HEIGHT):
            self.room[row][0] = "+"
            self.room[row][WIDTH-1] = "+"

    def __repr__(self):
        """
        prints the picobot board
        """
        self.room[self.prow][self.pcol] = "P"
        s = ""
        for row in range(HEIGHT):
            for col in range(WIDTH):
                s += self.room[row][col]
            s += "\n"
        return s
    
    def getCurrentSurroundings(self):
        """
        returns the current surroundings of Picobot
        """
        s = ""
        if self.room[self.prow-1][self.pcol] != "+":
            s += "x"
        else:
            s += "N"
        if self.room[self.prow][self.pcol+1] != "+":
            s += "x"
        else:
            s += "E"
        if self.room[self.prow][self.pcol-1] != "+":
            s += "x"
        else:
            s += "W"
        if self.room[self.prow+1][self.pcol] != "+":
            s += "x"
        else:
            s += "S"
        
        return s
    
    def step(self):
        """
        runs picobot one step in the based on its rule set
        """
        rule = self.prog.rules[(self.state,self.getCurrentSurroundings())]
        self.state = rule[1]
        self.room[self.prow][self.pcol] = "o"
        if rule[0] == "N":
            self.prow -= 1
        if rule[0] == "E":
            self.pcol += 1
        if rule[0] == "W":
            self.pcol -= 1
        if rule[0] == "S":
            self.prow += 1
    
    def run(self,steps):
        """
        runs picobot for a specified number of steps based on the ruleset
        """
        for n in range(steps):
            self.step()
    
    def fractionVisitedCells(self):
        """
        computes the proportion of cells visited by picobot
        """
        count = 0
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.room[row][col] == ("o" or "P"):
                    count += 1
        return count / ((WIDTH-2)*(HEIGHT-2))


x = World(22,22,p)
y = World(23,23,p)


def population(n):
    """
    returns n picobot programs
    """
    L = []
    for i in range(n):
        q = Program()
        q.randomize()
        L += [q]
    return L

def evaluateFitness(program,trials,steps):
    """
    the average number of cells visited by a program in a certain steps in a certain number of trials
    """
    frac = 0
    for n in range(trials):
        x = random.choice(range(1,HEIGHT-1))
        y = random.choice(range(1,WIDTH-1))
        w = World(x,y,program)
        w.run(steps)
        frac += w.fractionVisitedCells()
    frac /= trials
    return frac

def GA(popsize,numgens):
    """
    runs the genetic algorithm for a specified population and a specfied number of generations
    """
    p = population(popsize)
    TRIALS = 20
    STEPS = 800
    MUT = 0.15
    PARENT = 0.10
    #best = p[0]
    print("Fitness is measured using", TRIALS ,"random trials and running for", STEPS ,"steps per trial.")
    print()
    for n in range(numgens):
        L = []
        for i in range(len(p)):
            L += [(evaluateFitness(p[i],TRIALS,STEPS),p[i])]
        best = max(L)[1]
        print("Generation", n)
        SL = sorted(L)
        #print(SL)
        fitL = []
        for i in range(len(L)):
            fitL += [L[i][0]]
        avg = sum(fitL)/popsize
        print("Average Fitness:", avg)
        print("Best Fitness:", max(fitL))
        print()
        progL = []
        for i in range(len(SL)):
            progL += [SL[i][1]]
        newL = progL[-1:-(int(popsize*PARENT)+2):-1]
        #xL = []
        while len(newL) < popsize:
            x = random.choice(range(int(popsize*PARENT)+1))
            y = random.choice(range(int(popsize*PARENT)+1))
            newL += [newL[x].crossover(newL[y])]
            mut = random.uniform(0,1)
            if mut < MUT:
                z = random.choice(range(len(newL[int(popsize*PARENT)+1:])))
                if newL[z] == best:
                    pass
                else:
                    newL[z].mutate()
        p = newL

    print("The best Picobot program is:")
    return best
        
    
       






