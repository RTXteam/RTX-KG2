FROM ubuntu:18.04
MAINTAINER Stephen Ramsey (stephen.ramsey@oregonstate.edu)

# need to add user "ubuntu" and give sudo privilege:
RUN useradd ubuntu -m -s /bin/bash

# need to install git and sudo
RUN apt-get update
RUN apt-get install -y git sudo

# give sudo privilege to user ubuntu:
RUN usermod -aG sudo ubuntu
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu
RUN touch /home/ubuntu/.sudo_as_admin_successful
RUN chown ubuntu.ubuntu /home/ubuntu/.sudo_as_admin_successful

# make this container persistent
CMD tail -f /dev/null
