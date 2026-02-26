
[![RTX-KG2 Continous Integration](https://github.com/RTXteam/RTX-KG2/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/RTXteam/RTX-KG2/actions/workflows/main.yml)
<!-- TOC --><a name="kg2-the-second-generation-rtx-knowledge-graph"></a>
# KG2: the second-generation RTX knowledge graph

KG2 is the second-generation knowledge graph for the
[ARAX](https://github.com/RTXteam/RTX) biomedical reasoning system.  This [Github 
repository](https://github.com/RTXteam/RTX-KG2) contains all of
the code for building KG2 as well as all of the documentation about how to
build, host, access, and use KG2. The KG2 build system produces knowledge graphs
in a [Biolink model](https://biolink.github.io/biolink-model/)
standard-compliant JSON format and in a tab-separated value (TSV) format that
can be imported into a [Neo4j](https://neo4j.com) graph database system. Through
additional scripts in the ARAX `kg2c` subdirectory, the build system can
produce a "canonicalized" knowledge graph where synonym concepts (nodes) are
identified. Through additional scripts in the `mediKanren` subdirectory, the
build system can produce an export of the KG2 knowledge graph that is suitable
for importing into the [mediKanren](https://github.com/webyrd/mediKanren)
biomedical reasoning system.

The table of contents for this README is as follows:

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [KG2: the second-generation RTX knowledge graph](#kg2-the-second-generation-rtx-knowledge-graph)
- [KG2 team contact information](#kg2-team-contact-information)
   * [KG2 Team](#kg2-team)
   * [Bug reports](#bug-reports)
- [Is RTX-KG2 published?](#is-rtx-kg2-published)
- [How to access RTX-KG2](#how-to-access-rtx-kg2)
   * [Neo4j read-only endpoint for RTX KG2 as a graph database](#neo4j-read-only-endpoint-for-rtx-kg2-as-a-graph-database)
- [What data sources are used in KG2?](#what-data-sources-are-used-in-kg2)
- [How to build RTX-KG2 from its upstream sources](#how-to-build-rtx-kg2-from-its-upstream-sources)
   * [General notes:](#general-notes)
   * [Setup your computing environment](#setup-your-computing-environment)
   * [The KG2 build system assumes there is no MySQL already installed](#the-kg2-build-system-assumes-there-is-no-mysql-already-installed)
   * [AWS buckets](#aws-buckets)
   * [AWS authentication](#aws-authentication)
   * [Typical EC2 instance type used for building KG2](#typical-ec2-instance-type-used-for-building-kg2)
   * [Build instructions](#build-instructions)
         - [What to do if a build fails](#what-to-do-if-a-build-fails)
         - [Note about versioning of KG2](#note-about-versioning-of-kg2)
   * [Possible failure modes for the KG2 build](#possible-failure-modes-for-the-kg2-build)
   * [The output KG](#the-output-kg)
   * [Updating the installed KG2 build system software](#updating-the-installed-kg2-build-system-software)
   * [Hosting KG2 in a Neo4j server on a new AWS instance](#hosting-kg2-in-a-neo4j-server-on-a-new-aws-instance)
   * [Reloading KG2 into an existing Neo4j server](#reloading-kg2-into-an-existing-neo4j-server)
   * [Co-hosting the KG2 build system and Neo4j server?](#co-hosting-the-kg2-build-system-and-neo4j-server)
- [Post-setup tasks](#post-setup-tasks)
- [Schema of the JSON KG2](#schema-of-the-json-kg2)
   * [`build` slot](#build-slot)
   * [`nodes` slot](#nodes-slot)
   * [`edges` slot](#edges-slot)
      + [`publications_info` slot](#publications_info-slot)
   * [Biolink compliance](#biolink-compliance)
- [Frequently asked questions](#frequently-asked-questions)
   * [Where can I download a pre-built copy of KG2?](#where-can-i-download-a-pre-built-copy-of-kg2)
   * [What licenses cover KG2?](#what-licenses-cover-kg2)
   * [What criteria do you use to select sources to include in KG2?](#what-criteria-do-you-use-to-select-sources-to-include-in-kg2)
- [Troubleshooting](#troubleshooting)
   * [Error building DAG of jobs](#error-building-dag-of-jobs)
   * [Authentication Error in `tsv-to-neo4j.sh`](#authentication-error-in-tsv-to-neo4jsh)
   * [Errors in Extraction rules](#errors-in-extraction-rules)
      + [Role exists error](#role-exists-error)
- [For Developers](#for-developers)
   * [KG2 coding standards](#kg2-coding-standards)
      + [Python coding standards for KG2](#python-coding-standards-for-kg2)
- [Shell coding standards for KG2](#shell-coding-standards-for-kg2)
      + [File naming](#file-naming)
- [Credits](#credits)
   * [Code and development work](#code-and-development-work)
   * [Advice and feedback](#advice-and-feedback)
   * [Funding](#funding)

<!-- TOC end -->


<!-- TOC --><a name="kg2-team-contact-information"></a>
# KG2 team contact information

<!-- TOC --><a name="kg2-team"></a>
## KG2 Team

- Stephen Ramsey, Oregon State University (ramseyst@oregonstate.edu)
- Lili Acevedo, Oregon State University (acevedol@oregonstate.edu)
- Amy Glen, Oregon State University (glena@oregonstate.edu)
- Erica Wood, Stanford University

<!-- TOC --><a name="bug-reports"></a>
## Bug reports

Please use the GitHub [issues](https://github.com/RTXteam/RTX-KG2/issues) page for
this project.

<!-- TOC --><a name="is-rtx-kg2-published"></a>
# Is RTX-KG2 published?

Yes, please see:
>Wood, E.C., Glen, A.K., Kvarfordt, L.G. et al. RTX-KG2: a system for building a semantically standardized knowledge graph for translational biomedicine. BMC Bioinformatics 23, 400 (2022). [https://doi.org/10.1186/s12859-022-04932-3](https://doi.org/10.1186/s12859-022-04932-3)

The preprint can be found at: [doi:10.1101/2021.10.17.464747](https://doi.org/10.1101/2021.10.17.464747).

<!-- TOC --><a name="how-to-access-rtx-kg2"></a>
# How to access RTX-KG2

<!-- TOC --><a name="neo4j-read-only-endpoint-for-rtx-kg2-as-a-graph-database"></a>
## Neo4j read-only endpoint for RTX KG2 as a graph database

(RTX-KG2 team members only: contact the KG2 maintainer for the endpoint, username, and password)

<!-- TOC --><a name="what-data-sources-are-used-in-kg2"></a>
# What data sources are used in KG2?

Information from many knowledge databases is combined in building KG2. The table below was compiled from the [Snakemake diagram](https://user-images.githubusercontent.com/36611732/114226788-ea163e80-9928-11eb-808d-5d77e633d278.png) and [ont-load-inventory.yaml](https://github.com/RTXteam/RTX-KG2/blob/master/ont-load-inventory.yaml).





Knowledge Source | Type | Redistribution license info | Home page
-- | -- | -- | --
ChemBL | data | [link](https://chembl.gitbook.io/chembl-interface-documentation/about#data-licensing) | [link](https://www.ebi.ac.uk/chembl/)
DGIDB | data | [link](https://github.com/griffithlab/dgi-db/blob/master/LICENSE) | [link](http://www.dgidb.org/)
DisGeNET | data | [link](http://www.disgenet.org/legal) | [link](http://www.disgenet.org/)
DrugBank | data | [link](https://www.drugbank.ca/legal/terms_of_use) | [link](https://www.drugbank.ca/)
DrugCentral | data |   | [link](https://drugcentral.org/)
Ensembl | data | [link](https://uswest.ensembl.org/info/about/legal/code_licence.html) | [link](https://uswest.ensembl.org/index.html/)
GO_Annotations | data |   | [link](https://www.ebi.ac.uk/GOA/)
Guide to Pharmacology | data |  | [link](https://www.guidetopharmacology.org/)
HMDB | data |   | [link](http://www.hmdb.ca/)
IntAct | data |   | [link](https://www.ebi.ac.uk/intact/)
JensenLab | data |   | [link](https://diseases.jensenlab.org/About)
miRBase | data | [link](http://mirbase.org/help/FAQs.shtml#Do%20I%20need%20permission%20to%20download/use%20data%20contained%20in%20miRBase%20for%20my%20own%20research?) | [link](http://www.mirbase.org/)
NCBIGene | data |   | [link](https://www.ncbi.nlm.nih.gov/gene)
PathWhiz | data |   | [link](https://smpdb.ca/pathwhiz)
Reactome | data | [link](https://reactome.org/license) | [link](https://reactome.org/)
SemMedDB | data | [link](https://skr3.nlm.nih.gov/TermsAndCond.html) | [link](https://skr3.nlm.nih.gov/SemMedDB/)
SMPDB | data | [link](https://smpdb.ca/about#citing) | [link](https://smpdb.ca/)
Therapuetic Target Database | data | | [link](http://db.idrblab.net/ttd/)
Unichem | data |   | [link](https://www.ebi.ac.uk/unichem/)
UniprotKB | data | [link](https://www.uniprot.org/help/license) | [link](https://www.uniprot.org/help/uniprotkb)
Anatomical Therapeutic Chemical Classification System | ontology |   | [link](https://www.whocc.no/atc_ddd_index/)
Basic Formal Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/bfo.html)
Biological Spatial Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/bspo.html)
Cell Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/cl.html)
Chemical Entities of Biological Interest | ontology |   | [link](http://www.obofoundry.org/ontology/chebi.html)
CPT in HCPCS | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/HCPT/index.html)
Current Procedural Terminology | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/CPT/index.html)
Dictyostelium discoideum anatomy | ontology |   | [link](http://www.obofoundry.org/ontology/ddanat.html)
Disease Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/doid.html)
Experimental Factor Ontology | ontology |   | [link](https://www.ebi.ac.uk/efo/)
FOODON (Food Ontology) | ontology |   | [link](http://www.obofoundry.org/ontology/foodon.html)
Foundational Model of Anatomy | ontology |   | [link](http://www.obofoundry.org/ontology/fma.html)
Gene Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/go.html)
Gene Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/go.html)
Genomic Epidemiology Ontology | ontology |   | [link](http://purl.obolibrary.org/obo/genepio.owl)
Healthcare Common Procedure Coding System | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/HCPCS/index.html)
HL7 Version 3.0 | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/HL7)
HUGO Gene Nomenclature Committee | ontology |   | [link](https://www.genenames.org/)
Human developmental anatomy, abstract | ontology |   | [link](http://obofoundry.org/ontology/ehdaa2.html)
Human Phenotype Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/hp.html)
ICD-10 Procedure Coding System | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD10PCS/index.html)
Interaction Network Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/ino.html)
International Classification of Diseases, Ninth Revision, Clinical Modification | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/ICD9CM)
Medical Subject Headings | ontology |   | [link](https://www.nlm.nih.gov/mesh/meshhome.html)
Medication Reference Terminology | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MED-RT)
MedlinePlus Health Topics | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MEDLINEPLUS/index.html)
Metathesaurus Names | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/MTH)
Molecular Interactions Controlled Vocabulary | ontology |   | [link](http://purl.obolibrary.org/obo/mi.owl)
MONDO Disease Ontology | ontology |   | [link](http://obofoundry.org/ontology/mondo.html)
National Drug Data File | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NDDF/index.html)
National Drug File | ontology |  | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/VANDF)
National Drug File - Reference Terminology | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NDFRT)
NCBITaxon | ontology |   | [link](http://www.obofoundry.org/ontology/ncbitaxon.html)
NCI Thesaurus | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NCI)
Neuro Behavior Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/nbo.html)
Online Mendelian Inheritance in Man | ontology | [link](https://www.omim.org/help/copyright) | [link](https://www.omim.org/)
ORPHANET Rare Disease Ontology | ontology |   | [link](https://bioportal.bioontology.org/ontologies/ORDO)
Phenotypic Quality Ontology | ontology |   | [link](https://bioportal.bioontology.org/ontologies/PATO)
Physician Data Query | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/PDQ)
Protein Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/pr.html)
Psychological Index Terms | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/PSY)
Relation Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/ro.html)
RXNORM | ontology |   | [link](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/RXNORM/index.html)
Uber-anatomy Ontology | ontology |   | [link](http://www.obofoundry.org/ontology/uberon.html)


<!-- TOC --><a name="how-to-build-rtx-kg2-from-its-upstream-sources"></a>
# How to build RTX-KG2 from its upstream sources

<!-- TOC --><a name="general-notes"></a>
## General notes

The KG2 build system is designed only to run in an **Ubuntu 22.04** environment
(i.e., either (i)&nbsp;an Ubuntu 22.04 host OS or (ii)&nbsp;Ubuntu 22.04 running in a
Docker container) as a non-root user which must have passwordless `sudo` enabled
and should have `bash` as the default shell (the build commands in the
instructions in this README page assume a `bash` shell). The build system will
also need (but will set up for itself, prompting the user for access keys at
setup time) a local configured installation of the Amazon Web Services (AWS)
command-line interface (CLI) software in order to be able to retrieve various
required files on-demand from a storage bucket in the AWS Simple Storage Service
(S3) system. Currently, KG2 is built using a set of `bash` scripts that are
designed to run in Amazon's Elastic Compute Cloud (EC2), and thus,
configurability and/or coexisting with other installed software pipelines was
not a design consideration for the build system. The KG2 build system's `bash`
scripts create three subdirectories under the `${HOME}` directory of whatever
Linux user account you use to run the KG2 build software (if you run on an EC2
Ubuntu instance, this directory would by default be `/home/ubuntu`):

1. `~/kg2-build`, where various build artifacts are stored
2. `~/kg2-code`, which is a symbolic link to the git checkout directory `RTX-KG2/`
3. `~/kg2-venv`, which is the virtualenv for the KG2 build system

The various directories used by the KG2 build system are configured in the
`bash` include file `master-config.shinc`. Most of the KG2 build system code is
written in the Python3 programming language, and designed to run in python3.13.

Note about atomicity of file moving: The build software is designed to run with
the `kg2-build` directory being in the same file system as the Python temporary
file directory (i.e., the directory name that is returned by the variable
`tempfile.tempdir` in Python). If the KG2 software or installation is modified
so that `kg2-build` is in a different file system from the file system in which
the directory `tempfile.tempdir` (as referenced in the `tempfile` python module)
resides, then the file moving operations that are performed by the KG2 build
software will not be atomic and interruption of `build-kg2.sh` or its
subprocesses could then leave a source data file in a half-downloaded (i.e.,
broken) state. 

**Build Frequency:** We
are currently aiming to build KG2 approximately once per month, to keep it as
current as feasible given the cost to build and validate KG2 from its upstream
sources.

<!-- TOC --><a name="setup-your-computing-environment"></a>
## Setup your computing environment

The computing environment where you will be running the KG2 build should be
running **Ubuntu 22.04**.  Your build environment should have the following
*minimum* hardware specifications:

- 128 GiB of system memory
- 1,023 GiB of disk space in the root file system 
- high-speed networking (20 Gb/s networking) and storage
- if you are on the RTX-KG2 team: ideally your build system should be in the AWS
  region `us-west-2` since that is where the RTX KG2 S3 buckets are located

We use `r5a.4xlarge` AWS instances for KG2 builds.

<!-- TOC --><a name="the-kg2-build-system-assumes-there-is-no-mysql-already-installed"></a>
## If there is an existing MySQL database on the build system

The target Ubuntu system in which you will run the KG2 build should *not* have
MySQL installed; if MySQL is already installed, you will need to delete it,
which you can do using the following `bash` command, which requires `curl`:
(WARNING! Please don't run this command without first making a backup image of
your system, such as an AMI):

    source <(curl -s https://raw.githubusercontent.com/RTXteam/RTX-KG2/master/delete-mysql-ubuntu.sh)

The KG2 build system has been tested *only* under Ubuntu 18.04. If you want to
build KG2 but don't have a native installation of Ubuntu 18.04 available, your
best bet would be to use Docker (see Option 3 below). 

<!-- TOC --><a name="aws-buckets"></a>
## AWS buckets

In order to be able to build KG2, you'll need to have at least one AWS S3 bucket
set up (or use an existing bucket; for the KG2 creators, we use S3 three
buckets, `s3://rtx-kg2`, `s3://rtx-kg2-public`, and `s3://rtx-kg2-versioned`,
which are in the `us-west-2` AWS region) and you will need to have an AWS
authentication key pair that is configured to be able to read from (and write
to) the bucket(s), so that the build script can download a copy of the full
Unified Medical Language System (UMLS) distribution. The full UMLS distribution (`umls-2023AA-metathesaurus.zip`) can be obtained at the
[UMLS website](https://www.nlm.nih.gov/research/umls/) (only if you agree to the UMLS
license terms)), the DrugBank distribution (`drugbank.xml.gz`), the SMPDB publications CSV file (obtained from the Wishart Lab), and the SemMedDB distriction will need to
be pre-placed in the S3 bucket and the local copy of `master-config.shinc` will
need to be configured so that variables `s3_bucket`, `s3_bucket_public`, and
`s3_bucket_versioned` point to the S3 bucket(s) and so that the shell variable
`s3_region` identifies the AWS region in which the bucket(s) reside(s).

<!-- TOC --><a name="aws-authentication"></a>
## AWS authentication

For the KG2 build system that we (the creators of KG2) have set up for use by
Team Expander Agent, the authentication key pair is associated with an IAM
account with username `kg2-builder`; if you are setting up the KG2 build system
somewhere else, you will need to obtain your own AWS authentication key pair
that connects to an IAM account (or root AWS account, if you want to live
dangerously) that has S3 privileges to read from and write to the S3 buckets
that are configured in your local copy of `master-config.shinc`. When you run
the KG2 setup script, you will be asked (by the AWS Command-line Interface, CLI)
to provide an authentication key pair.  and it uploads the final output file
`kg2-simplified.json.gz` to the buckets identified by the shell variables
`s3_bucket` defined in `master-config.shinc` (for the KG2 creators, that bucket
is `s3://rtx-kg2`). Alternatively, you can set up your own S3 bucket to which to
copy the gzipped KG2 JSON file (which you would specify in the configuration
file `master-config.shinc`), or in the file `finish-snakemake.sh`, you can
comment out the line that copies the final gzipped JSON file to the S3
bucket. You will also need to edit (to fill in the correct Neo4j password) and
place a file `RTXConfiguration-config.json` (template is in the KG2 source code
directory) into the S3 bucket identified by the shell variable `s3_bucket` in
`master-config.shinc` (for the KG2 creators, that bucket is `s3://rtx-kg2/`);
As a minimal example of the data format for `RTXConfiguration-config.json`, see the file
`RTXConfiguration-config-EXAMPLE.json` in this repository code directory (note:
that config file can contain authentication information for additional server
types in the RTX system; those are not shown in the example file in this code
directory).

<!-- TOC --><a name="typical-ec2-instance-type-used-for-building-kg2"></a>
## Typical EC2 instance type used for building KG2

The KG2 build software has been tested with the following instance type:

- AMI: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type - `ami-005bdb005fb00e791` (64-bit x86)
- Instance type: `r5a.4xlarge` (128 GiB of memory)
- Storage: 1,023 GiB, Elastic Block Storage
- Security Group: ingress TCP packets on port 22 (`ssh`) permitted

As of summer 2024, an on-demand `r5a.4xlarge` instance in the `us-west-2` AWS
region costs $0.904 per hour, so the cost to build KG2 (estimated to take 25
hours) would be approximately $23 (rough estimate, plus or minus
20%).

<!-- TOC --><a name="build-instructions"></a>
## Build instructions

These instructions assume that you are logged into the target Ubuntu system, and
that the Ubuntu system has *not* previously had `setup-kg2-build.sh` run (if it
has previously had `setup-kg2-build.sh` run, you should first clear out the
instance by running `clear-instance.sh` before proceeding, in order to ensure
that you are getting the exact python packages needed in the latest
`requirements-kg2-build.txt` file in the KG2 codebase) and to ensure that
your build does not inadvertantly reuse artifacts from a previous RTX-KG2 build:

(1) Install the `git` and `screen` packages if they are not already installed (though
in an Ubuntu 22.04 instance created using the standard AWS AMI, they should already
be installed):

    sudo apt-get update && sudo apt-get install -y screen git

(2) change to the home directory for user `ubuntu`:

    cd 
    
(3) Clone the RTX software from GitHub:

    git clone https://github.com/RTXteam/RTX-KG2.git

[An advantage to having the `git clone` command separated out from the install script is
that it provides control over which branch you want to use for the KG2 build code.]

(4) Change branches to the KG2 build code if necessary

    cd ~/RTX-KG2/
    git checkout [branch name]

(5) Setup the KG2 build system: 

    cd
    bash -x ~/RTX-KG2/setup/setup-kg2-build.sh

Note that there is no need to redirect `stdout` or `stderr` to a log file, when
executing `setup-kg2-build.sh`; this is because the script saves its own `stdout` and
`stderr` to a log file `~/kg2-build/setup-kg2-build.log`. This script takes just a
few minutes to complete. At some point, the script will print

    fatal error: Unable to locate credentials
    
This is normal. The script will then prompt you to enter:
- your AWS Access Key ID
- your AWS Secret Access Key 
    - (both for an AWS account with access to the private S3 bucket that is configured in `master-config.shinc`)
- your default AWS region, which in our case is normally `us-west-2` 
    - (you should enter the AWS region that hosts the private S3 bucket that you intend to use with the KG2 build system)
- When prompted `Default output format [None]`, just hit enter/return.

For KG2 builders on the `RTX-KG2` team, just use the keypair for the `kg2-builder` IAM user.

If all goes well, the setup script should end with the message:

    upload: ../setup-kg2-build.log to s3://rtx-kg2-versioned/setup-kg2-build.log

printed to the console. The aforementioned message means that the logfile from
running the setup script has been archived in the `rtx-kg2-versioned` S3 bucket.

(6) Look in the log file `~/kg2-build/setup-kg2-build.log` to see if the script
completed successfully; it should end with `======= script finished ======`.
In that case it is safe to proceed.

(7) [**THIS STEP IS NORMALLY SKIPPED**] If (and *only* if) you have made code
changes to KG2 that will cause a change to the schema for KG2 (or added a major
new upstream source database), you will want to increment the "major" release
number for KG2. To do that, at this step of the build process, you would run
this command:

    touch ~/kg2-build/major-release

[**MORE COMMON ALTERNATIVE**] For regular releases, you want to increment the "minor"
release number. This is for situations where changes to the code have been made and
the build will likely be deployed. If you want to increment the "minor" release number
for KG2, you would run this command:

    touch ~/kg2-build/minor-release

If you don't increment the release number at all, you should not be planning to deploy
the build. This is useful for cases where you are testing the build system, but not
necessarily different code or bug fixes.

(8) Run a "dry-run" build:

    bash -x ~/kg2-code/build/build-kg2-snakemake.sh all -F -n
    
and inspect the file `~/kg2-build/build-kg2-snakemake-KG2.{major version}.{minor version}-n.log` that will be created, to make sure that
all of the KG2 build tasks are included. Currently, the file should end with the following
count of tasks:
```
Job counts:
        count   jobs
        1         ChEMBL
        1         ChEMBL_Conversion
        1         ClinicalTrialsKG
        1         ClinicalTrialsKG_Conversion
        1         DGIdb
        1         DGIdb_Conversion
        1         DisGeNET
        1         DisGeNET_Conversion
        1         DrugBank
        1         DrugBank_Conversion
        1         DrugCentral
        1         DrugCentral_Conversion
        1         Ensembl
        1         Ensembl_Conversion
        1         Finish
        1         GO_Annotations
        1         GO_Annotations_Conversion
        1         HMDB
        1         HMDB_Conversion
        1         IntAct
        1         IntAct_Conversion
        1         JensenLab
        1         JensenLab_Conversion
        1         KEGG
        1         KEGG_Conversion
        1         Merge
        1         NCBIGene
        1         NCBIGene_Conversion
        1         Ontologies
        1         Ontologies_Conversion
        1         Reactome
        1         Reactome_Conversion
        1         SMPDB
        1         SMPDB_Conversion
        1         SemMedDB
        1         SemMedDB_Conversion
        1         Simplify
        1         Simplify_Stats
        1         Slim
        1         Stats
        1         TSV
        1         UMLS
        1         UMLS_Conversion
        1         UniChem
        1         UniChem_Conversion
        1         UniProtKB
        1         UniProtKB_Conversion
        1         ValidationTests
        1         miRBase
        1         miRBase_Conversion
        50
This was a dry-run (flag -n). The order of jobs does not reflect the order of execution.
+ [[ '' != \t\e\s\t ]]
+ [[ -n != \-\n ]]
+ [[ '' != \t\e\s\t ]]
+ [[ -n != \-\n ]]
+ [[ '' != \t\e\s\t ]]
+ [[ -n != \-\n ]]
+ date
Mon Sep  9 02:17:09 UTC 2024
+ echo '================ script finished ============================'
================ script finished ============================
```
Assuming the log file looks correct, proceed.

(9) Initiate a `screen` session to provide a stable pseudo-tty:

    screen

(then hit return to get into the screen session).

(10) THIS STEP COMMENCES THE BUILD. Within the screen session, run:

    bash -x ~/kg2-code/build/build-kg2-snakemake.sh all -F

You may exit out of the screen session using the `ctrl-a d` key sequence.  The
`all` command line argument specifies that you would like to run a full build.
This is the best option if you are running on a new instance, or have added
upstream sources.  Otherwise, consider the following options:

<details>
  <summary> Partial Build of KG2 </summary>


In some circumstances, if there are no updates to any of the upstream source
databases (like UMLS, ChEMBL, SemMedDB, etc.) that are extracted using
`extract*.sh` scripts (as shown in the list of KG2 scripts), you can trigger
a "partial" build. This can be useful in cases where you are testing a change
to one of the YAML configuration files for KG2, for example. To do a partial
build, in Step (8) above, you would run

    bash -x ~/kg2-code/build/build-kg2-snakemake.sh

(note the absence of the `all` argument to `build-kg2-snakemake.sh`). A partial build of KG2
may take about 12 hours. Note, you have to have previously run an `all` build
of KG2, or else the partial build will not work. Note, when doing a partial build,
existing KG2 JSON files in the `/home/ubuntu/kg2-build` directory (which have filenames
like `kg2-*.json`) from previous
builds will just get used and will _not_ get updated; if you want any of those files
to get updated, you should _delete_ them before running the partial build.
</details>

<details>
  <summary> Test Build of KG2 </summary>

For testing/debugging purposes, it is helpful to have a faster way to exercise
the KG2 build code. For this, you may want to execute a "test" build. This build
mode builds a smaller graph with a significantly reduced set of nodes and edges.
Before you can do a test build, you must have previously done a full *non-test*
build of KG2 at least once. To execute a full *test*
build, in Step (8) above, you would run:

  bash -x ~/kg2-code/build/build-kg2-snakemake.sh test

In the case of a test build, the intermediate JSON and TSV and log files created by the build system
will have `-test` appended to the filename before the usual filename suffix
(`.json`).
</details>

Note that there is no need to redirect `stdout` or `stderr` to a log file, when
executing `build-kg2-snakemake.sh`; this is because the script saves its own
`stdout` and `stderr` to a log file `~/kg2-build/build-kg2-snakemake.log`. You
can watch the progress of your KG2 build by using this command:

    tail -f ~/kg2-build/build-kg2-snakemake-KG2.{major version}.{minor version}.log
    
That file shows what has finished and what is still happening. If any line says

`(exited with non-zero exit code)`

the code has failed. However, since the code is 
running in parallel, to minimize confusion, `stdout` and `stderr`
for extraction and conversion scripts is piped into its own final based on the name of the script that runs. Log scripts are stored in `~/kg2-build/`

At the end of the build process, you should inspect the logfile
`~/kg2-build/filter_kg_and_remap_predicates.log` to see if there are warnings
like ``` relation curie is missing from the YAML config file:
CURIEPREFIX:some_predicate ``` where `CURIEPREFIX` could be any CURIE prefix in
`curies-to-urls-map.yaml` and `some_predicate` is a snake-case predicate label
(or in the case of Relation Ontology, a numeric identifier). Any warnings of the
above format in `filter_kg_and_remap_predicates.log` probably indicates that an
addition needs to be made to the file `predicate-remap.yaml`, followed by a
partial rebuild starting with `filter_kg_and_remap_predicates.py`(the `Simplify` rule).

<!-- TOC --><a name="what-to-do-if-a-build-fails"></a>
#### What to do if a build fails

- Let's suppose the build failed on the rule `UniChem`. In that case, you could
fix the bug and then test your bugfix by running ```
/home/ubuntu/kg2-venv/bin/snakemake --snakefile /home/ubuntu/kg2-code/build/Snakefile
-R --until UniChem ``` which *just* runs that rule. Note, you should only use
the above command after you have run `build-kg2-snakemake.sh` (as in Step 8
above) at least once, otherwise you will get an error because the required
Snakefile `~/kg2-code/Snakefile` will not yet exist. Assuming that the above
command is successful, you could then proceed.

- Restart the full build:
```
bash -x ~/kg2-code/build/build-kg2-snakemake.sh all
```
(Note, you only need the `all` above if the rule is for an "extract-XXX.sh" script;
if it is for a rule that is downstream of the extract scripts, you can omit `all`.

<!-- TOC --><a name="note-about-versioning-of-kg2"></a>
#### Semantics versioning of KG2

KG2 has semantic versioning with a graph/major/minor release system:
- The graph release number is always 2. 
- The major release number is incremented when the schema for KG2 is changed
  (and the minor release is set to zero in that case)
- The minor release number is incremented for each non-test build for which the
  schema is not modified.
  
So an example version of KG2 would be "RTX KG 2.1.3" (graph release 2, major
release 1, minor release 3). This build version is recorded in three places:
- the top-level `build` slot in the KG2 JSON file
- in the `name` field of a node object with `id` field `RTX:KG2` (in both the
  JSON version of the KG2pre graph and in the Neo4j version of the KG2pre graph)
- the file `s3://rtx-kg2-public/kg2-version.txt` in the S3 bucket `rtx-kg2-public`.

By default, the KG2 build process (as outlined above) will automatically
increment the minor release number and update the file `kg2-version.txt` in the
S3 bucket.  If you are doing a build in which the KG2 schema has changed, you
should trigger the incrementing of the major release version by making sure to
do step (6) above.  The build script (specifically, the script `version.sh`)
will automatically delete the file `~/kg2-build/major-release` so that it will
not persist for the next build. Note: if the build system happens to terminate
unexpectedly while running `version.sh`, or after the `Simplify` rule,
you should check what state the file`s3://rtx-kg2-public/kg2-version.txt` was left in. 

The version history for KG2 can be found [here](kg2-versions.md).


<!-- TOC --><a name="possible-failure-modes-for-the-kg2-build"></a>
## Possible failure modes for the KG2 build

Occasionally a build will fail due to a connection error in attempting to
cURL a file from one of the upstream sources (e.g., SMPDB, and less frequently, 
UniChem). **As of KG2.10.1, several sources have hardcoded downloads from the S3 bucket - HMDB, DisGeNET, CHEBI, and ClinicalTrials KG. These hardcoded downloads should be backed out as the resolution improves.** If KEGG's download fails, the conversion will fail and the extraction log will finish extremely fast. If KEGG's extraction finishes in less than 15 minutes, there is a connection issue.

Another failure mode is the versioning of ChemBL. Once ChemBL upgrades their dataset, 
old datasets may become unavailable. This will result in failure when downloading. To 
fix this, change the version number in `extract-chembl.sh`.

If the extract script is run too many times, MySQL might generate too many binary log files filling up the instance storage. This can be verified using the following command:
```
sudo su - root
cd /var/lib/mysql
du -s -h
```
To fix this issue, the following command can be executed using the `mysql` command: 
```
mysql -u ubuntu -p
{Enter the mySQL password}
mysql> PURGE BINARY LOGS BEFORE now();
```

<!-- TOC --><a name="the-output-kg"></a>
## The output KG

The `build-kg2-snakemake.sh` script creates
 gzipped JSON Lines files and copies them to an S3 bucket
`rtx-kg2`. You can access the gzipped JSON Lines files using the AWS command-line
interface (CLI) tool `aws` with the command

    aws s3 cp s3://rtx-kg2/kg2-simplified-KG2.{major version}.{minor version}-nodes.jsonl.gz .
    aws s3 cp s3://rtx-kg2/kg2-simplified-KG2.{major version}.{minor version}-edges.jsonl.gz .

The TSV files for the knowledge graph can be accessed via HTTP as well, 

    aws s3 cp s3://rtx-kg2/kg2-tsv-KG2.{major version}.{minor version}.tar.gz .

You can access the various artifacts from the KG2 build (config file, log file,
etc.) at the AWS static website endpoint for the 
`rtx-kg2-public` S3 bucket: <http://rtx-kg2-public.s3-website-us-west-2.amazonaws.com/>

Each build of KG2 is labeled with a unique build date/timestamp. The build timestamp
can be found in the `build` slot of the `kg2-simplified.json` file and it can be
found in the node with ID `RTX:KG2` in the Neo4j KG2 database.

<!-- TOC --><a name="updating-the-installed-kg2-build-system-software"></a>
## Updating the installed KG2 build system software

We generally try to make the KG2 shell scripts idempotent, following best
practice for *nix shell scripting. However, changes to `setup-kg2-build.sh` (or
`setup-kg2-neo4j.sh`) that would bring in a new version of a major software
dependency (e.g., Python) of the KG2 build system are not usually tested for
whether they can also upgrade an *existing* installation of the build system;
this is especially an issue for software dependencies that are installed using
`apt-get`. In the event that `setup-kg2-build.sh` undergoes a major change that
would trigger such an upgrade (e.g., from Python3.13 to Python3.14 or whatever), 
instead of rerunning `setup-kg2-build.sh` on your existing build system, we recommend that
you create a clean Ubuntu instance and install using `setup-kg2-build.sh`.

<!-- TOC --><a name="hosting-kg2-in-a-neo4j-server-on-a-new-aws-instance"></a>
## Hosting KG2 in a Neo4j server on a new AWS instance

We host our production KG2 graph database in Neo4j version 3.5.13 with APOC
3.5.0.4, on an Ubuntu 18.04 EC2 instance with 64 GiB of RAM and 8 vCPUs
(`r5a.2xlarge`) in the `us-east-2` AWS region.

**Installation:** in a newly initialized Ubuntu 18.04 AWS
instance, as user `ubuntu`, run the following commands:

(1) Make sure you are in your home directory:

    cd
    
(2) Clone the RTX software from GitHub:

    git clone https://github.com/RTXteam/RTX-KG2.git

(3) Change branches to the KG2 buid code if necessary

    cd ~/RTX-KG2/
    git checkout [branch name]

(4) Install and configure Neo4j, with APOC:

    bash -x ~/RTX-KG2/neo4j/setup-kg2-neo4j.sh

This script takes just a few minutes to complete. At some point, the script will
print

    fatal error: Unable to locate credentials
    
This is normal. The script will then prompt you to enter your AWS Access Key ID
and AWS Secret Access Key, for an AWS account with access to the private S3
bucket that is configured in `master-config.shinc`. It will also ask you to
enter your default AWS region; you should enter the AWS region that hosts the
private S3 bucket that you intend to use with the KG2 build system, which in our
case would be `us-west-2`. When prompted `Default output format [None]`, just
hit enter/return. Also, the setup script will print a warning

    WARNING: Max 1024 open files allowed, minimum of 40000 recommended. See the Neo4j manual.
    
but this, too, can be ignored [The `/lib/systemd/service/neo4j.service` file 
that is installed (indirectly) by the setup script actually sets the limit to 60000,
for when the Neo4j database system is run via systemd (but when running `neo4j-admin`
at the CLI to set the password, Neo4j doesn't know this and it reports a limit warning).]

(5) Look in the log file `${HOME}/setup-kg2-neo4j.log` to see if the script
completed successfully; it should end with `======= script finished ======`.

(6) Start up a `screen` session, and within that screen session, load KG2 into Neo4j:

    bash -x ~/RTX-KG2/neo4j/tsv-to-neo4j.sh > ~/kg2-build/tsv-to-neo4j.log 2>&1

This script takes over three hours to complete.

(6) Look in the log file `~/kg2-build/tsv-to-neo4j.log` to see if the script
completed successfully; it should end with `======= script finished ======`.

<!-- TOC --><a name="reloading-kg2-into-an-existing-neo4j-server"></a>
## Reloading KG2 into an existing Neo4j server

Once you have loaded KG2 into Neo4j as described above, if you want to reload
KG2, just run (as user `ubuntu`):

    bash -x ~/RTX-KG2/tsv-to-neo4j.sh > ~/kg2-build/tsv-to-neo4j.log 2>&1

<!-- TOC --><a name="co-hosting-the-kg2-build-system-and-neo4j-server"></a>
## Co-hosting the KG2 build system and Neo4j server?

In theory, it should be possible to install Neo4j and load KG2 into it on the
same Ubuntu instance where KG2 was built; but this workflow is usually not
tested since in our setup, we nearly always perform the KG2 build and Neo4j
hosting on separate AWS instances. This is because the system requirements
to build KG2 are much greater than the system requirements to host KG2 in 
Neo4j.

<!-- TOC --><a name="post-setup-tasks"></a>
# Post-setup tasks

- We typically define a DNS `CNAME` record for the KG2 Neo4j server hostname, of
the form `kg2endpoint-kg2-X-Y.rtx.ai`, where `X` is the major version number and
`Y` is the minor version number.  
- Before you release a new build of KG2, please update the
[version history markdown file](kg2-versions.md) with the new build version and
the numbers of the GitHub issues that are addressed/implemented in the new KG2
version.
- After a build has successfully completed and verified, add a new release with the KG2 version number to GitHub. Include the `kg2-versions.md` entry for the version in the release text.
- Wherever possible we try to document the name of the build host (EC2 instance)
used for the KG2 build in `kg2-versions.md` and we try to preserve the `kg2-build`
directory and its contents on that host, until a new build has superseded the build.
Having the build directory available on the actual build host is very useful for
tracking down the source of an unexpected relationship or node property. 
*Any new data sources in the build or major updates* (e.g., DrugBank, UMLS, or ChEMBL)
should also be noted in the `kg2-versions.md` file.

- One of the key build artifacts that should be inspected in order to assess the
build quality is the JSON report
`kg-simplified-report-KG2.{major version}.{minor version}.json`.
This file should be inspected as a part of the post-build quality assessment process.

- After the build completes, review the file (in the `kg2-build` directory)
`kg2-orphan-edges-2.XX.XX.jsonl` to determine if there is an issue with an anomalously
large number of edges from a particular source being "orphaned" in the build.

<!-- TOC --><a name="schema-of-the-json-kg2"></a>
# Schema of the JSON KG2

The files `kg2-merged-KG2.{major version}.{minor version}-edges.jsonl` and `kg2-merged-KG2.{major version}.{minor version}-nodes.jsonl` are intermediate files probably only of use to KG2
developers.  The files `kg2-simplified-KG2.{major version}.{minor version}-edges.jsonl` and `kg2-simplified-KG2.{major version}.{minor version}-nodes.jsonl` are key artifacts of the build
process that feed into several downstream artifacts and may be of direct use to
application developers. Newlines, carriage returns, linefeed characters, or hard
tabs are not allowed in any string property or in any string scalar within a
list property in KG2. The JSON LInes data structure is a
name-value pair object (i.e., dictionary) with the following keys:

<!-- TOC --><a name="build-slot"></a>
## `build` slot
The top-level `build` slot contains a dictionary whose keys are:

  - `version`: a string containing the version identifier for the KG2 build,
    like `RTX KG2.2.3`.  For a "test" build, the version identifier will have
    `-TEST` appended to it.
  - `timestamp_utc`: a string containing the ISO 8601 date/timestamp (in UTC)
  for the build, like this: `2020-08-11 21:51`.
  
<!-- TOC --><a name="nodes-slot"></a>
## `nodes` slot

The top-level `nodes` slot contains a list of node objects. Each node object has
the following keys:
  - `category`: a string containing a CURIE ID for the semantic type of the
    node, as a category in the Biolink model. Example: `biolink:Gene`.
  - `category_label`: a `snake_case` representation of the `category` field,
    without the `biolink:` CURIE prefix.
  - `creation_date`: a string identifier of the date in which this node object
  was first created in the upstream source database; it has (at present) no
  consistent format, unfortunately (usual value is `null`).
  - `deprecated`: a Boolean field indicating whether or not this node has been
    deprecated by the upstream source database (usual value is `false`).
  - `description`: a narrative description field for the node, in prose text
  - `full_name`: a longer name for the node (often is identical to the `name` field)
  - `id`: a CURIE ID for the node; this CURIE ID will be unique across nodes in
    KG2 (that constraint is enforced in the build process)
  - `iri`: a URI where the user can get more information about this node (we try
    to make these resolvable wherever possible)
  - `name`: a display name for the node
  - `provided_by`: A CURIE ID list (which corresponds to an actual node in KG2) for the 
  upstream information resource that is the definitive source for information about
  this node. 
  - `publications`: a list of CURIE IDs of publications (e.g., `PMID` or `ISBN`
    or `DOI` identifiers) that contain information about this node
  - `replaced_by`: a CURIE ID for the node that replaces this node, for cases
    when this node has been deprecated (usually it is `null`).
  - `synonym`: a list of strings with synonyms for the node; if the node is a
  gene, the first entry in the list should be the official gene symbol; other
  types of information can for certain node types be found in this list, such as
  protein sequence information for UniProt protein nodes. The entries in the
  node synonym property (which is of type list) are not guaranteed to be `id`
  fields of actual nodes in KG2. Also, they are not comprehensive; if node Y is
  related to node X by a `biolink:same_as` relation type, there is no guarantee
  that Y will be in the synonym property list for X (in most cases, it won't
  be). 
  - `update date`: a string identifier of the date in which the information for
  this node object was last updated in the upstream source database; it has (at
  present) no consitent format, unfortunately; it is usually not `null`.
  - `has_biological_sequence`: a string of sequence information for nodes from DrugBank (SMILES),
  ChemBL (Canonical SMILES), HMDB (SMILES), miRBase ("sequence" - appears to be amino acids), and
  UniprotKB ("sequence" - also appears to be amino acids). For nodes from other sources,
  this property is `null`.

<!-- TOC --><a name="edges-slot"></a>
## `edges` slot
- `edges`: a list of edge objects. Each edge object has the following keys:
  - `relation_label`: a `snake_case` representation of the plain English label for
    the original predicate for the edge provided by the upstream source database
    (see the `relation` field)
  - `negated`: a Boolean field indicating whether or not the edge relationship
    is "negated"; usually `false`, in the normal build process for KG2
  - `object`: the CURIE ID (`id`) for the KG2 node that is the object of the
    edge
  - `primary_knowledge_source`: A list containing CURIE IDs (each of which corresponds to an actual node in KG2) for the 
  upstream information resources that reported this edge's specific
  combination of subject/predicate/object (in the case of multiple providers for
  an edge, the other fields like `publications` are merged from the information
  from the multiple sources).
  - `publications`: a list of CURIE IDs of publications supporting this edge
    (e.g., `PMID` or `ISBN` or `DOI` identifiers)
  - `publications_info`: a dictionary whose keys are CURIE IDs from the list in the
  `publications` field, and whose values are described in the next subsection ("publication_info")
  - `predicate_label`: a `snake_case` representation of the plain English
    label for the simplified predicate (see the `predicate`
    field); in most cases this is a predicate type from the Biolink model.
  - `predicate`: a CURIE ID for the simplified relation
  - `subject`: the CURIE ID (`id`) for the KG2 node that is the subject of the
    edge
  - `update_date`: a string identifier of the date in which the information for
  this node object was last updated in the upstream source database; it has (at
  present) no consitent format, unfortunately; it is usually not `null`.
  - `id`: a concatenated string of other edge attributes that uniquely identifies the edge
  - `source_predicate`: a CURIE ID for the relation as reported by the upstream
    database source.
  - `qualified_predicate`
  - `qualified_object_aspect`
  - `qualified_object_direction`

<!-- TOC --><a name="publications_info-slot"></a>
### `publications_info` slot

If it is not `null`, the `publications_info` object's values are objects containing
the following name/value pairs:
  - `publication date`: string representation of the date of the publication, in
    ISO 8601 format (`%Y-%m-%d %H:%i:%S`)
  - `sentence`: a string containing the natural language sentence from which the
    edge was inferred (this is only not `null` for SemMedDB edges, at present)
  - `subject score`: a string containing a confidence score; for SemMedDB edges,
    this score corresponds to a confidence with which the subject of the triple
    was correctly identified; for other edges (like ChEMBL drug to target
    predictions), the score corresponds to a confidence in a computational
    prediction of the ligand-to-target binding relationship; NOTE: there at
    present no unified scale for this field, unfortunately
  - `object score`: for SemMedDB edges, this score corresponds to a confidence
    with which the subject of the triple was correctly identified; otherwise
    `null`

<!-- TOC --><a name="biolink-compliance"></a>
## Biolink compliance

KG2 aims to comply with the Biolink knowledge graph format.

<!-- TOC --><a name="frequently-asked-questions"></a>
# Frequently asked questions

<!-- TOC --><a name="where-can-i-download-a-pre-built-copy-of-kg2"></a>
## Where can I download a pre-built copy of KG2?

Dump files of RTX-KG2pre and RTX-KG2c are available for download in the
[github:ncats/translator-lfs-artifacts](https://github.com/ncats/translator-lfs-artifacts/tree/main/files)
project area.

<!-- TOC --><a name="what-licenses-cover-kg2"></a>
## What licenses cover KG2?

It's complicated. The KG2 build software is provided free-of-charge via the
[MIT license](/RTXteam/RTX-KG2/blob/master/LICENSE). All documentation for KG2 and
any downloadable build artifacts hosted on GitHub or S3 are provided
free-of-charge via the (CC-BY
license)[https://creativecommons.org/licenses/by/4.0/]. If you are using KG2 in
your work, we ask that you attribute credit to the KG2 team as follows: *RTX KG2
development team, github.com/RTXteam*. Our assertion of the CC-BY license covers
only creative product our team (documentation, reports, and knowledge graph
formatting); the actual content of the KG2 knowledge graph is encumbered by
various licenses (e.g., UMLS) that prevent its redistribution.

<!-- TOC --><a name="what-criteria-do-you-use-to-select-sources-to-include-in-kg2"></a>
## What criteria do you use to select sources to include in KG2?

We emphasize knowledge souces that

1. Are available in a flat-file download (e.g., TSV, XML, JSON, DAT, or SQL dump)
2. Are being maintained and updated periodically
3. Provide content/knowledge that complements (does not duplicate) what is already in KG2.
4. Connect concept identifiers that are already in KG2.
5. Ideally, provide knowledge based on human curation (favored over computational text-mining).

<!-- TOC --><a name="troubleshooting"></a>
# Troubleshooting

<!-- TOC --><a name="error-building-dag-of-jobs"></a>
## Error building DAG of jobs
- In the case where Snakemake is forcibly quit due to a loss of power or other reason, it may result in the code directory becoming locked. To resolve, run:
```
/home/ubuntu/kg2-venv/bin/snakemake --snakefile /home/ubuntu/kg2-code/build/Snakefile --unlock
```

<!-- TOC --><a name="authentication-error-in-tsv-to-neo4jsh"></a>
## Authentication Error in `tsv-to-neo4j.sh`
Sometimes, when hosting KG2 in a Neo4j server on a new AWS instance, the initial password does not get set correctly, which will lead to an Authentication Error in `tsv-to-neo4j.sh`. To fix this, do the following:
1. Start up Neo4 (sudo service neo4j start)
2. Wait one minute, then confirm Neo4j is running (sudo service neo4j status)
3. Use a browser to connect to Neo4j via HTTP on port 7474. You should see a username/password authentication form.
4. Fill in "neo4j" and "neo4j" for username and password, respectively, and submit the form. You should be immediately prompted to set a new password. At that 	time, type in our "usual" Neo4j password (you'll have to enter it twice).
5. When you submit the form, Neo4j should be running and it should now have the correct password set.

<!-- TOC --><a name="errors-in-extraction-rules"></a>
## Errors in Extraction rules

<!-- TOC --><a name="role-exists-error"></a>
### Role exists error
Occasionally, when a database needs to be re-extracted, the error `ERROR:  role "jjyang" already exists` occurs.
If the following is not in the extraction script, add it to the line above where the role is created.
```
sudo -u postgres psql -c "DROP ROLE IF EXISTS ${role}"
```

<!-- TOC --><a name="for-developers"></a>
# For Developers

This section has some guidelines for the development team for the KG2 build system.

<!-- TOC --><a name="kg2-coding-standards"></a>
## KG2 coding standards

- Hard tabs are not permitted in source files such as python or bash (use spaces).

<!-- TOC --><a name="python-coding-standards-for-kg2"></a>
### Python coding standards for KG2

- Only python3 is allowed.
- Please follow PEP8 formatting standards, except we allow line length to go to 160.
- Please use type hints wherever possible.

<!-- TOC --><a name="shell-coding-standards-for-kg2"></a>
# Shell coding standards for KG2

- Use lower-case for variable names except for environment variables.
- The flags `nounset`, `pipefail`, *and* `errexit` should be set.

<!-- TOC --><a name="file-naming"></a>
### File naming

- For config files and shell scripts, use `kabob-case`
- For python modules, use `snake_case`.

<!-- TOC --><a name="kgx-validation"></a>
### KGX validation of the graph
Our goal and expectation is for the "normalized" RTX-KG2 graph (the one just prior
to the conflation step) to be validated as KGX, before generating the conflated file.
This means, for example, for the RTX-KG2.10.3 build, a key step is to validate the files 
`kg2-normalized-2.10.3-nodes.jsonl` and `kg2-normalized-2.10.3-edges.jsonl`. We do this
by cloning the code for the GitHub project 
[NCATSTranslator/translator-ingests](https://github.com/NCATSTranslator/translator-ingests),
and then placing the aforementioned files in the `translator-ingests/data` folder. Then `cd` 
into that folder and run `make validate-rtx-kg2.10.3`.

<!-- TOC --><a name="credits"></a>
# Credits

Thank you to the many people who have contributed to the development of RTX KG2:

<!-- TOC --><a name="code-and-development-work"></a>
## Code and development work
Stephen Ramsey, 
E. C. Wood,
Frankie Hodges,
Amy Glen, 
Lindsey Kvarfordt,
Finn Womack, 
Liliana Acevedo, 
Veronica Flores, and
Deqing Qu.

<!-- TOC --><a name="advice-and-feedback"></a>
## Advice and feedback
David Koslicki, Eric Deutsch, Yao Yao, Jared Roach, Chris Mungall, Tom Conlin, Matt Brush,
Chunlei Wu, Harold Solbrig, Will Byrd, Michael Patton, Jim Balhoff, Chunyu Ma, Chris Bizon,  
Deepak Unni, Richard Bruskiewich, and Jeff Henrikson.

<!-- TOC --><a name="funding"></a>
## Funding
National Center for Advancing Translational Sciences (award number OT2TR002520).

