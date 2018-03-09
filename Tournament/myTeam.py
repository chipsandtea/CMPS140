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
    self.treeDepth = 3
    self.opponents = self.getOpponents(gameState)
    self.distCalc = Distancer(gameState.data.layout)
    self.distCalc.getMazeDistances()
    self.prevPos = gameState.getAgentPosition(self.index)


    ''' 
    Your initialization code goes here, if you need any.
    '''

  def maximizer(self, gameState, currDepth):
    # PacMan maximizer node.
    # If game is over, return the value of the current gameState.
    if gameState.isOver():
      evalVal = self.evaluationFunction(gameState)
      print(evalVal)
      return evalVal
    # Default best move to STOP.
    bestMove = Directions.STOP
    bestVal = float('-inf')
    legalActions = gameState.getLegalActions(self.index)
    # For every action, find the max value and action the minimizer nodes one level down would return.
    successors = [(gameState.generateSuccessor(self.index, action), action) for action in legalActions]
    for succ in successors:
      tempVal = self.minimizer(succ[0], currDepth, 0)
      if tempVal > bestVal:
        bestVal = tempVal
        bestMove = succ[1]

    # If we have recursed back to the root maximizer node, return the action.
    # Otherwise, return the value (only at the root does the action matter).
    if currDepth == 1:
      return bestMove
    return bestVal

  def minimizer(self, gameState, currDepth, agentIdx):
    # Ghost minimizer node.
    if gameState.isOver():
      return self.evaluationFunction(gameState)
    # If we have run out of ghosts, we must now consider PacMan's turn and return the minimum.
    if agentIdx == self.numOfOpponents-1:
      legalActions = gameState.getLegalActions(self.opponents[agentIdx])
      expVal = 0
      successors = [gameState.generateSuccessor(self.opponents[agentIdx], action) for action in legalActions]
      # If we are at maximum depth, return the value of each successor gameState.
      if currDepth == self.treeDepth:
        for succGameState in successors:
          expVal += self.evaluationFunction(succGameState)
      # If not, then return the min value of maximizer nodes on successor gameStates.
      else:
        for succGameState in successors:
          expVal += self.maximizer(succGameState, currDepth+1)
      return expVal / (self.numOfOpponents)
    # If we are at not at maximum depth, return the minimum of each successive ghosts minimizer value.
    # Eventually, this will proc the previous if statement, complete the level traversal at currDepth,
    # and move on to the next one.
    else:
      legalActions = gameState.getLegalActions(self.opponents[agentIdx])
      print(legalActions)
      successors = [gameState.generateSuccessor(self.opponents[agentIdx], action) for action in legalActions]
      print(len(successors))
      ghostVals = 0
      for succGameState in successors:
        ghostVals += self.minimizer(succGameState, currDepth, agentIdx+1)
      return ghostVals/self.numOfOpponents


  def chooseAction(self, gameState):
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
    if ghostDist <= 3:
      ghostDist -= 1000

    if ghostDist > 18:
      ghostDist -= 500
    
    if ghostDist == 0:
      ghostDist = 1
    ghostDist = float(ghostDist)
    foodDist = float(foodDist) 
    score += (ghostDist / foodDist)
    return score, ghostDist, foodDist

