# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.curdepth = 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state

        util.raiseNotDefined()
        """
        "*** YOUR CODE HERE ***"
        self.curdepth = 0
        curdepth = 1
        curagent = 0

        # Collect legal moves
        legalMoves = gameState.getLegalActions(curagent)
        score = []
        legalSucc = [gameState.generateSuccessor(curagent, action) for action in legalMoves]
        # Choose one of the best successors
        scores = [self.value(gameState, curagent, curdepth) for gameState in legalSucc]

        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    # value function && min function && max function, written from the ppt psuedo code
    def maxvalue(self, gameState, curagent, curdepth):
        # Collect legal moves
        legalMoves = gameState.getLegalActions(curagent)

        legalSucc = [gameState.generateSuccessor(curagent, action) for action in legalMoves]
        # Choose one of the best successors
        scores = [self.value(gameState, curagent, curdepth) for gameState in legalSucc]
        bestScore = max(scores)

        return bestScore

    def minvalue(self, gameState, curagent, curdepth):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(curagent)
        legalSucc = [gameState.generateSuccessor(curagent, action) for action in legalMoves]
        # Choose one of the best successors
        scores = [self.value(gameState, curagent, curdepth) for gameState in legalSucc]
        worstScore = min(scores)

        return worstScore

    def value(self, gameState, curagent, curdepth):
        """
        here i came up with two sets of logic
        #1 if curagent == agentnum --> if curdepth == depth
        #1 if curagent == depth --> if curagent == agentnum  --> if curagent == 0
        """

        # if the successor is an end, then return the value
        if (gameState.isWin() or gameState.isLose()):
            score = self.evaluationFunction(gameState)
            return score

        agentnum = gameState.getNumAgents()
        temp = agentnum - 1
        if curagent == temp:
            if curdepth == self.depth:
                score = self.evaluationFunction(gameState)
                return score
            else:
                curdepth += 1
                curagent = 0
                score = self.maxvalue(gameState, curagent, curdepth)
                return score
        else:
            curagent += 1
            score = self.minvalue(gameState, curagent, curdepth)
            return score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        """
        "*** YOUR CODE HERE ***"
        self.curdepth = 0
        curdepth = 1
        curagent = 0
        bestScore = -99999
        alpha = -99999
        beta = 99999
        scores = []
        # Collect legal moves
        legalMoves = gameState.getLegalActions(curagent)
        # Choose one of the best successors
        for action in legalMoves:
            succ = gameState.generateSuccessor(curagent, action)
            newScore = self.value(succ, curagent, curdepth, alpha, beta)
            scores.append(newScore)
            bestScore = max(bestScore, newScore)
            alpha = max(alpha, bestScore)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    # value function && min function && max function, written from the ppt psuedo code
    def maxvalue(self, gameState, curagent, curdepth, alpha, beta):
        # initialize
        bestScore = -99999
        # Collect legal moves
        legalMoves = gameState.getLegalActions(curagent)
        # Choose one of the best successors
        for action in legalMoves:
            succ = gameState.generateSuccessor(curagent, action)
            newScore = self.value(succ, curagent, curdepth, alpha, beta)
            if newScore > bestScore:
                bestScore = newScore
            if bestScore > beta:
                return bestScore
            alpha = max(alpha, bestScore)
        return bestScore

    def minvalue(self, gameState, curagent, curdepth, alpha, beta):
        # initialize
        worstScore = 99999

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(curagent)
        # Choose one of the best successors
        for action in legalMoves:
            succ = gameState.generateSuccessor(curagent, action)
            newScore = self.value(succ, curagent, curdepth, alpha, beta)
            if newScore < worstScore:
                worstScore = newScore
            if worstScore < alpha:
                return worstScore
            beta = min(beta, worstScore)
        return worstScore

    def value(self, gameState, curagent, curdepth, alpha, beta):
        """
        here i came up with two sets of logic
        #1 if curagent == agentnum --> if curdepth == depth
        #1 if curagent == depth --> if curagent == agentnum  --> if curagent == 0
        """

        # if the successor is an end, then return the value
        if (gameState.isWin() or gameState.isLose()):
            score = self.evaluationFunction(gameState)
            return score

        agentnum = gameState.getNumAgents()
        temp = agentnum - 1
        if curagent == temp:
            if curdepth == self.depth:
                score = self.evaluationFunction(gameState)
                return score
            else:
                curdepth += 1
                curagent = 0
                score = self.maxvalue(gameState, curagent, curdepth, alpha, beta)
                return score
        else:
            curagent += 1
            score = self.minvalue(gameState, curagent, curdepth, alpha, beta)
            return score

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """
    def getAction(self, gameState):
        self.curdepth = 0
        curdepth = 1
        curagent = 0

        # Collect legal moves
        legalMoves = gameState.getLegalActions(curagent)
        score = []
        legalSucc = [gameState.generateSuccessor(curagent, action) for action in legalMoves]
        # Choose one of the best successors
        scores = [self.value(gameState, curagent, curdepth) for gameState in legalSucc]

        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    # value function && min function && max function, written from the ppt psuedo code
    def maxvalue(self, gameState, curagent, curdepth):
        # Collect legal moves
        legalMoves = gameState.getLegalActions(curagent)

        legalSucc = [gameState.generateSuccessor(curagent, action) for action in legalMoves]
        # Choose one of the best successors
        scores = [self.value(gameState, curagent, curdepth) for gameState in legalSucc]
        bestScore = max(scores)

        return bestScore

    def expvalue(self, gameState, curagent, curdepth):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(curagent)
        legalSucc = [gameState.generateSuccessor(curagent, action) for action in legalMoves]
        # Choose one of the best successors
        scores = [self.value(gameState, curagent, curdepth) for gameState in legalSucc]
        expScore = self.average(scores)

        return expScore

    def value(self, gameState, curagent, curdepth):
        """
        here i came up with two sets of logic
        #1 if curagent == agentnum --> if curdepth == depth
        #1 if curagent == depth --> if curagent == agentnum  --> if curagent == 0
        """

        # if the successor is an end, then return the value
        if (gameState.isWin() or gameState.isLose()):
            score = self.evaluationFunction(gameState)
            return score

        agentnum = gameState.getNumAgents()
        temp = agentnum - 1
        if curagent == temp:
            if curdepth == self.depth:
                score = self.evaluationFunction(gameState)
                return score
            else:
                curdepth += 1
                curagent = 0
                score = self.maxvalue(gameState, curagent, curdepth)
                return score
        else:
            curagent += 1
            score = self.expvalue(gameState, curagent, curdepth)
            return score

    def average(self, scores):
        cnt = 0
        sum = 0
        for score in scores:
            sum += score
            cnt += 1
        ret = sum/cnt
        return ret

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION:
    There are a couple of factors to consider
    ( "+" for positive to increase, "-" for negative factors to decrease)
    1. Current Scores                       +
    2. Current Food Num                     +
    3. Current Capsule Num                  +
    4. Current Capsule Distance             -
    5. Current Ghost Distance               +
    6. Current Eatable Ghosts Distance      -
    """
    "*** YOUR CODE HERE ***"
    # holds the return value
    ret = 0

    ghost_num = currentGameState.getNumAgents() - 1
    pacman_pos = currentGameState.getPacmanPosition()

    current_score = currentGameState.getScore()

    food_num = currentGameState.getNumFood()

    capsule_pos_list = currentGameState.getCapsules()
    capsule_dist_list = [manhattanDistance(capsule, pacman_pos) for capsule in capsule_pos_list]
    capsule_num = len(capsule_pos_list)

    ghosts_pos_list = currentGameState.getGhostPositions()
    ghost_dist_list = [manhattanDistance(ghost, pacman_pos) for ghost in ghosts_pos_list]
    ghosts_states = currentGameState.getGhostStates()
    # ghostState.scaredTimer can indicate if a ghost is eatable if return value > 0
    ghosts_scared = [ghost.scaredTimer for ghost in ghosts_states]

    # now construct a ghost score, taking ghost position and eatable ghosts into consideration.
    ghost_score = 0
    for i in range(ghost_num):
        temp_score = 0
        if ghosts_scared[i] > 0:
            temp_score = - ghost_dist_list[i]
        if ghosts_scared[i] < 0:
            temp_score = ghost_dist_list[i]
        ghost_score += temp_score

    # construct other scores
    capsule_score = 50 * (5-capsule_num)
    food_score = 100 - food_num

    ret = 0.7 * current_score + 0.2 * capsule_score + 0.0 * food_score + 0.1 * ghost_score
    return ret

# Abbreviation
better = betterEvaluationFunction
