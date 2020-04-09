# -*- coding: utf-8 -*-
# @Author: sniky-lyu
# @Date:   2020-04-08 21:48:40
# @Last Modified by:   sniky-lyu
# @Last Modified time: 2020-04-09 21:49:09


'''
Docstr Tips:
    To obtain the docstr if this module, pls go to <conda prompt>, then cd to current
    module path, typing the command below:
        pydoc person > person.docstr
    The docstring file is saved as person.docstr (or any file suffix you perfer)
'''

from classtools import AttrDisplay, ClassTree


class Person(AttrDisplay):
    """
    继承实例属性显示__str__的封装类
    Extends:
        AttrDisplay
    """

    def __init__(self, name, job=None, pay=0):
        '''
        Arguments:
            name {[str]} -- [person name]

        Keyword Arguments:
            job {[str]} -- [person job] (default: {None})
            pay {float} -- [salary] (default: {0})
        '''
        self.name = name
        self.job = job
        self.pay = pay

    def lastName(self):
        '''
        Returns:
            [str] -- [the lastname of person]
        '''
        return self.name.split()[-1]

    def giveRaise(self, percent):
        '''
        Arguments:
            percent {[float]} -- [percentage of salary increment]
        '''
        self.pay = int(self.pay * (1 + percent))


class Manager(Person):
    def __init__(self, name, pay):                      # name, pay 本地变量
        # Person.__init__(self, name, 'manager', pay)   # 调用Person的__init__方法初始化Manager, 继承Person的属性
        super().__init__(name, 'Manager', pay)      # 调用父类super class 的 __init__ 方法来继承 父类 的属性

    def giveRaise(self, percent, bonus=0.1):
        # Person.giveRaise(self, percent + bonus)       # 需要 传入 self, self代表的是Person类的实例
        super().giveRaise(percent + bonus)              # 不需要传入self, super()相当于实例化了一个 super 类


if __name__ == '__main__':
    bob = Person("Bob Smith")
    sue = Person("Sue Jones", job='dev', pay=10000)
    tom = Manager('Tom Jones', 50000)
    sue.giveRaise(0.1)
    tom.giveRaise(0.1)
    print('--- All three --')
    for object in (bob, sue, tom):
        object.giveRaise(0.1)
        print(object)
    print()
    # print(object.__dict__, dir(object))

    # class tree
    ClassTree().instanceTree(tom)
    print()

    x = Manager
    print(x.mro())
    # 列表：[<class '__main__.Manager'>, <class '__main__.Person'>, <class 'classtools.AttrDisplay'>, <class 'object'>]
    print(x.__mro__)
    # 元组：(<class '__main__.Manager'>, <class '__main__.Person'>, <class 'classtools.AttrDisplay'>, <class 'object'>)
