# multiAgents.py
# --------------
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
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodCount = 0
        foodDistances = []
        minDistToFood = 0
        closeToGhostScore = 0
        ghostScaredTimes = 0

        for ghost in newGhostStates:
            distance = manhattanDistance(newPos, ghost.getPosition())
            if 4 > distance >= 2:
                closeToGhostScore += 2*distance
            elif distance == 1:
                closeToGhostScore += 10.0/distance
            else:
                closeToGhostScore += 0

        foodCount = len(newFood.asList())

        for food in newFood.asList():
            foodDistances.append(manhattanDistance(newPos,food))

        if foodDistances:
            minDistToFood = min(foodDistances)

        if not minDistToFood:
            minDistToFood = 1000000

        for i in newScaredTimes:
            ghostScaredTimes += i

        currentScore = successorGameState.getScore()
        evalScore = currentScore + (11.0/minDistToFood) - 0.4*foodCount - closeToGhostScore + 0.3*ghostScaredTimes
        return evalScore

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
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        depthCount = self.depth
        startingAgent = 0   # Pacman starts
        numOfAgents = gameState.getNumAgents()

        def minimax(state, depth, agent):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            legalMoves = state.getLegalActions(agent)

            if agent == 0:
                value = float('-inf')
                successors = []
                scores = []

                for action in legalMoves:
                    successors.append((state.generateSuccessor(agent, action)))

                for childNode in successors:
                    nodeScore = minimax(childNode, depth, agent+1)[0]
                    scores.append(nodeScore)
                    value = max(value, nodeScore)

                bestIndices = [index for index in range(len(scores)) if scores[index] == value]
                chosenIndex = random.choice(bestIndices)
                return value, legalMoves[chosenIndex]
            else:
                value = float('inf')
                successors = []
                scores = []

                if agent == numOfAgents-1:
                    for action in legalMoves:
                        successors.append((state.generateSuccessor(agent, action)))

                    for childNode in successors:
                        nodeScore = minimax(childNode, depth-1, 0)[0]
                        scores.append(nodeScore)
                        value = min(value, nodeScore)
                else:
                    for action in legalMoves:
                        successors.append((state.generateSuccessor(agent, action)))

                    for childNode in successors:
                        nodeScore = minimax(childNode, depth, agent+1)[0]
                        scores.append(nodeScore)
                        value = min(value, nodeScore)

                bestIndices = [index for index in range(len(scores)) if scores[index] == value]
                chosenIndex = random.choice(bestIndices)
                return value, legalMoves[chosenIndex]

        returnValue = minimax(gameState, depthCount, startingAgent)
        return returnValue[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        depthCount = self.depth
        startingAgent = 0   # Pacman starts
        numOfAgents = gameState.getNumAgents()
        alpha = float('-inf')
        beta = float('inf')

        def minimax(state, depth, agent, a, b):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            legalMoves = state.getLegalActions(agent)

            if agent == 0:
                value = float('-inf')
                takenAction = Directions.STOP

                for action in legalMoves:
                    successor = state.generateSuccessor(agent, action)
                    nodeScore = minimax(successor, depth, agent+1, a, b)[0]

                    if nodeScore >= value:
                        takenAction = action

                    value = max(value, nodeScore)

                    if value > b:
                        return value, takenAction

                    a = max(a, value)

                return value, takenAction

            else:
                value = float('inf')
                takenAction = Directions.STOP

                if agent == numOfAgents-1:
                    for action in legalMoves:
                        successor = state.generateSuccessor(agent, action)
                        nodeScore = minimax(successor, depth-1, 0, a, b)[0]

                        if nodeScore <= value:
                            takenAction = action

                        value = min(value, nodeScore)

                        if value < a:
                            return value, takenAction

                        b = min(b, value)

                else:
                    for action in legalMoves:
                        successor = state.generateSuccessor(agent, action)
                        nodeScore = minimax(successor, depth, agent+1, a, b)[0]

                        value = min(value, nodeScore)

                        if nodeScore <= value:
                            takenAction = action

                        if value < a:
                            return value, takenAction

                        b = min(b, value)

                return value, takenAction

        returnValue = minimax(gameState, depthCount, startingAgent, alpha, beta)
        return returnValue[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        depthCount = self.depth
        startingAgent = 0  # Pacman starts
        numOfAgents = gameState.getNumAgents()

        def expectimax(state, depth, agent):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            legalMoves = state.getLegalActions(agent)

            if agent == 0:
                value = float('-inf')
                successors = []
                scores = []

                for action in legalMoves:
                    successors.append((state.generateSuccessor(agent, action)))

                for childNode in successors:
                    nodeScore = expectimax(childNode, depth, agent + 1)[0]
                    scores.append(nodeScore)
                    value = max(value, nodeScore)

                bestIndices = [index for index in range(len(scores)) if scores[index] == value]
                chosenIndex = random.choice(bestIndices)
                return value, legalMoves[chosenIndex]

            else:
                value = 0.0
                successors = []

                if agent == numOfAgents - 1:
                    for action in legalMoves:
                        successors.append((state.generateSuccessor(agent, action)))

                    for childNode in successors:
                        nodeScore = expectimax(childNode, depth - 1, 0)[0]
                        value += nodeScore

                    value = value /float(len(successors))

                else:
                    for action in legalMoves:
                        successors.append((state.generateSuccessor(agent, action)))

                    for childNode in successors:
                        nodeScore = expectimax(childNode, depth, agent + 1)[0]
                        value += nodeScore

                    value = value / float(len(successors))

                return value, random.choice(legalMoves)

        returnValue = expectimax(gameState, depthCount, startingAgent)
        return returnValue[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>

      This evaluation function is really similar to the reflex agent evaluation function.
      I just replaced successorGameState with currentGameState and this better evaluation
      function works fine. This evaluation function uses number of food on board, closest food
      distance, closest ghost distance, ghost scared time, and current score as features. The
      evaluation function score is calculated from the weighted linear sum of these features.

    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodCount = 0
    foodDistances = []
    minDistToFood = 0
    closeToGhostScore = 0
    ghostScaredTimes = 0

    for ghost in newGhostStates:
        distance = manhattanDistance(newPos, ghost.getPosition())
        if 4 > distance >= 2:
            closeToGhostScore += 2 * distance
        elif distance == 1:
            closeToGhostScore += 10.0 / distance
        else:
            closeToGhostScore += 0

    foodCount = len(newFood.asList())

    for food in newFood.asList():
        foodDistances.append(manhattanDistance(newPos, food))

    if foodDistances:
        minDistToFood = min(foodDistances)

    if not minDistToFood:
        minDistToFood = 1000000

    for i in newScaredTimes:
        ghostScaredTimes += i

    currentScore = currentGameState.getScore()
    evalScore = currentScore + (11.0 / minDistToFood) - 0.4 * foodCount - closeToGhostScore + 0.3 * ghostScaredTimes
    return evalScore

# Abbreviation
better = betterEvaluationFunction
