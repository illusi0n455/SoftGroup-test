import re


def func(x):
    try:
        if re.split(expr, x)[1] == x:
            return True
        else:
            return False
    except:
        return False


expr = re.compile(r'(.*fu)')
list1 = ['fu', 'tofu', 'snafu']
list2 = ['futz', 'fusillade', 'functional', 'discombobulated']

res1 = list(filter(func, list1))
res2 = list(filter(func, list2))

if len(res1) == len(list1) and len(res2) == 0:
    print("Well done")
