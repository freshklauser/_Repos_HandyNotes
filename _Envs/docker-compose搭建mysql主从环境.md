



## 1. 目录结构

```
mysql_sync/
   - docker-compose.yml
   - master/
       - Dockerfile
       - my.cnf
   - slave/
       - Dockerfile
       - my.cnf
```

## 2. 配置文件 my.cnf

- `master/my.cnf`

```
[mysqld]
# 主数据库端ID号
server_id = 101
# 开启二进制日志
log-bin = mysql-bin
# 不需要复制的数据库名
binlog-ignore-db = mysql
binlog_cache_size=1M
# 二进制日志自动删除的天数，默认值为0,表示“没有自动删除”，启动时和二进制日志循环时可能删除
expire_logs_days = 7
# 将函数复制到slave
log_bin_trust_function_creators = 1
binlog_format=mixed
```

- `slave/my.cnf`

```
[mysqld]
# 从数据库端ID号
server_id = 102
log-bin = mysql-bin
relay_log=replicas-mysql-relay-bin
log-slave-updates = 1
# 指定slave要复制哪个库
binlog-ignore-db=mysql
log_bin_trust_function_creators = 1
binlog_format=mixed
read_only=1
```

## 3. Dockerfile

- `master/Dockerfile`

```
FROM mysql:5.7.26
MAINTAINER klaus
ADD ./master/my.cnf /etc/mysql/my.cnf
```

- `slave/Dockerfile`

```
FROM mysql:5.7.26
MAINTAINER klaus
ADD ./slave/my.cnf /etc/mysql/my.cnf
```

## 4. docker-compose.yml

```
version: "3"
services:

  mysql-master:
    build:
      context: ./
      dockerfile: master/Dockerfile
    container_name: mysql_master
    ports:
      - 3306:3306
    volumes:
      - mysql-master-vol:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: asd123456
      MYSQL_DATABASE: rule_platform
      MYSQL_USER: ruler
      MYSQL_PASSWORD: asd123456
    restart: unless-stopped
    networks:
      mysql-ms-network:
        ipv4_address: 172.25.0.101

  mysql-slave:
    build:
      context: ./
      dockerfile: slave/Dockerfile
    container_name: mysql_slave
    ports:
      - 3307:3306
    volumes:
      - mysql-slave-vol:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: asd123456
      MYSQL_DATABASE: rule_platform
      MYSQL_USER: ruler
      MYSQL_PASSWORD: asd123456
    restart: unless-stopped
    networks:
      mysql-ms-network:
        ipv4_address: 172.25.0.102

volumes:
  mysql-master-vol:
  mysql-slave-vol:

networks:
  mysql-ms-network:
    driver: bridge
    ipam:
      config:
      - subnet: 172.25.0.0/24
```

## 5. 主从复制mysql镜像构建

- `docker-compose.yml`所在目录下

```
# 构建镜像和容器并启动容器
docker-compose up -d
# 查看构建的容器  state up则构建成功
docker-compose ps
```

- `docker-compose`进入容器中设置主从配置

```
# ------ 主mysql
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
```

```
# ------ 从mysql （根据master的status设置 File 和 Postion）
[klaus@messi mysql_sync]$ docker-compose exec mysql-slave bash
root@1b90daad057a:/# mysql -uroot -p

mysql> reset slave;
Query OK, 0 rows affected (0.07 sec)

# 设置 HOST, USER, PASSWORD, (LOG_FILE, LOG_POS)---master中对应的File和Position
mysql> CHANGE MASTER TO MASTER_HOST='172.25.0.101', MASTER_USER='root', MASTER_PASSWORD='asd123456', MASTER_LOG_FILE='mysql-bin.000003', MASTER_LOG_POS=600;
Query OK, 0 rows affected, 2 warnings (0.11 sec)

mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

# 查看从mysql是否配置成功
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
             Slave_IO_Running: Yes							# Yes is Success --------
            Slave_SQL_Running: Yes							# Yes is Success --------
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: 
	  ......
```

