---
name: Build KG2
about: Checklist for KG2 build process
title: Build KG2.X.Y
labels: ''
assignees: ''

---

##### 1. Build and load KG2:
- [ ] (if necessary) Clear the instance using `bash -x instance_management/clear-instance.sh`
- [ ] (preferred option) Launch a new AWS EC2 `r5a.4xlarge` instance called `kg2XYbuild.rtx.ai`
- [ ] Clone the RTX repo from Github `git clone https://github.com/RTXteam/RTX-KG2.git`
- [ ] Checkout the branch that will be used for the build
- [ ] Setup the KG2 build system `bash -x ~/RTX-KG2/setup/setup-kg2-build.sh`
- [ ] Check `~/kg2-build/setup-kg2-build.log` to ensure setup completed successfully 
- [ ] Run `touch ~/kg2-build/minor-release` for a minor release or `touch ~/kg2-build/major-release` for a major release. If you don't want to change the version number, ignore this step.
- [ ] Run a dry build using `bash -x ~/kg2-code/build/build-kg2-snakemake.sh all -F -n`
- [ ] Check `~/kg2-build/build-kg2-snakemake-KG2.X.Y-n.log` to ensure all rules are included
- [ ] Initiate a screen session `screen -S buildkg2`
- [ ] Start the build `bash -x ~/kg2-code/build/build-kg2-snakemake.sh all -F`
- [ ] Verify build completed by checking `~/kg2-build/build-kg2-snakemake-KG2.X.Y.log`
- [ ] Check the build version number in `~/kg2-build/kg2-version.txt`
- [ ] Check report file `kg2-simplified-report-KG2.X.Y.json`; compare against previous `kg2-simplified-report.json` to identify any major changes
- [ ] Find an available kg2endpoint by checking `rtx.ai` under `Networking` on Lightsail
- [ ] Update code on kg2endpoint, then run setup-kg2-neo4j.sh if necessary
- [ ] Load KG2 into Neo4J `bash -x ~/RTX-KG2/neo4j/tsv-to-neo4j.sh > ~/kg2-build/tsv-to-neo4j.log 2>&1`
- [ ] Update `kg2-versions.md`
- [ ] create a new DNS CNAME record with CNAME `kg2endpoint-kg2-X-Y.rtx.ai` pointing to the hostname for the Neo4j endpoint (which might be something like `kg2endpoint3.rtx.ai`).
- [ ] Update version numbers of upstream knowledge sources, for the new version of KG2 in `kg2-versions.md` (see Cypher command below).
- [ ] (if necessary) Merge working branch into `master`
- [ ] Create a new release for the build on GitHub, including the content from `kg2-versions.md` in the description.

Example Cypher to get versions of many of the knowledge sources in a specific build of KG2pre:
```
match (n:`biolink:RetrievalSource`) where not n.id =~ 'umls_.*' and not n.id =~ 'OBO:.*' return n.id, n.name order by n.id;
```

