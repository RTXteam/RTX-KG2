---
name: Build KG2
about: Checklist for KG2 build process
title: Build KG2.X.Y
labels: ''
assignees: ''

---

##### 1. Build and load KG2:
- [ ] Clear the instance using `bash -x clear-instance.sh`
- [ ] Clone the RTX repo from Github `git clone https://github.com/RTXteam/RTX-KG2.git`
- [ ] Setup the KG2 build system `bash -x RTX-KG2/setup-kg2-build.sh`
- [ ] Check `~/kg2-build/setup-kg2-build.log` to ensure setup completed successfully 
- [ ] Run a dry build using `bash -x ~/kg2-code/build-kg2-snakemake.sh all -F -n`
- [ ] Check `~/kg2-build/build-kg2-snakemake-n.log` to ensure all rules are included
- [ ] Initiate a screen session `screen -S buildkg2`
- [ ] Start the build `bash -x ~/kg2-code/build-kg2-snakemake.sh all -F`
- [ ] Verify build completed by checking `~/kg2-build/build-kg2-snakemake.log`
- [ ] Check the build version number in `~/kg2-build/kg2-version.txt`
- [ ] Check report file `kg2-simplified-report.json`; compare against previous `kg2-simplified-report.json` to identify any major changes
- [ ] Generate nodes.tsv and edges.tsv by running `python3 kg2_json_to_kgx_tsv.py kg2-simplified.json`
- [ ] Generate `content-metadata.json` on build instance
- [ ] Push nodes.tsv and edges.tsv to public S3 bucket with `aws s3 /file/name s3://rtx-kg2-public`
- [ ] Find an available kg2endpoint by checking `rtx.ai` under `Networking` on Lightsail
- [ ] install the new KG2 TSV files into Neo4j on the kg2endpoint
- [ ] Update code on kg2endpoint, then run setup-kg2-neo4j.sh if necessary
- [ ] Load KG2 into Neo4J `RTX-KG2/tsv-to-neo4j.sh > ~/kg2-build/tsv-to-neo4j.log 2>&1`
- [ ] Update kg2-versions.md

Example Cypher to get versions of many of the knowledge sources in a specific build of KG2pre:
```
match (n:`biolink:InformationResource`) return n.id, n.name order by n.id;
```
