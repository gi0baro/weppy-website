# weppy website development dockerfile
FROM python:2.7

MAINTAINER gi0baro

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y libjpeg-dev libfreetype6-dev zlib1g-dev libpq-dev

# install python requirements
RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt --src /usr/src/app
WORKDIR /home/app
