[TOC]

## 1. 服务器离线配置python环境

### 1.1 上传anaconda和whl文件，离线安装

离线安装anaconda， 下载whl文件，直接pip安装对应的whl，需要依赖的包下载后上传再重新安装

#### 1.1.1 anaconda

- Anaconda3-5.2.0-Linux-x86_64.sh 对应 python3.6.5 版本
- 下载链接： [清华大学源](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)
- pip更新包（可以不用更新目标服务器的pip）: `pip-20.1.1-py2.py3-none-any.whl`

#### 1.1.2 python库离线包下载

- requirements.txt

```
msgpack==1.0.0
attrdict==2.0.1
PyMySQL==0.9.3
pyshark==0.4.2.11
PyYAML==3.12
ua-parser==0.10.0
user-agents==2.1
```

- 有网的服务器上，base环境 下载离线包并补充依赖基础包和打包安装

```
# 用国内源下载源码包
pip download -r /home/klaus/offline/requirements.txt -d /home/klaus/offline/pkts/ -i https://pypi.tuna.tsinghua.edu.cn/simple
# 补充依赖基础包并打包安装（不可缺）
pip wheel -w ./pkts/ -r requirements.txt
```

- 将 pkts目录复制到目标服务器上，可以放在相同的路径中

  `scp -r pkts/ sniky@192.168.13.131:~/py/`

```
[sniky@localhost py]$ ll pkts/ -h
总用量 12M
-rw-rw-r--. 1 sniky sniky 9.8K 7月  11 18:29 attrdict-2.0.1-py2.py3-none-any.whl
-rw-rw-r--. 1 sniky sniky 5.3M 7月  11 18:29 lxml-4.5.1-cp36-cp36m-manylinux1_x86_64.whl
-rw-rw-r--. 1 sniky sniky 5.3M 7月  11 18:29 lxml-4.5.2-cp36-cp36m-manylinux1_x86_64.whl
-rw-rw-r--. 1 sniky sniky 269K 7月  11 18:52 msgpack-1.0.0-cp36-cp36m-manylinux1_x86_64.whl
-rw-rw-r--. 1 sniky sniky  97K 7月  11 18:29 py-1.9.0-py2.py3-none-any.whl
-rw-rw-r--. 1 sniky sniky  47K 7月  11 18:29 PyMySQL-0.9.3-py2.py3-none-any.whl
-rw-rw-r--. 1 sniky sniky  30K 7月  11 18:29 pyshark-0.4.2.11-py3-none-any.whl
-rw-rw-r--. 1 sniky sniky  42K 7月  11 18:29 PyYAML-3.12-cp36-cp36m-linux_x86_64.whl
-rw-rw-r--. 1 sniky sniky  11K 7月  11 18:29 six-1.15.0-py2.py3-none-any.whl
-rw-rw-r--. 1 sniky sniky  35K 7月  11 18:29 ua_parser-0.10.0-py2.py3-none-any.whl
-rw-rw-r--. 1 sniky sniky 9.4K 7月  11 18:29 user_agents-2.1-py3-none-any.whl
```

#### 1.1.3 离线安装anaconda

离线服务器中，安装anaconda，创建虚拟环境，安装whl

```
# 安装anaconda
sh Anaconda3-5.2.0-Linux-x86_64.sh
# 创建离线虚拟环境（以下命令创建后python的版本与base的版本一样）
conda create -n platform --offline
# 虚拟环境下安装requirements.txt中的whl
source activate rule
pip install --no-index --find-links=/home/sniky/py/pkts -r /home/sniky/py/requirements.txt
```

缺少依赖包：`distributed 1.21.8 requires msgpack, which is not installed.`需要添加到requirements.txt文件中，在pip install

### 1.2 anaconda整体迁移(问题比较多，弃用)

```
# 示例： node 传输文件到 slave
scp Anaconda3-5.2.0-Linux-x86_64.sh sniky@192.168.13.131:/home/sniky/py
```

- 1）直接将node服务器上的anaconda3文件夹整体传送到slave用户根目录下（可以压缩后传，也可直接传）

```
[klaus@messi ~]$ scp -r anaconda3.tar.gz sniky@192.168.13.131:/home/sniky/
```

- 2）分别单独修改pip和conda的路径 

```
vim ~/anaconda3/bin/pip
vim ~/anaconda3/bin/conda
# 在第一行中修改路径为正确路径
```

 - 问题
   - 所有用到python解释器的都需要该文件首行的路径，包括 ipython， ipython3, pip3等，太麻烦
   - clear命令会报错：`terminals database is inaccessible`

## 2. 离线安装tshark

- 可联网则直接如下命令下载：

```
yum install wireshark
# 可选图像化界面如下：
yum -y install wireshark-gnome
```

- 离线安装

  - 1) rpm包：   [wireshark](https://centos.pkgs.org/7/centos-x86_64/wireshark-1.10.14-24.el7.x86_64.rpm.html) 包，加上两个依赖包 [libsmi](https://centos.pkgs.org/7/centos-x86_64/libsmi-0.4.8-13.el7.x86_64.rpm.html)， [libcares](https://altlinux.pkgs.org/sisyphus/classic-x86_64/libcares-1.16.1-alt1.x86_64.rpm.html)（选择适合系统的版本）

  ```
  # wireshark Binary Package: 
  http://mirror.centos.org/centos/7/os/x86_64/Packages/wireshark-1.10.14-24.el7.x86_64.rpm
  # libsmi Binary Package:
  http://mirror.centos.org/centos/7/os/x86_64/Packages/libsmi-0.4.8-13.el7.x86_64.rpm
  # libcares Binary Package:
  http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/x86_64/RPMS.classic/libcares-1.16.1-alt1.x86_64.rpm
  ```

  - 2) 安装： `rpm -Uvh *.rpm --nodeps --force`
  - 3) 若非root用户安装，加sudo, 且需添加当前用户到 wireshark 用户组

  ```
  [klaus@messi wireshark_env]$ tshark
  tshark: Couldn't run /usr/sbin/dumpcap in child process: 权限不够
  Are you a member of the 'wireshark' group? Try running
  'usermod -a -G wireshark _your_username_' as root.
  [klaus@messi wireshark_env]$ sudo cat /etc/group
  ......
  wireshark:x:980:
  
  # 添加当前用户到wireshark用户组
  [klaus@messi wireshark_env]$ sudo usermod -aG wireshark $USER
  [klaus@messi wireshark_env]$ sudo cat /etc/group
  ......
  wireshark:x:980:klaus
  ```

  - 4) 测试： `tshark -i ens33 port 22`

  ```
  [klaus@messi ~]$ tshark -i ens33 port 22
  Capturing on 'ens33'
    1 0.000000000 192.168.13.1 -> 192.168.13.130 SSH 90 Encrypted request packet len=36
    2 0.043446647 192.168.13.130 -> 192.168.13.1 TCP 54 ssh > 59852 [ACK] Seq=1 Ack=37 Win=254 Len=0
    ......
  ```




- cmake: `https://www.jianshu.com/p/4c55642ed358`,需要配置全局

- libcap： 

  ```
  tar -xvf tar -xvf /home/Private/Compressed/libpcap-libpcap-1.9.0.tar.gz -C ./ 
  cd libpcap-libpcap-1.9.0 
  ./configure && make && make install
  ```

  

- wireshark



## 3. docker离线部署服务器环境

### 3.1 docker离线安装

有网的服务器上下载到本地

- 1）查询可用的软件版本(A)

```
[klaus@messi ~]$ sudo wget -O /etc/yum.repos.d/docker-ce.repo https://download.docker.com/linux/centos/docker-ce.repo
[sudo] klaus 的密码：
--2020-07-11 18:35:03--  https://download.docker.com/linux/centos/docker-ce.repo
正在解析主机 download.docker.com (download.docker.com)... 13.224.166.30, 13.224.166.20, 13.224.166.18, ...
正在连接 download.docker.com (download.docker.com)|13.224.166.30|:443... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度：2424 (2.4K) [binary/octet-stream]
正在保存至: “/etc/yum.repos.d/docker-ce.repo”

100%[================================================================>] 2,424       --.-K/s 用时 0s      

2020-07-11 18:35:03 (403 MB/s) - 已保存 “/etc/yum.repos.d/docker-ce.repo” [2424/2424])
```

```
[klaus@messi ~]$ sudo sed -i 's+download.docker.com+mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
```

```
[klaus@messi ~]$ sudo yum update
# 查看docker可用版本，可以针对性安装特定版本的docker
[klaus@messi offline]$ sudo yum list docker-ce --showduplicates|sort -r
[sudo] klaus 的密码：
已加载插件：fastestmirror, langpacks
可安装的软件包
 * updates: mirrors.163.com
Loading mirror speeds from cached hostfile
 * extras: mirrors.163.com
docker-ce.x86_64            3:19.03.9-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.8-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.7-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.6-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.5-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.4-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.3-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.2-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.1-3.el7                     docker-ce-stable
......
```

- 2）下载指定版本docker到本地指定文件夹中（先导入公钥）

```
# 导入公匙
wget https://get.docker.com/gpg
sudo rpmkeys --import ./gpg
# 安装
sudo yum install --downloadonly --downloaddir=/home/klaus/lyu/tmp/docker-19.03 docker-ce-19.03.8-3.el7 docker-ce-cli-19.03.8-3.el7
```

​	问题：`docker-ce-cli-19.03.8-3.el7.x86_64.rpm 的公钥尚未安装` （未导入公匙时）

​	解决方法：执行以下cmd后重新yum install

​		`wget https://get.docker.com/gpg`

​		`sudo rpmkeys --import ./gpg`

- 3）将下载到 docker-19.03 目录下的文件复制到目标服务器

```
[klaus@messi docker-19.03]$ scp * sniky@192.168.13.131:~/rule_deploy/docker/
```

- 4）目标服务器上使用 yum 安装

```
[sniky@localhost docker]$ sudo yum install *.rpm
```

- 5）启动 docker

```
[sniky@localhost ~]$ sudo systemctl start docker
```

- 6）非root用户下安装的话需要配置docker用户组权限(`cat /etc/group`可查看用户组)

  避免每次使用sudo，配置好用户组之后需要退出当前终端并重新登录即可。

```
# 建立docker组（docker安装后默认会创建好）
[sniky@localhost ~]$ sudo groupadd docker
groupadd：“docker”组已存在
# 当前用户添加到docker组
[sniky@localhost ~]$ sudo usermod -aG docker $USER
# /etc/group文件： docker:x:981 --> docker:x:981:sniky
```

- 7）更换国内源

```
[klaus@messi docker_env]$ vim /etc/docker/daemon.json 
# 新建 daemon.json，内容如下：
{"registry-mirrors":["https://reg-mirror.qiniu.com/", "http://hub-mirror.c.163.com/"]}
```

### 3.2 python镜像

有网环境下构建python镜像并创建应用容器

- 1）python基础环境 dockerfile

```
FROM python:3.6.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /pyroot
WORKDIR /pyroot
COPY requirements.txt /pyroot/
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```
# python应用部署示例
FROM ubuntu:16.04

MAINTAINER jhao104 "j_hao104@163.com"

RUN apt-get update -y && \  
apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "app/app.py" ] 
```

- 2）构建python基础环境镜像

```
docker build -t py36:rule_v1 . -f Dockerfile_py36
```

​	测试python镜像构建容器：

```
推荐2
# 使用python镜像构建的容器的python环境执行程序后删除镜像（每次执行完删除容器, 可随时更换挂载的宿主机主程序目录）
[klaus@messi myapp]$ docker run -v /home/klaus/myapp:/usr/src/myapp -w /usr/src/myapp -it --rm --name pyapp py36:rule_v1 python test.py
hello world
# 说明：
	命令说明：
    -v $PWD/myapp:/usr/src/myapp: 将主机中当前目录下的 myapp 挂载到容器的 /usr/src/myapp。
    -w /usr/src/myapp: 指定容器的 /usr/src/myapp 目录为工作目录。
    python helloworld.py: 使用容器的 python 命令来执行工作目录中的 helloworld.py 文件


# 使用python镜像构建容器并保持容器运行，利用docker容器中的python解释器执行宿主机.py文件（需要挂载，建议固定主程序目录）
-----------------------------------------------------------------------------------------
docker run -v $PWD:/usr/src/myapp -w /usr/src/myapp -itd --name pyenv py36:rule_v1
docker exec -it pyenv python test.py
-----------------------------------------------------------------------------------------
[klaus@messi myapp]$ docker run -v $PWD:/usr/src/myapp -w /usr/src/myapp -itd --name pyenv py36:rule_v1
[klaus@messi myapp]$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
666c0a76c8c0        py36:rule_v1        "python3"           11 minutes ago      Up 11 minutes                           pyenv
[klaus@messi myapp]$ docker exec -it pyenv python test.py
/usr/local/bin/python
['FileCapture', 'InMemCapture', 'LiveCapture', 'LiveRingCapture', 'RemoteCapture', 'UnsupportedVersionException', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'capture', 'config', 'packet', 'sys', 'tshark']
hello world
AttrDict({'name': 'tim'})
[klaus@messi myapp]$ python test.py
/home/klaus/anaconda3/bin/python
['FileCapture', 'InMemCapture', 'LiveCapture', 'LiveRingCapture', 'RemoteCapture', 'UnsupportedVersionException', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'capture', 'config', 'packet', 'sys', 'tshark']
hello world
AttrDict({'name': 'tim'})
# /usr/local/bin/python为容器中默认的python解释器路径
# /home/klaus/anaconda3/bin/python 为宿主机中的python解释器路径

```

- 3）应用部署（dockerfile构建python应用镜像）





## 4. neo4j

- docker部署

```
[klaus@messi neo4j]$ docker pull neo4j:3.5.20

[klaus@messi neo4j]$ docker run -idt -v $PWD/data:/data -v $PWD/import:/import -p 7474:7474 -p 7687:7687 --restart=always --name neo4j_server neo4j:3.5.20

# 可实现远程访问
http://<ip>:7474

# 进入容器中的neo4j命令行模式
[klaus@messi ~]$ docker exec -it neo4j_server bin/cypher-shell
username: neo4j
password: *********
Connected to Neo4j 3.5.20 at bolt://localhost:7687 as user neo4j.
Type :help for a list of available commands or :exit to exit the shell.
Note that Cypher queries must end with a semicolon.
neo4j> 
```



- 直接部署不知道为什么在自己电脑上无法实现远程，neo4j.conf 里面的都修改过也不行