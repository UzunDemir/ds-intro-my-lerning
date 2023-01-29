from collections import deque
import collections


# Функция bfs возвращает True, если
# результат поиска в ширину элемента
# desired в дереве tree, начиная с
# элемента start, удачен, и False,
# если нет.
def bfs(tree, start, desared):
    result = 'False'  #
    visited, queue = set(), collections.deque([start])  # Создадим множества, visited - которые посетили,
    # queue - очередь для посещения
    # Множества примечательны тем, что операция проверки “принадлежит ли объект множеству” происходит значительно
    # быстрее аналогичных операций в других структурах данных.
    visited.add(start)  # Добавим в посещенные начало нашего давижения по графу
    while queue:  # Пока есть очередь
        vertex = queue.popleft()  # удалим из нее слева элемент и перенесем в переменную "вершина"
        for neighbour in tree[vertex]:  # Для соседей посещенной вершины
            if neighbour not in visited: # если сосед не был посещен
                visited.add(neighbour) # добавить соседа в посещенные
                queue.append(neighbour) # добавить в очередь соседа
    if desared in visited: # проверим, если искомый элемент графа есть в множестве, то есть, его посетили
        result = 'True'
    print(result, visited)
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
