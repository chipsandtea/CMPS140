# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from distanceCalculator import Distancer

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    ''' 
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    '''
    CaptureAgent.registerInitialState(self, gameState)
    self.myTeam = self.getTeam(gameState)
    if self.myTeam[0] == self.index:
      self.offense = True
    else:
      self.offense = False
    self.opponents = self.getOpponents(gameState)
    self.distCalc = Distancer(gameState.data.layout)
    self.distCalc.getMazeDistances()
    self.prevPos = gameState.getAgentPosition(self.index)
    self.lastEaten = None


    ''' 
    Your initialization code goes here, if you need any.
    '''
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)
    #print(values)
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def evaluate(self, currentGameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    if self.offense:
      features = self.getOffenseFeatures(currentGameState, action)
      weights = self.getOffenseWeights(currentGameState, action)
    else:
      features = self.getDefenseFeatures(currentGameState, action)
      weights = self.getDefenseWeights(currentGameState, action)
    '''
    if self.index == 1:
      print(features)
      print(features * weights)
      print('---')
    '''
    return features * weights
  
  def getDefenseFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
    
    eatenFood = set(tuple(self.getFoodYouAreDefending(gameState).asList())) - set(tuple(self.getFoodYouAreDefending(successor).asList()))
    if eatenFood:
      minEatenDist = float('inf')
      minLastEaten = None
      for eatenCoord in eatenFood:
        tempMinEatenDist = self.getMazeDistance(eatenCoord, myPos)
        if tempMinEatenDist < minEatenDist:
          minEatenDist = tempMinEatenDist
          minLastEaten = eatenCoord
      self.lastEaten = minLastEaten
      features['distanceLostFood'] = minEatenDist
    else:
      if self.lastEaten:
        features['distanceLostFood'] = self.getMazeDistance(self.lastEaten, myPos)
      else:
        pass


    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features
  
  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != util.nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def getDefenseWeights(self, gameState, action):
    return {'numInvaders': -100, 'onDefense': 100, 'invaderDistance': -300, 'stop': -100, 'reverse': -0.5, 'distanceLostFood': -200}
  
  def getOffenseFeatures(self, currentGameState, action):
    features = util.Counter()
    successor = currentGameState.generateSuccessor(self.index, action)
    features['successorScore'] = self.getScore(successor)
    myPos = successor.getAgentState(self.index).getPosition()

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      
    features['distanceToFood'] = minDistance

    scaryGhostList = []
    noisyDists = successor.getAgentDistances()
    for opp_idx in self.getOpponents(currentGameState):
      oppAgent = successor.getAgentState(opp_idx)
      if oppAgent.getPosition() != None:
        if not oppAgent.isPacman and oppAgent.scaredTimer == 0:
          scaryGhostList.append(self.distCalc.getDistance(myPos, oppAgent.getPosition()))
      else:
        if not oppAgent.isPacman and oppAgent.scaredTimer == 0:
          scaryGhostList.append(noisyDists[opp_idx])
    
    if scaryGhostList:
      minGhostDist = min(scaryGhostList)
    else:
      minGhostDist = 0

    features['distanceToGhost'] = minGhostDist
    return features

  def getOffenseWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1, 'distanceToGhost': 3, 'distanceToScaredGhost': -2}


  def chooseAction2(self, gameState):
    """
    Picks among actions randomly.
    """
    maxVal = float('-inf')
    bestAction = Directions.STOP
    legalActions = gameState.getLegalActions(self.index)
    closestGhost = float('-inf')
    closestFood = float('-inf')
    myState = gameState.getAgentState(self.index)

    for action in legalActions:
      if action == Directions.STOP:
        continue
      succState = gameState.generateSuccessor(self.index, action)
      tempVal, ghostDist, foodDist = self.evaluationFunction(succState)
      if self.index == 1:
        print(ghostDist, foodDist, tempVal)
      if tempVal > maxVal:
        maxVal = tempVal
        bestAction = action
      if ghostDist > closestGhost:
        closestGhost = ghostDist
      if foodDist > closestFood:
        closestFood = foodDist
    if self.index == 1:
      print(closestGhost, closestFood, maxVal)
      print(bestAction)
      print('=====')
    self.prevPos = myState.getPosition()
    return bestAction
  
  def evaluationFunction(self, currentGameState):
    if currentGameState.isOver():
      return float('inf')
    myState = currentGameState.getAgentState(self.index)
    pacManPos = myState.getPosition()
    score = float(currentGameState.getScore())
    foodList = self.getFood(currentGameState).asList()
    foodDist = min([self.distCalc.getDistance(fPos, pacManPos) for fPos in foodList])
    
    #print(myState)

    scaryGhostList = []
    # print(currentGameState.getAgentState(self.index).configuration)
    #print(type(currentGameState.getAgentDistances()))
    #print(currentGameState.getAgentDistances())
    noisyDists = currentGameState.getAgentDistances()
    for opp_idx in self.getOpponents(currentGameState):
      oppAgent = currentGameState.getAgentState(opp_idx)
      if oppAgent.getPosition() != None:
        if not oppAgent.isPacman and oppAgent.scaredTimer == 0:
          scaryGhostList.append(self.distCalc.getDistance(myState.getPosition(), oppAgent.getPosition()))
      else:
        if not oppAgent.isPacman and oppAgent.scaredTimer == 0:
          scaryGhostList.append(noisyDists[opp_idx])
    #print(scaryGhostList)
    unseen = True
    if unseen:
      #print(currentGameState)
      unseen = False
    ghostDist = min(scaryGhostList)
    if ghostDist <= 1:
      ghostDist -= 1000

    if ghostDist == 0:
      ghostDist = 1
    ghostDist = float(ghostDist)
    foodDist = float(foodDist) 
    score = (ghostDist / foodDist)
    return score, ghostDist, foodDist

