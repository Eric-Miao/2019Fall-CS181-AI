# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
"""
    "*** YOUR CODE HERE ***"
    from game import Directions
    if problem.isGoalState(problem.getStartState()): return Directions.STOP
    # if the start state is the goal state, return.

    path = []  # for the result to be returned, which stores the list of actions to get to the goal
    closed = []  # for the nodes visited
    fringe = util.Stack()  # for the nodes on the fringe to be visited and use stack to implement LIFO
    curState = problem.getStartState()  # to mark a temporary state.
    parent_map = {}  # a map to find the way back to start point, child key parent value

    def path_finding(goal):  # path finding using the parent map to give out a ret path
        curState = goal
        ret = []
        while not curState == problem.getStartState():
            ret.append(parent_map[curState][1])
            curState = parent_map[curState][0]
        return ret

    fringe.push(curState)
    while not fringe.isEmpty():
        curState = fringe.pop()
        closed.append(curState)
        # if current successor is the goal state, return
        if problem.isGoalState(curState):
            path = path_finding(curState)
            path.reverse()
            return path

        successors = problem.getSuccessors(curState)

        for succ in successors:
            # check for no double visit
            visit_flag = 0  # a flag to indicate if a new state has been visited.
            for state in closed:
                if state == succ[0]:
                    visit_flag = 1
            # if visited, do nothing and continue the loop
            if visit_flag == 1:
                continue
            else:
                # if the successor is not goal nor visited nodes, add to fringe
                fringe.push(succ[0])
                parent_map[succ[0]] = (curState, succ[1])
    '''
            for i in range(len(successors)):
                # check for no double visit
                visit_flag = 0  # a flag to indicate if a new state has been visited.
                for state in closed:
                    if state == successors[i][0]:
                        visit_flag = 1
                # delete the visited ones and index--
                if visit_flag == 1:
                    del(successors[i])
                    i-=1
                else:
                    # if current successor is the goal state, return
                    if problem.isGoalState(successors[i][0]):
                        path = path_finding(successors[i][0])
                        return path.reverse()
                    # if the successor is not goal nor visited nodes, add to fringe
                    fringe.push(successors[i][0])
                    parent_map[successors[i][0]] = (curState, successors[i][1])

    "util.raiseNotDefined()"
    '''


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    if problem.isGoalState(problem.getStartState()): return Directions.STOP
    # if the start state is the goal state, return.

    path = []  # for the result to be returned, which stores the list of actions to get to the goal
    closed = []  # for the nodes visited
    fringe = util.Queue()  # for the nodes on the fringe to be visited and use queue to implement LIFO
    curState = problem.getStartState()  # to mark a temporary state.
    parent_map = {}  # a map to find the way back to start point, child key parent value

    def path_finding(goal):  # path finding using the parent map to give out a ret path
        curState = goal
        ret = []
        while not curState == problem.getStartState():
            ret.append(parent_map[curState][1])
            curState = parent_map[curState][0]
        return ret

    fringe.push(curState)
    closed.append(curState)
    while not fringe.isEmpty():
        curState = fringe.pop()
        # if current successor is the goal state, return
        if problem.isGoalState(curState):
            path = path_finding(curState)
            path.reverse()
            return path

        successors = problem.getSuccessors(curState)
        for succ in successors:
            # check for no double visit
            visit_flag = 0  # a flag to indicate if a new state has been visited.
            for state in closed:
                if state == succ[0]:
                    visit_flag = 1
            if (visit_flag == 0):
                closed.append(succ[0])
                fringe.push(succ[0])
                parent_map[succ[0]] = (curState, succ[1])
    # util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    path = []  # for the result to be returned, which stores the list of actions to get to the goal
    closed = []  # for the nodes visited
    fringe = util.PriorityQueue()  # for the nodes on the fringe to be visited and use queue to implement LIFO
    curState = problem.getStartState()  # to mark a temporary state.
    parent_map = {}

    # a map to find the way back to start point, child key parent value.
    # {"child node":(father node, action, priority)}

    def path_finding(goal):  # path finding using the parent map to give out a ret path
        curState = goal
        ret = []
        while not curState == problem.getStartState():
            ret.append(parent_map[curState][1])
            curState = parent_map[curState][0]
        return ret

    # fringe is now a priority queue, accept a priority parameter
    # the start node has a priority of 0
    fringe.push(curState, 0)
    while not fringe.isEmpty():
        curState = fringe.pop()

        # if current successor is the goal state, return
        if problem.isGoalState(curState):
            path = path_finding(curState)
            path.reverse()
            return path

        # check if poped a visited node, if not add to visited
        visit_flag = 0
        for state in closed:
            if state == curState:
                visit_flag = 1
        if visit_flag == 1:
            continue
        else:
            closed.append(curState)

        # start to explore neighbor.
        successors = problem.getSuccessors(curState)
        for succ in successors:
            # check for no double visit
            visit_flag = 0  # a flag to indicate if a new state has been visited.
            for state in closed:
                if state == succ[0]:
                    visit_flag = 1
            if visit_flag == 0:
                if curState == problem.getStartState():
                    priority = 0 + succ[2]
                else:
                    priority = parent_map[curState][2] + succ[2]
                fringe.push(succ[0], priority)

                if (not parent_map.has_key(succ[0])):
                    # before new node pushed into pqueue, compute the priority function
                    # option1: like path finding, everytime calculate
                    # option2: store the cost of every node.
                    # accept option2, add one parameter in the parent_map dict
                    parent_map[succ[0]] = (curState, succ[1], priority)
                else:
                    # if find a closer path of a node, update the parent path.
                    if (succ[0] != problem.getStartState()):
                        priority = parent_map[curState][2] + succ[2]
                        pre_cost = parent_map[succ[0]][2]
                        if priority < pre_cost:
                            parent_map[succ[0]] = (curState, succ[1], priority)
    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    path = []  # for the result to be returned, which stores the list of actions to get to the goal
    closed = []  # for the nodes visited
    fringe = util.PriorityQueue()  # for the nodes on the fringe to be visited and use queue to implement LIFO
    curState = problem.getStartState()  # to mark a temporary state.
    parent_map = {}
    fv = 0
    gv = 0

    # a map to find the way back to start point, child key parent value.
    # {"child node":(father node, action, priority)}

    def path_finding(goal):  # path finding using the parent map to give out a ret path
        curState = goal
        ret = []
        while not curState == problem.getStartState():
            ret.append(parent_map[curState][1])
            curState = parent_map[curState][0]
        return ret

    # fringe is now a priority queue, accept a priority parameter
    # the start node has a priority of 0
    fv = gv + heuristic(curState, problem)
    fringe.push(curState, fv)
    while not fringe.isEmpty():
        curState = fringe.pop()

        # if current successor is the goal state, return
        if problem.isGoalState(curState):
            path = path_finding(curState)
            path.reverse()
            return path

        # check if poped a visited node, if not add to visited
        visit_flag = 0
        for state in closed:
            if state == curState:
                visit_flag = 1
        if visit_flag == 1:
            continue
        else:
            closed.append(curState)

        # start to explore neighbor.
        successors = problem.getSuccessors(curState)
        for succ in successors:
            # check for no double visit
            visit_flag = 0  # a flag to indicate if a new state has been visited.
            for state in closed:
                if state == succ[0]:
                    visit_flag = 1
                    break
            if visit_flag == 0:
                if curState == problem.getStartState():
                    gv = 0 + succ[2]
                else:
                    gv = parent_map[curState][2] + succ[2]
                fv = gv + heuristic(succ[0], problem)
                fringe.push(succ[0], fv)

                if not parent_map.has_key(succ[0]):
                    # a node never explored before
                    parent_map[succ[0]] = (curState, succ[1], gv, fv)
                elif succ[0] != problem.getStartState():
                    # if find a closer path of a pre-explored node, update the parent path.
                    gv = parent_map[curState][2] + succ[2]
                    fv = gv + heuristic(succ[0], problem)
                    pre_fv = parent_map[succ[0]][3]
                    if fv < pre_fv:
                        parent_map[succ[0]] = (curState, succ[1], gv, fv)

# util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
