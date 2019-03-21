FROM ubuntu:18.04
MAINTAINER Stephen Ramsey (stephen.ramsey@oregonstate.edu)

# need to add user "ubuntu" and give sudo privilege:
RUN useradd ubuntu -m -s /bin/bash

# need to install sudo and wget
RUN apt-get update
RUN apt-get install -y git sudo wget git

# give sudo privilege to user ubuntu:
RUN usermod -aG sudo ubuntu
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu

# copy setup scripts
RUN git clone https://github.com/RTXteam/RTX.git
#COPY * /home/ubuntu/RTX/code/kg2/
RUN su - ubuntu -c "cd /home/ubuntu && /home/ubuntu/RTX/code/kg2/setup-kg2.sh"
