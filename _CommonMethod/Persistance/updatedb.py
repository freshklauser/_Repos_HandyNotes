# -*- coding: utf-8 -*-
# @Author: KlausLyu
# @Date:   2020-04-08 16:40:23
# @Last Modified by:   KlausLyu
# @Last Modified time: 2020-04-08 17:09:40

import shelve

db = shelve.open('persondb')
for key in sorted(db):
    print(key, '-->', db[key])

sue = db['Sue Jones']
sue.giveRaise(0.10)
db['Sue Jones'] = sue

db.close()
