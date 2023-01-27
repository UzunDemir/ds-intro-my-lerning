import random

def bubble_sort(data):
    counter_i = 0
    counter_j = 0

    for i in range(len(data)):
        for j in range(len(data) - counter_i - 1):
            if data[j] < data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            counter_j += 1
        counter_i += 1

    print('sorted', counter_i, counter_j, len(data), data)

    counter_i = 0
    counter_j = 0
    for i in range(len(data)):
        for j in range(len(data) - 1):
            if data[j] < data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            counter_j += 1
        counter_i += 1
    print('sorted', counter_i, counter_j, len(data), data)


data = [random.randint(0, 1000) for i in range(10)]
print('unsorted', data)
data_to_sort = data.copy()
bubble_sort(data_to_sort)

def is_balanced(line):
    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    opened = '([{'
    closed = ')]}'
    stack_for_symbols = ['']
    result = 'True'
    print(line)



    for i in range(len(line)):
        
        print('control', i, 'stack', stack_for_symbols)

        if line[i] in opened:
            # print(line[i])
            if line[i] != stack_for_symbols[-1]:
                stack_for_symbols.append(line[i])
                print(i, stack_for_symbols)

        if line[i] in closed:
            # print('cllllll')
            if len(stack_for_symbols) > 1:
                # print('jhj')
                if stack_for_symbols[-1] == pairs.get(line[i]):
                    print('999999999999', stack_for_symbols[-1], line[i])
                    stack_for_symbols.pop()
                    print('closed', stack_for_symbols)
                    if len(stack_for_symbols) > 1:
                        result = 'False'


    if len(stack_for_symbols) > 1:
        result = "False"
    print(result)








line = '(()'
is_balanced(line)


