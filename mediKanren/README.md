# Importing KG2 into MediKanren

NOTE: This was tested on Ubuntu 18.04 system and requires a user with passwordless sudo setup

## 1) Generate mediKanren files and indexes from KG2 tsv files

### Setup the enviroment

First, install git and clone the RTX repository if you have not already:
```
git clone https://github.com/RTXteam/RTX.git
```

Then, navigate to the repository subdirectory `RTX/code/kg2/mediKanren`. To download and install everything you need to run kg2 into mediKanren simply run the `setup.sh` script on a unpriveliged user with passwordless sudo enabled like so:
```
bash -x ./setup.sh > setup.log 2>&1
```
On successful completion, the log file should end with "======== Script Finished ========".
 
### Generate new graph tsvs from kg2 tsv file

**NOTE:** This is the prefered method as it is much faster to generate the tsvs locally than going through neo4j. The alternative method that uses kgx is also listed below. This script takes about an hour to run.


**Currently, only the tsv conversion script `kg2_tsv_to_medikanren_tsv.py` is supported.**

From the `RTX/code/kg2/mediKanren` subdirectory run the following: (entering in the path to the kg2 tsv file)
```
mkdir -p mediKanren/biolink/data/rtx_kg2
python3.7 kg2_tsv_to_medikanren_tsv.py /path/to/kg2/tsv/files mediKanren/biolink/data/rtx_kg2
```

### Download graph csvs from neo4j using KGX

**NOTE:** Skip this section if you generated the tsvs or csvs from the kg2 tsv using the instuctions above

 **This method takes alot of memory! For KG2 versions 3.5 and above, this script won't complete on typical r5a.8xlarge EC2 instance used for kg2 builds.** 

<details>
 <summary> Click to view instructions </summary>

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

</details>

### Generate index files

From the `RTX/code/kg2/mediKanren` subdirectory run the following:

run `bash -x ./create-index.sh > create-index.log 2>&1` (This could take a few days and require between 64 and 128 GB of ram)

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

### Upload the indexes and TSV files

Navigate to the `RTX/code/kg2/mediKanren/mediKanren/biolink/data/rtx_kg2` subdirectory.

Compress the TSV files into one tar.gz file:
```
tar -zcvf kg2-medikanren-tsvs.tar.gz *.tsv
```
And compress the index files into another:

```
tar --exclude='*.tsv' -zcvf kg2-medikanren-indexes.tar.gz .
```

Rename the old TSV and mediKanren-index tarballs in the S3 bucket, to preserve them (add the ISO date).

Upload both tarballs to the public s3 bucket
```
aws s3 cp kg2-medikanren-tsvs.tar.gz s3://rtx-kg2-public/
aws s3 cp kg2-medikanren-indexes.tar.gz s3://rtx-kg2-public/

```

The tarballs should look something like this, in terms of S3 URLs:

- `s3://rtx-kg2-public/kg2-medikanren-tsvs.tar.gz`
- `s3://rtx-kg2-public/kg2-medikanren-indexes.tar.gz`

But make sure to provide downloadable HTTP links to the mediKanren team, like this:

- `http://rtx-kg2-public.s3-website-us-west-2.amazonaws.com/kg2-medikanren-tsvs.tar.gz`
- `http://rtx-kg2-public.s3-website-us-west-2.amazonaws.com/kg2-medikanren-indexes.tar.gz`

---

## 2) Run mediKanren locally from pregenerated indexes

### Setup the enviroment

First, install git and racket. Then, clone the RTX repository if you have not already:
```
git clone https://github.com/RTXteam/RTX.git
```

Next, navigate to the repository subdirectory `RTX/code/kg2/mediKanren` and run `git clone https://github.com/webyrd/mediKanren.git` to clone the mediKanren repository.

### Download the index files.

First make sure that you have created the following directory in the mediKanren repository by running the following from the `RTX/code/kg2/mediKanren` subdirectory:
```
mkdir -p mediKanren/biolink/data/rtx_kg2
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

---

## Additional Information 

### Output File Format

The conversion scripts should create four files with the following logical format:
  * rtx_kg2.edges.tsv
    ```
    :ID,:START,:END
    0,biolink:MacromolecularComplex,biolink:MacromolecularMachine
    ```
  * rtx_kg2.edgeprop.tsv
    ```
    :ID,propname,value
    0,original_edge_label,subclass_of
    0,negated,False
    ```
  * rtx_kg2.node.tsv
    ```
    :ID
    biolink_download_source:biolink-model.owl
    biolink:PhenotypicSex
    biolink:sequence_variant_qualifier
    ```
    * rtx_kg2.nodeprop.tsv
    ```
    :ID,propname,value
    biolink_download_source:biolink-model.owl,category,biolink:DataFile
    biolink_download_source:biolink-model.owl,deprecated,False
    ```
 If the third field of the `*prop` files resembles json, it is interpreted as json by the racket code.
 As such, using the `json.dumps()` function is a necessary way of converting property values with problematic characters ("\t" for tsvs, "," for CSV files, and double quotes for either) to strings with those characters escaped.

### Debugging
Sometimes, `create-index.sh` will appear to fail silently. This is because the racket error messages do not neccessarily end up at the bottom of the log file. Search through the file manually, or for the string "context" to find a more relevant error message.

### Updating Dependent Repositories
The code in this directory relies on two forks of external repositories, `kgx` and `mediKanren`. If you wish to sync these forks with the original upstream repositories, do the following from the directory you want to update:

```
git fetch upstream
git checkout master
git merge upstream/master
```
