from queue import PriorityQueue
from unittest.mock import _patch_dict
import random

'Heuristic function which calculates node distance to goal based on row and column distance'
def distance(location,goal):
    locationCube = offsetToCube(location)
    goalCube = offsetToCube(goal)
    return (abs(locationCube[0] -goalCube[0]) + abs(locationCube[1] - goalCube[1]) + abs (locationCube[2] - goalCube[2]))/2

'Generates children based on an offset list and board location/proximity'
def generateChildren(board, location, n):
    children = []
    offsets = [(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1)]
    for x,y in offsets:
        if (location[0] + x in range(0,n) and location[1] + y in range(0,n)) and board[location[0] + x][location[1] + y] != -1:
            children.append((location[0] + x, location[1] + y))
    return children

def cubeToOffset(node):
    q = node[0] - (node[1] - node[1]&1)/2
    r = node[1]
    return [r,q]

def offsetToCube(node):
    q = node[1] - (node[0] - node[0]&1)/2
    r = node[0]
    return [q,r, -q-r]


# A slightly altered implementation of Dijkstra's algorithm with a heuristic function.
# This algorithm  creates a priority queue, a dictionary of previous paths, and a dictionary of
# current path costs for each given grid tile. It starts at the start location and generates a series
# of possible paths via the generateChildren() function. It then iterates over each child location. 
# If the child has not yet been visited or if the current child node has a cheaper cost to visit a 
# previously known child node, then the algorithm will build the path by inserting the current node
# as the previously visited node for the child node in the previous paths dictionary. It will then 
# insert the cost of the path so far into the cost dictionary for the child node. Lastly it will
# push this child node to the priority queue, adding it to the list of nodes to visit once the current
# set of children has finished iterating.
# The algorithm will then pop the next node and iterate based on the priority value which is generated
# using the current path length (i.e. g(n)) plus the heuristic value (h(n)). It will continue generating
# children and checking paths until it has found the goal node

# Note that some of the specific structure of the algorithm was adapted from the A* algorithm implemented at the following website:
# https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar

def lineHeuristicAlgo(board, start, goal, n):
    pq = PriorityQueue()
    pq.put((0,tuple(start)))
    previousDict = {}
    currCost = {}
    previousDict[tuple(start)] = None
    currCost[tuple(start)] = 0

    while not pq.empty():
        currNode = pq.get()[1]

        if currNode == goal:
            break
        
        for nextNode in generateChildren(board, currNode, n):
            if board[currNode[0]][currNode[1]] == 1:
                nextCost = currCost[currNode]
            else:
                nextCost = currCost[currNode] + 1
            if nextNode not in currCost or nextCost < currCost[nextNode]:
                currCost[nextNode] = nextCost
                pq.put((distance(nextNode, goal) + currCost[nextNode], nextNode))
                previousDict[nextNode] = currNode
    return previousDict, currCost

'Driver function that calls A* search on every valid start and end for the player to find the best direct path, and returns nodes along that path'
# def optimalPathSearch(board, n):
#     bestCost = n*n
#     bestPath = []
#     for x in range(0,n):
#         for y in range (0,n):
#             previousDict, currCost = lineHeuristicAlgo(board,(0,x),(n-1,y),n)
#             if currCost[(n-1,y)] < bestCost:
#                 bestCost = currCost[(n-1,y)]
#                 bestPath = buildPath(previousDict, currCost, (0,x), (n-1,y), 0)
#     return bestPath

'Driver function that just returns random pieces'
def optimalPathSearch(board , n):
    bestPath = []
    numOpenTiles, openTiles = getTiles(board, n , 'open')

    # If first turn, remove middle piece lol cant be COMPLETELY RANDOM
    if (numOpenTiles == n*n):
        openTiles.remove((n//2,n//2))

    # while (len(bestPath)==0):
    #     coord = random.choice(openTiles)
    #     if(coord in openTiles):
    #         bestPath.append(coord)
    #         break
    
    bestPath.append(random.choice(openTiles))

    return bestPath

'Returns number of tiles of a given colour and their coordinates'
def getTiles(board, n, colour):
    colourDict = {'red': 1, "blue":-1, "open":0}
    colourDictInverse = {'1':'red', '-1': 'blue', '0':'open'}
    counter=0
    tiles=[]
    for x in range(n):
        for y in range(n):
            if (board[x][y] == colourDict[colour]):
                counter+=1
                tiles.append((x,y))
    return (counter , tiles)

'Small function to rebuild goal path based on the previous node dictionary, as well as the known cost'
# Note printTru either < 0 or > 0 to print.
def buildPath(previousDict: dict, currCost,goal,start, printTru):
    currNode = tuple(goal)
    path = [currNode]
    if currNode not in previousDict.keys():
        print(0)
        return
    while previousDict[currNode] != start:
        currNode = previousDict[currNode]
        path.append(currNode)
        if currNode == None:
            break
    path.reverse()
    path.remove(None)
    if printTru > 0:
        print(currCost[tuple(goal)] + 1)
        for x in path:
            x = str(x).replace(' ','')
            print(x)
    return path