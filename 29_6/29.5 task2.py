
# Функция принимает на вход строку, которая
# состоит из скобок трех типов: круглые, квадратные
# и фигурные. Функция должна проверить, является ли
# переданная последовательность скобок сбалансированной
# или нет. Функция возвращает True, если последовательность
# сбалансирована, и False – в противном случае.
def is_balanced(line):
    # Словарь со значениями (каждой открытой скобке соответсвует ее закрытая пара)
    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    opened = '([{'                                       # Список для проверки если скобка открытая
    stack_for_symbols = []                               # Стэк, в который сверху кладем скобки и берем сверху,
                                                         # если нашли ей пару
    result = 'True'                                      # Конечный результат

    for i in range(len(line)):                           # Цикл перебора каждого элемента подаваемого списка line
        if line[i] in opened:                            # Если элемент одна из открытых скобок
            stack_for_symbols.append(line[i])            # ...то присоединим его к стэку
        else:                                            # Иначе, если элемент - закрытая скобка
            if len(stack_for_symbols) != 0:              # ...то если стэк уже имеет какие-то элементы
                if stack_for_symbols[-1] == pairs.get(line[i]): # то если верхний элемент стэка - открытая пара скобки
                    stack_for_symbols.pop()                     # то удалим его со стэка, так как для него нашлась пара
                else:                               # иначе верхний элемент стэка - тоже закрытая скобка, это уже False
                    break                           # Поэтому можно остановить цикл for
            else:                                   # иначе стэк пустой и есть закрытая скообка - False
                stack_for_symbols = ['Х']           # Заполним стэк чем-то, так как полный стэк - False
    if len(stack_for_symbols) != 0:                 # Если стэк не пустой
        result = 'False'                            # То это - False
    return result == 'True'                         # Для решения задания требуется вывод булевого значения


def test_is_balanced():
    cases = {
        '((((((((())))))))': False,
        '{[()]}{{}}': True,
        '{[()]}{]{}}': False,
        '{{{((([[[]]])))}}}': True,
        '{}': True,
        '(': False,
        '(}': False,
        '(((())))[]{}': True,
        '((()': False,
        '[{}{})(]': False,
        '{[]{([[[[[[]]]]]])}}': True,
        '{[]{([[[[[[]])]]])}}': False,
    }
    for i, case in enumerate(cases.keys()):
        if is_balanced(case) == cases[case]:
            print(f'{i}: OK')
        else:
            print(f'{i}: Not OK')


def main():
    test_is_balanced()


if __name__ == '__main__':
    main()