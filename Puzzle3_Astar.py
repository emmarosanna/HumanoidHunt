import numpy as np
from math import sqrt, inf
import csv
from queue import PriorityQueue

# Read data (saved as csv)
data = open('data3.csv','r')
data = csv.reader(data, delimiter=',', quotechar='|')

# Initialize a maze as a matrix of zeros
# Here, assuming tha size of the maze is not greater than 200x200 - this would have to 
# be adjusted accordingly
maze = np.zeros((200,200))

# Initialize start- and endpoints
start = tuple()    # one startpoint
endpoints = []     # several endpoints

# Go through all the neural strands and add ones to the maze to represent possible 
# routes:
for line in data:

    # starting point of a strand
    x = int(line[0])
    y = int(line[1])
    maze[x][y] = 1

    # following the directions
    for char in line[2:]:
        if char == 'D':
            y = y+1
        elif char == 'U':
            y = y-1
        elif char == 'R':
            x = x+1
        elif char == 'L':
            x = x-1
        # listing also the endpoints
        elif char == 'F':
            endpoints.append((x,y))
        # and finding the starting point
        elif char == 'S':
            start = (x,y)
        # adding resulting routes to the maze   
        maze[x][y] = 1


########################################################################################
################## Using the A* -algorithm to find an optimal solution #################
########################################################################################

# Function to find out if given location is in the "finishing area"
def isgoal(loc:tuple):
    return loc in endpoints

# Find the possible successors of given state, that is, the allowed (on-route) locations 
# that are one step away from given location.
# Return the location with corresponding direction
def successors(loc:tuple):
    x,y = loc
    succ = []
    for i in [('R',(x+1,y)),('L',(x-1,y)),('D',(x,y+1)),('U',(x,y-1))]:
        if maze[i[1][0]][i[1][1]]==1:
            succ.append(i)
    return succ

# Heuristic function: Euclidean distance from given location to the nearest
# "finishing area"-location
# Serves as the lower bound for the remaining distance
def goaldist(loc:tuple):
    x,y = loc
    return min(list(map(lambda z: sqrt((x-z[0])**2 + (y-z[1])**2),endpoints)))

# Priority of a search node is given by the estimated distance to a goal state = 
# the length of the path that took us there + the euclidean distance to the closest 
# goal state
def est_dist(loc: tuple):
    return pathlength[loc] + goaldist(loc)

# A dictionary to keep up with predecessors of each expanded state and the action that 
# took us there
predecessors = {} # dict(tuple(x,y) --> tuple(action,predecessors))

# A dictionary to keep up with the length of the shortest route found to given location 
# (so far)
pathlength = {} # dict(tuple(x,y) --> int length)

# A priority queue to guide the search. Priority of each entry (search node) is the 
# estimated distance to a goal state as returned by est_dist
Q = PriorityQueue() # PriorityQueue((est_dist(loc),loc)) (lowest values retrieved first)

# Variables to keep up with the best path to goal state found
bestpath_length = inf
bestpath_end = None # the location (x,y) in the finishing area


##################################### Begin search #####################################

# Put start state in queue
Q.put((goaldist(start),start))

# and in pathlength- and predecessors-dictionaries
pathlength[start] = 0
predecessors[start]=(None,None)

# While the queue is non-empty do:
while not Q.empty():

    # Take out the search node with the highest priority = lowest estimated distance
    curr = Q.get()[1]

    # Only if the estimated distance (lower bound) is shorter than the current best 
    # path to goal state do:
    if est_dist(curr) < bestpath_length:
        
        # go through all the possible successor-locations
        for act,succ in successors(curr):
            
            # if the location has not yet been expanded, or this new path is shorter 
            # than the one found previously
            if ((not succ in pathlength) or ((pathlength[curr]+ 1) < pathlength[succ])):
                # update pathlength and predecessors
                pathlength[succ]=pathlength[curr]+ 1
                predecessors[succ] = (act,curr)
                # if the location is not a goal location, add it in queue    
                if not isgoal(succ):
                    Q.put((est_dist(succ),succ))
                # and if it is a goal location, see if it's better than the previous 
                # best and update when needed
                elif pathlength[succ]<bestpath_length:
                    bestpath_length = pathlength[succ]
                    bestpath_end = succ

# Recursively follow the predecessors to reconstruct the solution
actions = ''

# Check that there is a solution in the first place
if bestpath_end is not None:

    # Start from the goal
    currstate = bestpath_end
    
    # Move backwards until reaching start-state
    while currstate != start:
        
        predecessor = predecessors[currstate]
        # collect actions
        actions= predecessor[0]+actions
        currstate = predecessor[1]


print(actions)
