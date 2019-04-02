
# How to build RTX kg2

## General notes:

The KG2 build system is designed only to run in an Ubuntu 18.04 environment
(i.e., host OS or container). Currently, KG2 is built using a set of bash scripts that
are designed to run in Amazon's Elastic Compute Cloud (EC2), and thus,
configurability and/or coexisting with other installed software pipelines was
not a design consideration for the KG2 build system. The KG2 build system's bash
scripts create three subdirectories `~/kg2-build`, `~/kg2-code`, and
`~/kg2-venv` under the `${HOME}` directory of whatever Linux user account you
use to run the KG2 build software (if you run on an EC2 Ubuntu instance, this
directory would by default be `/home/ubuntu`).  The build software is is
configured to run with the `kg2-build` directory being in the same file system
as the Python temporary file directory (i.e., the directory name that is
returned by `tempfile.tempdir` in Python). If you modify the KG2 software or
runtime environment so that `kg2-build` is in a different file system from the
file system in which the directory `tempfile.tempdir` resides, then the file
copying operations that are performed by the KG2 build software will not be
atomic and interruption of `build-kg2.py` could then leave a source data file in
a half-downloaded (i.e., broken) state.

## Setup your computing environment

The computing environment where you will be running the KG2 build should be
running Ubuntu 18.04 with `git` installed and configured in your shell path.
Your build environment should have the following minimum specifications:

- 64 GB of system RAM
- 500 GB of disk space in the root file system 
- high-speed network access

The KG2 build system has been tested *only* under Ubuntu 18.04. If you want to
build KG2 but don't have a native installation of Ubuntu 18.04 available, your
best bet would be to use Docker (see the `Dockerfile` for this project). You'll
need to have an Amazon Web Services (AWS) authentication key that is configured
to be able to read from the `s3://rtx-kg2` Amazon Simple Cloud Storage Service
(S3) bucket (ask Stephen Ramsey to set this up) and to write to the S3 bucket
`rtx-kg2-public`. The KG2 build script downloads the UMLS and SNOMED CT
distributions from a private S3 bucket `rtx-kg2` (these distributions are
encumbered by licenses so they cannot be put on a public server for download) and
it uploads the `kg2.json` file to the public S3 bucket `rtx-kg2-public`.

## My normal EC2 instance

- AMI: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - `ami-005bdb005fb00e791` (64-bit x86)
- Instance type: `m5.4xlarge` 
- Storage: 500 GB General Purpose SSD
- Security Group: `http+ssh`

## Build instructions

### Option 1: build KG2 directly on an Ubuntu system, not via ssh:

Run these commands in the `bash` shell, in order:

    cd
    
    git clone https://github.com/RTXteam/RTX.git
    
    screen

Within the `screen` session, run:

    RTX/code/kg2/setup-kg2.sh > setup-kg2.log 2>&1
    
Then exit screen (`ctrl-a d`). You can watch the progress of `setup-kg2.sh` by
using the command:

    tail -f setup-kg2.log

Next, rejoin the screen session using `screen -r`.  Within the `screen` session, run:

    RTX/code/kg2/build-kg2.sh

Then exit screen (`ctrl-a d`). You can watch the progress of your KG2 build by using these
two commands (run them in separate bash shell terminals):

    tail -f /home/ubuntu/kg2-build/build-kg2-stdout.log
    tail -f /home/ubuntu/kg2-build/build-kg2-stderr.log
    
### Option 2: remotely build KG2 in an EC2 instance via ssh, orchestrated from your local computer

Run these commands in the `bash` shell, in order:

    git clone https://github.com/RTXteam/RTX.git
    
    RTX/code/kg2/ec2-setup-remote-instance.sh

### Option 3: in an Ubuntu container in Docker (UNTESTED, IN DEVELOPMENT)

If you are on Ubuntu and you need to install Docker, you can run this script:
   
    RTX/code/kg2/install-docker.sh
    
Then run these commands in the `bash` shell:

    cd
    
    sudo docker build -t kg2 RTX/code/kg2/

    screen
    
    sudo docker run --name kg2 kg2:latest su - ubuntu -c "RTX/code/kg2/setup-kg2.sh > setup-kg2.log 2>&1"
    
Then exit screen (`ctrl-a d`). You can watch the progress of your KG2 setup using the command:

    sudo docker exec kg2 "tail -f setup-kg2.log"

Then again inside screen, run:

    sudo docker exec kg2 "kg2-code/build-kg2.sh"

Then exit screen (`ctrl-a d`). You can watch the progress of your KG2 setup using the
following two commands (in two two separate terminals):

    sudo docker exec -it kg2 tail -f /home/ubuntu/kg2-build/build-kg2-stdout.log
    sudo docker exec -it kg2 tail -f /home/ubuntu/kg2-build/build-kg2-stderr.log

