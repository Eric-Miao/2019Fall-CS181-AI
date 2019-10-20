# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')

    clause_one = A | B
    clause_two = ~A % (~B | C)
    clause_three = logic.disjoin ((~A), (~B), C)

    instance = logic.conjoin(clause_one, clause_two, clause_three)

    return instance

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')

    clause_one = C % (B | D)
    clause_two = A >> (~B & ~D)
    clause_three = (~(B & ~C)) >> A
    clause_four = ~D >> C

    instance = logic.conjoin(clause_one, clause_two, clause_three, clause_four)

    return instance

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WumpusAlive_1 = logic.PropSymbolExpr("WumpusAlive", 1)
    WumpusAlive_0 = logic.PropSymbolExpr("WumpusAlive", 0)
    WumpusBorn_0 = logic.PropSymbolExpr("WumpusBorn", 0)
    WumpusKilled_0 = logic.PropSymbolExpr("WumpusKilled", 0)

    clause_one = WumpusAlive_1 % ((WumpusAlive_0 & (~WumpusKilled_0)) | \
                ((~WumpusAlive_0) & WumpusBorn_0) )
    clause_two = ~(WumpusAlive_0 & WumpusBorn_0)
    clause_three = WumpusBorn_0

    instance = logic.conjoin(clause_one, clause_two, clause_three)

    return instance

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    cnf = logic.to_cnf(sentence)
    model = logic.pycoSAT(cnf)
    return model

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    expression = literals[0]
    for i in range(len(literals)-1):
        expression = logic.disjoin(expression, literals[i+1])

    return expression

def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    expression = (~literals[0]) | (~literals[1])
    for i in range(len(literals)):
        j = i + 1
        while (j<len(literals)):
            if (j == 1):
                j += 1
                continue
            clause = (~literals[i]) | (~literals[j])
            expression = logic.conjoin(expression, clause)
            j += 1
    
    return expression
def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    n = len(literals)
    clause_brev = []
    clauses = []

    for i in range(2**n):
        bstr = str(bin(i))
        clause_brev.append(bstr[2:].zfill(n))

    for brev in clause_brev:
        clause = []
        if (bin(int(brev,2)).count('1') == 1):
            continue
        for i in range(n):
            if (brev[i] == '1'):
                clause.append(~literals[i])
            elif (brev[i] == '0'):
                clause.append(literals[i])
        
        temp=clause[0]
        for i in range(n-1):
            temp = logic.disjoin(temp,clause[i+1])
        clauses.append(temp)

    expression = clauses[0]
    for i in range(2**n-n-1):
        expression = logic.conjoin(expression,clauses[i+1])
    
    return expression
    
def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    ret = []
    path = []
    for key, value in model.items():
        if (value):
            temp = key.parseExpr(key)
            action = temp[0]
            time = temp[1]
            if action in actions:
                elem = (int(time), action)
                ret.append(elem)
    ret.sort(key = lambda x:x[0])
    for elem in ret:
        path.append(elem[1])

    return path


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous cposition at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    P_cur = logic.PropSymbolExpr(pacman_str, x, y, t)
    literals = []

    P_prev_north = logic.PropSymbolExpr(pacman_str, x, y+1, t-1)
    move_south = logic.PropSymbolExpr("South", t-1)
    is_wall_north = walls_grid[x][y+1]
    if(is_wall_north == False):
        clause_one = P_prev_north & move_south
        literals.append(clause_one)

    P_prev_south = logic.PropSymbolExpr(pacman_str, x, y-1, t-1)
    move_north = logic.PropSymbolExpr("North", t-1)
    is_wall_south = walls_grid[x][y-1]
    if(is_wall_south == False):
        clause_two = P_prev_south & move_north
        literals.append(clause_two)

    P_prev_east = logic.PropSymbolExpr(pacman_str, x+1, y, t-1)
    move_west = logic.PropSymbolExpr("West", t-1)
    is_wall_east = walls_grid[x+1][y]
    if(is_wall_east == False):
        clause_three = P_prev_east & move_west
        literals.append(clause_three)

    P_prev_west = logic.PropSymbolExpr(pacman_str, x-1, y, t-1)
    move_east = logic.PropSymbolExpr("East", t-1)
    is_wall_west = walls_grid[x-1][y]
    if(is_wall_west == False):   
        clause_four = P_prev_west & move_east
        literals.append(clause_four)

    if (len(literals)>0):
        expression = P_cur % atLeastOne(literals)
        return expression
    return True # Replace this with your expression

def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start = problem.startState
    goal = problem.goal
    
    def check_boundray(x,y):
        if (0 <= x <= width and 0 <= y <= height):
            return True
        return False
    
    '''
    1. Start with the start position.
    2. Each time explore four directions if 1) in boundary 2) not wall 3) not visited.
    3. add the explored node and the action to it into the list. Updating x,y,t.
    4. Pop from the list.
    5. If visited, pass; If not visited, add to visited.
    6. If is the goal, use the states and actions to states to find model.
    7. If model. return.
    8. Extract path from model.
    '''
    cur_path = []
    visited = []
    actions = ['East', 'West', 'North', 'South']
    x = start[0]
    y = start[1]
    t = 0
    '''
    states = [[state1], [state2], [state3], ...]
    state = [path_to_current_state, x, y, t]
    
    '''
    cur_path = logic.PropSymbolExpr(pacman_str, x, y, t)
    state = [cur_path, x, y, t] 
    states = [state]
    while (len(states) != 0):
        state = states.pop()
        x = state[1]
        y = state[2]
        t = state[3]
        if (x, y) in visited:
            continue
        visited.append((x, y))

        if (x == goal[0] and  y == goal[1]):
            model = findModel(state[0])
            break
        else :
            # explore east successor
            if not walls[x+1][y] and check_boundray(x+1, y):
                cur_path = state[0] & logic.PropSymbolExpr(pacman_str, x+1, y, t+1)&\
                    (logic.PropSymbolExpr(pacman_str, x+1, y, t+1) %\
                    (logic.PropSymbolExpr(pacman_str, x, y, t) &\
                     logic.PropSymbolExpr('East', t)))
                states.append([cur_path, x+1, y, t+1])

            # explore west successor
            if not walls[x-1][y] and check_boundray(x-1, y):
                cur_path = state[0] & logic.PropSymbolExpr(pacman_str, x-1, y, t+1)&\
                    (logic.PropSymbolExpr(pacman_str, x-1, y, t+1) %\
                    (logic.PropSymbolExpr(pacman_str, x, y, t) &\
                     logic.PropSymbolExpr('West', t)))
                states.append([cur_path, x-1, y, t+1])

            # explore north successor
            if not walls[x][y-1] and check_boundray(x, y+1):
                cur_path = state[0] & logic.PropSymbolExpr(pacman_str, x, y+1, t+1)&\
                    (logic.PropSymbolExpr(pacman_str, x, y+1, t+1) %\
                    (logic.PropSymbolExpr(pacman_str, x, y, t) &\
                     logic.PropSymbolExpr('North', t)))
                states.append([cur_path, x, y+1, t+1])

            # explore south successor
            if not walls[x][y-1] and check_boundray(x, y-1):
                cur_path = state[0] & logic.PropSymbolExpr(pacman_str, x, y-1, t+1)&\
                    (logic.PropSymbolExpr(pacman_str, x, y-1, t+1) %\
                    (logic.PropSymbolExpr(pacman_str, x, y, t) &\
                     logic.PropSymbolExpr('South', t)))
                states.append([cur_path, x, y-1, t+1])
    print('before return\n********************\n')
    print(model)
    return extractActionSequence(model, actions)


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    