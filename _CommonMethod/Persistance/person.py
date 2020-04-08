# -*- coding: utf-8 -*-
# @Author: KlausLyu
# @Date:   2020-04-08 11:11:57
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-08 17:16:51

'''
运算符重载：__init__, __str__ (截获并处理内置的操作)
    __init__: 构造函数，初始化一个新创建的示例Instance
    __str__: 打印一个对象会显示对象的__str__方法所返回的内容
super()用法：
    refer: https://mozillazg.com/2016/12/python-super-is-not-as-simple-as-you-thought.html
getattr():
    getattr() 函数用于返回一个对象属性值。
    语法：
    getattr(object, name[, default])
        object：对象。
        name：字符串，对象属性。
        default：默认返回值，如果不提供该参数，在没有对应属性时，将触发 AttributeError。
'''

class AttrDisplay:
    '''
    Provides an inheritable print overload method that displays instances with
    their class names and a name=value pair for each attrbute stored on the instance
    itself(but not attrs inherited from its classes). Can be mixed into any class,
    and will work on any instance
    '''
    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('{}={}'.format(key, getattr(self, key)))
        return ','.join(attrs)

    def __str__(self):
        return '[{}: {}]'.format(self.__class__.__name__, self.gatherAttrs())


class Person(AttrDisplay):
    """
    继承实例属性显示__str__的封装类
    Extends:
        AttrDisplay
    """
    THEME = 'person class'

    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay

    def lastName(self):
        return self.name.split()[-1]

    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))


class Manager(Person):
    def __init__(self, name, pay):                      # name, pay 本地变量
        # Person.__init__(self, name, 'manager', pay)   # 调用Person的__init__方法初始化Manager, 继承Person的属性
        super().__init__(name, 'AreaManager', pay)      # 调用父类super class 的 __init__ 方法来继承 父类 的属性

    def giveRaise(self, percent, bonus=0.1):
        # Person.giveRaise(self, percent + bonus)       # 需要 传入 self, self代表的是Person类的实例
        super().giveRaise(percent + bonus)              # 不需要传入self, super()相当于实例化了一个 super 类


if __name__ == '__main__':
    bob = Person("Bob Smith")
    sue = Person("Sue Jones", job='dev', pay=10000)
    # print(sue)                                  # [Person: Sue Jones, 100000]
    # print(bob.lastName(), sue.lastName())
    sue.giveRaise(0.1)
    # print(sue.pay)
    tom = Manager('Tom Jones', 50000)
    # print(tom)
    tom.giveRaise(0.1)
    # print(tom)
    # print(tom.lastName())
    print(sue.THEME)
    print(tom.THEME)

    print('--- All three --')
    for object in (bob, sue, tom):
        object.giveRaise(0.1)
        print(object)
