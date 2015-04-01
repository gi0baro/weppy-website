# weppy website development dockerfile
FROM ubuntu:14.04

MAINTAINER gi0baro

# Remove some useless errors which appear when installing packages with apt
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Install required packages
RUN apt-get update
RUN apt-get install -y software-properties-common g++
RUN apt-get install -y git python python-dev python-setuptools wget

# Build dependencies
RUN easy_install pip

## TEMP: weppy master
WORKDIR /root
ADD http://www.random.org/strings/?num=10&len=8&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new uuid
RUN git clone https://github.com/gi0baro/weppy.git weppy
RUN cd weppy && python setup.py install

# install python requirements
RUN mkdir /home/app
ADD requirements.txt /home/app/
WORKDIR /home/app
RUN pip install -r requirements.txt

# Cleanup to reduce image size
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/pip-build-root
