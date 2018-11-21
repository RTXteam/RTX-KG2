FROM ubuntu:18.04
MAINTAINER Stephen Ramsey (stephen.ramsey@oregonstate.edu)
RUN useradd ubuntu -m -s /bin/bash
COPY /home/ubuntu/RTX/ /home/ubuntu/RTX
RUN cd /home/ubuntu && /home/ubuntu/RTX/code/kg2/setup-kg2.sh
