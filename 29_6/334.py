from collections import deque
# Функция bfs возвращает True, если
# результат поиска в ширину элемента
# desired в дереве tree, начиная с
# элемента start, удачен, и False,
# если нет.
def bfs(tree, start, desired):
    pairs = list(zip(tree.keys(), tree.values()))
    for_control = []
    work_list = pairs[start -1]
    print(work_list)
    for_control = work_list[1]
    len_for_control = len(for_control)
    result = 'True'
    i = 0
    while result == 'True':
        print(for_control[i])
        next = pairs[for_control[i]-1][1]
        #if len(for_control) != 0:
        for_control.pop(0)

        if len(next) != 0:
            for_control.pop(0)

            for_control.extend(next)
            print(for_control, next, i)



    return True



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