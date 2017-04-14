import re

expr = re.compile(r'foo')
list1 = ['afoot', 'catfoot', 'dogfoot', 'fanfoot', 'foody', 'foolery', 'foolish', 'fooster',
         'footage', 'foothot', 'footle', 'footpad', 'footway', 'hotfoot', 'jawfoot', 'mafoo',
         'nonfood', 'padfoot', 'prefool', 'sfoot', 'unfool']
list2 = ['Atlas', 'Aymoro', 'Iberic', 'Mahran', 'Ormazd', 'Silipan', 'altered', 'chandoo', 'crenel',
         'crooked', 'fardo', 'folksy', 'forest', 'hebamic', 'idgah', 'manlike', 'marly', 'palazzo',
         'sixfold', 'tarrock', 'unfold']

res1 = list(filter(lambda x: re.search(expr, x), list1))
res2 = list(filter(lambda x: re.search(expr, x), list2))

if len(res1) == len(list1) and len(res2) == 0:
    print("Well done")
