#!/bin/bash
# shell 脚本传参
workdir=$(cd `dirname $0`; pwd)
echo "当前python环境镜像：$1"
echo "当前工作目录：$workdir"
echo "当前待执行文件：$2"
docker run -v $workdir:/usr/local/myapp -w /usr/local/myapp --rm --name virtual_py $1 python $workdir/$2