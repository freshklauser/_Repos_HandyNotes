# -*- coding: utf-8 -*-
# @Author: KlausLyu
# @Date:   2020-04-10 11:29:50
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-10 11:42:33

'''{基于类的异常 自定义}
sys.exc_info():
    return tuple(type, value, traceback)
        type: 正在处理的异常的异常类型
        value: 引发的异常类实例
        traceback: 代表异常最初发生时所调用的堆栈

Exception:
    BaseException的子类，是所有其他内置异常的超类，除了系统退出事件类之外(SystemExit, KeyboardInterrupt和GeneratorExit)
    几乎所有的用户定义的类都应该继承Exception，而不是BaseException
'''


if __name__ == '__main__':
    try:
        x = 1 / 0
    except:
        import sys
        print(sys.exc_info(), '-->', len(sys.exc_info()))
        # (<class 'ZeroDivisionError'>, ZeroDivisionError('division by zero',), <traceback object at 0x0000024219FE9A48>) --> 3
        print('Uncaught!', sys.exc_info()[0], '----', sys.exc_info()[1])
        # sys.exc_info()[0]: 引发异常的类
        # sys.exc_info()[1]: 引发异常的实例对象
