# -*- coding: utf-8 -*-
# @Author: KlausLyu
# @Date:   2020-04-08 16:24:16
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-08 16:40:14

'''{持久化类实例}
'''


import shelve
from person import Person, Manager

flag = False
if flag:
    bob = Person("Bob Smith")
    sue = Person("Sue Jones", job='dev', pay=10000)
    tom = Manager('Tom Jones', 50000)
    with shelve.open('persondb') as db:
        for obj in (bob, sue, tom):
            db[obj.name] = obj
    flag = False

# 生产3个文件 persondb.bak, persondb.dat, persondb.dir
# new_db = shelve.open('persondb')
# print(type(new_db), len(new_db), new_db['Bob Smith'].__dict__)
# print(list(new_db.keys()))
# print()
# for key in sorted(new_db):
#     print(key, '-->', new_db[key])
