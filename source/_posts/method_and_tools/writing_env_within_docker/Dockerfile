FROM ubuntu

VOLUME ["/data"]

# 使用163的 apt 源
RUN echo "更新 apt 源列表" \
    && echo "" > /etc/apt/sources.list \
    && echo "deb http://mirrors.163.com/ubuntu/ xenial main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.163.com/ubuntu/ xenial-backports main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.163.com/ubuntu/ xenial-proposed main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.163.com/ubuntu/ xenial-security main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.163.com/ubuntu/ xenial-updates main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.163.com/ubuntu/ xenial main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.163.com/ubuntu/ xenial-backports main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.163.com/ubuntu/ xenial-proposed main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.163.com/ubuntu/ xenial-security main multiverse restricted universe" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.163.com/ubuntu/ xenial-updates main multiverse restricted universe" >> /etc/apt/sources.list \
    && apt-get clean \
    && apt-get update \
    && echo "从 apt 获取软件" \
    && apt-get install -y locales bzip2 wget ttf-wqy-microhei
    
# 初始化 /etc/machine-id
RUN systemd-machine-id-setup

# 使用传统的 bash 作为 shell 解释器
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# 时区设置
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 中文支持
RUN locale-gen zh_CN.UTF-8 \
    && DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales \
    && locale-gen zh_CN.UTF-8
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh
ENV LC_ALL zh_CN.UTF-8


RUN echo "安装需要软件包" \
    && apt-get install -y python3-pip pandoc graphviz plantuml git npm \
    && ln -s /usr/bin/nodejs /usr/bin/node 

# RUN echo "配置python" \
    && python3 -m pip install --upgrade pip \
    && ln -s /usr/bin/pip3 /usr/bin/pip \
    && pip install --upgrade pip \
    && pip install jupyter \
    && pip install matplotlib 

# RUN echo "配置 nodejs" \
    && npm install -g hexo-cli gitbook-cli 