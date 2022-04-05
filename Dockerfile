FROM ubuntu:20.04
RUN mkdir patcher
WORKDIR /patcher
COPY . ./
ARG DEBIAN_FRONTEND=noninteractive
RUN (apt-get update && apt-get upgrade -y && apt-get install $(cat pkglist) -y) >> apt_log
RUN pip3 install -r requirements.txt --no-warn-script-location 
