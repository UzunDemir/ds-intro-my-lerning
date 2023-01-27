def is_balanced(line):
    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    opened = '([{'
    closed = ')]}'
    stack_for_symbols = []
    result = 'True'
    print(line)


    for i in range(len(line)):
        print(line[i])
        if line[i] in opened:
            stack_for_symbols.append(line[i])
            print(stack_for_symbols)
        else:
            print('hhhhhhhhhhhhhhhhhhhhh')
            if len(stack_for_symbols) != 0:
                if stack_for_symbols[-1] == pairs.get(line[i]):
                    stack_for_symbols.pop()
                    print(len(stack_for_symbols))
                else:
                    print('stop')
                    break
            else:
                stack_for_symbols = ['Х']
    if len(stack_for_symbols) != 0:
        result = 'False'
    print(result, len(stack_for_symbols))




line = '{[()]}{]{}}'
is_balanced(line)
