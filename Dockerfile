FROM ubuntu:18.04
MAINTAINER Stephen Ramsey (stephen.ramsey@oregonstate.edu)
RUN useradd ubuntu -m -s /bin/bash
RUN usermod -aG sudo ubuntu
RUN apt-get update
RUN apt-get install -y git sudo wget
COPY * /home/ubuntu/RTX/code/kg2/
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu
RUN su - ubuntu -c "cd /home/ubuntu && /home/ubuntu/RTX/code/kg2/setup-kg2.sh"
