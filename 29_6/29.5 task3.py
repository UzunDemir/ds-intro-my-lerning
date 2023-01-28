from collections import deque
import collections

# Функция bfs возвращает True, если
# результат поиска в ширину элемента
# desired в дереве tree, начиная с
# элемента start, удачен, и False,
# если нет.
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


def test_bfs():
    tree = {
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
    if bfs(tree, 1, 11):
        print('OK')
    if bfs(tree, 1, 6):
        print('OK')
    if bfs(tree, 2, 10):
        print('OK')
    if not bfs(tree, 2, 11):
        print('OK')
    if bfs(tree, 4, 12):
        print('OK')
    if not bfs(tree, 4, 10):
        print('OK')


def main():
    test_bfs()


if __name__ == '__main__':
    main()