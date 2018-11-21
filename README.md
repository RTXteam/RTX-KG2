
# How to build RTX kg2

## Directly in Ubuntu 18.04 host OS in AWS:

In a new instance based on the Ubuntu 18.04 EC2 AMI, as user `ubuntu`, in
directory `/home/ubuntu`, execute the following commands in order:

    git clone https://github.com/RTXteam/RTX.git
    RTX/code/kg2/setup-kg2.sh
    kg2-code/build-kg2.sh

## In a Docker container Ubuntu 18.04 host OS in AWS:

In a new instance based on the Ubuntu 18.04 EC2 AMI, as user `ubuntu`, in
directory `/home/ubuntu`, execute the following commands in order:

    git clone https://github.com/RTXteam/RTX.git
    RTX/code/kg2/install-docker.sh
    sudo docker build -t kg2 RTX/code/kg2/
    sudo docker run --name kg2 kg2:latest su - ubuntu -c "kg2-code/build-kg2.sh"

## In a Docker container in another host OS (untested):

This assumes (1) you are running as an unprivileged user that is set up for
passwordless `sudo`; (2) you have `git` installed and in your PATH; (3) you have
`docker` installed and in your PATH; and (4) you are in your home directory.

    git clone https://github.com/RTXteam/RTX.git
    sudo docker build -t kg2 RTX/code/kg2/
    sudo docker run --name kg2 kg2:latest su - ubuntu -c "kg2-code/build-kg2.sh"

