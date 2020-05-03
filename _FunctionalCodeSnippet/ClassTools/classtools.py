# -*- coding: utf-8 -*-
# @Author: KlausLyu
# @Date:   2020-04-08 15:31:14
# @Last Modified by:   sniky-lyu
# @Last Modified time: 2020-05-01 17:15:58


'''
Theme: 定制类、实例属性显示
Functions:
    InstanceAttrDisplay:  实例属性显示
    InheritedAttrDisplay: 继承属性显示
    ClassTreeAttributesDisplay： 类和属性树显示

Tips:
    运算符重载：__init__, __str__ (截获并处理内置的操作)
        __init__: 构造函数，初始化一个新创建的示例Instance
        __str__: 打印一个对象会显示对象的__str__方法所返回的内容
        __dict__: 实例属性instance attribute 命名空间
    getattr():
        getattr() 函数用于返回一个对象属性值。
        语法：
        getattr(object, name[, default])
            object：对象。
            name：字符串，对象属性。
            default：默认返回值，如果不提供该参数，在没有对应属性时，将触发 AttributeError。
        内置函数getattr执行继承搜索协议，__dict__不会继承搜索

    <20200501, KlausLyu>
    1) 如果在类中定义了__getitem__()方法，那么他的实例对象（假设为P）就可以这样P[key]取值。
    当实例对象做P[key]运算时，就会调用类中的__getitem__()方法;
    2) 可以让对象实现迭代功能（对象可迭代的前提下）
        -- 解释器需要迭代对象x时， 会自动调用iter(x)方法。内置的 iter(x) 方法有以下作用
           检查对象是否实现了__inter__ 方法，如果实现了就调用它（也就是我们偶尔用到的特殊方法重载），获取一个迭代器。
        -- 如果没有实现iter()方法， 但是实现了 __getitem__方法，Python会创建一个迭代器，尝试按顺序
          （从索引0开始，可以看到我们刚才是通过s[0]取值）获取元素。
        -- 如果尝试失败，Python抛出TypeError异常，通常会提示TypeError: '***' object is not iterable。
    Example:

    序列最重要的特征就是可包含多个元素， 因此和序列有关的特殊方法有如下几个：
        __len__(self)：该方法的返回值决定序列中元素的个数。
        __getitem__(self, key)：该方法获取指定索引对应的元素。该方法的 key 应该是整数值或 slice 对象，否则该方法会引发 KeyError 异常。
        __contains__(self, item)：该方法判断序列是否包含指定元素。
        __setitem__(self, key, value)：该方法设置指定索引对应的元素。该方法的 key 应该是整数值或 slice 对象，否则该方法会引发 KeyError 异常。
        __delitem__(self, key)：该方法删除指定索引对应的元素。


    修改记录：
        【20200501，KlausLyu】:
            添加关于 __getitem__ 魔方方法的内容到 docstring
'''


import os


class InstanceAttrDisplay:
    '''实例属性
    Provides an inheritable print overload method that displays instances with
    their class names and a name=value pair for each attrbute stored on the instance
    itself(but not attrs inherited from its classes). Can be mixed into any class,
    and will work on any instance
    '''

    def __str__(self):
        '''
        相比于__repr__, print(inst)会优先调用__str___
        '''
        return '<Instance of {}, address {}:\n{}>'.format(
            self.__class__.__name__,
            id(self),
            self.__gatherAttrs())

    def __repr__(self):
        '''
        理论上，__repr__对任何地方用于实例的打印或字符串转换的显示, 除了当定义了一个__str__时
        '''
        return '<{}: {}>'.format(self.__class__.__name__, self.__gatherAttrs())

    def __gatherAttrs(self):
        attrs = ''
        for key in sorted(self.__dict__):
            # format第二参数：self.__dict__[key] 不执行继承搜索, getattr(self, key)会执行继承搜索
            attrs += "\tname: {}={}\n".format(key, self.__dict__[key])
        return attrs


class InheritedAttrDisplay:
    '''实例属性+继承属性
    Use dir() to collect both instance attrs and names inherited from its classes.
    '''

    def __str__(self):
        '''
        相比于__repr__, print(inst)会优先调用__str___
        '''
        return '<Instance of {}, address {}:\n{}>'.format(
            self.__class__.__name__,
            id(self),
            self.__gatherAttrs())

    def __gatherAttrs(self):
        attrs = ''
        for attr in dir(self):                          # Instance dir()
            if attr[:2] == "__" and attr[-2:] == "__":  # Skip internal attrs
                attrs += '\tname: {}=<>\n'.format(attr)
            else:
                attrs += '\tname: {}={}\n'.format(attr, getattr(self, attr))
        return attrs


class ClassTreeAttributesDisplay:
    """类树+属性树
    Mix-in that returns an __str__ trace of the entire class tree and all its
    objects' attrs at and above self; run by print() or str() returns constructed string;
    use __x attr names to avoid impacting clients;
    use generator expr to recurse to superclasses;
    use str.format() to make substitutions clearer
    """

    def __str__(self):
        self.__visited = {}
        return '<Instance of {}, address {}:\n{}{}>'.format(
            self.__class__.__name__,
            id(self),
            self.__gatherAttrs(self, 0),
            self.__gatherClass(self.__class__, 4))

    def __gatherClass(self, aClass, indent):
        dot_prefix = '.' * (indent + 4)
        if aClass in self.__visited.keys():
            return '\n{0}<Class {1}, address {2}: (see above)>\n'.format(
                dot_prefix,
                aClass.__name__,
                id(aClass))
        else:
            self.__visited[aClass] = 1              # 1: 访问过
            supercls_iter = (self.__gatherClass(c, indent + 4) for c in aClass.__bases__)
            return '\n{0}<Class {1}, address {2}:\n{3}{4}{5}\n>'.format(
                dot_prefix,
                aClass.__name__,
                id(aClass),
                self.__gatherAttrs(aClass, indent),
                ''.join(supercls_iter),
                dot_prefix)

    def __gatherAttrs(self, obj, indent):
        '''
        获取并返回每个obj中的属性 key=value
        Arguments:
            obj {class or instance} -- 类或实例
            indent {int} -- 缩进
        '''
        space_prefix = ' ' * (indent + 4)
        attrs = ''
        for attr in sorted(obj.__dict__):
            if attr.startswith('__') and attr.endswith('__'):
                attrs += space_prefix + '{}=<>\n'.format(attr)
            else:
                attrs += space_prefix + '{}={}\n'.format(attr, getattr(obj, attr))
        return attrs


def create_directory(dir_name):
    '''创建文件夹(如果文件夹不存在)

    Arguments:
        dir_name {str} -- [文件夹名称]

    Returns:
        [int] -- [创建文件夹的状态 1：文件夹已存在或创建成功； 0：创建失败]
    '''
    dir_abspath = os.path.join(os.getcwd(), dir_name)        # 路径连接
    # print(os.getcwd(), dir_abspath)
    try:
        if os.path.exists(dir_abspath):
            dir_status = 1
            print('%s 文件夹已经存在' % dir_name)
            return dir_status
        os.mkdir(dir_abspath)
    except Exception as e:
        print(e)
        dir_status = 0
    else:
        print('%s 文件夹创建成功' % dir_name)
        dir_status = 1
    return dir_status


if __name__ == '__main__':
    try:
        x = 1 / 0
    except ZeroDivisionError:
        import sys
        print(sys.exc_info(), '-->', len(sys.exc_info()))
        # (<class 'ZeroDivisionError'>, ZeroDivisionError('division by zero',), <traceback object at 0x0000024219FE9A48>) --> 3
        print('Uncaught!', sys.exc_info()[0], '----', sys.exc_info()[1])
        # sys.exc_info()[0]: 引发异常的类
        # sys.exc_info()[1]: 引发异常的实例对象

        sta = create_directory('logs')
        print(sta)
