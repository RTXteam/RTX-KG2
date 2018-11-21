FROM ubuntu:18.04
MAINTAINER Stephen Ramsey (stephen.ramsey@oregonstate.edu)
WORKDIR /home/ubuntu
RUN useradd ubuntu -m -s /bin/bash
COPY RTX /home/ubuntu
RUN cd /home/ubuntu && /home/ubuntu/RTX/code/kg2/setup-kg2.sh
