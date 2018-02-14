# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
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
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    foodCount = currentGameState.getNumFood()
    foodList = oldFood.asList()
    #print(foodList)


    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    score = successorGameState.getScore()
    if successorGameState.isWin():
      return float('inf')

    # Get distance of closest ghost.
    ghostDist = min([manhattanDistance(gPos, newPos) for gPos in successorGameState.getGhostPositions()])

    # If ghost is on this position, you die. So, penalize.
    if ghostDist == 0:
      ghostDist -= 1000

    # If the closest ghost is really far away, penalize, but not as much.
    # 18 because PacMan kept getting stuck around 18?
    # is 18 a magic number? 17 fails like 3/10 times but 18 works 10/10 times lol.
    # Definitely has to do with the size of the game board.
    if ghostDist > 18:
      ghostDist -= 500

    # Found that PacMan would play too conservatively(?) if the ratio of ghostDist / foodDist wasn't very optimal.
    # This is to penalize inaction. In theory should work because we have sufficient penalizing for actually
    # terrible decisions. Might thrash a bit more, but at the very least won't waste time otherwise.
    if action == Directions.STOP:
      score -= 10

    foodDist = min([manhattanDistance(pellPos, newPos) for pellPos in foodList if manhattanDistance(pellPos, newPos) != 0])


    # Ratio between closer ghost and closer food. Scale of priority.
    # If a ghost is close and food is far, then the action will be penalized.
    # If a ghost is far and food is close, then action will be preferred!
    score += ghostDist / foodDist
    #print(score)
    return score

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
    self.treeDepth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    initDepth = 1
    action = self.maximizer(gameState, initDepth)
    #print(action)
    return action

  def maximizer(self, gameState, currDepth):
    # PacMan maximizer node.
    # If game is over, return the value of the current gameState
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    # Default best move to STOP.
    bestMove = Directions.STOP
    bestVal = float('-inf')
    legalActions = gameState.getLegalActions(0)
    # For every action, find the max value and action the minimizer nodes one level down would return.
    successors = [(gameState.generateSuccessor(0, action), action) for action in legalActions]
    for succ in successors:
      tempVal = self.minimizer(succ[0], currDepth, 1)
      if tempVal > bestVal:
        bestVal = tempVal
        bestMove = succ[1]

    # If we have recursed back to the root maximizer node, return the action.
    # Otherwise, return the value (only at the root does the action matter).
    if currDepth == 1:
      #print(bestVal)
      return bestMove
    return bestVal

  def minimizer(self, gameState, currDepth, agentIdx):
    # Ghost minimizer node.
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    # If we have run out of ghosts, we must now consider PacMan's turn and return the minimum.
    if agentIdx == gameState.getNumAgents() - 1:
      legalActions = gameState.getLegalActions(agentIdx)
      worstVal = float('inf')
      successors = [gameState.generateSuccessor(agentIdx, action) for action in legalActions]
      # If we are at maximum depth, return the value of each successor gameState.
      if currDepth == self.treeDepth:
        for succGameState in successors:
          worstVal = min(worstVal, self.evaluationFunction(succGameState))
      # If not, then return the min value of maximizer nodes on successor gameStates.
      else:
        for succGameState in successors:
          worstVal = min(worstVal, self.maximizer(succGameState, currDepth+1))
      return worstVal
    # If we are at not at maximum depth, return the minimum of each successive ghosts minimizer value.
    # Eventually, this will proc the previous if statement, complete the level traversal at currDepth,
    # and move on to the next one.
    else:
      legalActions = gameState.getLegalActions(agentIdx)
      worstVal = float('inf')
      successors = [gameState.generateSuccessor(agentIdx, action) for action in legalActions]
      for succGameState in successors:
        worstVal = min(worstVal, self.minimizer(succGameState, currDepth, agentIdx+1))
      return worstVal



'''
  def minimax(self, gameState, agentIdx, currDepth):
    # If terminal node, return node value.
    if currDepth == self.treeDepth:
      return ('', self.evaluationFunction(gameState))

    # If agentIdx > number of agents, reset to PacMan idx.
    if agentIdx >= gameState.getNumAgents():
      agentIdx = 0
      currDepth += 1

    if agentIdx == 0: # If we're PacMan, then play as Maximizer node.
      val = (Directions.STOP, float('-inf'))
      legalActions = gameState.getLegalActions(agentIdx)
      for action in legalActions:
        #print(action)
        if action == Directions.STOP:
          continue
        tempVal = (action, self.minimax(gameState.generateSuccessor(agentIdx, action), agentIdx+1, currDepth))
        if tempVal[1] > val[1]:
          val = tempVal
      #print(val)
      return val
    else:
      val = (Directions.STOP, float('inf'))
      legalActions = gameState.getLegalActions(agentIdx)
      for action in legalActions:
        #print(action)
        if action == Directions.STOP:
          continue
        tempVal = (action, self.minimax(gameState.generateSuccessor(agentIdx, action), agentIdx+1, currDepth))
        if tempVal[1] < val[1]:
          val = tempVal
      #print(val)
      return val
'''





class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    initDepth = 1
    action = self.maximizer(gameState, initDepth, float('-inf'), float('inf'))
    #print(action)
    return action

  def maximizer(self, gameState, currDepth, alpha, beta):
    # PacMan maximizer node.
    # If game is over, return the value of the current gameState
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    # Default best move to STOP.
    bestMove = Directions.STOP
    bestVal = float('-inf')
    legalActions = gameState.getLegalActions(0)
    # For every action, find the max value and action the minimizer nodes one level down would return.
    successors = [(gameState.generateSuccessor(0, action), action) for action in legalActions]
    for succ in successors:
      if succ[1] == Directions.STOP:
        continue
      tempVal = self.minimizer(succ[0], currDepth, 1, alpha, beta)
      if tempVal > bestVal:
        bestVal = tempVal
        bestMove = succ[1]
      if bestVal > beta:
        return bestVal
      alpha = max(alpha, bestVal)

    # If we have recursed back to the root maximizer node, return the action.
    # Otherwise, return the value (only at the root does the action matter).
    if currDepth == 1:
      #print(bestVal)
      return bestMove
    return bestVal

  def minimizer(self, gameState, currDepth, agentIdx, alpha, beta):
    if agentIdx == gameState.getNumAgents() - 1:
      legalActions = gameState.getLegalActions(agentIdx)
      worstVal = float('inf')
      successors = [gameState.generateSuccessor(agentIdx, action) for action in legalActions]
      # If we are at maximum depth, return the value of each successor gameState.
      if currDepth == self.treeDepth:
        for succGameState in successors:
          worstVal = min(worstVal, self.evaluationFunction(succGameState))
          if worstVal < alpha:
            #print(worstVal, alpha)
            return worstVal
          beta = min(beta, worstVal)
      # If not, then return the min value of maximizer nodes on successor gameStates.
      else:
        for succGameState in successors:
          worstVal = min(worstVal, self.maximizer(succGameState, currDepth+1, alpha, beta))
          #print(worstVal)
          if worstVal < alpha:
            #print(worstVal, alpha)
            return worstVal
          beta = min(beta, worstVal)
      return worstVal
    # If we are at not at maximum depth, return the minimum of each successive ghosts minimizer value.
    # Eventually, this will proc the previous if statement, complete the level traversal at currDepth,
    # and move on to the next one.
    else:
      legalActions = gameState.getLegalActions(agentIdx)
      worstVal = float('inf')
      successors = [gameState.generateSuccessor(agentIdx, action) for action in legalActions]
      for succGameState in successors:
        worstVal = min(worstVal, self.minimizer(succGameState, currDepth, agentIdx+1, alpha, beta))
        if worstVal <= alpha:
          return worstVal
        beta = min(beta, worstVal)
      return worstVal



class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    initDepth = 1
    action = self.maximizer(gameState, initDepth)
    print(action)
    return action

  def maximizer(self, gameState, currDepth):
    # PacMan maximizer node.
    # If game is over, return the value of the current gameState
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    # Default best move to STOP.
    bestMove = Directions.STOP
    bestVal = float('-inf')
    legalActions = gameState.getLegalActions(0)
    # For every action, find the max value and action the minimizer nodes one level down would return.
    successors = [(gameState.generateSuccessor(0, action), action) for action in legalActions]
    for succ in successors:
      tempVal = self.minimizer(succ[0], currDepth, 1)
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
    if gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState)
    # If we have run out of ghosts, we must now consider PacMan's turn and return the minimum.
    if agentIdx == gameState.getNumAgents() - 1:
      legalActions = gameState.getLegalActions(agentIdx)
      expVal = 0
      successors = [gameState.generateSuccessor(agentIdx, action) for action in legalActions]
      # If we are at maximum depth, return the value of each successor gameState.
      if currDepth == self.treeDepth:
        for succGameState in successors:
          expVal += self.evaluationFunction(succGameState)
      # If not, then return the min value of maximizer nodes on successor gameStates.
      else:
        for succGameState in successors:
          expVal += self.maximizer(succGameState, currDepth+1)
      return expVal / (gameState.getNumAgents() - 1)
    # If we are at not at maximum depth, return the minimum of each successive ghosts minimizer value.
    # Eventually, this will proc the previous if statement, complete the level traversal at currDepth,
    # and move on to the next one.
    else:
      legalActions = gameState.getLegalActions(agentIdx)
      successors = [gameState.generateSuccessor(agentIdx, action) for action in legalActions]
      ghostVals = 0
      for succGameState in successors:
        ghostVals += self.minimizer(succGameState, currDepth, agentIdx+1)
      return ghostVals/(gameState.getNumAgents() - 1)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

