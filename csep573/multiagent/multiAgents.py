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
import sys

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        #print("chosen action: " + str(legalMoves[chosenIndex]) + " has best score: " + str(bestScore))
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
        newCapsules = successorGameState.getCapsules()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        currentPos = currentGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()
        currentCapsules = currentGameState.getCapsules()
        currentGhostStates = currentGameState.getGhostStates()
        currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]

        scoreChange = successorGameState.getScore() - currentGameState.getScore()
        if scoreChange > 490:
            return sys.maxsize

        if scoreChange < -490:
            return -sys.maxsize

        currentFoodDist = [util.manhattanDistance(currentPos, foodPos) for foodPos in currentFood.asList()]
        newFoodDist = [util.manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]

        score = min(currentFoodDist, default=0) - min(newFoodDist, default=0)
        if min(newFoodDist, default=0) != 0:
            altScore = 1 / min(newFoodDist, default=0)

        currentCapsulesDist = [util.manhattanDistance(currentPos, capsulesPos) for capsulesPos in currentCapsules]
        newCapsulesDist = [util.manhattanDistance(newPos, capsulesPos) for capsulesPos in newCapsules]

        #score += min(currentCapsulesDist, default=0) - min(newCapsulesDist, default=0)
        if min(newCapsulesDist, default=0) != 0:
            altScore += 1 / min(newCapsulesDist, default=0)

        currentGhostPositions = [ghostState.getPosition() for ghostState in currentGhostStates if ghostState.scaredTimer <= 0]
        currentGhostDist = [util.manhattanDistance(currentPos, ghostPos) for ghostPos in currentGhostPositions]
        newGhostPositions = [ghostState.getPosition() for ghostState in newGhostStates if ghostState.scaredTimer <= 0]
        newGhostDist = [util.manhattanDistance(newPos, ghostPos) for ghostPos in newGhostPositions]

        score += min(newGhostDist, default=0) - min(currentGhostDist, default=0)
        altScore += min(newGhostDist, default=0)

        currentScaredGhostPositions = [ghostState.getPosition() for ghostState in currentGhostStates if ghostState.scaredTimer > 1]
        currentScaredGhostDist = [util.manhattanDistance(currentPos, ghostPos) for ghostPos in currentScaredGhostPositions]
        newScaredGhostPositions = [ghostState.getPosition() for ghostState in newGhostStates if ghostState.scaredTimer > 1]
        newScaredGhostDist = [util.manhattanDistance(newPos, ghostPos) for ghostPos in newScaredGhostPositions]

        score += min(currentScaredGhostDist, default=0) - min(newScaredGhostDist, default=0)
        if min(newScaredGhostDist, default=0) != 0:
            altScore += 1 / min(newScaredGhostDist, default=0)

        if len(newFood.asList()) > 0 and action == Directions.STOP:
            score -= 10
            altScore -= 10

        if len(newFood.asList()) > 0 and newPos == currentPos:
            score -= 20
            altScore -= 20

        score += successorGameState.getScore()
        altScore += successorGameState.getScore()

        #print("Score: " + str(score) + " altScore: " + str(altScore) + " for current state: " + str(currentPos) + " and action: " + str(action))
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        return self.value(gameState, 0, 0)[1]

    def value(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth >= (self.depth * gameState.getNumAgents()):
            return (self.evaluationFunction(gameState), None)

        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.minValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        a = None
        v = float('-inf')
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            successorValue, _ = self.value(successor, nextAgentIndex, depth+1)
            if successorValue > v:
                v = successorValue
                a = action

        return (v, a)

    def minValue(self, gameState, agentIndex, depth):
        a = None
        v = float('inf')
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            successorValue, _ = self.value(successor, nextAgentIndex, depth+1)
            if successorValue < v:
                v = successorValue
                a = action

        return (v, a)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        return self.value(gameState, 0, 0, float("-inf"), float("inf"))[1]

    def value(self, gameState, agentIndex, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth >= (self.depth * gameState.getNumAgents()):
            return (self.evaluationFunction(gameState), None)

        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.minValue(gameState, agentIndex, depth, alpha, beta)

    def maxValue(self, gameState, agentIndex, depth, alpha, beta):
        a = None
        v = float('-inf')
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            successorValue, _ = self.value(successor, nextAgentIndex, depth+1, alpha, beta)
            if successorValue > v:
                v = successorValue
                a = action
            if v > beta:
                return (v, a)
            alpha = max(alpha, v)

        return (v, a)

    def minValue(self, gameState, agentIndex, depth, alpha, beta):
        a = None
        v = float('inf')
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            successorValue, _ = self.value(successor, nextAgentIndex, depth+1, alpha, beta)
            if successorValue < v:
                v = successorValue
                a = action
            if v < alpha:
                return (v, a)
            beta = min(beta, v)

        return (v, a)

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

        return self.value(gameState, 0, 0)[1]

    def value(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth >= (self.depth * gameState.getNumAgents()):
            return (self.evaluationFunction(gameState), None)

        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.expValue(gameState, agentIndex, depth)

    def expValue(self, gameState, agentIndex, depth):
        v = 0
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        actions = gameState.getLegalActions(agentIndex)
        p = 1.0 / len(actions)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            successorValue, _ = self.value(successor, nextAgentIndex, depth+1)
            v += p * successorValue

        return (v, None)

    def maxValue(self, gameState, agentIndex, depth):
        a = None
        v = float('-inf')
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            successorValue, _ = self.value(successor, nextAgentIndex, depth+1)
            if successorValue > v:
                v = successorValue
                a = action

        return (v, a)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    score = 0

    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    currentCapsules = currentGameState.getCapsules()
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]

    if len(currentFood.asList()) == 0:
        return sys.maxsize

    currentFoodDist = [util.manhattanDistance(currentPos, foodPos) for foodPos in currentFood.asList()]

    currentCapsulesDist = [util.manhattanDistance(currentPos, capsulesPos) for capsulesPos in currentCapsules]

    currentGhostPositions = [ghostState.getPosition() for ghostState in currentGhostStates if ghostState.scaredTimer <= 0]
    currentGhostDist = [util.manhattanDistance(currentPos, ghostPos) for ghostPos in currentGhostPositions]

    currentScaredGhostPositions = [ghostState.getPosition() for ghostState in currentGhostStates if ghostState.scaredTimer > 1]
    currentScaredGhostDist = [util.manhattanDistance(currentPos, ghostPos) for ghostPos in currentScaredGhostPositions]

    if len(currentFoodDist) > 0:
        avgFoodDist = sum(currentFoodDist) / len(currentFoodDist)
        score += 7 * (1.0 / avgFoodDist)

    score += 10 * (1.0 / min(currentFoodDist, default=0))

    #if len(currentCapsulesDist) > 0:
    #    avgCapsuleDist = sum(currentCapsulesDist) / len(currentCapsulesDist)
    #    score += 1.0 / avgCapsuleDist

    if len(currentScaredGhostDist) > 0:
        avgScaredGhostDist = sum(currentScaredGhostDist) / len(currentScaredGhostDist)
        score += 1.0 / avgScaredGhostDist
        score *= 5

    score += 0.7 * min(currentGhostDist, default=0)

    return currentGameState.getScore() + score

# Abbreviation
better = betterEvaluationFunction
