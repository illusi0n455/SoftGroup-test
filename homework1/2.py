funcs = [oct, hex, bin]


def fineprint(n):
    for i in range(1, n + 1):
        row = str(i).ljust(10, ' ')
        for func in funcs:
            row += func(i)[2:].ljust(10, ' ')
        print(row)


fineprint(15)
