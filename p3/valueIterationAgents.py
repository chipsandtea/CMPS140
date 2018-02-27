# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0

    """Description:
    V_k+1(s) := max_a sum_(s') T(s,a,s')[R(s,a,s') + gV_k(s')]
    """
    """ YOUR CODE HERE """
    # We want to start at V_0(s) and work our way up.
    # Currently, all values default to 0 for every state.
    allStates = mdp.getStates()
    for _ in range(iters):
      tempValues = self.values.copy()
      for state in allStates:

        if self.mdp.isTerminal(state):
          continue
        actions = self.mdp.getPossibleActions(state)
        maxVal = max(self.getQValue(state, action) for action in actions)
        tempValues[state] = maxVal
      self.values = tempValues.copy()
    """ END CODE """

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    """Description:
    V_k+1(s) := max_a sum_(s') T(s,a,s')[R(s,a,s') + gV_k(s')]
    """
    """ YOUR CODE HERE """
    return self.values[state]
    """ END CODE """

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    """Description:
    Q(s,a) = expected utility starting out having taken an action from state s and acting optimally.
    To compute, we need:
      - Possible next states weighted by their probability of occuring.
      - Reward for going from R(s,a,s')
      - Discount (mdp.discountRate)
      - k-1's discounted value for s': V(s')
    """
    """ YOUR CODE HERE """
    # Get list of successor states and their probabilities as (state, probability)
    successorStates = self.mdp.getTransitionStatesAndProbs(state, action)
    # For each successor, compute its reward and add discounted value of previous s'.
    totalVal = 0
    for successor, probability in successorStates:
      reward = self.mdp.getReward(state, action, successor)
      futureVal = self.discountRate * self.getValue(successor)
      totalVal += probability * (reward + futureVal)
    return totalVal
    """ END CODE """

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """

    """Description:
    Given a state, loop through possible actions one can make from this state.
    Return the action with the highest Q-Value.
    """
    """ YOUR CODE HERE """
    if self.mdp.isTerminal(state):
      return None
    possibleActions = self.mdp.getPossibleActions(state)
    maxVal = float('-inf')
    bestAction = None
    for action in possibleActions:
      tempVal = self.getQValue(state, action)
      if tempVal > maxVal:
        if tempVal > maxVal:
          maxVal = tempVal
          bestAction = action
    return bestAction
    """ END CODE """

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
