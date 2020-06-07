```
# 参看所有镜像 / 镜像信息
docker images						
docker inspect hadoop
# 拉取镜像
docker pull microsoft/dotnet:2.2-sdk
# 创建镜像(利用Dockerfile文件创建)
docker build -t runoob/ubuntu:v1 .
docker build -f /path/to/a/Dockerfile .
# 删除镜像
docker rmi mysql
# 镜像迁移（保存 / 载入）
docker save dockerapi/tgdataflow > tgdataflow.tar
docker load < tgdataflow.tar
```



```
# 在镜像下创建容器（新建并启动container）：docker run 之后生成container
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
		  -i:   # 以交互模式运行容器，通常与 -t 同时使用；
		  -t: 	# 为容器重新分配一个伪输入终端，通常与 -i 同时使用
		  -d: 	# 后台运行容器，并返回容器ID
		  -p: 	# （小写）指定端口映	射，格式为：主机(宿主)端口:容器端口
		  -P:	# （大写）随机端口映射，容器内部端口随机映射到主机的高端口 
		  --name="nginx-lb": 为容器指定一个名称
		  --volume , -v: 绑定一个卷 -v host_dir:container_dir
		  --rm  # Automatically remove the container when it exits(容器存在则重建容器覆盖)
# 后台创建并启动一个容器
docker run -d -p 2222:22 --name base csphere/centos:7.1
# 交互模型进入容器环境
docker exec -it redis /bin/bash
# 查看运行中的容器(-a 查看所有容器)
docker ps
docker inspect spark
# 删除容器 / 删除容器并删除挂载的数据卷
docker rm mysql
docker rm -v mysql
# 清理所有处于终止状态的容器
docker container prune
# 容器启停等操作
docker start/stop/restart/attach/kill webserver
# 容器导入和导出
docker export mongodb > mongo.tar
docker import - hello:laster
```



```
RUN apt-get update
	&& apt-get install python
	&& pip install flask
	&& pip install flask-mysql
```

```
RUN apt-get update
RUN apt-get install python
RUN pip install flask
RUN pip install flask-mysql
```



```
CMD 指令的格式和 RUN 相似，也是两种格式：
    - shell 格式：CMD <命令>
    - exec 格式：CMD ["可执行文件", "参数1", "参数2"...]
    - 参数列表格式：CMD ["参数1", "参数2"...]。在指定了 ENTRYPOINT 指令后，用 CMD 指定具体的参数。
```

```
FROM centos 7.0
MAINTAINER    chy<chy@qq.com>
#把宿主机当前上下文的c.txt拷贝到容器/usr/local/路径下
COPY c.txt /usr/local/cincontainer.txt
#把java与tomcat添加到容器中
ADD jdk-8u11-linux-x64.tar.gz /usr/local/
ADD apache-tomcat-9.0.27.tar.gz /usr/local/
#安装vim编辑器
RUN yum -y install vim
#设置工作访问时候的WORKDIR路径，登录落脚点
ENV MYPATH /usr/local
WORKDIR $MYPATH
#配置java与tomcat环境变量
ENV JAVA_HOME /usr/local/jdk1.8.0_11
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV CATALINA_HOME /usr/local/apache-tomcat-9.0.27
ENV CATALINA_BASE /usr/local/apache-tomcat-9.0.27
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/lib:$CATALINA_HOME/bin
#容器运行时监听的端口
EXPOSE  8080
#启动时运行tomcat
# ENTRYPOINT ["/usr/local/apache-tomcat-9.0.8/bin/startup.sh" ]
# CMD ["/usr/local/apache-tomcat-9.0.8/bin/catalina.sh","run"]
CMD /usr/local/apache-tomcat-9.0.27/bin/startup.sh 
	&& tail -F /usr/local/apache-tomcat-9.0.27/bin/logs/catalina.out

```

```
挂载一个主机目录作为数据卷:
	使用 --mount 标记指定挂载一个本地主机的目录到容器里
$ docker run -d -P \
    --name web \
    # -v /src/webapp:/opt/webapp:ro \
    --mount type=bind,source=/src/webapp,target=/opt/webapp,readonly \
    training/webapp \
    python app.py
    
挂载一个数据卷：
	使用 --mount 标记直接将 数据卷 挂载到容器里
$ docker volume create my-vol
$ docker run -d -P \
    --name web \
    # -v my-vol:/wepapp \
    --mount source=my-vol,target=/webapp \
    training/webapp \
    python app.py
```



```
1）`-P:`随机映射一个 `49000~49900` 的端口到内部容器开放的网络端口
2）`-p:`手动指定主机端口映射容器端口，在一个指定端口上只可以绑定一个容器，可以多次使用`-p`来绑定多个端口
	支持的格式有` ip:hostPort:containerPort | ip::containerPort | hostPort:containerPort`
			   - hostPort:containerPort     映射所有接口地址
                - ip::containerPort	         映射到指定地址的任意端口
                - ip:hostPort:containerPort	 映射到指定地址的指定端口
```

```
hostPort:containerPort       映射所有接口地址
ip::containerPort			映射到指定地址的任意端口
ip:hostPort:containerPort	 映射到指定地址的指定端口
```



docker-compose case

```
# Dockerfile
FROM tomcat
ADD https://github.com/JpressProjects/jpress/raw/alpha/wars/jpress-web-newest.war /usr/local/tomcat/webapps/
RUN cd /usr/local/tomcat/webapps/ \
    && mv jpress-web-newest.war jpress.war
```

```
version: "3"
services: 
  web: 
    build: .
    container_name: jpress
    ports: 
      - "8080:8080"
    volumes: 
      - /usr/local/tomcat/
    depends_on: 
      - db
  db: 
    image: mysql
    container_name: mysql
    command: --default-authentication-plugin=mysql_native_password
    restart: always 
    ports: 
      - "3306:3306"
    environment: 
      MYSQL_ROOT_PASSWORD: 123
      MYSQL_DATABASE: jpress
```



mysql主从搭建 (从改变，主不会跟着改变)  ---> 下一步 读写分离

```
# 创建好容器后, mysql-master
[klaus@messi mysql_sync]$ docker-compose exec mysql-master bash
root@dd8d062e1e72:/# mysql -uroot -p

mysql> grant replication slave on *.* to 'root'@'172.25.0.102' identified by 'asd123456';
Query OK, 0 rows affected, 1 warning (0.14 sec)
mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000003 |      600 |              | mysql            |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)


# 创建好容器后, mysql-slave (根据master的status设置)
[klaus@messi mysql_sync]$ docker-compose exec mysql-slave bash
root@1b90daad057a:/# mysql -uroot -p

mysql> reset slave;
Query OK, 0 rows affected (0.07 sec)
mysql> CHANGE MASTER TO MASTER_HOST='172.25.0.101', MASTER_USER='root', MASTER_PASSWORD='asd123456', MASTER_LOG_FILE='mysql-bin.000003', MASTER_LOG_POS=600;
Query OK, 0 rows affected, 2 warnings (0.11 sec)
mysql> start slave;
Query OK, 0 rows affected (0.00 sec)
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 172.25.0.101
                  Master_User: root
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000003
          Read_Master_Log_Pos: 600
               Relay_Log_File: replicas-mysql-relay-bin.000002
                Relay_Log_Pos: 320
        Relay_Master_Log_File: mysql-bin.000003
             Slave_IO_Running: Yes				# Yes is Success
            Slave_SQL_Running: Yes				# Yes is Success
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: 
	  ......
```







