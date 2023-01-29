# Depth-first search
# Поиск в глубину (англ. Depth-first search, DFS) — один из методов обхода графа.
# Стратегия поиска в глубину, как и следует из названия, состоит в том,
# чтобы идти «вглубь» графа, насколько это возможно.


# 1. Проверяем, посещён ли текущий узел. Если да, то он добавляется в соответствующий набор.
# 2. Функция повторно вызывается для каждого соседа узла.
# 3. Если нашли desared, то можно остановить и выйти с 'True' иначе ищем до конца и выходим с 'False'

def loop(visited, graph, node, desared):                            # loop принимает из dfs значения и node -
    if node not in visited:                                         # если проверяемый не в visited
        visited.add(node)                                           # то добавляем его к visited
        for neighbor in graph[node]:                                # для его подчиненного соседа
            loop(visited, graph, neighbor, desared)                 # повторяем loop
    if desared in visited:                                          # если дошли до искомого, то путь к нему установлен
        result = 'True'                                             # присвоим флаг и выйдем, чтобы по всему графу
    else:                                                           # не ходить
        result = 'False'
    return result


def dfs(tree, start, desared):                                     # подали данные как требуется
    visited = set()                                                # организуем множество
    graph = tree                                                   # готовим данные для loop
    node = start
    result = loop(visited, graph, node, desared)                   # принимаем флаг из loop
    return result == 'True'







def test_dfs():
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
    if dfs(tree, 1, 11):
        print('OK')
    if dfs(tree, 1, 6):
        print('OK')
    if dfs(tree, 2, 10):
        print('OK')
    if not dfs(tree, 2, 11):
        print('OK')
    if dfs(tree, 4, 12):
        print('OK')
    if not dfs(tree, 4, 10):
        print('OK')


def main():
    test_dfs()


if __name__ == '__main__':
    main()
