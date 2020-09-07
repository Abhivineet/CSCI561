######################## ASSIGNMENT 1 ##################################

# By Abhivineet Veeraghanta

from collections import deque
import heapq as pq
import random
import time
import math

start_time = time.time()
f = open("input.txt", "r")
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
    if a[2] not in connectors.keys():
        connectors[a[2]] = [b[2]]
    else:
        c1 = connectors.get(a[2])
        c1.append(b[2])
        connectors[a[2]] = c1
    if a not in tt_channel.keys():
        tt_channel[a] = [list(b)]
    else:
        c = tt_channel.get(a)
        c.append(list(b))
        tt_channel[a] = tuple(c)
    if b[2] not in connectors.keys():
        connectors[b[2]] = [a[2]]
    else:
        c1 = connectors.get(b[2])
        c1.append(a[2])
        connectors[b[2]] = c1
    if b not in tt_channel.keys():
        tt_channel[b] = [list(a)]
    else:
        c = tt_channel.get(b)
        c.append(list(a))
        tt_channel[b] = c

explored_set = set()
dummy_open_set = set()
print_list = []
tt_list = {}

def dist(point, point1):
    return math.sqrt((point[0]-point1[0])**2 + (point[1] - point1[1])**2)

for key in connectors:
    key_list = []
    for loc in tt_channel:
        if loc[2] == key:
            temp2 = tt_channel.get(loc)
            for every in temp2:
                key_list.append(every)
    tt_list[key] = key_list

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


#############################################    BFS     #############################################

if (alg_instruction.lower())=='bfs':

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

    class BFS():
        def __init__(self, start_state, end_state, tt_channel, dummy_open, explored_s):
            start_state = start_state
            end_state = end_state
            tt_channel = tt_channel
            bfs_open_set = dummy_open
            bfs_explored_set = explored_s

        def explore(self):
            bfs_list = deque(a)
            f = open("output.txt", "w+")
            bfs_list.append(Node(start_state, None, 0, 0))
            self.bfs_open_set.add(Node(start_state, None, 0, 0))
            while (len(bfs_list) != 0):
                curr_node = bfs_list.popleft()
                self.bfs_open_set.remove(curr_node)
                if curr_node.location == end_state:
                    return curr_node
                self.bfs_explored_set.add(curr_node)
                next_locations = valid_points(curr_node)
                for point in next_locations:  ## IF CODE DOESN'T WORK THIS IS THE FIRST PLACE TO CHECK!
                    t = Node(point[0], curr_node, curr_node.cost + 1, curr_node.printer + 1)
                    if t in self.bfs_explored_set or t in self.bfs_open_set:
                        continue
                    else:
                        bfs_list.append(t)  ## NOTE THE COST IS ONLY FOR BFS
                        self.bfs_open_set.add(t)
            f.write("FAIL")
            return None

        def valid_points(self, node):

            def adder(a, b):
                return [a[0] + b[0], a[1] + b[1], a[2]]

            directions_10 = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            directions_14 = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
            valid = []

            if tuple(node.location) in tt_channel.keys():
                d = tt_channel.get(tuple(node.location))
                for loc in d:
                    if loc[0] < grid_size[0] and loc[1] < grid_size[1] and loc[0] >= 0 and loc[1] >= 0:
                        valid.append([loc, abs(node.location[2] - loc[2])])

            for pos in directions_10:
                temp = adder(node.location, pos)
                if temp[0] < grid_size[0] and temp[1] < grid_size[1] and temp[0] >= 0 and temp[1] >= 0:
                    valid.append([temp, 10])

            for pos in directions_14:
                temp = adder(node.location, pos)
                if temp[0] < grid_size[0] and temp[1] < grid_size[1] and temp[0] >= 0 and temp[1] >= 0:
                    valid.append([temp, 14])

            return valid

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

        def f_value(self):
            if self.location[2] == end_state[2]:
                return self.cost + (math.sqrt(((self.location[0] - end_state[0]) ** 2) + ((self.location[1] - end_state[1]) ** 2)))
            else:
                return self.cost
            # elif self.location[2] in connectors:
            #     if tuple(self.location) in tt_channel and end_state[2] in connectors.get(self.location[2]) and len(connectors.get(self.location[2]))<2:
            #         return self.cost + 1
            #     elif tuple(self.location) in tt_channel and end_state[2] in connectors.get(self.location[2]):
            #         return self.cost + 2
            #     elif tuple(self.location) in tt_channel:
            #         return self.cost + 2
            #     else:
            #         a = -grid_size[1]
            #         b = grid_size[0]
            #         first_dist = abs((a * self.location[0]+ b * self.location[1])) / (math.sqrt(a * a + b * b))
            #         a = (1.0/grid_size[0])
            #         b = (1.0/grid_size[1])
            #         c = -1
            #         second_dist = abs((a * self.location[0] + b * self.location[1] + c)) / (math.sqrt(a * a + b * b))
            #         return self.cost + min(first_dist, second_dist)
                    # list = tt_list.get(self.location[2])
                    # temp = []
                    # for item in list:
                    #     temp.append(dist(self.location, item))
                    # return self.cost + min(temp)

        def __eq__(self, other):
            return self.location == other.location

        def __hash__(self):
            return hash(tuple(self.location))

        def __lt__(self, other):
            return ((self.f_value()) < (other.f_value()))

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
            for point in next_locations:  ## IF CODE DOESN'T WORK THIS IS THE FIRST PLACE TO CHECK!
                t = Node(point[0], curr_node, curr_node.cost + point[1], curr_node.printer + 1)
                if t in explored_set or t in dummy_open_set:
                    continue
                pq.heappush(astar_list, t)
                dummy_open_set.add(t)
        print("FAIL")
        return None

def main():
    a = BFS(start_state, end_state, tt_channel, dummy_open_set, explored_set)
    curr_node = a.explore()
    if curr_node is not None:
        print_method(curr_node)


if __name__ == '__main__':
    # if possibilities(end_state, connectors, start_state):
    main()
    print("time: " + str(time.time() - start_time))
    print(len(explored_set))
    # else:
    #     f = open("output.txt", "w+")
    #     f.write("FAIL")
