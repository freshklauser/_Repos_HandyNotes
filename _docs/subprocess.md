

## subprocess
- REFER:
    
    1、Python中subprocess库的用法介绍 http://www.gxlcms.com/python-362495.html

- TIPS:

    1、使用subprocess模块的目的是用于替换os.system等一些旧的模块和方法；
    
    2、
    
## 常用函数介绍
- `subprocess.call()`: 命令执行
    
    执行由参数提供的命令，把数组作为参数运行命令。其功能类似于os.system(cmd)
    
    父进程等待子进程完成
    
    `shell=False`可以屏蔽掉 `call`的`cmd`执行命令的功能
    
    参数格式： `cmd param1 param2`  or [`cmd`, `param1`, `param2`]
    
    返回值： `call()`不返回值，若需要返回值，可以使用 `check_out()`函数
    
    ```
    In [1]: import subprocess
    In [2]: subprocess.call("ls -l", shell=True)
    total 8020
    drwxrwxr-x. 23 klaus klaus    4096 Jan 31 21:52 anaconda3
    drwxrwxr-x.  4 klaus klaus      63 Jan 31 10:46 cluster
    drwxr-xr-x.  2 klaus klaus       6 Feb 18 13:28 Desktop
    drwxr-xr-x.  4 klaus klaus     143 Jun  7 19:37 Documents
    drwxr-xr-x.  2 klaus klaus      70 Feb  1 15:31 Downloads
    -rw-rw-r--.  1 klaus klaus   13216 Jan 28 12:26 get-docker.sh
    -rw-rw-r--   1 klaus klaus   23791 Feb  3 18:35 history.txt
    drwxrwxr-x   4 klaus klaus      61 Jun  7 18:02 jpress
    -rw-rw-r--   1 klaus klaus 8165473 Jun  7 17:52 jpress.tar.gz
    drwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Music
    drwxrwxr-x   4 klaus klaus      59 Jun  7 21:22 mysql_sync
    drwxrwxr-x.  5 klaus klaus      57 Jun  7 19:38 opt
    drwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Pictures
    drwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Public
    drwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Templates
    drwxrwxr-x.  2 klaus klaus      32 Jan 29 23:34 uhopper
    drwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Videos
    Out[2]: 0
    
    In [3]: subprocess.call("ls -l", shell=False)
    ---------------------------------------------------------------------------
    FileNotFoundError                         Traceback (most recent call last)
    <ipython-input-3-799298f4b20d> in <module>()
    ----> 1 subprocess.call("ls -l", shell=False)
    ```
    ```
    In [4]: subprocess.call(["df",'-h'], shell=True)
    Filesystem              1K-blocks     Used Available Use% Mounted on
    devtmpfs                   914680        0    914680   0% /dev
    tmpfs                      931552        0    931552   0% /dev/shm
    tmpfs                      931552    10796    920756   2% /run
    tmpfs                      931552        0    931552   0% /sys/fs/cgroup
    /dev/mapper/centos-root  52403200 10166572  42236628  20% /
    /dev/sda1                 1038336   170196    868140  17% /boot
    /dev/mapper/centos-home  28289540  4917608  23371932  18% /home
    tmpfs                      186312       40    186272   1% /run/user/1000
    /dev/sr0                  4554702  4554702         0 100% /run/media/klaus/CentOS 7 x86_64
    ```
- `subprocess.check_out()`
    ```buildoutcfg
    In [6]: res = subprocess.check_output(['ls', '-l'], shell=True)
    
    In [7]: res
    Out[7]: b'anaconda3\ncluster\nDesktop\nDocuments\nDownloads\nget-docker.sh\nhistory.txt\njpress\njpress.tar.gz\nMusic\nmysql_sync\nopt\nPictures\nPublic\nTemplates\nuhopper\nVideos\n'
    
    In [8]: res.decode('utf-8')
    Out[8]: 'anaconda3\ncluster\nDesktop\nDocuments\nDownloads\nget-docker.sh\nhistory.txt\njpress\njpress.tar.gz\nMusic\nmysql_sync\nopt\nPictures\nPublic\nTemplates\nuhopper\nVideos\n'
    ```
  
- `subprocess.Popen()`: 进程创建和管理`Popen`类

    `subprocess.popen`代替`os.popen`, 可以创建一个`Popen`类来创建进程和进行复杂的交互;
    
    dsd
    ```buildoutcfg
    In [12]: def popen():
    ...:     child = subprocess.Popen(['ping', '-c', '4', 'www.baidu.com'])
    ...:     print('Finished')
    ...:     
    
  # -------------------- poen: 主进程不等待子进程 -------------
    In [13]: popen()
    Finished
    
    In [14]: PING www.a.shifen.com (163.177.151.110) 56(84) bytes of data.
    64 bytes from 163.177.151.110 (163.177.151.110): icmp_seq=1 ttl=128 time=56.0 ms
    64 bytes from 163.177.151.110 (163.177.151.110): icmp_seq=2 ttl=128 time=53.7 ms
    64 bytes from 163.177.151.110 (163.177.151.110): icmp_seq=3 ttl=128 time=59.6 ms
    64 bytes from 163.177.151.110 (163.177.151.110): icmp_seq=4 ttl=128 time=78.2 ms
    
    --- www.a.shifen.com ping statistics ---
    4 packets transmitted, 4 received, 0% packet loss, time 3006ms
    rtt min/avg/max/mdev = 53.799/61.920/78.258/9.658 ms

  
    # -------------------- poen: 主进程不等待子进程 -------------
    In [14]: def popen_wait():
        ...:     child = subprocess.Popen(['ping', '-c', '4', 'www.baidu.com'])
        ...:     child.wait()
        ...:     print('Finished')
        ...:     
    
    In [15]: popen_wait()
    PING www.a.shifen.com (163.177.151.110) 56(84) bytes of data.
    64 bytes from 163.177.151.110 (163.177.151.110): icmp_seq=1 ttl=128 time=39.5 ms
    64 bytes from 163.177.151.110 (163.177.151.110): icmp_seq=2 ttl=128 time=55.6 ms
    64 bytes from 163.177.151.110 (163.177.151.110): icmp_seq=3 ttl=128 time=71.6 ms
    64 bytes from 163.177.151.110 (163.177.151.110): icmp_seq=4 ttl=128 time=66.5 ms
    
    --- www.a.shifen.com ping statistics ---
    4 packets transmitted, 4 received, 0% packet loss, time 3007ms
    rtt min/avg/max/mdev = 39.565/58.363/71.619/12.287 ms
    Finished

    ```
    上述两个函数中，子进程时 `ping`, 主进程时`print('Finished')`。添加了`child.wait()`之后，主进程会等待子进程先执行完，之后才会继续主进程程序

- `stdout=subprocess.PIPE`标准输出重定向
    ```buildoutcfg
    In [32]: child = subprocess.Popen(['ls','-l'],stdout=subprocess.PIPE)
    In [33]: res = child.stdout.read().decode('utf-8')
    
    In [34]: res
    Out[34]: 'total 8020\ndrwxrwxr-x. 23 klaus klaus    4096 Jan 31 21:52 anaconda3\ndrwxrwxr-x.  4 klaus klaus      63 Jan 31 10:46 cluster\ndrwxr-xr-x.  2 klaus klaus       6 Feb 18 13:28 Desktop\ndrwxr-xr-x.  4 klaus klaus     143 Jun  7 19:37 Documents\ndrwxr-xr-x.  2 klaus klaus      70 Feb  1 15:31 Downloads\n-rw-rw-r--.  1 klaus klaus   13216 Jan 28 12:26 get-docker.sh\n-rw-rw-r--   1 klaus klaus   23791 Feb  3 18:35 history.txt\ndrwxrwxr-x   4 klaus klaus      61 Jun  7 18:02 jpress\n-rw-rw-r--   1 klaus klaus 8165473 Jun  7 17:52 jpress.tar.gz\ndrwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Music\ndrwxrwxr-x   4 klaus klaus      59 Jun  7 21:22 mysql_sync\ndrwxrwxr-x.  5 klaus klaus      57 Jun  7 19:38 opt\ndrwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Pictures\ndrwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Public\ndrwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Templates\ndrwxrwxr-x.  2 klaus klaus      32 Jan 29 23:34 uhopper\ndrwxr-xr-x.  2 klaus klaus       6 Jan 22 23:10 Videos\n'
    ```
- `stdin, stdout; subprocess.communicate()`管道文本流控制
    
    配合使用 `stdin, stdout`实现管道流控制
    ```buildoutcfg
    <file: std_in_out.py>
    import subprocess
    
    def std_in_out():
        child1 = subprocess.Popen(['cat', '/etc/passwd'],
                                  stdout=subprocess.PIPE)
        child2 = subprocess.Popen(['grep', 'root'],
                                  stdin=child1.stdout,
                                  stdout=subprocess.PIPE)
        tmp_tuple = child2.communicate()
        return tmp_tuple[0].decode('utf-8')
    res = std_in_out()
    
    print(res)
  
    [klaus@messi ~]$ python std_in_out.py
    root:x:0:0:root:/root:/bin/bash
    operator:x:11:0:operator:/root:/sbin/nologin
    ```
    上述代码实现的同能与如下代码的功能相同：
    ```buildoutcfg
    [klaus@messi ~]$ cat /etc/passwd | grep root
    root:x:0:0:root:/root:/bin/bash
    operator:x:11:0:operator:/root:/sbin/nologin
    ```
    `Popen.communicate(input=None)：`
    与子进程进行交互。向stdin发送数据，或从stdout和stderr中读取数据。可选参数input指定发送到子进程的参数。Communicate()返回一个元组：(stdoutdata, stderrdata)。
    
    注意：如果希望通过进程的stdin向其发送数据，在创建Popen对象的时候，参数stdin必须被设置为PIPE。同样，如果希望从stdout和stderr获取数据，必须将stdout和stderr设置为PIPE。
    
    当你用 communicate()函数的时候意味着你要执行命令了
    
- 其他命令
    ```buildoutcfg
    1、Popen.poll()：用于检查子进程是否已经结束。设置并返回returncode属性。
    2、Popen.wait()：等待子进程结束。设置并返回returncode属性。
    3、Popen.communicate(input=None)：与子进程进行交互。向stdin发送数据，或从stdout和stderr中读取数据。可选参数input指定发送到子进程的参数。Communicate()返回一个元组：(stdoutdata, stderrdata)。注意：如果希望通过进程的stdin向其发送数据，在创建Popen对象的时候，参数stdin必须被设置为PIPE。同样，如果希望从stdout和stderr获取数据，必须将stdout和stderr设置为PIPE。
    4、Popen.send_signal(signal)：向子进程发送信号。
    5、Popen.terminate()：停止(stop)子进程。在windows平台下，该方法将调用Windows API TerminateProcess（）来结束子进程。
    6、Popen.kill()：杀死子进程。
    7、Popen.stdin：如果在创建Popen对象是，参数stdin被设置为PIPE，Popen.stdin将返回一个文件对象用于策子进程发送指令。否则返回None。
    8、Popen.stdout：如果在创建Popen对象是，参数stdout被设置为PIPE，Popen.stdout将返回一个文件对象用于策子进程发送指令。否则返回None。
    9、Popen.stderr：如果在创建Popen对象是，参数stdout被设置为PIPE，Popen.stdout将返回一个文件对象用于策子进程发送指令。否则返回None。
    10、Popen.pid：获取子进程的进程ID。
    11、Popen.returncode：获取进程的返回值。如果进程还没有结束，返回None。
    12、subprocess.call(*popenargs, **kwargs)：运行命令。该函数将一直等待到子进程运行结束，并返回进程的returncode。文章一开始的例子就演示了call函数。如果子进程不需要进行交互,就可以使用该函数来创建。
    13、subprocess.check_call(*popenargs, **kwargs)：与subprocess.call(*popenargs, **kwargs)功能一样，只是如果子进程返回的returncode不为0的话，将触发CalledProcessError异常。在异常对象中，包括进程的returncode信息。
    ```