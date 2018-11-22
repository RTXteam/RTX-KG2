
# How to build RTX kg2

## Build `snowmed.owl`

Prerequisites:
- `git` is installed and in the bash PATH
- `java` is installed and in the bash PATH

Run these commands in the `bash` shell:

    cd
    
    git clone https://github.com/RTXteam/RTX.git
    
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

## Option 2: setup the KG2 builder in a Docker container Ubuntu 18.04 host OS in AWS:

Prerequisites:
- You are in a new EC2 instance based on the Ubuntu 18.04 AMI
- You are logged in as user `ubuntu`
- You have previously cloned the RTX repo (see above) so that the RTX repo is
under `/home/ubuntu/RTX`.
- You have generated `snomed.owl` and copied it to `/home/ubuntu/RTX/code/kg2`.

Then run these commands in the `bash` shell:

    cd
    
    RTX/code/kg2/install-docker.sh
    
    sudo docker build -t kg2 RTX/code/kg2/

    screen
    
    sudo docker run --name kg2 kg2:latest su - ubuntu -c "kg2-code/build-kg2.sh"

## Option 3: setup the KG2 builder in a Docker container in another host OS (untested):

Prequisites:
- You are running as an unprivileged user that is set up for passwordless `sudo`
- you have `git` installed and in the bash PATH
- you have `docker` installed and in the bash PATH
- You have previously cloned the RTX repo (see above) so that the RTX repo is
under `~/RTX`.

Then run these commands in the `bash` shell:

    cd
    
    sudo docker build -t kg2 RTX/code/kg2/
    
    screen

    sudo docker run --name kg2 kg2:latest su - ubuntu -c "kg2-code/build-kg2.sh"

