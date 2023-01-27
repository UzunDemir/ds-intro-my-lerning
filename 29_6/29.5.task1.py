import random


# Функция bubble_sort принимает список целых чисел
# data и сортирует его в порядке убывания элементов с
# помощью пузырьковой сортировки. Кроме того, функция
# должна посчитать количество операций (итераций цикла),
# которые выполняет алгоритм, и вернуть это число вызывающей
# стороне.
def bubble_sort(data):
    counter_i = 0
    counter_j = 0

    for i in range(len(data)):
        for j in range(len(data) - counter_i - 1):
            if data[j] < data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            counter_j += 1
        counter_i += 1
    return counter_j



def test_sorted():
    data = [random.randint(0, 1000) for i in range(100)]
    print(data)
    data_to_sort = data.copy()
    bubble_sort(data_to_sort)
    if data_to_sort == sorted(data, reverse=True):
        print('OK')
    else:
        print('NOT OK')


def make_observations():
    size = 10
    results = []
    for i in range(100):
        data = [random.randint(0, 1000) for i in range(size)]
        results.append((size, bubble_sort(data)))
        size += 10
    return results


def main():
    test_sorted()
    with open('bubble.csv', 'w') as file:
        file.write(f'size, iterations\n')
        for row in make_observations():
            file.write(f'{row[0]}, {row[1]}\n')
    print('Done!')


if __name__ == '__main__':
    main()



