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
    foodList = oldFood.asList()


    score = successorGameState.getScore()
    if successorGameState.isWin():
      return float('inf')
    if successorGameState.isLose():
      return float('-inf')

    scaryGhostList = [ghost.getPosition() for ghost in currentGameState.getGhostStates() if ghost.scaredTimer == 0]
    # Get distance of closest ghost.
    ghostDist = min([manhattanDistance(gPos, newPos) for gPos in scaryGhostList] + [500])

    # If ghost is on this position, you die. So, penalize.
    if ghostDist == 0:
      ghostDist -= 1000

    # If the closest ghost is really far away, penalize, but not as much.
    # 18 because PacMan kept getting stuck around 18?
    # is 18 a magic number? 17 fails like 3/10 times but 18 works 10/10 times lol.
    # Definitely has to do with the size of the game board.
    # EDIT: Upped the value to 20 because was getting errors 2/10 times on 19 (w/ fixed seed).
    # Got better score w/ 20. I should have printed these out and averaged them to be honest.
    if ghostDist > 20:
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

    DESCRIPTION: I wanted to capitalize on the ratio: closest ghost dist / closest food dist, along with
                  penalizing and rewarding factors added on, given different conditions.
    Consider the following cases for this ratio:
        1. ghostDist and foodDist are similar
            - Then this state is fairly neutral. The score sees a moderate boost.
            - If this state is picked, it's because neither extreme is present.
        2. ghostDist is small (but not too small!) and foodDist is large
            - then the score will see a smaller boost compared to the neutral case.
            - If ghostDist is too small, then we heavily penalize it with -1000
            - We definitely never want to move where ghosts are too close for comfort.
        3. If ghostDist is large, and foodDist is small
            - Highly preferred state to be in, so score gets a large boost.
            - NOTE: that if the ghostDist is too large, then it may be hard to differentiate between
            - similar states, and might lead to stalling or thrashing.
              - Thus if ghostDist is too large, we penalize it to prefer getting closer to ghosts for
              - food pellets. Pacman won't be as hyper-safe in this case, and will be willing
              - to move closer to ghosts (because we already know the closest is far away).
    This is a slightly augmented version of my reflex agent, because this can't evaluate given an action.
    On top of this, I also added several things.
    1. Only evaluate ghosts who are not scared. I've also added this to my reflex agent, but previously it
        would evaluate all ghosts, regardless of their state.
    2. If a closest ghost is <= 3 units away, then severely penalize this state.
        Because of the unpredictable nature of Expectimax, it is too risky to let ghosts get close.
        So I shy away from all states where ghosts are too close to comfort.

  """
  "*** YOUR CODE HERE ***"
  if currentGameState.isWin():
    return float('inf')
  if currentGameState.isLose():
    return float('-inf')
  pacManPos = currentGameState.getPacmanPosition()
  score = currentGameState.getScore()
  foodList = currentGameState.getFood().asList()
  scaryGhostList = [ghost.getPosition() for ghost in currentGameState.getGhostStates() if ghost.scaredTimer == 0]
  ghostDist = min([manhattanDistance(gPos, pacManPos) for gPos in scaryGhostList] + [500])
  if ghostDist <= 3:
    ghostDist -= 1000

  if ghostDist > 18:
    ghostDist -= 500

  foodDist = min([manhattanDistance(fPos, pacManPos) for fPos in foodList])
  score += ghostDist / foodDist
  return score


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

