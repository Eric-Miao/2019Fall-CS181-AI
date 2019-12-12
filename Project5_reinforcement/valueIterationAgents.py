# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp
import util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        """ 
        loop through iteration times. each time 
        compute the value of all state based on prev-loop
        update the self.values after each loop.
        Inside each loop, get the q value of all possible actions
        and obtain the argMax of the q values of a certain state
        and take it as the new value of this state.

        NOTE: HERE, must update the states per big loop, that is 
        cannot update self.values as u go, must use a new util.Counter
        to take down the certain loop and then copy the new counter to 
        the old one to overwrite. 
        This is because in side the big loop, obtaining the correct q 
        value depends on the right self.values, which shall not be change 
        when updates are performing on all states as they depend on each
        other and should always maintain the original version, only modified
        after update is done once.   
        """
        cnt = self.iterations
        while(cnt > 0):
            tempvalue = util.Counter()
            for state in self.mdp.getStates():
                qValue = util.Counter()
                for action in self.mdp.getPossibleActions(state):
                    qValue[action] = self.getQValue(state, action)
                qargMax = qValue.argMax()
                tempvalue[state] = qValue[qargMax]
            self.values = tempvalue
            cnt -= 1

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qtemp = util.Counter()
        for (nextState, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
            qtemp[action] += prob * \
                (self.mdp.getReward(state, action, nextState) +
                 self.discount*self.getValue(nextState))
        return qtemp.totalCount()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        qtemp = util.Counter()
        for action in self.mdp.getPossibleActions(state):
            qtemp[action] += self.getQValue(state, action)
        return qtemp.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        cnt = 0
        states = self.mdp.getStates()
        while(cnt < self.iterations):

            state = states[(cnt % len(states))]
            if(self.mdp.isTerminal(state)):
                cnt += 1
                continue

            qValue = util.Counter()
            for action in self.mdp.getPossibleActions(state):
                qValue[action] = self.getQValue(state, action)
            qargMax = qValue.argMax()
            self.values[state] = qValue[qargMax]
            # self.values = tempvalue
            cnt += 1

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        """ 
        Compute predecessors of all states.        
        """
        predecessors = {}
        for state in self.mdp.getStates():
            if (self.mdp.isTerminal(state)):
                continue
            for action in self.mdp.getPossibleActions(state):
                for (nextState, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
                    if nextState in predecessors:
                        predecessors[nextState].add(state)
                    else:
                        predecessors[nextState] = {state}

        """  
        Initialize an empty priority queue.
        """
        PriorityQueue = util.PriorityQueue()

        """  
        For each non-terminal state s, do:
        Find the absolute value of the difference between the current value of s in self.values 
        and the highest Q-value across all possible actions from s (this represents what the value should be); 
        call this number diff. Do NOT update self.values[s] in this step.
        Push s into the priority queue with priority -diff (note that this is negative). 
        We use a negative because the priority queue is a min heap, but we want to prioritize updating states that have a higher error.
        """
        for state in self.mdp.getStates():
            if (self.mdp.isTerminal(state)):
                continue
            qtemp = util.Counter()
            cur_value = self.values[state]
            for action in self.mdp.getPossibleActions(state):
                qtemp[action] = self.getQValue(state, action)
            qargMax = qtemp.argMax()
            priority = -abs(cur_value - qtemp[qargMax])
            PriorityQueue.update(state, priority)
            
        """           
        For iteration in 0, 1, 2, ..., self.iterations - 1, do:

            If the priority queue is empty, then terminate.
            Pop a state s off the priority queue.
            Update s's value (if it is not a terminal state) in self.values.

            For each predecessor p of s, do:
                Find the absolute value of the difference between the current value 
            of p in self.values and the highest Q-value across all possible 
            actions from p (this represents what the value should be); 
            call this number diff. Do NOT update self.values[p] in this step.
        
                If diff > theta, push p into the priority queue with priority -diff 
            (note that this is negative), as long as it does not already exist 
            in the priority queue with equal or lower priority. As before, we use 
            a negative because the priority queue is a min heap, but we want to 
            prioritize updating states that have a higher error.
        """
        cnt = 0
        while (cnt < self.iterations and not PriorityQueue.isEmpty()):
            state = PriorityQueue.pop()
            if (self.mdp.isTerminal(state)):
                continue
            qtemp_one = util.Counter()
            for action in self.mdp.getPossibleActions(state):
                qtemp_one[action] = self.getQValue(state, action)
            qargMax = qtemp_one.argMax()
            self.values[state] = qtemp_one[qargMax]
            
            for predecessor in predecessors[state]:
                if (self.mdp.isTerminal(predecessor)):
                    continue
                qtemp_two = util.Counter()
                print(predecessor)
                for action in self.mdp.getPossibleActions(predecessor):
                    qtemp_two[action] = self.getQValue(predecessor, action)
                qargMax = qtemp_two.argMax()
                diff = abs(qtemp_two[qargMax] - self.values[predecessor])

                if (diff > self.theta):
                    """ Inside the PQ.update() the condition judgements have already been done."""
                    PriorityQueue.update(predecessor, -diff)
            cnt += 1

