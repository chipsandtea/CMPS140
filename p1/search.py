# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def startingState(self):
    """
    Returns the start state for the search problem
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())
  """
  # print "Start:", problem.startingState()
  # print "Is the start a goal?", problem.isGoal(problem.startingState())
  # print "Start's successors:", problem.successorStates(problem.startingState())
  from game import Directions


  # Init an empty LIFO stack, and push start state.
  # Each entry is a tuple: (node, path to node as a list)
  frontier = util.Stack()
  # start state and empty path
  frontier.push(((problem.startingState(), "null", 0), []))

  # Init an empty explored set
  explored = set()
  while True:
      # If no nodes to expand, failure.
      if frontier.isEmpty():
          return []
      # Pop off the top of the stack
      node, path = frontier.pop()
      if problem.isGoal(node[0]):
          # print path
          return path
      explored.add(node)
      successors = problem.successorStates(node[0])
      for succ_node in successors:
          if succ_node not in explored:
              frontier.push((succ_node, path + [succ_node[1]]))


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  frontier = util.Queue()
  frontier.push(((problem.startingState(), "null", 0), []))

  # Init an empty explored set
  explored = set()
  while True:
      # If no nodes to expand, failure.
      if frontier.isEmpty():
          return []
      # Pop off the top of the stack
      node, path = frontier.pop()
      if problem.isGoal(node[0]):
          print path
          return path
      explored.add(node)
      successors = problem.successorStates(node[0])
      for succ_node in successors:
          if succ_node not in explored:
              frontier.push((succ_node, path + [succ_node[1]]))


def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  frontier = util.PriorityQueue()
  frontier.push(((problem.startingState(), "null", 0), []), 0)

  # Init an empty explored set
  explored = set()
  while True:
      # If no nodes to expand, failure.
      if frontier.isEmpty():
          return []
      # Pop off the top of the stack
      node, path = frontier.pop()
      if problem.isGoal(node[0]):
          print path
          return path
      explored.add(node)
      successors = problem.successorStates(node[0])
      for succ_node in successors:
          if succ_node not in explored:
              frontier.push((succ_node, path + [succ_node[1]]), succ_node[2])

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  util.raiseNotDefined()



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
