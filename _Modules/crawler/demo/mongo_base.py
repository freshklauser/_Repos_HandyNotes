# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/6 22:18
# @FileName : mongo_base.py
# @SoftWare : PyCharm


"""
1. mongo 安装
docker pull mongo

2. mongo 容器创建和用户创建
docker run -d --name mongo_node1 -p 27018:27017 -v /home/sniky/docker/mongo:/data/db mongo --auth
docker exec -it mongodb mongo admin
> db.createUser({user:"xxx", pwd:"xxxx", roles:["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]});
    Successfully added user: {
        "user" : "admin",
        "roles" : [
            "userAdminAnyDatabase",
            "dbAdminAnyDatabase",
            "readWriteAnyDatabase"
        ]
    }

3. 宿主机访问
docker exec -it mongo_node1 mongo admin -u mongo -p
MongoDB shell version v4.4.0
Enter password:
connecting to: mongodb://127.0.0.1:27017/admin?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("e3785cef-1d8c-4a54-aa8d-957901e2fcc7") }
MongoDB server version: 4.4.0
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB

"""


"""
python os 设置环境变量

import os

# 设置环境变量
os.environ['WORKON_HOME']="value"
# 获取环境变量方法1
os.environ.get('WORKON_HOME')
#获取环境变量方法2(推荐使用这个方法)
os.getenv('path')
# 删除环境变量
del os.environ['WORKON_HOME']
其他key值：
os.environ['HOMEPATH']:当前用户主目录。
os.environ['TEMP']:临时目录路径。
os.environ['PATHEXT']:可执行文件。
os.environ['SYSTEMROOT']:系统主目录。
os.environ['LOGONSERVER']:机器名。
os.environ['PROMPT']:设置提示符。

import os
path=r"E:\env"
command =r"setx WORK1 %s /m"%path
os.system(command)

"""

import os
print(os.environ)
print(os.getenv("MONGO_PASSWORD"))
os.environ['MONGO_PASSWORD'] = "asd123456"


import pymongo

# myclient = pymongo.MongoClient("mongodb://192.168.13.132:27018/")
myclient = pymongo.MongoClient("mongodb://mongo:asd_123456@192.168.13.132:27018/")
# db = myclient.admin
print(myclient)
# # 认证
# db.authenticate('mongo', os.getenv("MONGO_PASSWORD"))
dblist = myclient.list_database_names()
print(dblist)
# mydb = myclient["runoobdb"]

print(id(locals()))