######################## ASSIGNMENT 1 ##################################

# By Abhivineet Veeraghanta

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
    a = (int(temp[1]), int(temp[2]), int(temp[0]))
    b = (int(temp[1]), int(temp[2]), int(temp[3]))
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


print(tt_channel)