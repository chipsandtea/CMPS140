# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    # Dictionary of (state, action) pairs, init at 0.
    self.qvalues = util.Counter()



  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description:
    Returns the self.qvalues[(state, action)] value.
    B/C self.qvalues is a counter, unseen (state, action) pairs init to 0.
    """
    """ YOUR CODE HERE """
    return self.qvalues[(state, action)]
    """ END CODE """



  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    """Description:
    1. Get legal actions.
    2. Look up Q-Values of (state, action) pairs.
    3. Return the maxVal.
    
    NOTE: Init maxVal to 0.0 so if all known Q values are negative, might be better to explore!
    """
    """ YOUR CODE HERE """
    legalActions = self.getLegalActions(state)
    if len(legalActions) == 0:
      return 0.0
    maxVal = float('-inf')
    for action in legalActions:
      maxVal = max(maxVal, self.getQValue(state, action))
    return maxVal
    """ END CODE """

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    """Description:
    1. Get legal actions.
    2. Look up Q-Values of (state, action) pairs.
    3. If maxVal ties w/ new Q-value, break tie randomly.
    4. Return bestAction.
    """
    """ YOUR CODE HERE """
    legalActions = self.getLegalActions(state)
    if len(legalActions) == 0:
      return None
    maxVal = float('-inf')
    bestAction = None
    for action in legalActions:
      tempVal = self.getQValue(state, action)
      if maxVal == tempVal:
        if util.flipCoin(0.5):
          maxVal = tempVal
          bestAction = action
        else:
          continue
      else:
        if maxVal < tempVal:
          maxVal = tempVal
          bestAction = action
        else:
          continue
    return bestAction
    """ END CODE """

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    action = None

    """Description:
    1. Flip a coin w/ p = self.epsilon.
    2. If true, then randomly return action from legalActions.
    3. Else, lookup and return policy action w/ self.getPolicy(state).
    """
    """ YOUR CODE HERE """
    legalActions = self.getLegalActions(state)
    if len(legalActions) == 0:
      return action
    if util.flipCoin(self.epsilon):
      return random.choice(legalActions)
    else:
      return self.getPolicy(state)
    """ END CODE """

    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    """Description:
    Given an instance (s, a, s', r), perform the Q update.
    EQN: Q(s,a) = (1-alpha) * Q(s,a) + (alpha) * [r + (lambda * max(Q(s', a')))]
    """
    """ YOUR CODE HERE """
    learningRate = self.alpha
    discount = self.discountRate

    prevQ = (1 - learningRate) * self.getQValue(state, action)
    nextQ = learningRate * (reward + (discount * self.getValue(nextState)))
    self.qvalues[(state, action)] = prevQ + nextQ
    """ END CODE """

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    """Description:
    [Enter a description of what you did here.]
    """
    """ YOUR CODE HERE """
    util.raiseNotDefined()
    """ END CODE """

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
    [Enter a description of what you did here.]
    """
    """ YOUR CODE HERE """
    util.raiseNotDefined()
    """ END CODE """

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      util.raiseNotDefined()
