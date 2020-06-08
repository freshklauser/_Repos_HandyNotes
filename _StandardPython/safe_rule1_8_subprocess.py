# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/8 23:19
# @FileName : safe_rule1_8_subprocess.py
# @SoftWare : PyCharm

"""
REFER:
    1) Python中subprocess库的用法介绍 http://www.gxlcms.com/python-362495.html

TIPS:
    1) 使用subprocess模块的目的是用于替换os.system等一些旧的模块和方法；
    2)
"""


import subprocess


def RunCmd_wrong(_directory):
    return subprocess.check_output('notepad.exe %s' % _directory, shell=True)


def test():
    expect_script = """
    echo ssss2222222222 >> test_write_something.txt
    echo ssss3333333333 >> test_write_something.txt
    calc.exe
    """
    process = subprocess.Popen(["cmd.exe"],
                               shell=False,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)


def popen():
    child = subprocess.Popen(['ping', '-c', '4', 'www.baidu.com'])
    print('Finished')


def popen_wait():
    child = subprocess.Popen(['ping', '-c', '4', 'www.baidu.com'])
    child.wait()  # 等待子进程结束
    print('Finished')


def std_in_out():
    child1 = subprocess.Popen(['cat', '/etc/passwd'],
                              stdout=subprocess.PIPE)
    child2 = subprocess.Popen(['grep', 'root'],
                              stdin=child1.stdout,
                              stdout=subprocess.PIPE)
    print(child2.communicate())



if __name__ == '__main__':
    # _out = RunCmd_wrong("d:/abc.txt && calc.exe")
    # popen()
    # popen_wait()
    std_in_out()