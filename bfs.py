from collections import deque

start_state = [8,12,2020]
end_state = [8,12,2021]
grid_size = [10,15]
tt_channel = {}

inspected_states = []

#BFS

bfs_list = deque([])

class Node:
    def __init__(self, loc, par, cost):
        self.location = loc
        self.parent = par
        self.cost = cost

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.location==other.location
        else:
            return False

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


def adder(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2])

def valid_points(node):
    directions = [[0,1], [1,0], [1,1], [-1, 0], [0, -1], [-1,-1], [-1, 1], [1, -1]]
    valid = []
    if tuple(node.location) in tt_channel.keys():
        valid.append(tt_channel.get(tuple(node.location)))
    for pos in directions:
        temp = adder(node.location, pos)
        if temp[0]<grid_size[0] and temp[1]<grid_size[1] and temp[0] >= 0 and temp[1]>= 0:
            valid.append(temp)
    return valid


explored_set = set()

def explore():
    bfs_list.append(Node(start_state, None, 0))

    SUCCESS=0
    while(len(bfs_list)!=0):
        curr_node = bfs_list.popleft()
        if curr_node.location == end_state:
            print('Success')
            SUCCESS=1
            return curr_node

        print(curr_node.location)

        explored_set.add(curr_node)

        next_locations = valid_points(curr_node)
        for point in next_locations:                    ## IF CODE DOESN'T WORK THIS IS THE FIRST PLACE TO CHECK!
            if tuple(point) not in [x.location for x in explored_set]:
                checker = 0
                for node in bfs_list:
                    if point == node.location:
                        checker=1
                        break
            if checker:
                    continue
                    #CHANGE FOR OTHER ALGs
            bfs_list.append(Node(point, curr_node, curr_node.cost+1)) ## NOTE THE COST IS ONLY FOR BFS
    print("FAIL")
    print(len(explored_set))



################################################

# TEST RUN FOR BFS

curr_node = explore()
#
# while(curr_node!=None):
#     print(curr_node.location)
#     curr_node = curr_node.parent

################################################