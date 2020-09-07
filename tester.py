######################## ASSIGNMENT 1 ##################################

# By Abhivineet Veeraghanta

from collections import deque
import heapq as pq
import random
import time
import math

start_time = time.time()
f = open("input50.txt", "r")
lines = f.readlines()

l = []

i=0
for line in lines:
    if i==5:
        break
    l.append(line.split())
    i+=1

alg_instruction = l[0][0]
grid_size = [int(l[1][0]), int(l[1][1])]
start_state = [int(l[2][1]), int(l[2][2]), int(l[2][0])]
end_state = [int(l[3][1]), int(l[3][2]), int(l[3][0])]
num_tt_channel = int(l[4][0])
connectors = {}

tt_channel = {}
for j in range(i, len(lines)):
    temp = lines[j].split()
    a = (int(temp[1]), int(temp[2]), int(temp[0]))
    b = (int(temp[1]), int(temp[2]), int(temp[3]))
    if a!=b:
        if a not in tt_channel.keys():
            tt_channel[a] = [list(b)]
        else:
            c = tt_channel.get(a)
            c.append(list(b))
            tt_channel[a] = tuple(c)
        if b not in tt_channel.keys():
            tt_channel[b] = [list(a)]
        else:
            c = tt_channel.get(b)
            c.append(list(a))
            tt_channel[b] = c

explored_set = set()
dummy_open_set = set()
print_list = []

def dist(point, point1):
    return math.sqrt((point[0]-point1[0])**2 + (point[1] - point1[1])**2 + (point[2]-point1[2])**2)

def valid_points(node):
    directions_10 = [[1,0], [0,1], [-1,0], [0,-1]]
    directions_14 = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    valid = []

    if tuple(node.location) in tt_channel.keys():
        d = tt_channel.get(tuple(node.location))
        for loc in d:
            if loc[0] < grid_size[0] and loc[1] < grid_size[1] and loc[0] >= 0 and loc[1] >= 0:
                valid.append([loc, abs(node.location[2]-loc[2])])

    for pos in directions_10:
        temp = adder(node.location, pos)
        if temp[0] < grid_size[0] and temp[1] < grid_size[1] and temp[0] >= 0 and temp[1] >= 0:
            valid.append([temp, 10])

    for pos in directions_14:
        temp = adder(node.location, pos)
        if temp[0] < grid_size[0] and temp[1] < grid_size[1] and temp[0] >= 0 and temp[1] >= 0:
            valid.append([temp, 14])

    return valid

def print_method(curr_node):
    writer = open("output.txt", "w+")
    writer.write(str(curr_node.cost) + "\n")
    writer.write(str(curr_node.printer + 1) + "\n")
    for i in range(curr_node.printer + 1):
        print_list_temp = [curr_node.location[2], curr_node.location[0], curr_node.location[1], curr_node.cost]
        print_list.append(print_list_temp)
        curr_node = curr_node.parent
    print_list.reverse()

    if len(print_list) ==1:
        writer.write(str(print_list[0][0]) + " " + str(print_list[0][1]) + " " + str(print_list[0][2]) + " " + str(print_list[0][3]))

    elif len(print_list)>=2:
        writer.write(str(print_list[0][0]) + " " + str(print_list[0][1]) + " " + str(
            print_list[0][2]) + " " + str(print_list[0][3]) + "\n")

        writer.write(str(print_list[1][0]) + " " + str(print_list[1][1]) + " " + str(
            print_list[1][2]) + " " + str(print_list[1][3]) + "\n")

    for i in range(2, len(print_list)):
        non_cumu_cost = abs(print_list[i][3] - print_list[i - 1][3])
        writer.write(str(print_list[i][0]) + " " + str(print_list[i][1]) + " " + str(print_list[i][2]) + " " + str(
            non_cumu_cost) + "\n")

def adder(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2]]

#############################################    BFS     #############################################

if (alg_instruction.lower())=='bfs':
    bfs_list = deque([])


    class Node:
        def __init__(self, loc, par, cost, ptinrter):
            self.location = loc
            self.parent = par
            self.cost = cost
            self.printer = ptinrter

        def __eq__(self, other):
            return (self.location == other.location)

        def __hash__(self):
            return hash(tuple(self.location))


    def explore():
        f = open("output.txt", "w+")
        bfs_list.append(Node(start_state, None, 0, 0))
        dummy_open_set.add(Node(start_state, None, 0, 0))
        while (len(bfs_list) != 0):
            curr_node = bfs_list.popleft()
            dummy_open_set.remove(curr_node)
            if curr_node.location == end_state:
                return curr_node
            explored_set.add(curr_node)
            next_locations = valid_points(curr_node)
            for point in next_locations:
                t = Node(point[0], curr_node, curr_node.cost + 1, curr_node.printer + 1)
                if t in explored_set or t in dummy_open_set:
                    continue
                else:
                    bfs_list.append(t)
                    dummy_open_set.add(t)
        f.write("FAIL")
        return None


#############################################    UCS     #############################################

elif (alg_instruction.lower())=='ucs':

    ucs_list = []

    class Node:
        def __init__(self, loc, par, cost, printer):
            self.location = loc
            self.parent = par
            self.cost = cost
            self.printer = printer

        def __eq__(self, other):
            return self.location == other.location

        def __hash__(self):
            return hash(tuple(self.location))

        def __lt__(self, other):
            return ((self.cost) < (other.cost))

    def explore():
        pq.heappush(ucs_list, Node(start_state, None, 0, 0))
        dummy_open_set.add(Node(start_state, None, 0, 0))
        while (len(ucs_list) != 0):
            curr_node = pq.heappop(ucs_list)
            dummy_open_set.remove(curr_node)
            if curr_node.location == end_state:
                return curr_node
            explored_set.add(curr_node)
            next_locations = valid_points(curr_node)
            for point in next_locations:  ## IF CODE DOESN'T WORK THIS IS THE FIRST PLACE TO CHECK!
                t = Node(point[0], curr_node, curr_node.cost + point[1], curr_node.printer+1)
                if t in explored_set or t in dummy_open_set:
                    continue
                pq.heappush(ucs_list, t)
                dummy_open_set.add(t)
        return None

#############################################    A*     #############################################

elif (alg_instruction.lower())=='a*':
    astar_list = []

    class Node:
        def __init__(self, loc, par, cost, printer):
            self.location = loc
            self.parent = par
            self.cost = cost
            self.printer = printer
            self.fvalue = self.f_value()

        def f_value(self):
            # if self.location[2] == end_state[2]:
            dx = abs(self.location[0] - end_state[0])
            dy = abs(self.location[1] - end_state[1])
            dz = abs(self.location[2]-end_state[2])
            return self.cost + dx+dy+dz
            # return self.cost + (dx+dy+dz)

        def __eq__(self, other):
            return self.location == other.location

        def __hash__(self):
            return hash(tuple(self.location))

        def __lt__(self, other):
            return ((self.fvalue) < (other.fvalue))

    def explore():
        pq.heappush(astar_list, Node(start_state, None, 0, 0))
        dummy_open_set.add(Node(start_state, None, 0, 0))
        while (len(astar_list) != 0):
            curr_node = pq.heappop(astar_list)
            dummy_open_set.remove(curr_node)
            if curr_node.location == end_state:
                return curr_node
            explored_set.add(curr_node)
            next_locations = valid_points(curr_node)
            for point in next_locations:
                t = Node(point[0], curr_node, curr_node.cost + point[1], curr_node.printer + 1)
                if t in explored_set or t in dummy_open_set:
                    continue
                pq.heappush(astar_list, t)
                dummy_open_set.add(t)
        print("FAIL")
        return None

def main():
    curr_node = explore()
    if curr_node is not None:
        print_method(curr_node)

if __name__ == '__main__':
    main()
    print("time: " + str(time.time() - start_time))