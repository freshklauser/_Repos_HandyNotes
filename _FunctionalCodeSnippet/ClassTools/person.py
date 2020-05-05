# -*- coding: utf-8 -*-
# @Author: sniky-lyu
# @Date:   2020-04-08 21:48:40
# @Last Modified by:   sniky-lyu
# @Last Modified time: 2020-05-03 13:06:31


'''
Docstr Tips:
    To obtain the docstr if this module, pls go to <conda prompt>, then cd to current
    module path, typing the command below:
        pydoc person > person.docstr
    The docstring file is saved as person.docstr (or any file suffix you perfer)

运算符重载：__init__, __str__ (截获并处理内置的操作)
    __init__: 构造函数，初始化一个新创建的示例Instance
    __str__: 打印一个对象会显示对象的__str__方法所返回的内容
    __getattr__: 拦截未定义的属性获取
    __getattribute__: 拦截所有的属性获取（慎用）
    __del__: 删除对象，当系统要收回对象时，会自动调用__del__方法。当使用del() 手动删除变量指向的对象时，
             则会减少对象的引用计数。如果对象的引用计数不为1，那么会让这个对象的引用计数减1，
             当对象的引用计数为0的时候，则对象才会被真正删除（内存被回收）

getattr():
    getattr() 函数用于返回一个对象属性值。
    语法：
    getattr(object, name[, default])
        object：对象。
        name：字符串，对象属性。
        default：默认返回值，如果不提供该参数，在没有对应属性时，将触发 AttributeError。
'''

from decorators import decorator_timmer
from classtools import InstanceAttrDisplay, InheritedAttrDisplay
from classtools import ClassTreeAttributesDisplay


class Person(ClassTreeAttributesDisplay):
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

    def __getattr__(self, attrname):
        '''
        拦截未定义的属性，如果属性不存在，raise异常
        Arguments:
            attrname  -- attribute intercepted
        Returns:
            self.attrname
        Raises:
            AttributeError -- 属性不存在异常
        '''
        if attrname in self.__dict__.keys():
            return self.__dict__[attrname]
        elif attrname == 'department':
            self.__dict__[attrname] = 'sales department'  # 新增性并返回, 用self.__dict__[attrname]而不是self.attrname
            return self.__dict__[attrname]
            # self.attrname = 'sales'                    # 'attrname': 'sales', 属性名编程了 attrname 而不是预期的 department
            # return self.attrname
        else:
            raise AttributeError("Attribute '{}' is not existed".format(attrname))

    def __del__(self):
        ''' 对象回收 '''
        print('对象{}被销毁'.format(self.__class__.__name__))

    def lastName(self):
        '''
        Returns:
            [str] -- [the lastname of person]
        '''
        return self.name.split()[-1]

    # @decorator_timmer
    def giveRaise(self, percent):
        '''
        Arguments:
            percent {[float]} -- [percentage of salary increment]
        '''
        self.pay = int(self.pay * (1 + percent))

    @property
    def getJob(self):
        return self.job


class Manager(Person):
    def __init__(self, name, pay):                      # name, pay 本地变量
        # Person.__init__(self, name, 'manager', pay)   # 调用Person的__init__方法初始化Manager, 继承Person的属性
        super().__init__(name, 'Manager', pay)      # 调用父类super class 的 __init__ 方法来继承 父类 的属性

    @decorator_timmer
    def giveRaise(self, percent, bonus=0.1):
        # Person.giveRaise(self, percent + bonus)       # 需要 传入 self, self代表的是Person类的实例
        super().giveRaise(percent + bonus)              # 不需要传入self, super()相当于实例化了一个 super 类


if __name__ == '__main__':
    bob = Person("Bob Smith")
    tom = Manager('Tom Jones', 50000)
    sue = Person("Sue Jones", job='dev', pay=10000)
    sue.giveRaise(0.1)
    tom.giveRaise(0.1)
    # print('--- All three --')
    # for object in (bob, sue, tom):
    #     object.giveRaise(0.1)
    #     print(object)
    print(tom.lastName())
    print(tom.department)
    # print(tom.__dict__['department'])
    print(tom.pay, end='\n\n')
    # print(tom.salary)
    print(tom.__dict__)         #
    print(bob.__dict__)
    print(sue.__dict__)
    # print(object.__dict__, dir(object))
    print()

    x = Manager
    print(type(x), x.__class__.__name__)
    print(x.mro())
    # 列表：[<class '__main__.Manager'>, <class '__main__.Person'>, <class 'classtools.AttrDisplay'>, <class 'object'>]
    # print(x.__mro__)
    # 元组：(<class '__main__.Manager'>, <class '__main__.Person'>, <class 'classtools.AttrDisplay'>, <class 'object'>)

    # class tree
    # ClassTreeDisplay().instanceTree(tom)
    # print(tom)

    # del tom             # 删除对象，会自动调用__del__方法，当计数为0时完全删除
    # print(tom)        # 手动del后，tom不存在了（由于这里tom的引用计数只有1，所有del后为0，直接回收）
    print('over-----------------')

    # 不加 @property: lastName方法需要按照方法的规则调用， Person().lastName()   --- lastName() 后的()不能少
    print("tom's lastName: ", tom.lastName())
    # 加 @property: getJob方法利用属性进行了装饰, 需要按照属性的规则调用， Person().getJob   --- getJob后不能加()
    print("tom's job: ", tom.getJob)

    print(tom, file=open('class_tree.txt', 'w'))
