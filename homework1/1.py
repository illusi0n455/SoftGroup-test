def like(numbers, a_set, b_set):
    likes = 0
    a_set = a_set.split()
    b_set = b_set.split()
    for i in numbers.split():
        if i in a_set:
            likes += 1
        if i in b_set:
            likes -= 1
    return likes


numbers = '1 4 10 20 1 11 12'
a = '1 4 1 12'
b = '1 12 10 20'
print(like(numbers, a, b))
