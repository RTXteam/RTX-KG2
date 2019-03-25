
# How to build RTX kg2

## General notes:

Currently, KG2 is built using a set of bash scripts that are designed to run in
Amazon's Elastic Compute Cloud (EC2), and thus, configurability and/or
coexisting with other installed software pipelines was not a design
consideration for the KG2 build system. The KG2 build system's bash scripts
create three subdirectories `~/kg2-build`, `~/kg2-code`, and `~/kg2-venv` under
the `$HOME$` directory of whatever Linux user account you use to run the KG2
build software (by default, this home directory would be `/home/ubuntu` since
the KG2 build system is designed only to run in Ubuntu; see below).  The build
software is is configured to run with the `kg2-build` directory being in the
same file system as the Python temporary file directory (i.e., the directory
name that is returned by `tempfile.tempdir` in Python). If you modify the KG2
software or runtime environment so that `kg2-build` is in a different file
system from the file system in which the directory `tempfile.tempdir` resides,
then the file copying operations that are performed by the KG2 build software
will not be atomic and interruption of `build-kg2.py` could then leave a source
data file in a half-downloaded (i.e., broken) state.

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
(S3) bucket (ask Stephen Ramsey to set this up); this is because the KG2 build
script downloads the UMLS and SNOMED CT distributions from a private S3 bucket
(these distributions are encumbered by licenses so they cannot be put on a
public server for download).

## My normal EC2 instance

- AMI: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - `ami-005bdb005fb00e791` (64-bit x86)
- Instance type: `m5.4xlarge` 
- Storage: 500 GB General Purpose SSD
- Security Group: `http+ssh`

## Build instructions

Run these commands in the `bash` shell, in order:

    cd
    
    git clone https://github.com/RTXteam/RTX.git
    
    RTX/code/kg2/setup-kg2.sh

Next, in order to build the RTX KG2, you will need to get a copy of the SNOMED
CT United States Edition distribution as a ZIP archive from the United Sates
National Library of Medicine (NLM). In order to do so, you should go to the
SNOMED CT United States Edition
[distribution page](https://www.nlm.nih.gov/healthit/snomedct/us_edition.html)
[NLM]. Click on the "Download Now!" button, which will take you to a login page
for the Unified Medical Language System (UMLS) at the NLM. You will need to log
in using a UMLS account or click on the "Request one now" hyperlink (where you
will be asked to click through three separate license agreements and then you
will get to a form where you can register for a UMLS account). Once you have
received your login credentials, go back to the SNOMED CT US page (above
hyperlink), click "Download Now!", and log in using your UMLS account. Your
browser then be redirected to a download page. Download
`SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z.zip` to your home directory
where you cloned the RTX git repo (so your home directory should now contain a
subdirectory `RTX`). Then run the following commands in the `bash` shell:

    cd
    
    wget https://github.com/IHTSDO/snomed-owl-toolkit/releases/download/2.0.1/snomed-owl-toolkit-2.0.1-executable.jar
    
    RTX/code/kg2/make-snowmed-owl.sh

The above code will create a new file `ontology-YYYY-MM-DD_HH-mm-SS.owl` (where YYYY
is the year, MM is the month, etc.). Copy this file to `RTX/code/kg2/snomed.owl`:

    cp ontology-YYYY-MM-DD_HH-mm-SS.owl RTX/code/kg2/snomed.owl

Now you are ready to run the setup for building the RTX KG2; select one of the following
subsections to proceed.

## Option 1: setup the KG2 builder directly in Ubuntu 18.04 host OS in AWS:

Prerequisites:
- You are in a new EC2 instance based on the Ubuntu 18.04 AMI
- You are logged in as user `ubuntu`
- You have previously cloned the RTX repo (see above) so that the RTX repo is
under `/home/ubuntu/RTX`.
- You have generated `snomed.owl` and copied it to `/home/ubuntu/RTX/code/kg2`.

Then run these commands in the `bash` shell:

    cd
    
    RTX/code/kg2/setup-kg2.sh
    
    screen
    
    kg2-code/build-kg2.sh

Then exit screen (`ctrl-a d`). You can watch the progress of your KG2 build by using these
two commands (run them in separate bash shell terminals):

    tail -f build-kg2/stdout.log
    
    tail -f build-kg2/stderr.log
    
## Option 2: setup the KG2 builder in a Docker container Ubuntu 18.04 host OS in AWS:

Prerequisites:
- You are in a new EC2 instance based on the Ubuntu 18.04 AMI
- You are logged in as user `ubuntu`
- you have `screen` installed and in the bash PATH
- You have previously cloned the RTX repo (see above) so that the RTX repo is
under `/home/ubuntu/RTX`.
- You have generated `snomed.owl` and copied it to `/home/ubuntu/RTX/code/kg2`.

Then run these commands in the `bash` shell:

    cd
    
    RTX/code/kg2/install-docker.sh
    
    sudo docker build -t kg2 RTX/code/kg2/

    screen
    
    sudo docker run --name kg2 kg2:latest su - ubuntu -c "kg2-code/build-kg2.sh"

Then exit screen (`ctrl-a d`). You can watch the progress of your KG2 build by using these
two commands (run them in separate bash shell terminals):

    sudo docker exec -it kg2 tail -f /home/ubuntu/kg2-build/stdout.log
    
    sudo docker exec -it tail -f /home/ubuntu/kg2-build/stderr.log
    

## Option 3: setup the KG2 builder in a Docker container in another host OS (untested):

Prequisites:
- You are running as an unprivileged user that is set up for passwordless `sudo`
- you have `git` installed and in the bash PATH
- you have `docker` installed and in the bash PATH
- you have `screen` installed and in the bash PATH
- You have previously cloned the RTX repo (see above) so that the RTX repo is
under `~/RTX`.
- You have generated `snomed.owl` and copied it to `~/RTX/code/kg2`.

Then run these commands in the `bash` shell:

    cd
    
    sudo docker build -t kg2 RTX/code/kg2/
    
    screen

    sudo docker run --name kg2 kg2:latest su - ubuntu -c "kg2-code/build-kg2.sh"

Then exit screen (`ctrl-a d`). You can watch the progress of your KG2 build by using these
two commands (run them in separate bash shell terminals):

    sudo docker exec -it kg2 tail -f /home/ubuntu/kg2-build/stdout.log
    
    sudo docker exec -it tail -f /home/ubuntu/kg2-build/stderr.log
    

