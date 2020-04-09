# -*- coding: utf-8 -*-
# @Author: KlausLyu
# @Date:   2020-04-09 11:43:53
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-09 11:46:52

'''{description}

'''

class Callback:
    def __init__(self, color):
        self.color = color

    def __call__(self):
        print("turn", self.color * 3)


if __name__ == '__main__':
    cb1 = Callback('blue')
    cb1()