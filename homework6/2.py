import re

expr = re.compile(r'fu$')
list1 = ['fu', 'tofu', 'snafu']
list2 = ['futz', 'fusillade', 'functional', 'discombobulated']

res1 = list(filter(lambda x: re.search(expr, x), list1))
res2 = list(filter(lambda x: re.search(expr, x), list2))

if len(res1) == len(list1) and len(res2) == 0:
    print("Well done")
