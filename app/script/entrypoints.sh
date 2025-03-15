#!/bin/bash
PYTHON=python

# 设置一个在项目根目录且唯一的文件，用于定位根目录
BUILD_REQUIREMENT="requirements.txt"

# 定位根目录
ROOT_PATH=$(cd `dirname $0`; pwd)
echo $ROOT_PATH
cd $ROOT_PATH
if [ ! -z $BUILD_REQUIREMENT ]; then
  for ((i=0; i<=5; i++)); do
    if [ -f $BUILD_REQUIREMENT ]; then
      echo "Get project root path:`pwd`"
      ROOT_PATH=`pwd`
      break
    else
      cd ../
    fi
  done
fi

cd $ROOT_PATH
echo $ROOT_PATH
export PYTHONPATH=$ROOT_PATH
echo "python path: $PYTHONPATH"


# 容器云的环境变量加载
ENV_CONFIG=.env
if test -f "$ENV_CONFIG"; then
    echo "source config file: $ENV_CONFIG"
    source $ENV_CONFIG
    echo "ENV_PORT: $ENV_PORT"
fi

# 非 docker 环境的 venv
if test -f venv/bin/activate; then
  echo "source venv/bin/activate"
  source venv/bin/activate
  pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  pip install -r requirements.txt
fi

if [ -n "$ENV_PORT" ]; then
  PORT=$ENV_PORT;
  echo "LOAD EVN_PORT: PORT=$ENV_PORT"
else
  echo "default PORT=10081"
  PORT=10081;
fi

LOCALHOST="127.0.0.1"
HOST="0.0.0.0"

MSG="Listening at: http://$HOST:$PORT"
echo $PYTHONPATH
python -V
set -x
case $PHASE in
  "PRODUCTION")
    echo "RUN app in production mode, $MSG"
    cpu_cnt=`cat /proc/cpuinfo |grep "processor"|wc -l`
    echo "cpus $cpu_cnt"
    workers=`expr $cpu_cnt + 1`
    echo "workers $workers"
    gunicorn -w $workers -b "$HOST:$PORT" -k uvicorn.workers.UvicornWorker app.main:app --timeout 90
#   gunicorn -w 1 -b "$HOST:$PORT" -k uvicorn.workers.UvicornWorker app.main:app --timeout 90
    ;;
  "TEST")
    echo "RUN app in test mode, $MSG"
    uvicorn app.main:app --host $HOST --port $PORT
    ;;
  *)
    echo "RUN app in debug mode, $MSG, with option --reload"
    uvicorn app.main:app --host $HOST --port $PORT --reload
#   uvicorn app.main:app --host $HOST --port $PORT
    ;;
esac