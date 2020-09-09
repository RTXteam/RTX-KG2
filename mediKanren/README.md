# Importing KG2 into MediKanren

NOTE: This was tested on Ubuntu 18.04 system and requires a user with passwordless sudo setup

## Generate mediKanren file

### Setup the enviroment

To download and install everything you need to run kg2 into mediKanren simply run the `setup.sh` script on a unpriveliged user with passwordless sudo enabled like so:
```
bash -x ./setup.sh > setup.log 2>&1
```

Alternatively, if you are just trying to run mediKanren and not download and process a new graph you just need to install racket (and git if you do not have it) then run `git clone https://github.com/webyrd/mediKanren.git` to clone the mediKanren repository.

### Downloading a new graph version and generate index files

If you wish to download a new graph version and generate the indexes yourself from that then do the following:
1) Edit `config.yml` so that it has the correct url, username, and password for the kg2 instance you want to download.
  e.g.
  ```
  neo4j:
    outputname: rtx_kg2
    username: neo4j
    password: your_pass
    host: http://your.url.here:7474
  ```
2) run `bash -x ./setup.sh > setup.log 2>&1`
3) run `bash -x ./download-graph.sh > download-graph.log 2>&1`
4) run `bash -x ./create-index.sh > create-index.log 2>&1` (This could take a few days and require between 64 and 128 GB of ram)
5) Follow the the avove steps starting from Run MediKanren onward

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

## Run mediKanren localy from pregenerated indexes

### Setup the enviroment

To download and install everything you need to run kg2 into mediKanren simply run the `setup.sh` script on a unpriveliged user with passwordless sudo enabled like so:
```
bash -x ./setup.sh > setup.log 2>&1
```

Alternatively, if you are just trying to run mediKanren and not download and process a new graph you just need to install racket (and git if you do not have it) then run `git clone https://github.com/webyrd/mediKanren.git` to clone the mediKanren repository.

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


