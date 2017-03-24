def decorator(func):
    def func_wrapper(x, y, **kwargs):
        try:
            result = func(x, y)
        except Exception as err:
            print('Exception occurred in func: %s' % err)
            print('Input args: {0} {1}'.format(x, y))
            print('Input kwargs: {0}'.format(kwargs))

            result = None
        return result
    return func_wrapper

@decorator
def func(x, y, **kwargs):
    return x / y


print(func(10, 0, op='division', base=10))
