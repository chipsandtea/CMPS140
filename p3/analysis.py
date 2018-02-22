# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.0
  """Description:
  The discount factor isn't small enough to make the agent stand still.
  This means the agent will attempt to cross the bridge.
  However, 0.2 noise is enough of a chance that the agent will fall off
  the bridge unintentionally, so lowering it to 0 means the agent
  will both attempt to cross and successfully execute on its chosen actions.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.3
  answerNoise = 0.0
  answerLivingReward = 0.0
  """Description:
  High confidence (to walk cliff side)
  Prioritize 1.0 exit must highly penalize further rewards.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.3
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  Low confidence at all means prioritizing closer exit but safer route.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.9
  answerNoise = 0.0
  answerLivingReward = 0.0
  """Description:
  High confidence to walk cliff side.
  Very little discount so further reward (+10) is still better.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  """Description:
  Reduced confidence means cliff side pretty much never preferred.
  Little discount so further reward (+10) still better.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 1.0
  answerNoise = 0.0
  answerLivingReward = 1.0
  """Description:
  [Enter a description of what you did here.]
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = None
  answerLearningRate = None
  """Description:
  [Enter a description of what you did here.]
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
