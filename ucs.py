from collections import deque
import heapq as pq


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


tt_channel = {}
for j in range(i, len(lines)):
    temp = lines[j].split()
    key = (int(temp[1]), int(temp[2]), int(temp[0]))
    value = (int(temp[1]), int(temp[2]), int(temp[3]))
    if key not in tt_channel.keys():
        tt_channel[key] = [value]
    else:
        c = tt_channel.get(key)
        c.append(value)
        tt_channel[key] = c
    if value not in tt_channel.keys():
        tt_channel[value] = [key]
    else:
        c = tt_channel.get(value)
        c.append(key)
        tt_channel[value] = c

explored_set = set()
#UCS

ucs_list = []


class Node:
    def __init__(self, loc, par, cost, printer):
        self.location = loc
        self.parent = par
        self.cost = cost
        self.printer = printer

    def __eq__(self, other):
        return self.cost == other.cost

    def __hash__(self):
        return hash(tuple(self.location))

    def __ne__(self, other):
        return ((self.cost) != (other.cost))

    def __lt__(self, other):
        return ((self.cost) < (other.cost))

    def __le__(self, other):
        return ((self.cost) <= (other.cost))

    def __gt__(self, other):
        return ((self.cost) > (other.cost))

    def __ge__(self, other):
        return ((self.cost) >= (other.cost))


def print_method(curr_node):
    for i in range(curr_node.printer + 1):
        print(curr_node.location)
        curr_node = curr_node.parent


def adder(a, b):
    print(a,b)
    return [a[0] + b[0], a[1] + b[1], a[2]]


def valid_points(node):
    directions_10 = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    directions_14 = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    valid = []

    if tuple(node.location) in tt_channel.keys():
        c = tt_channel.get(tuple(node.location))
        for loc in c:
            if loc[0] < grid_size[0] and loc[1] < grid_size[1] and loc[0] >= 0 and loc[1] >= 0:
                valid.append([list(c), abs(node.location[2]-loc[2])])
    for pos in directions_10:
        temp = adder(node.location, pos)
        if temp[0] < grid_size[0] and temp[1] < grid_size[1] and temp[0] >= 0 and temp[1] >= 0:
            valid.append([temp, 10])

    for pos in directions_14:
        temp = adder(node.location, pos)
        if temp[0] < grid_size[0] and temp[1] < grid_size[1] and temp[0] >= 0 and temp[1] >= 0:
            valid.append([temp, 14])

    return valid


def in_set(a, set):
    for value in set:
        if tuple(a) == value:
            return True
    return False


def in_list(a, list):
    for node in list:
        if a == node.location:
            return True
    return False


def explore():
    pq.heappush(ucs_list, Node(start_state, None, 0, 0))

    while (len(ucs_list) != 0):
        curr_node = pq.heappop(ucs_list)
        if curr_node.location == end_state:
            return curr_node
        explored_set.add(tuple(curr_node.location))
        next_locations = valid_points(curr_node)
        print(len(explored_set))
        for point in next_locations:  ## IF CODE DOESN'T WORK THIS IS THE FIRST PLACE TO CHECK!
            if in_set(point[0], explored_set) or in_list(point[0], ucs_list):
                continue
            pq.heappush(ucs_list, Node(point[0], curr_node, curr_node.cost + point[1], curr_node.printer + 1))
    print("FAIL")


curr_node = explore()################################################