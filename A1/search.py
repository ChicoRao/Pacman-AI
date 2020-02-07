# search.py
# ---------
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

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 21
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
I find this course really fun because of how good the lecture slides are
and how interesting the concepts about artificial intelligence are. I loved this assignment
because it helped me understand more about the different concepts that we learned in class.
It is my first time coding in Python but it was overall a fun assignment that makes me think.
Heuristics was a bit hard to understand for me but from this assignment, I think I definitely
understood more about heuristics and how to design an admissible and consistent heursitic.

"""
#####################################################
#####################################################

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Q1.1
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() )
    You will get (5,5)

    print (problem.isGoalState(problem.getStartState()) )
    You will get True

    print ( problem.getSuccessors(problem.getStartState()) )
    You will get [((x1,y1),'South',1),((x2,y2),'West',1)]
    """
    "*** YOUR CODE HERE ***"

    fringe = util.Stack()
    nodesVisited = []
    fringe.push(([],problem.getStartState()))

    while not fringe.isEmpty():
        # Pushes the unexplored nodes inside the fringe
        path, currentState = fringe.pop()

        # Add currentState node to nodesVisited
        nodesVisited.append(currentState)

        # Checks if current explored state is the goal state
        if problem.isGoalState(currentState):
            return path

        successors = problem.getSuccessors(currentState)

        # x[0] contains the state, x[1] contains the action, x[2] contains the cost
        for x in successors:
            if not x[0] in nodesVisited:
                fringe.push((path + [x[1]], x[0]))

    return path

def breadthFirstSearch(problem):
    """
    Q1.2
    Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    fringe = util.Queue()
    nodesVisited = []
    # Push start state to fringe, which contains no action but a starting point
    startState = problem.getStartState()
    fringe.push(([], startState))
    # Add startState node to nodesVisited
    nodesVisited.append(startState)

    while not fringe.isEmpty():
        # Pushes the unexplored nodes inside the fringe
        path, currentState = fringe.pop()

        # Checks if current explored state is the goal state
        if problem.isGoalState(currentState):
            return path

        successors = problem.getSuccessors(currentState)

        # x[0] contains the state, x[1] contains the action, x[2] contains the cost
        for x in successors:
            if not x[0] in nodesVisited:
                fringe.push((path + [x[1]],x[0]))
                # Any of the nodes that are not visited gets added to nodesVisited
                nodesVisited.append(x[0])

    return path


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Q1.3
    Search the node that has the lowest combined cost and heuristic first."""
    """Call heuristic(s,problem) to get h(s) value."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    nodesVisited = []
    startState = problem.getStartState()
    heuristicCost = heuristic(startState,problem)
    pathCost = 0
    sum = 0
    fringe.push(([],startState,0),pathCost+heuristicCost)

    while not fringe.isEmpty():
        # Pushes the unexplored nodes inside the fringe, will pop the lowest number priority from the priority queue
        path, currentState, pathCost = fringe.pop()

        # Add currentState node to nodesVisited
        if not currentState in nodesVisited:
            nodesVisited.append(currentState)
        else:
            continue

        # Checks if current explored state is the goal state
        if problem.isGoalState(currentState):
            return path

        successors = problem.getSuccessors(currentState)

        # x[0] contains the state, x[1] contains the action, x[2] contains the cost
        for x in successors:
            if not x[0] in nodesVisited:
                cost = pathCost + x[2]
                heuristicCost = heuristic(x[0],problem)
                # Adding backward cost and forward cost
                sum = cost + heuristicCost
                fringe.update((path + [x[1]], x[0], cost),sum)

    return path

def priorityQueueDepthFirstSearch(problem):
    """
    Q1.4a.
    Reimplement DFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    nodesVisited = []
    # Creating priorityCount such that priority queue will act like a stack
    priorityCount = 0
    fringe.push(([],problem.getStartState()),priorityCount)
    priorityCount += 1

    while not fringe.isEmpty():
        # Pushes the unexplored nodes inside the fringe
        path, currentState = fringe.pop()

        # Add currentState node to nodesVisited
        nodesVisited.append(currentState)

        # Checks if current explored state is the goal state
        if problem.isGoalState(currentState):
            return path

        successors = problem.getSuccessors(currentState)

        # x[0] contains the state and x[1] contains the action
        for x in successors:
            if not x[0] in nodesVisited:
                fringe.push((path + [x[1]], x[0]),-priorityCount)
                priorityCount += 1

    return path

def priorityQueueBreadthFirstSearch(problem):
    """
    Q1.4b.
    Reimplement BFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    nodesVisited = []
    fringe.push(([],problem.getStartState()),0)

    while not fringe.isEmpty():
        # Pushes the unexplored nodes inside the fringe
        path, currentState = fringe.pop()

        # Add currentState node to nodesVisited
        if not currentState in nodesVisited:
            nodesVisited.append(currentState)
        else:
            continue

        # Checks if current explored state is the goal state
        if problem.isGoalState(currentState):
            return path

        successors = problem.getSuccessors(currentState)

        # x[0] contains the state, x[1] contains the action, x[2] contains the cost
        for x in successors:
            if not x[0] in nodesVisited:
                priority = problem.getCostOfActions(path)
                fringe.push((path + [x[1]], x[0]),priority)

    return path

#####################################################
#####################################################
# Discuss the results of comparing the priority-queue
# based implementations of BFS and DFS with your original
# implementations.

"""
For DFS:

There seems to be no visual difference for DFS whether the fringe was implemented with
a stack or a priority queue. The cost and nodes expanded for tinyMaze, mediumMaze,
and bigMaze remains the same whether we used the normal DFS or the priority queue
DFS. As for the compute time, it seems like both implementations have similar compute time.

For BFS:

There seems to be no visual difference for BFS as well whether the fringe was implemented with
a queue or a priority queue. The cost and nodes expanded for tinyMaze, mediumMaze,
and bigMaze remains the same whether we used the normal BFS or the priority queue
BFS. However, it seems like with prioirty queue, the BFS takes a bit longer to find the path,
since when the priority-queue BFS is used in bigMaze, the compute time became a bit longer.

From these comparisons:

We can see that in general the original implementations the priority-queue based implementations
will be very similar. However, when we looked at the compute time for the implementations, both
DFS implementations have similar compute time, while the difference in compute times for both BFS
implementations become more evident as the maze size increases. In conclusion, I think using the
priority-queue based implementation for DFS and BFS is not as good of an implementation strategy
as using stack based implementation for DFS and queue based implementation for BFS.

"""



#####################################################
#####################################################



# Abbreviations (please DO NOT change these.)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
bfs2 = priorityQueueBreadthFirstSearch
dfs2 = priorityQueueDepthFirstSearch
