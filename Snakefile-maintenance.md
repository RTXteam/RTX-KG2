# Table of Contents
Hover over the menu (circled in red) for a clickable table of contents. 
<img width="1027" alt="image" src="https://user-images.githubusercontent.com/39020520/120412943-48014a00-c30c-11eb-8052-dd8bd91245a3.png">


# Contact

If you have any questions about these instructions or
the snakemake build system, please contact
Erica Wood (Crescent Valley High School) by logging a GitHub issue and assigning @ericawood or contacting them directly through email.

# Understanding Snakemake

![Overview of Snakemake Build System](https://user-images.githubusercontent.com/36611732/119391891-ceba8500-bc83-11eb-8847-aad7f2edcb58.png)

The Snakemake build system relies on three files to work:
- `build-kg2-snakemake.sh`
- `snakemake-config-var.yaml` (which is [preprocessed](https://github.com/RTXteam/RTX-KG2/issues/48#issuecomment-773508378) into `snakemake-config.yaml` and used by the Snakefile)
- `Snakefile` (and its subcomponents, which are all named with the prefix `Snakefile-`)



## `build-kg2-snakemake.sh`

`build-kg2-snakemake.sh` runs the commands necessary for `snakemake` to run without error. It preprocesses  `snakemake-config-var.yaml` to be used by snakemake, assembles the `Snakefile-*` components into the main `Snakefile`, and runs the actual `snakemake` command.

### Snakemake Configuration Variables
These variables are passed in through the processed config file `snakemake-config.yaml` and accessed through the `config` dictionary in the `Snakefile`. Note that `snakemake-config.yaml` is generated from `snakemake-config-var.yaml` and the script `generate_snakemake_config_file.py`, so `snakemake-config.yaml` never needs to be created or edited directly. Additional config variables should be added to `snakemake-config-var.yaml`.

### Snakefile Construction
`build-kg2-snakemake.sh` passes into `Snakefile` the different sub-`Snakefile`s. `Snakefile-finish` (the last rule in the build process) must be listed first in the `Snakefile`. It must be added using `cat`, so that its contents are in `Snakefile` as they are in `Snakefile-finish`. The other `Snakefile-*`s can be incorporated into the `Snakefile` through an `include` statment. The order of these, with the exception of `Snakefile-finish`, does not matter as `snakemake` figures it out. All of the `Snakefile-*`s also have access to the `snakemake-config.yaml` variables.

```
cat ${CODE_DIR}/Snakefile-finish >> ${snakefile}

echo 'include: "Snakefile-pre-etl"' >> ${snakefile}

echo 'include: "Snakefile-conversion"' >> ${snakefile}

echo 'include: "Snakefile-post-etl"' >> ${snakefile}

if [[ "${build_flag}" == "all" || "${build_flag}" == "alltest" ]]
then
    echo 'include: "Snakefile-semmeddb-extraction"' >> ${snakefile}
fi

if [[ "${build_flag}" == "all" ]]
then
    echo 'include: "Snakefile-extraction"' >> ${snakefile}
fi

if [[ "${nodes_flag}" == "nodes" ]]
then
    echo 'include: "Snakefile-generate-nodes"' >> ${snakefile}
fi

```

### Snakemake Command Flags
There are many command-line options available for running `build-kg2-snakemake.sh`. If you have run `build-kg2-snakemake.sh` before, you likely had to manually edit `build-kg2-snakemake.sh` to get the build type you wanted (especially after failures). In order to minimize the potential for error that follows that build style, command-line options have been added in to get the effect you are looking for. These are slightly different than the ones for Snakemake itself, but are noticeably similar. The biggest difference is that there are less options.

Here are the available options: (Format: `flag` [slots it works in, starting at 1])

- `test` [1]: This flag initiates a test build, which creates a much smaller graph (which can be used for debugging).
- `all` [1]: This flag initiates a full build, which includes the extraction scripts. (Omitting this flag initiates a partial build, which requires that the output of all of the extraction scripts already exits).
- `alltest` [1]: This flag initaites a test build that includes extracting SemMedDB's test edges file. Before you can run a build with the `test` flag, you **must** run a build on that same instance with the `alltest` flag. (SemMedDB's conversion requires a test version of the input). 
- `-n` [1-4]: This flag initiates a dryrun of the build, outputting to a different file (with the `-n` flag in the file name). This is good to do before running a real build to make sure that the scripts you want to run will be included and the scripts you don't won't.
- `nodes` [1-4]: This flag generates a version of `kg2-simplified.json` that is exclusively the nodes (for debugging purposes). It takes extra time, so it should only be included when necessary. Also, if you plan to use it, familiarize yourself with the `nodes` related code in `build-kg2-snakemake.sh`.
- `-R_*` [1-3]: This is our version of Snakemake's `-R` flag. However, rather than using it in the form `-R Rule` (ex. `-R Merge`), we add an underscore between them (`-R_Rule`) to simplify the command line options decoding process. This forces a rerun of all the rules that provide an input to the rule listed. For example, if you wanted to rerun all of the conversion rules, you might use `-R_Merge`. This one is more tricky to use and I'd recommend both reading up on what Snakemake says about it and doing dryruns until you get the effect you are looking for.
- `-F` [1-3]: This flag forces a rerun of all of the rules that lead up to the first rule in the Snakefile, which is `Finish` and depends on all of the rules. Thus, this will rebuild everything.
- `graphic` [1-3]: This flag generates the PNG diagram of the Snakemake workflow
- `travisci` [3-5]: This flag should only be used in the `.travis.yml` file (for usage on a Travis CI instance). It ensures that the commands are configured to run on a Travis CI instance (where we can't use a virtualenv).

Examples:

- Bad: `bash -x build-kg2-snakemake.sh -n test` (`test` flag **must** be in position 1)
- Good: `bash -x build-kg2-snakemake.sh all -F nodes -n travisci` (every flag is in an allowable position for it)



## `Snakefile`

The `Snakefile` contains functions that enable KG2 to be built in parallel, in the form of a rule. A rule is made up of an `input`, `output`, `log` (optional), and `shell` command. Each Bash command from `build-kg2.sh` (or in a few rare instances, groups of commands) belongs to a rule.
**Snakemake determines the order of the rules and which rules can run in parallel using the `input` and `output` parameters to the rule**. If `snakemake` is run with the `-j` build flag, `snakemake` will automatically parallelize the build process using the data you've provided. First, the process(es) with no `input` run. Then, the process(es) with an `input` matching the `output` of the previous process(es) run. As many processes run at the same time as there are (1) cores for and (2) have their `input` requirements met. This results in processes that aren't dependent on each other running in parallel. **The file listed in `input` must exist for a rule to start.**
The bash command you want to run goes under the `shell` property for most commands
and the `run` property for others (when you want to run a group of commands in one rule). Below is the format of a Snakemake rule:

```
rule Rule_Name:
    input:
        input_filename_as_a_string
    output:
        output_filename_as_a_string
    log:
        log_filename_as_a_string
    shell:
        bash_command_as_a_string
```

In the past, we had all of the rules of build KG2 directly in the `Snakefile`. This was not effective, as the different build types (full, partial, test, and test including SemMedDB) each required different rules. Now, different types of rules are split into different `Snakefile`s that are all run in one central `Snakefile`.

- `Snakefile-pre-etl`: This script runs for every type of build. It includes running the verification tests and may include other processes later.
- `Snakefile-extraction`: This script only runs during full builds. This runs all of the `extract-*` scripts with the exception of `extract-semmeddb.sh` (and any others that have separate outputs depending on if the build is a test build or not)
- `Snakefile-semmeddb-extraction`: This script only runs on full or full test builds. Currently, it runs `extract-semmeddb.sh`, as this script has a separate output depending on the build type. Any future extraction scripts with this characteristic should also be put in here RATHER than in `Snakefile-extraction`
- `Snakefile-conversion`: This script runs for every type of build. It runs the scripts that convert each dataset into the KG2 JSON format.
- `Snakefile-post-etl`: This script manages almost everything (see `Snakefile-generate-nodes` for exception) after the databases have been converted into the KG2 JSON format until the data is ready to be compressed and uploaded to the S3 bucket.
- `Snakefile-generate-nodes`: If the user includes the `nodes` flag on the build, this Snakefile is included in the build process. This runs the `Simplify-Nodes` rule, generating a file of just KG2's nodes.
- `Snakefile-finish`: This script contains the rule that manages the rest of the build process. This includes compressing the output files and uploading them to the S3 bucket.

## Bash Shell Script to Snakemake Shell:

For the `shell` section of a Snakemake rule, you should use Bash commands. However, there are some `snakemake` conventions that differ from Bash shell scripts. Below is how to convert them:



`build-kg2.sh` | `Snakefile` | Explanation
-- | -- | --
`${var_name}` | `config[‘VAR_NAME’]` | Variables are passed into the `Snakefile` through the config file (which for KG2 is created through `build-kg2-snakemake.sh`. In the `Snakefile`, the convention is to use uppercase variables (see [#593](https://github.com/RTXteam/RTX/issues/593#issuecomment-668746540) for more information). In addition to this, you can’t access any variable within the `Snakefile` using `${}`. You also can’t access variables in the Snakefile within the quotations (the Bash command must be a string) and must instead concatenate your command strings with your call to the `config` dictionary.
`${build_flag}` | `config['TEST_FLAG']` | The build_flag (which contains “test” or “”) is passed into the `Snakefile` as ‘TEST_FLAG’ and accessed in the `Snakefile` through `config['TEST_FLAG']`.
`${test_arg}` | `config['TEST_ARG']` | The test_arg (which contains “--test” or “”) is passed into the `Snakefile` as ‘TEST_ARG’ and accessed in the `Snakefile` through `config['TEST_ARG']`
`${test_suffix}` | `config['TEST_SUFFIX']` | The test_suffix (which contains “-test” or “”) is passed into the `Snakefile` as ‘TEST_SUFFIX’ and accessed in the `Snakefile` through `config['TEST_SUFFIX']`
`${input_file}` | `{input}` | As long as the input file is listed under `input`, you can access the input file **within** the `shell` command (inside the quotations) using `{input}`.
`${output_file}` | `{output}` | As long as the output file is listed under `output`, you can access the output file **within** the `shell` command (inside the quotations) using `{output}`.
`${log_file}` | `{log}` | As long as the log file is listed under `log`, you can access the log file **within** the `shell` command (inside the quotations) using `{log}`.


# Adding to Snakemake Build System

## Adding an ETL Script

### Editing `snakemake-config-var.yaml`:

#### General Steps

(1) Insert any variables managing the input and output files for that ETL script into `snakemake-config-var.yaml` and place in the appropriate location (find the last ETL filename set and put them on the next line after an empty line). For an ETL script, the variable name should be something like `{source}_{input/output}_file` for the file and `{source}_{dir}` for the source directory (if applicable). If there are any other variables needed to run that ETL script, add them in the same location (e.g. source directory, mysql database).

Example:
```
go_annotation_input_file: ${BUILD_DIR}/goa_human.gpa
go_annotation_output_file: ${BUILD_DIR}/kg2-go-annotation${test_suffix}.json
```

These variable names will be capitalized when `build-kg2-snakemake.sh` runs `generate_snakemake_config_file.py`. So, when using these variables in a `Snakefile`, make sure to fully capitalize them.


### Editing the `Snakefile`s:

#### General Steps

(1) First, you need to add a rule to `Snakefile-extraction` (or `Snakefile-semmeddb-extraction` if there is a different output for a test build) for the extraction script (most are structured in the form 'extract-{database name}.sh').

**`input`**: the file that is created upon the successful completion of the validation tests (a placeholder located at `${BUILD_DIR}/validation-placeholder.empty` in Bash and `config['BUILD_DIR'] + "/validation-placeholder.empty"` in `snakemake`)

**`output`**: the data file that was downloaded. If there is more than one data file that was downloaded and they were put into a directory OR the data is in a mysql database, use a placeholder file instead.

**`log`**: Since script you will be running is most likely a bash script, use a log file to capture the output of `bash -x`, since it would otherwise fill the Snakemake log file in an unorganized manner that makes it difficult to read and debug issues.

**`shell`**: looks the same as it would in `build-kg2.sh`, but remember to follow the conversions listed under [Understanding Snakemake->Bash Shell Script to Snakemake Shell](#bash-shell-script-to-snakemake-shell).

Example: (no placeholder)
```
rule UniprotKB:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['UNIPROTKB_DAT_FILE']
    log:
        config['BUILD_DIR'] + "/extract-uniprotkb.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-uniprotkb.sh {output} > {log} 2>&1"
```

Example: (placeholder) -- the key difference is that you must run `touch` to create the output file
```
rule ChemBL:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        placeholder = config['BUILD_DIR'] + "/chembl-placeholder.empty"
    log:
        config['BUILD_DIR'] + "/extract-chembl.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-chembl.sh " + config['CHEMBL_MYSQL_DBNAME'] +" > {log} 2>&1 && touch {output.placeholder}"
```

(2) Then, you will need to add a rule to `Snakefile-conversion` for the conversion (which converts the data into KG2's format).

**`input`**: the output of the previous rule, whether that is a placeholder or a datafile.

**`output`**: the KG2 JSON file for that database.

**`log`**: a log file is only necessary if the script will produce a lot of print outs

**`shell`**: looks the same as it would in `build-kg2.sh`, but remember to convert to follow the conversions listed under [Understanding Snakemake->Bash Shell Script to Snakemake Shell](#bash-shell-script-to-snakemake-shell).

Example: (no placeholder - data file instead - for input)
```
rule Uniprot_Conversion:
    input:
        config['UNIPROTKB_DAT_FILE']
    output:
        config['UNIPROTKB_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/uniprotkb_dat_to_json.py " + config['TEST_ARG'] + " {input} {output}"
```

Example: (placeholder for input)
```
rule ChemBL_Conversion:
    input:
        placeholder = config['BUILD_DIR'] + "/chembl-placeholder.empty"
    output:
        config['CHEMBL_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/chembl_mysql_to_kg_json.py " + config['TEST_ARG'] + " " + config['MYSQL_CONF'] + " " + config['CHEMBL_MYSQL_DBNAME'] + " {output}"
```

(3) Finally, you need to merge the new KG2 JSON file into the full KG2 JSON file. This requires editing the `Merge` rule (which is in `Snakefile-post-etl`, which is the convergence point of all of the ETL rules. After this, you won't have to add any new rules as the files are already merged and everything is handled through the one, merged file.

**`input`**: You will likely notice that there are already input files present. Your job is to add a new input file to the list of input files. 

 - First, add a comma to the end of the last line in input (in the example below, `go_annotations = config['GO_ANNOTATION_OUTPUT_FILE']` would become `go_annotations = config['GO_ANNOTATION_OUTPUT_FILE'],`).

 - Then, add a new entry to the list in the form `database_name = config['DATABASE_OUTPUT_FILE']`

 - Finally, add the entry to the list of input files at the end of the `shell` command.

Example diff of the Merge Rule:
```diff
rule Merge:
    input:
         owl = config['OUTPUT_FILE_FULL'],
         uniprot = config['UNIPROTKB_OUTPUT_FILE'],
         semmeddb = config['SEMMED_OUTPUT_FILE'],
         chembl = config['CHEMBL_OUTPUT_FILE'],
         ensembl = config['ENSEMBL_OUTPUT_FILE'],
         unichem = config['UNICHEM_OUTPUT_FILE'],
         ncbigene = config['NCBI_GENE_OUTPUT_FILE'],
         dgidb = config['DGIDB_OUTPUT_FILE'],
         repoddb = config['REPODB_OUTPUT_FILE'],
         drugbank = config['DRUGBANK_OUTPUT_FILE'],
         smpdb = config['SMPDB_OUTPUT_FILE'],
         hmdb = config['HMDB_OUTPUT_FILE'],
-        go_annotations = config['GO_ANNOTATION_OUTPUT_FILE']
+        go_annotations = config['GO_ANNOTATION_OUTPUT_FILE'],
+        database_name = config['DATABASE_OUTPUT_FILE']
     output:
         full = config['FINAL_OUTPUT_FILE_FULL'],
         orph = config['OUTPUT_FILE_ORPHAN_EDGES']
     shell:
-        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/merge_graphs.py " + config['TEST_ARG'] + " --kgFileOrphanEdges {output.orph} --outputFile {output.full} {input.owl} {input.uniprot} {input.semmeddb} {input.chembl} {input.ensembl} {input.unichem} {input.ncbigene} {input.dgidb} {input.kg_one} {input.repoddb} {input.drugbank} {input.smpdb} {input.hmdb} {input.go_annotations}"
+        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/merge_graphs.py " + config['TEST_ARG'] + " --kgFileOrphanEdges {output.orph} --outputFile {output.full} {input.owl} {input.uniprot} {input.semmeddb} {input.chembl} {input.ensembl} {input.unichem} {input.ncbigene} {input.dgidb} {input.kg_one} {input.repoddb} {input.drugbank} {input.smpdb} {input.hmdb} {input.go_annotations} {input.database_name}"
```


#### Special Circumstances

If you need to run multiple commands in one rule, rather than using `shell`, use `run`. When using `run`, you must specify that you are using the shell. To do this, place your bash commands into the function `shell()`.

Example (note, this particular command no longer used in the snakemake build process):
```
rule KG_One:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['KG1_OUTPUT_FILE']
    run:
        shell(config['S3_CP_CMD'] + " s3://rtx-kg2/" + config['RTX_CONFIG_FILE'] + " " + config['BUILD_DIR'] + "/" + config['RTX_CONFIG_FILE'])
        shell(config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/rtx_kg1_neo4j_to_kg_json.py " + config['TEST_ARG'] + " --configFile " + config['BUILD_DIR'] + "/" + config['RTX_CONFIG_FILE'] + " " + config['CURIES_TO_URLS_FILE'] + " {output}")
```

___


## Adding Scripts that Go **BEFORE** ETL Scripts

### Editing `Snakefile-pre-etl`:

#### General Steps

(1) Determine if your code can run in parallel with [run-validation-tests.sh](https://github.com/RTXteam/RTX-KG2/blob/master/run-validation-tests.sh). If it can go to 2a. If it must run after `run-validation-tests.sh`, go to 2b. If it must run before `run-validation-tests.sh`, go to 2c. 

(2a) In parallel with `run-validation-tests.sh`: you don't need an `input`, so configure the rule to have an `output`, whether a data file or a placeholder (which you will need to `touch` in your `shell` command). Use that `output` as another input for the ETL Extraction Script rules (discussed in [Adding to Snakemake Build System->Adding an ETL Script->Editing `Snakefile`->General Steps->Step 1](#general-steps)). Make sure to put a comma after the first input line. Finally, add your Bash command to the `shell` field (and a `log` file as necessary).

(2b) After `run-validation-tests.sh`: use `validation-placeholder.empty` in the `input` field of your new rule. Then, configure your new rule to have an `output` file, whether a data file or placeholder (which you will need to `touch` in your `shell` command). Then, change all of the ETL Extraction Script rules (discussed in [Adding to Snakemake Build System->Adding an ETL Script->Editing `Snakefile`->General Steps->Step 1](#general-steps)) to use this new `output` as their `input`. Finally, add your Bash command to the `shell` field (and a `log` file as necessary).

(2c) Before `run-validation-tests.sh`: you don't need an `input`, so configure the rule to have an `output`, whether a data file or a placeholder (which you will need to `touch` in your `shell` command). Use that `output` as the `input` for `rule ValidationTests`. Finally, add your Bash command to the `shell` field (and a `log` file as necessary).

___
## Adding Scripts that Go **AFTER** Merge

### Editing `Snakefile-post-etl`:

#### General Steps

(1) For the scripts after merge, we cannot run the build in parallel, despite the `input`/`output` allowing for it. On an r5a.8xlarge AWS instance, loading the merged KG2 JSON file into memory in Python uses approximately 70% of the memory. Thus, it cannot be loaded into two different scripts at once without running out of memory. Therefore, the first step in editing `Snakefile-post-etl` is to determine where in the build process the script should go. It will likely look similar to the order in `build-kg2.sh`.

![End of Snakemake Build System](https://user-images.githubusercontent.com/36611732/90065571-5b6df680-dca1-11ea-95fc-25ed1c5f6c4d.png)

Once you have determined where in the pipeline you would like your new rule to go, you will need to change the `input` of nearby rules. In this example, we will use the example of a rule between `Stats` and `Simplify`.

(2) Identify the `output` of the preceding rule.

Preceding Rule:
```
rule Stats:
    input:
        config['FINAL_OUTPUT_FILE_FULL']
    output:
        config['REPORT_FILE_FULL']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/report_stats_on_json_kg.py {input} {output}"
```
In this example, the `output` of the preceding rule is `config['REPORT_FILE_FULL']`. This becomes the `input` for the new rule, but as the placeholder `input` rather than the actual `input` (unless it is the actual input, which means you don't need a placeholder `input`). The role of the placeholder `input` is to ensure that the build doesn't run in parallel and runs in the order that you want. The real `input` will likely be either the output file from `Merge` (`config['FINAL_OUTPUT_FILE_FULL']`) or `Simplify` (`config['SIMPLIFIED_OUTPUT_FILE_FULL']`).

(3) Write your new rule in the space after the preceding rule using information from the Understanding Snakemake section. Notice how the real `input` is the output of `Merge`. This is why, in the diagram above, there is an arrow from `Merge` to multiple later rules. It is the real `input` for multiple rules. 
```
rule New_Rule:
    input:
        real = config['FINAL_OUTPUT_FILE_FULL'],
        placeholder = config['REPORT_FILE_FULL']
    output:
        config['NEW_RULE_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/new_rule_kg_json.py " + config['TEST_ARG'] + "{input.real} {output}"
```

(4) Edit the placeholder `input` of the rule following the new rule to match the `output` of the new rule.

Diff of the Following Rule:
```diff
 rule Simplify:
     input:
         real = config['FINAL_OUTPUT_FILE_FULL'],
-        placeholder = config['REPORT_FILE_FULL']
+        placeholder = config['NEW_RULE_OUTPUT_FILE']
     output:
         config['SIMPLIFIED_OUTPUT_FILE_FULL']
     log:
         config['BUILD_DIR'] + "/filter_kg_and_remap_predicates.log"
     run:
         shell("bash -x " + config['CODE_DIR'] + "/version.sh " + config['VERSION_FILE'] + " " + code['TEST_FLAG'] + " > {log} 2>&1")
         shell(config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/filter_kg_and_remap_predicates.py " + config['TEST_ARG'] + " --dropNegated --dropSelfEdgesExcept interacts_with,positively_regulates,inhibits,increase " + config['PREDICATE_MAPPING_FILE'] + " " + config['CURIES_TO_URLS_FILE'] + " {input.real} {output} " + config['VERSION_FILE'] + " >> {log} 2>&1")
```

### Editing `Snakefile-generate-nodes`

#### General Steps

You aren't really going to update `Snakefile-generate-nodes`, unless some unpredicted reason shows up. In general, treat the rule(s) in `Snakefile-generate-nodes` like they are part of [`Snakefile-post-etl`](#Editing-Snakefile-post-etl). You may have to edit the `sed`-ing that happens in `build-kg2-snakemake.sh`, which allows `Snakefile-generate-nodes` to be taken out if it is not desired. To do that, I would recommend creating a temporary text file with the lines you want to change (and some that you don't) and running sed commands on it until you figure out how to do what you're looking for.


### Editing `Snakefile-finish`:

#### General Steps

This is only necessary if you need to compress and upload anything new to the S3 bucket.

(1) To curb the accumulation of `shell` commands in the `Finish` rule, we put them in a separate shell script. This shell script is called `finish-snakemake.sh`. Using bash,
add your new command to `finish-snakemake.sh`.

(2) If it requires any variables that are not already being passed in (`master-config.shinc` is not sourced), add them to the list of parameters, both in documentation (the top) and
receiving (approximately the middle).

(3) If you added a parameter in step 2, add its value to the `Finish` rule in the appropriate spot.

(4) MAKE SURE THERE ARE A FEW SPARE LINES AT THE END OF `Snakefile-finish`. Since it is `cat`ted into the `Snakefile`, with includes `echo`ed in afterwards, those includes CANNOT be on the same line as the rule or they will not run and the build will fail.

