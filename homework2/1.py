class PublicMeta(type):
    @staticmethod
    def pretty_func(self):
        print('Some useful message')

    def do_things(self):
        print(self.var)

    def __new__(mcs, cls_name, cls_parents, cls_attr):
        skip = len(cls_name)+3
        buf = ((name, value) for name, value in cls_attr.items() if name.startswith('_' + cls_name))
        for name, value in buf:
            cls_attr.pop(name)
            cls_attr.update({name[skip:]: value})
        cls_attr.update({'pretty_func': PublicMeta.pretty_func, 'do_things': PublicMeta.do_things})
        return type(cls_name, cls_parents, cls_attr)


class MyClass(metaclass=PublicMeta):
    __var = 1
    another_var = 2


inst = MyClass()
print(inst.var)
inst.pretty_func()
inst.do_things()
