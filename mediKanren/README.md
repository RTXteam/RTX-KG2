# Importing KG2 into MediKanren

NOTE: This was tested on Ubuntu 18.04 system and requires a user with passwordless sudo setup

## 1) Generate mediKanren file

### Setup the enviroment

First, install git and clone the RTX repository if you have not already:
```
git clone https://github.com/RTXteam/RTX.git
```

Then, navigate to the repository subdirectory `RTX/code/kg2/mediKanren`. To download and install everything you need to run kg2 into mediKanren simply run the `setup.sh` script on a unpriveliged user with passwordless sudo enabled like so:
```
bash -x ./setup.sh > setup.log 2>&1
```

### Generating new graph csvs from kg2 tsv file

**Note:** This is the prefered method as it is much faster to generate the csvs locally than going through neo4j. The alternative method that uses kgx is also listed below.

From the `RTX/code/kg2/mediKanren` subdirectory run the following: (entering in the path to the kg2 tsv file)
```
mkdir -p mediKanren/biolink/data/rtx_kg2
python3.7 kg2_tsv_to_medikanren_csv.py /path/to/kg2/tsv/files mediKanren/biolink/data/rtx_kg2
```

### Downloading graph csvs from neo4j using KGX

**NOTE:** Skip this section if you generated the csvs from the kg2 tsv using the instuctions above

1) Edit `config.yml` so that it has the correct url, username, and password for the kg2 instance you want to download.
  e.g.
  ```
  neo4j:
    outputname: rtx_kg2
    username: neo4j
    password: your_pass
    host: http://your.url.here:7474
  ```
2) run `bash -x ./download-graph.sh > download-graph.log 2>&1`

### Generate index files

From the `RTX/code/kg2/mediKanren` subdirectory run the following:

run `bash -x ./create-index.sh > create-index.log 2>&1` (This could take a few days and require between 64 and 128 GB of ram)

### Run mediKanren to test indexes

Navigate back to `/mediKanren/biolink` and make a copy of the `config.defaults.scm` named `config.scm` so that we don't edit `config.defaults.scm` as per the warning message at the top of the file.

In `config.scm` at the top there will be a few lines (starting at line 3) adding the databases:
```
((databases . (
               semmed
               orange
               robokop
               rtx
               ))
```
Add "rtx_kg2" under "rtx" so that this now becomes:
```
((databases . (
               semmed
               orange
               robokop
               rtx
               rtx_kg2
               ))
```

While still in `mediKanren/biolink` run the command `racket gui-simple-v2.rkt` (this may take a little time to load the graph into ram)
The gui should pop up after it loads everything.


### Testing the Indexes

Run `racket` and run the following commands:
```
(require "mk-db.rkt")
(define rtx2 (make-db "data/rtx_kg2"))
(run* (c) (db:categoryo rtx2 c))
(run* (p) (db:predicateo rtx2 p))
(run 10 (c) (db:concepto rtx2 c))
(run 10 (e) (db:edgeo rtx2 e))
```

The the above should return:
1) All of the node labels
2) All of the predicates
3) A sample of 10 nodes
4) A sample of 10 edges

Verify that the above information returned looks correct.

## 2) Run mediKanren localy from pregenerated indexes

### Setup the enviroment

If you are just trying to run mediKanren and not download and process a new graph you just need to install racket and git then run `git clone https://github.com/webyrd/mediKanren.git` to clone the mediKanren repository.

### Download the index files.

First make sure that you have created the following directory in the mediKanren repository:
```
<path to repository>/mediKanren/biolink/data/rtx_kg2/
```

Next, download the indexes from [here](https://s3-us-west-2.amazonaws.com/rtx-kg2-public/kg2_indexes.tar.gz) and extract the files into the above mentioned `mediKanren/biolink/data/rtx_kg2` directory.

### Run mediKanren

Navigate back to `/mediKanren/biolink` and make a copy of the `config.defaults.scm` named `config.scm` so that we don't edit `config.defaults.scm` as per the warning message at the top of the file.

In `config.scm` at the top there will be a few lines (starting at line 3) adding the databases:
```
((databases . (
               semmed
               orange
               robokop
               rtx
               ))
```
Add "rtx_kg2" under "rtx" so that this now becomes:
```
((databases . (
               semmed
               orange
               robokop
               rtx
               rtx_kg2
               ))
```

While still in `mediKanren/biolink` run the command `racket gui-simple-v2.rkt` (this may take a little time to load the graph into ram)
The gui should pop up after it loads everything.


### Testing the Indexes

Run `racket` and run the following commands:
```
(require "mk-db.rkt")
(define rtx2 (make-db "data/rtx_kg2"))
(run* (c) (db:categoryo rtx2 c))
(run* (p) (db:predicateo rtx2 p))
(run 10 (c) (db:concepto rtx2 c))
(run 10 (e) (db:edgeo rtx2 e))
```

The the above should return:
1) All of the node labels
2) All of the predicates
3) A sample of 10 nodes
4) A sample of 10 edges

Verify that the above information returned looks correct.


