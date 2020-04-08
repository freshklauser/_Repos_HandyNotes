# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2020-04-07 21:36:25
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-08 08:31:58

'''Tips
a.__dict__: {'data': 'abcabcabc', 'name': 'kk', 'grade': 4}
            定义的当前类 ThirdClass 赋值了的属性 （不包括继承的父类的属性）
a.__str__:  print(class_instance), 可以用来规范化打印格式
'''


class FirstClass:
    def setdata(self, value):
        self.data = value
        self.name = 'kitty'
        self.age = 18

    def display(self):
        print(self.data)


class SecondClass(FirstClass):          # inherits setdata
    def display(self):                  # chages display
        print("Current value = '%s'" % self.data)


class ThirdClass(SecondClass):          # Inherits from SecondClass
    def __init__(self, value):
        self.data = value
        self.name = 'sue'
        self.grade = 4

    def __add__(self, others):
        return ThirdClass(self.data + others)

    def __str__(self):
        return '[ThirdClass: %s]' % self.data

    def mul(self, others):
        self.data *= others

    def plotFig(self):
        print("Plot Figures Here")

    def upperName(self):
        return self.name.upper()


if __name__ == '__main__':
    a = ThirdClass('abc')       # __init__ called
    a.display()                 # Current value = 'abc'     <--- Inherited method called
    print(a)                    # [ThirdClass: abc]         <---- __str__
    print(a.upperName())
    a.mul(3)                    #
    print(a)                    # [ThirdClass: abcabcabc]   <---- __str__
    print(a.__str__())          # [ThirdClass: abcabcabc]
    print()
    b = a + 'xyz'
    b.display()                 # Current value = 'abcabcabcxyz'
    print(b)                    # [ThirdClass: abcabcabcxyz]

    print(list(a.__dict__.keys()))  # ['data', 'name', 'grade']
    print(a.__dict__)               # {'data': 'abcabcabc', 'name': 'kk', 'grade': 4}

    print()

    print(a.__class__)
    print(__name__)
