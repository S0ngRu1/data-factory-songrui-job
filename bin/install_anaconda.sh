!/bin/bash

set -x
# 设置Anaconda安装文件的路径
ANACONDA_INSTALLER="Anaconda3-2023.03-1-Linux-x86_64.sh"


if [ ! -f "$ANACONDA_INSTALLER" ]; then
    # 下载Anaconda安装文件
    wget https://repo.anaconda.com/archive/$ANACONDA_INSTALLER
fi


# 安装Anaconda
bash $ANACONDA_INSTALLER -b -p $HOME/anaconda3

# 添加Anaconda到环境变量
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> $HOME/.bashrc
source $HOME/.bashrc

# 删除Anaconda安装文件
rm $ANACONDA_INSTALLER