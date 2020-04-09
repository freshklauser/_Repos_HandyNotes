# -*- coding: utf-8 -*-
# @Author: KlausLyu
# @Date:   2020-04-08 15:31:14
# @Last Modified by:   sniky-lyu
# @Last Modified time: 2020-04-08 22:16:22


'''
<AttrDisplay> tips:
    运算符重载：__init__, __str__ (截获并处理内置的操作)
        __init__: 构造函数，初始化一个新创建的示例Instance
        __str__: 打印一个对象会显示对象的__str__方法所返回的内容
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

    def _gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('{}={}'.format(key, getattr(self, key)))
        return ', '.join(attrs)

    def __str__(self):
        return '[{}: {}]'.format(self.__class__.__name__, self._gatherAttrs())


class ClassTree:
    """
    Climb inheritance trees using namespace links, displaying higher superclasses
    with indentation
    """

    def classTree(self, cls, indent):
        print('.' * indent + cls.__name__)
        for supercls in cls.__bases__:              # recur to all superclasses
            self.classTree(supercls, indent + 3)

    def instanceTree(self, inst, indent=3):
        print('Tree of {}'.format(inst))
        self.classTree(inst.__class__, indent)

    def selftest(self):
        class A:
            pass

        class B(A):
            pass

        class C(A):
            pass

        class D(B, C):
            pass

        class E:
            pass

        class F(D, E):
            pass

        self.instanceTree(B())
        self.instanceTree(F())


if __name__ == '__main__':
    ClassTree().selftest()
