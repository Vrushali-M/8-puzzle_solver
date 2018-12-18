import copy
from operator import itemgetter
import numpy as np
import sys


def get_state_from_user():
    n = 3
    state = [[0 for row in range(n)] for col in range(n)]
    for row in range(3):
        for col in range(3):
            state[row][col] = int(input())
    return state


def display_state(state):
    '''Dislays state like a 8 puzzle '''
    row, col = len(state),len(state[0])
    print('\n')
    for r in range(row):
        for c in range(col):
            print(state[r][c] , end=' ')
        print()


def misplaced_tiles(current_state, goal_state):
   ''' Calculates misplaced tiles heuristic value'''
   tiles = 0
   rows = len(current_state)
   columns = len(current_state[0])
   for i in range(rows):
       for j in range(columns):
           if current_state[i][j] != goal_state[i][j]:
               tiles = tiles+1
   return tiles


def manhattan_distance(current_state, goal):
   '''Calucates manhattan distance heuristic'''
   distance = 0
   rows = len(current_state)
   columns = len(current_state[0])
   for i in range(rows):
       for j in range(columns):
           a = current_state[i][j]
           for h in range(rows):
               for k in range(columns):
                   if a == goal[h][k]:
                       expected_row = h
                       expected_col = k
           actual_row =i
           actual_col = j
           distance_h = abs(expected_col-actual_col)+abs(expected_row-actual_row)
           distance = distance+distance_h
   return distance


def get_next_states(state):
   """generate all possible next state by
   1. get zero index
   2. get indices of neighbouring cells of 0
   3. swap 0 with neighbouring element"""

   for r in range(3):
       for c in range(3):
           if state[r][c] == 0:
               z_row, z_col = r, c

   """finished 1"""
   next_zero_positions = []
   if z_row > 0:
       next_zero_positions.append((z_row - 1, z_col))
   if z_col > 0:
       next_zero_positions.append((z_row, z_col - 1))
   if z_row < 2:
       next_zero_positions.append((z_row + 1, z_col))
   if z_col < 2:
       next_zero_positions.append((z_row, z_col + 1))

   """"finished 2. next_zero_positions has list of all possible zero locations"""

   next_states = []
   for position in next_zero_positions:
       new_state = copy.deepcopy(state)
       nz_row, nz_col = position
       new_state[z_row][z_col], new_state[nz_row][nz_col] = new_state[nz_row][nz_col], new_state[z_row][z_col]
       next_states.append(new_state)

   """finished 3"""
   return next_states


def make_node(state, heuristic, parent_node):
   """ makes node using dictionary as node structure"""
   nodes = {"state":"", "path_cost":0,  "parent":"", "heuristic":"", "total_cost": "", "path":""}
   node = copy.deepcopy(nodes)
   node["state"] = state
   if heuristic == "h2":
       node["heuristic"] = manhattan_distance(node["state"], goal_state)
   if heuristic == "h1":
       node["heuristic"] = misplaced_tiles(node["state"], goal_state)

   if parent_node == 'None':
       node["path_cost"] = 0
       node["total_cost"] = node["heuristic"] + node["path_cost"]
       node["parent"] = 'None'
       node["path"] = (node["state"])
   else:
       node["parent"] = parent_node["state"]
       node["path_cost"] = parent_node["path_cost"]+1
       node["total_cost"] = node["heuristic"]+node["path_cost"]
       node["path"]=  (node["state"])
       node["path"] = (node["path"])+((parent_node["path"]))

   return node


def get_path(path):
   """prints all the states from initial to goal state """
   path_len = len(path)
   temp_x = []
   n = path_len
   while n>=3:
       temp_x.append(path[n-3:n])
       n= n-3
   for x in temp_x:
       display_state(x)



print("Enter initial state ")

input_state = get_state_from_user()
print("Enter goal state ")
#goal = [[1,2,3],[8,6,4],[7,5,0]]
goal_state =  get_state_from_user()

# openset has all nodes which are in fringe.
openset =[]
# closedset has all nodes which are poped from openset and expanded. In short, duplicate of these must be avoided
closedset = []

heuristic = str(input('''Give Heuristic - 
type 'h1' for misplaced tile 
type 'h2' manhattan distance : '''))
parent_node = make_node(input_state, heuristic, 'None')     # input converted to parent node
number_of_nodes = 0         #keep count of number of nodes generated
next_states = get_next_states(parent_node["state"])
for state in next_states:
    child = make_node(state, heuristic, parent_node)
    if child["state"] == goal_state:
        print("reached goal")
        print("\n number of nodes generated : " + str(number_of_nodes))
        print("\n number of nodes expanded " + str(len(closedset)))
        print("\n number of nodes in queue "+str(len(openset)))
        print("\n states to reach goal are "+"\n")
        get_path(child["path"])
        sys.exit()

    openset.append(child)
    number_of_nodes += 1

sorted(openset, key=itemgetter('total_cost'))

while openset!=[]:
    pick_one = openset[0]
    next_states = get_next_states(pick_one["state"])
    for state in next_states:
        child = make_node(state, heuristic, pick_one)

        if child["state"] == goal_state:
            print("Reached Goal State")

            for child_keys in child.keys():
                    print(str(child_keys) + " : " + str(child[child_keys]))
            print("\nNumber of nodes generated : " + str(number_of_nodes))
            print("\nNumber of nodes expanded " + str(len(closedset)))
            print("\nNumber of nodes in queue " + str(len(openset)))
            print("states to reach goal are")
            get_path(child["path"])
            sys.exit()

        else:
            closedset_list = []
            openset_list = []
            for close in closedset:
                    closedset_list.append(close["state"])
            for open_ in openset:
                    openset_list.append(open_["state"])

            if (child["state"] != parent_node["state"]) and (child["state"] not in closedset_list) and (child["state"] not in openset_list):
                    openset.append(child)
                    number_of_nodes += 1

            elif ((child["state"] != parent_node["state"]) and (child["state"] not in closedset_list) and (child["state"] in openset_list)):
                    open_index = openset_list.index((child["state"]))
                    open_f = openset[open_index]["total_cost"]
                    if child["total_cost"]<open_f:
                            openset.pop(open_index)
                            openset.append(child)
                            number_of_nodes += 1

    closedset.append(pick_one)
    openset.pop(0)
    openset = sorted(openset, key=itemgetter('total_cost','heuristic'))