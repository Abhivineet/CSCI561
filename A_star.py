import heapq as pq

start_state = [8,12,2020]
end_state = [8,13,2024]
grid_size = [99,87]
tt_channel = {(12,16,2020):(12,16,3011), (12,16,3011):(12,16,2020), (56,77,1):(56,77,3011), (56,77,3011):(56,77,1), (0,0,12):(0,0,2), (0,0,2):(0,0,12), (0,0,2):(0,0,2024), (0,0,2024):(0,0,2), (8,13,2020):(8,13,2024), (8,13, 2024):(8,13,2020)}


inspected_states = []

#A*

astar_list = []

class Node:
    def __init__(self, loc, par, cost, printer):
        self.location = loc
        self.parent = par
        self.cost = cost
        self.printer = printer
        self.f_value = self.cost + ((((loc[0]-end_state[0])**2) + ((loc[1]-end_state[1])**2) + ((loc[2]-end_state[2])**2))**1/2)

    def __eq__(self, other):
        return self.f_value == other.f_value

    def __hash__(self):
        return hash(tuple(self.location))

    def __ne__(self, other):
        return ((self.f_value) != (other.f_value))

    def __lt__(self, other):
        return ((self.f_value) < (other.f_value))

    def __le__(self, other):
        return ((self.f_value) <= (other.f_value))

    def __gt__(self, other):
        return ((self.f_value) > (other.f_value))

    def __ge__(self, other):
        return ((self.f_value) >= (other.f_value))


def print_method(curr_node):
    for i in range(curr_node.printer + 1):
        print(curr_node.location)
        curr_node = curr_node.parent

def adder(a, b):
    return [a[0]+b[0], a[1]+b[1], a[2]]

def valid_points(node):
    directions_10 = [[1,0], [0,1], [-1,0], [0, -1]]
    directions_14 = [[1,1], [-1,1], [1,-1], [-1,-1]]
    valid = []

    if tuple(node.location) in tt_channel.keys():
        jaunted = list(tt_channel.get(tuple(node.location)))
        valid.append([jaunted , abs(node.location[2] - jaunted[2])])

    for pos in directions_10:
        temp = adder(node.location, pos)
        if temp[0]<grid_size[0] and temp[1]<grid_size[1] and temp[0] >= 0 and temp[1]>= 0:
            valid.append([temp, 10])

    for pos in directions_14:
        temp = adder(node.location, pos)
        if temp[0]<grid_size[0] and temp[1]<grid_size[1] and temp[0] >= 0 and temp[1]>= 0:
            valid.append([temp, 14])

    return valid

def in_set(a, set):
    for value in set:
        if tuple(a)==value:
            return True
    return False

def in_list(a, list):
    for node in list:
        if a == node.location:
            return True
    return False


explored_set = set()

def explore():
    pq.heappush(astar_list, Node(start_state, None, 0, 0))

    while(len(astar_list)!=0):
        curr_node = pq.heappop(astar_list)
        if curr_node.location == end_state:
            print('Success')
            return curr_node
        explored_set.add(tuple(curr_node.location))
        next_locations = valid_points(curr_node)
        for point in next_locations:                    ## IF CODE DOESN'T WORK THIS IS THE FIRST PLACE TO CHECK!
            checker = 0
            if in_set(point[0], explored_set) or in_list(point[0], astar_list):
                continue
                    #CHANGE FOR OTHER ALGs
            pq.heappush(astar_list, Node(point[0], curr_node, curr_node.cost+point[1], curr_node.printer + 1))
    print("FAIL")


################################################

# TEST RUN FOR BFS

curr_node = explore()

print_method(curr_node)

################################################