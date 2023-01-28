import collections
def bfs(tree, start, desared):
    result = 'False'
    visited, queue = set(), collections.deque([start])
    visited.add(start)
    while queue:
        print(queue, visited)
        vertex = queue.popleft()
        for neighbour in tree[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    if desared in  visited:
        result = 'True'
    return result == 'True'

if __name__ == '__main__':
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
    bfs(graph, 2, 10)