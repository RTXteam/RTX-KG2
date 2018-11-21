
# How to build RTX kg2

## In the host OS (Ubuntu):

In a clean installation of Ubuntu 18.04 (EC2 AMI), as user `ubuntu`, in `/home/ubuntu`,
execute the following commands in order:

    git clone https://github.com/RTXteam/RTX.git
    ln -s RTX/code/kg2 kg2-code
    kg2-code/setup-kg2.sh
    kg2-code/build-kg2.sh

## In a Docker container:

In a clean installation of Ubuntu 18.04 (EC2 AMI), as user `ubuntu`, in `/home/ubuntu`,
execute the following commands in order:

    git clone https://github.com/RTXteam/RTX.git
    ln -s RTX/code/kg2 kg2-code
    kg2-code/install-docker.sh
    sudo docker build -t kg2 kg2-code/

