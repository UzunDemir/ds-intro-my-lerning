
import collections
from collections import deque
graph = {
        1: [2, 3, 4],
        2: [5, 6],
        3: [],
        4: [7, 8],
        5: [9, 10],
        6: [],
        7: [11, 12],
        8: [],
        9: [],
        10: [],
        11: [],
        12: []
    }
visited = [] # List to keep track of visited nodes.
queue = []   # Initialize a queue
def bfs(visited, graph, node):
    print(visited, graph, node)
    global queue
    visited.append(node)
    queue.append(node)
    while queue:
        s = queue.pop(0)
        print (s, end = " ")
        for neighbour in graph[s]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
# Driver Code
bfs(4, graph, 10)