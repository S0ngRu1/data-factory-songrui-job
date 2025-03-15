#!/bin/bash

USER="jiang_bohuai"
MACHINE="$1"
REMOTE="$MACHINE:/home/$USER/Project/"
# 远程目录
LOCAL="/Users/bohuaijiang/Phram/rdk_server"
# 出了什么问题
set -x
rsync -a --exclude ".git/" --exclude "venv/" --exclude "Data/" --exclude "data/" -v  $LOCAL $REMOTE