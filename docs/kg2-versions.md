# KG2 v2.10.3 Release Notes
### Date:  2026.02.24
KG2 v2.10.3 introduces major improvements to canonicalization, build determinism, packaging, and pipeline integration. This release consolidates previously separated build stages into a unified, reproducible Snakemake workflow.

---

## Architectural Change: Unified Build Pipeline

Historically, the build process (≤ 2.10.2) was split into two distinct phases: production of the `KG2pre` files, and then a separate, manual production of `KG2c` files.

Starting in 2.10.3:

- Canonicalization and conflation are integrated into the main build pipeline.
- The build now produces:
  - KG2pre files (nodes, edges) 
  - KG2 normalized files (nodes, edges) 
  - KG2 conflated files (nodes, edges) 

Canonicalization and conflation are now performed using three scripts located in `RTXteam/RTX-KG2/process`. The scripts `kg2pre_to_kg2c_nodes.py` and `kg2pre_to_kg2c_edges.py` each take a local copy of the Babel SQLite database along with the corresponding KG2pre nodes or edges file and produce canonicalized versions of those files. The `conflate_kg2c.py` script then operates on the canonicalized nodes and edges to generate the final conflated KG2c nodes and edges files.

The new pipeline:

`ETL → Merge graphs → Simplify graph → Normalize graph → Conflate graph → Deploy to PloverDB`

---

## Canonicalization Changes

Canonicalization is now fully driven by a local **Babel SQLite database**.

- Babel version: `babel-sqlite-20250901-p1`
- The old (bespoke) KG2c canonicalization algorithm is deprecated. 
- Babel is now the single source of truth for identifier equivalence.

Conflation is deterministic given:
- Babel database version
- Normalized graph inputs
- Biolink version
- Git tag

---

## Graph Statistics

### Normalized Graph (KG2pre)
- Nodes: 5,964,484 (~2.7 GB gzipped)
- Edges: 36,756,612 (~35 GB gzipped)

### Canonicalized Graph (KG2c)
- Conflated Nodes: 5,841,477 (~2.1 GB gzipped)
- Conflated Edges: 36,277,511 (~35 GB gzipped)

---

## Schema & Core Dependencies

- Biolink Model version: 4.2.5
- Babel version: `babel-sqlite-20250901-p1`
- Python requirement: Python ≥ 3.12
- Build host: `kg2103build.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`

---

## Major Knowledge Source Versions

- SemMedDB: 43 (2023)
- UMLS: 2023AA
- ChEMBL: 35
- DrugBank: 5.1.10
- Ensembl: 106
- Reactome: 93
- UniProtKB: 2025_03
- DrugCentral: 11012023
- KEGG: 115.0

---

## Deprecated Sources (Removed in v2.10.3)

- DisGeNET
- Guide to Pharmacology
- Therapeutic Target Database
- PathWhiz
- Experimental Factor Ontology

---

## Packaging Updates

The following components are now distributed via PyPI and used during build:

- `biolink_helper`
- `stitch_proj.local_babel`

Local repository copies are no longer used.

---

## Checksums (MD5)

### Canonicalized (KG2c)
- kg2-conflated-2.10.3-edges.jsonl.gz  
  `40dfdf4fe14af24db19735d7ce434572`
- kg2-conflated-2.10.3-nodes.jsonl.gz  
  `05172c6c359c4bc412b76db3c2a35d1b`

### Normalized (KG2pre)
- kg2-normalized-2.10.3-edges.jsonl.gz  
  `33164b17ea3d5bd23f1f3001623dc527`
- kg2-normalized-2.10.3-nodes.jsonl.gz  
  `cd5d1a1e691ae98fc3d2da87402e133d`

---

## Breaking / Behavioral Changes

- Canonicalization now fully Babel-driven.
- The old (bespoke) KG2c canonicalization algorithm is deprecated. 
- Build pipeline unified under Snakemake.
- Python ≥ 3.12 required.
- Deprecated sources removed.

---

## Deployment

Artifacts from this release are deployed to PloverDB in the CI environment.

# 2.10.2
**Date:  2025.04.02**

Counts:
- Nodes: 8,675,681
- Edges: 57,803,754

Issues:
 - Issue [#412](https://github.com/RTXteam/RTX-KG2/issues/412)
 - Issue [#414](https://github.com/RTXteam/RTX-KG2/issues/414)
 - Issue [#416](https://github.com/RTXteam/RTX-KG2/issues/416)
 - Issue [#420](https://github.com/RTXteam/RTX-KG2/issues/420)
 - Issue [#430](https://github.com/RTXteam/RTX-KG2/issues/430)

Build info:
- Biolink Model version: 4.2.5
- InfoRes Catalog version: 1.0.0
- Build host: `kg2102build.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `kg2.10.2`
- Neo4j endpoint CNAME: `kg2endpoint-kg2-10-2.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint3.rtx.ai`
- Tracking project for the build: [RTXteam/projects/4](https://github.com/orgs/RTXteam/projects/4)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2023AA`
  - ChEMBL: `33`
  - DrugBank: `5.1.10`
  - Ensembl: `106`
  - Reactome: `92`
  - UniProtKB: `2025_01`
  - DrugCentral: `08222022`
  - KEGG: `113.0`
    
# 2.10.1
**Date:  2024.9.02**

Counts:
- Nodes: 8,507,201
- Edges: 57,418,405

Issues:
- Issue [#140](https://github.com/RTXteam/RTX-KG2/issues/140)
- Issue [#387](https://github.com/RTXteam/RTX-KG2/issues/387)
- Issue [#388](https://github.com/RTXteam/RTX-KG2/issues/388)
- Issue [#390](https://github.com/RTXteam/RTX-KG2/issues/390)
- Issue [#392](https://github.com/RTXteam/RTX-KG2/issues/392)
- Issue [#393](https://github.com/RTXteam/RTX-KG2/issues/393)
- Issue [#398](https://github.com/RTXteam/RTX-KG2/issues/398)
- Issue [#399](https://github.com/RTXteam/RTX-KG2/issues/399)
- Issue [#400](https://github.com/RTXteam/RTX-KG2/issues/400)
- Issue [#404](https://github.com/RTXteam/RTX-KG2/issues/404)
- Issue [#405](https://github.com/RTXteam/RTX-KG2/issues/405)
- Additional issues that arose during the build: [#408 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/408#issuecomment-2336826509)

Build info:
- Biolink Model version: 4.2.1
- InfoRes Registry version: 0.2.8
- Build host: `kg2101build.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `midjuly24work`
- Neo4j endpoint CNAME: `kg2endpoint-kg2-10-1.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint4.rtx.ai`
- Tracking issue for the build: [#408](https://github.com/RTXteam/RTX-KG2/issues/408)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2023AA`
  - ChEMBL: `33`
  - DrugBank: `5.1.10`
  - Ensembl: `106`
  - Reactome: `80`
  - UniProtKB: `2024_04`
  - DrugCentral: `52`
  - KEGG: `111.0`


# 2.10.0
**Date:  2024.07.11**

Counts:
- Nodes: 8,566,249
- Edges: 57,650,718

Issues:
- Issue [#358](https://github.com/RTXteam/RTX-KG2/issues/358)
- Issue [#383](https://github.com/RTXteam/RTX-KG2/issues/383) - temporary patch for `DRUGBANK:drug-interaction`
- Additional issues that arose during the build: [#395 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/395#issuecomment-2223612095)

Build info:
- Biolink Model version: 4.2.0
- InfoRes Registry version: 0.2.8
- Build host: `kg2100build.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `kg2100build`
- Neo4j endpoint CNAME: `kg2endpoint-kg2-10-0.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint3.rtx.ai`
- Tracking issue for the build: [#395](https://github.com/RTXteam/RTX-KG2/issues/395)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2023AA`
  - ChEMBL: `33`
  - DrugBank: `5.1.10`
  - Ensembl: `106`
  - GO annotations: `2024-6-14`
  - UniProtKB: `2024_03`
  - DrugCentral: `52`
  - KEGG: `111.0`


# 2.9.3
**Date:  2024.07.03**

Counts:
- Nodes: 8,566,172
- Edges: 57,646,688

Issues:
- Issue [#378](https://github.com/RTXteam/RTX-KG2/issues/378)
- Issue [#380](https://github.com/RTXteam/RTX-KG2/issues/380)
- Issue [#383](https://github.com/RTXteam/RTX-KG2/issues/383) - included in code, but not mapped into predicates
- Issue [#385](https://github.com/RTXteam/RTX-KG2/issues/385)
- Issue [#389](https://github.com/RTXteam/RTX-KG2/issues/389) - major code restructure
- Issue [#390](https://github.com/RTXteam/RTX-KG2/issues/390) - partially done

Build info:
- Biolink Model version: 4.2.0
- InfoRes Registry version: 0.2.8
- Build host: `kg2erica2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `archiving2`
- Neo4j endpoint CNAME: N/A
- Neo4j endpoint hostname: N/A
- Tracking issue for the build: N/A
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2023AA`
  - ChEMBL: `33`
  - DrugBank: `5.1.10`
  - Ensembl: `106`
  - GO annotations: `2024-6-14`
  - UniProtKB: `2024_03`
  - DrugCentral: `52`
  - KEGG: `111.0`



# 2.9.0
**Date:  2024.03.18**

Counts:
- Nodes: 8,558,851
- Edges: 57,138,154

Issues:
- Issue [#316](https://github.com/RTXteam/RTX-KG2/issues/316)
- Issue [#344](https://github.com/RTXteam/RTX-KG2/issues/344)
- Additional issues that arose during the build: [#349 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/349#issuecomment-1712645052)

Build info:
- Biolink Model version: 4.0.0
- Build host: `kg290build.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `master`
- Neo4j endpoint CNAME: 
- Neo4j endpoint hostname: `kg2endpoint3.rtx.ai`
- Tracking issue for the build: NA
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2023AA`
  - ChEMBL: `33`
  - DrugBank: `5.1.10`
  - Ensembl: `106`
  - GO annotations: `2023-6-11`
  - UniProtKB: `2023_02`
  - DrugCentral: `52`
  - KEGG: `107.0`

# 2.8.6
**Date:  2023.09.09**

Counts:
- Nodes: 8,493,096
- Edges: 56,911,675

Issues:
- Issue [#316](https://github.com/RTXteam/RTX-KG2/issues/316)
- Issue [#344](https://github.com/RTXteam/RTX-KG2/issues/344)
- Additional issues that arose during the build: [#349 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/349#issuecomment-1712645052)

Build info:
- Biolink Model version: 3.5.2
- Build host: `kg286build.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `issue-316`
- Neo4j endpoint CNAME: 
- Neo4j endpoint hostname: 
- Tracking issue for the build: Issue [#349](https://github.com/RTXteam/RTX-KG2/issues/349)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2023AA`
  - ChEMBL: `33`
  - DrugBank: `5.1.10`
  - Ensembl: `106`
  - GO annotations: `2023-6-11`
  - UniProtKB: `2023_02`
  - DrugCentral: `52`
  - KEGG: `107.0`

# 2.8.5
**Date:  2023.08.05**

Counts:
- Nodes: 8,437,312
- Edges: 54,274,882

Issues:
- Issue [#321](https://github.com/RTXteam/RTX-KG2/issues/321)
- Issue [#323](https://github.com/RTXteam/RTX-KG2/issues/323)
- Issue [#336](https://github.com/RTXteam/RTX-KG2/issues/336) - attempt failed though
- Issue [#337](https://github.com/RTXteam/RTX-KG2/issues/337)
- Issue [#339](https://github.com/RTXteam/RTX-KG2/issues/339)
- Additional issues that arose during the build: [#343](https://github.com/RTXteam/RTX-KG2/issues/343)

Build info:
- Biolink Model version: 3.5.2
- Build host: `kg285build.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `jsonlines`
- Neo4j endpoint CNAME: 
- Neo4j endpoint hostname: 
- Tracking issue for the build: Issue [#312](https://github.com/RTXteam/RTX-KG2/issues/321)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2023AA`
  - ChEMBL: `33`
  - DrugBank: `5.1.10`
  - Ensembl: `106`
  - GO annotations: `2023-6-11`
  - UniProtKB: `2023_02`
  - DrugCentral: `52`
  - KEGG: `107.0`

# 2.8.4
**Date:  2023.07.20**

Counts:
- Nodes: 8,436,874
- Edges: 54,363,492

Issues:
- Issue [#216](https://github.com/RTXteam/RTX-KG2/issues/216)
- Issue [#230](https://github.com/RTXteam/RTX-KG2/issues/230)
- Issue [#232](https://github.com/RTXteam/RTX-KG2/issues/232)
- Issue [#262](https://github.com/RTXteam/RTX-KG2/issues/262)
- Issue [#276](https://github.com/RTXteam/RTX-KG2/issues/276)
- Issue [#278](https://github.com/RTXteam/RTX-KG2/issues/278)
- Issue [#279](https://github.com/RTXteam/RTX-KG2/issues/279)
- Issue [#280](https://github.com/RTXteam/RTX-KG2/issues/280)
- Issue [#281](https://github.com/RTXteam/RTX-KG2/issues/281)
- Issue [#286](https://github.com/RTXteam/RTX-KG2/issues/286)
- Issue [#287](https://github.com/RTXteam/RTX-KG2/issues/287)
- Issue [#290](https://github.com/RTXteam/RTX-KG2/issues/290)
- Issue [#291](https://github.com/RTXteam/RTX-KG2/issues/291)
- Issue [#292](https://github.com/RTXteam/RTX-KG2/issues/292)
- Issue [#293](https://github.com/RTXteam/RTX-KG2/issues/293)
- Issue [#294](https://github.com/RTXteam/RTX-KG2/issues/294)
- Issue [#295](https://github.com/RTXteam/RTX-KG2/issues/295)
- Issue [#296](https://github.com/RTXteam/RTX-KG2/issues/296)
- Issue [#297](https://github.com/RTXteam/RTX-KG2/issues/297)
- Issue [#298](https://github.com/RTXteam/RTX-KG2/issues/298)
- Issue [#299](https://github.com/RTXteam/RTX-KG2/issues/299)
- Issue [#300](https://github.com/RTXteam/RTX-KG2/issues/300)
- Issue [#301](https://github.com/RTXteam/RTX-KG2/issues/301)
- Issue [#302](https://github.com/RTXteam/RTX-KG2/issues/302)
- Issue [#303](https://github.com/RTXteam/RTX-KG2/issues/303) - we are using a pickled copy of an old version of FOODON in this build
- Issue [#304](https://github.com/RTXteam/RTX-KG2/issues/304)
- Issue [#305](https://github.com/RTXteam/RTX-KG2/issues/305)
- Issue [#307](https://github.com/RTXteam/RTX-KG2/issues/307) – LOINC dropped from KG2
- Issue [#310](https://github.com/RTXteam/RTX-KG2/issues/310)
- Issue [#311](https://github.com/RTXteam/RTX-KG2/issues/311)
- Issue [#315](https://github.com/RTXteam/RTX-KG2/issues/315)
- Issue [#319](https://github.com/RTXteam/RTX-KG2/issues/319)
- Issue [#320](https://github.com/RTXteam/RTX-KG2/issues/320)
- Issue [#324](https://github.com/RTXteam/RTX-KG2/issues/324)
- Issue [#325](https://github.com/RTXteam/RTX-KG2/issues/325)
- Additional issues that arose during the build: [#294 (comment)](https://github.com/RTXteam/RTX-KG2/issues/294#issuecomment-1644489313), [#312 (comment)](https://github.com/RTXteam/RTX-KG2/issues/312#issuecomment-1645008620), [#327](https://github.com/RTXteam/RTX-KG2/issues/327), [#328](https://github.com/RTXteam/RTX-KG2/issues/328), [#329](https://github.com/RTXteam/RTX-KG2/issues/329), [#330](https://github.com/RTXteam/RTX-KG2/issues/330)

Build info:
- Biolink Model version: 3.5.2
- Build host: `buildkg2.rtx.ai` (new instance, old version was deprecated)
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `kg2.8.4prep`
- Neo4j endpoint CNAME:  `kg2-8-4.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint4.rtx.ai`
- Tracking issue for the build: Issue [#312](https://github.com/RTXteam/RTX-KG2/issues/312)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2023AA`
  - ChEMBL: `33`
  - DrugBank: `5.1.10`
  - Ensembl: `106`
  - GO annotations: `2023-6-11`
  - UniProtKB: `2023_02`
  - DrugCentral: `52`
  - KEGG: `107.0`
 
# 2.8.3
**Date:  2023.XX.XX**

Counts:
- Nodes: 10,370,747
- Edges: 54,078,936

Issues:
- Issue [#265](https://github.com/RTXteam/RTX-KG2/issues/265)
- Issue [#269](https://github.com/RTXteam/RTX-KG2/issues/269)
- Issue [#273](https://github.com/RTXteam/RTX-KG2/issues/273)
- Additional issues that arose during the build: [#](https://github.com/RTXteam/RTX-KG2/issues/)

Build info:
- Biolink Model version: 3.1.2
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `issue-263`
- Neo4j endpoint CNAME: 
- Neo4j endpoint hostname: 
- Tracking issue for the build: Issue [#264](https://github.com/RTXteam/RTX-KG2/issues/264)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2022AA`
  - ChEMBL: `30`
  - DrugBank: `5.1.9`
  - Ensembl: `106`
  - GO annotations: `2023-6-11`
  - UniProtKB: `2023_02`
  - DrugCentral: `52`
  - KEGG: `105.0`
 
# 2.8.2
**Date:  2023.XX.XX**

Counts:
- Nodes: 10,370,747
- Edges: 54,078,936

Issues:
- Issue [#263](https://github.com/RTXteam/RTX-KG2/issues/263)
- Build abandoned due to nonsensical predicates [#269]
- Additional issues that arose during the build: [#269](https://github.com/RTXteam/RTX-KG2/issues/269)

Build info:
- Biolink Model version: 3.1.2
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `issue-263`
- Neo4j endpoint CNAME: 
- Neo4j endpoint hostname: 
- Tracking issue for the build: Issue [#264](https://github.com/RTXteam/RTX-KG2/issues/264)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2022AA`
  - ChEMBL: `30`
  - DrugBank: `5.1.9`
  - Ensembl: `106`
  - GO annotations: `2023-6-11`
  - UniProtKB: `2023_02`
  - DrugCentral: `52`
  - KEGG: `105.0`

# 2.8.1
**Date:  2022.XX.XX**

Counts:
- Nodes: 10,370,747
- Edges: 54,078,936

Issues:
- Issue [#253](https://github.com/RTXteam/RTX-KG2/issues/253)
- Issue [#251](https://github.com/RTXteam/RTX-KG2/issues/251)
- Issue [#250](https://github.com/RTXteam/RTX-KG2/issues/250)
- Issue [#246](https://github.com/RTXteam/RTX-KG2/issues/246)
- Additional issues that arose during the build: 

Build info:
- Biolink Model version: 3.1.2
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `issue-252`
- Neo4j endpoint CNAME: `kg2-8-1.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint2.rtx.ai`
- Tracking issue for the build: Issue [#252](https://github.com/RTXteam/RTX-KG2/issues/252)
- Major knowledge source versions:
  - SemMedDB: `43 (2023)`
  - UMLS: `2022AA`
  - ChEMBL: `30`
  - DrugBank: `5.1.9`
  - Ensembl: `106`
  - GO annotations: `2022-11-17`
  - UniProtKB: `2022_03`
  - UniChem: `385`
  - DrugCentral: `48`
  - KEGG: `105.0`


# 2.8.0
**Date:  2022.12.12**

Counts:
- Nodes: 10,370,747
- Edges: 54,078,936

Issues:
- Issue [#220](https://github.com/RTXteam/RTX-KG2/issues/220)
- Issue [#221](https://github.com/RTXteam/RTX-KG2/issues/221)
- Issue [#222](https://github.com/RTXteam/RTX-KG2/issues/222)
- Additional issues that arose during the build: #227, #228, #229, #230, #231, #232, #233, #234, #235, #236, #237, #238, #243, #244

Build info:
- Biolink Model version: 3.0.0
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `issue-226`
- Neo4j endpoint CNAME: `kg2-8-0.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint2.rtx.ai`
- Tracking issue for the build: Issue [#226](https://github.com/RTXteam/RTX-KG2/issues/226)
- Major knowledge source versions:
  - SemMedDB: `23 (2021)`
  - UMLS: `2022AA`
  - ChEMBL: `30`
  - DrugBank: `5.1.9`
  - Ensembl: `106`
  - GO annotations: `2021-07-01`
  - UniProtKB: `2022_02`
  - UniChem: `385`
  - DrugCentral: `48`
  - KEGG: `103.0`

# 2.7.6
**Date:  2022.05.10**

Counts:
- Nodes: 10,370,747
- Edges: 54,078,936

Issues:
- Issue [#196](https://github.com/RTXteam/RTX-KG2/issues/196)
- Issue [#201](https://github.com/RTXteam/RTX-KG2/issues/201)
- Additional issues that arose during the build: 203, 204, 205, 206

Build info:
- Biolink Model version: 2.2.11
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `master`
- Neo4j endpoint CNAME: `kg2-7-6.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint2.rtx.ai`
- Tracking issue for the build: Issue [#202](https://github.com/RTXteam/RTX-KG2/issues/202)
- Major knowledge source versions:
  - SemMedDB: `23 (2021)`
  - UMLS: `2020AA`
  - ChEMBL: `27`
  - DrugBank: `5.1`
  - Ensembl: `103`
  - GO annotations: `2021-11-08`
  - UniProtKB: `2021_04`
  - UniChem: `385`
  - DrugCentral: `48`
  - KEGG: `101.0`
  
# 2.7.5
**Date:  2022.02.08**

Counts:
- Nodes: 10,361,234
- Edges: 54,068,633

Issues:
- Issue [#193](https://github.com/RTXteam/RTX-KG2/issues/193)
- Additional issues that arose during the build: In build ticket

Build info:
- Biolink Model version: 2.2.11
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `master`
- Neo4j endpoint CNAME: `kg2-7-5.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint4.rtx.ai`
- Tracking issue for the build: Issue [#193](https://github.com/RTXteam/RTX-KG2/issues/193)

# 2.7.4
**Date:  2021.11.12**

Counts:
- Nodes: 10,346,321
- Edges: 54,828,529

Issues:
- Issue [#167](https://github.com/RTXteam/RTX-KG2/issues/167)
- Issue [#165](https://github.com/RTXteam/RTX-KG2/issues/165)
- Issue [#164](https://github.com/RTXteam/RTX-KG2/issues/164)
- Issue [#157](https://github.com/RTXteam/RTX-KG2/issues/157)
- Issue [#156](https://github.com/RTXteam/RTX-KG2/issues/156)
- Issue [#155](https://github.com/RTXteam/RTX-KG2/issues/155)
- Additional issues that arose during the build: 180, 178, 177, 175, 174, 173, 168, 164

Build info:
- Biolink Model version: 2.2.6
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `issue165`
- Neo4j endpoint CNAME: `kg2-7-4.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint3.rtx.ai`
- Tracking issue for the build: Issue [#166](https://github.com/RTXteam/RTX-KG2/issues/166)

# 2.7.3
**Date:  2021.09.17**

Counts:
- Nodes: 10,238,961
- Edges: 54,041,267

Issues:
- Issue [#145](https://github.com/RTXteam/RTX-KG2/issues/145)
- Issue [#142](https://github.com/RTXteam/RTX-KG2/issues/142)
- Issue [#141](https://github.com/RTXteam/RTX-KG2/issues/141)
- Issue [#136](https://github.com/RTXteam/RTX-KG2/issues/136)
- Issue [#131](https://github.com/RTXteam/RTX-KG2/issues/131)
- Additional issues that arose during the build: 150, 149, 148, 147, 146, 145, 144

Build info:
- Biolink Model version: 2.1.0
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `master`
- Neo4j endpoint CNAME: `kg2-7-3.rtx.ai`
- Neo4j endpoint hostname: `kg2endpoint4.rtx.ai`
- Tracking issue for the build: Issue [#138](https://github.com/RTXteam/RTX-KG2/issues/138)

# 2.7.2
**Date: 2021.08.19**

Counts:
- Nodes: 10,237,436
- Edges: 54,036,959

Issues:
 - Issue [#95](https://github.com/RTXteam/RTX-KG2/issues/95)
 - Issue [#105](https://github.com/RTXteam/RTX-KG2/issues/105)
 - Issue [#120](https://github.com/RTXteam/RTX-KG2/issues/120)
 - Additional issues that arose during the build: 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119

Build info:
- Biolink Model version: 2.1.0
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `issue95`
- Neo4j endpoint CNAME: `kg2-7-2.rtx.ai`
- Tracking issue for the build: Issue [#104](https://github.com/RTXteam/RTX-KG2/issues/104)

# 2.7.1
**Date: 2021.07.13**

Counts:
- Nodes: 9,738,008
- Edges: 48,781,064

Note:
 - Building on `kg2steve.rtx.ai` inadvertantly pulled in old versions of ontologies (from Sept. 2020)
 
Issues:
 - Issue [#97](https://github.com/RTXteam/RTX-KG2/issues/97)
 
Build info:
- Biolink Model Version: 2.1.0
- Build host: `kg2steve.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build/`
- Build code branch: `biolink-2.0`
- Neo4j endpoint CNAME: `kg2endpoint-kg2-7-1.rtx.ai`

# 2.7.0
**Date: 2021.07.08**

Biolink Model Version: 2.1.0

Nodes: 9,738,008
Edges: 48,781,064

Notes:
 - Reactome released a new version which resulted in a failure of the compartment related queries, which are now commented out in the code.

Issues:
 - Issue [#77](https://github.com/RTXteam/RTX-KG2/issues/77)
 - Issue [#64](https://github.com/RTXteam/RTX-KG2/issues/64)

Build host: `kg2steve.rtx.ai`
Build directory: `/home/ubuntu/kg2-build/`
Build code branch: `biolink-2.0`

# 2.6.7
**Date: 2021.06.23**

Biolink Model Version: 1.8.1

Nodes: 9,781,698

Edges: 46,296,048

Notes:
 - Only edited `edges.tsv` file from KG2.6.6 (and `nodes.tsv` to increase version)

Issues:

 - Issue [#81](https://github.com/RTXteam/RTX-KG2/issues/81)

Build host: `kg2lindsey.rtx.ai` 
Build directory: `/home/ubuntu/kg2-build/`
Build code branch: `master`
Neo4j endpoint CNAME: `kg2endpoint-kg2-6-7.rtx.ai`

# 2.6.6
**Date: 2021.06.22**

Biolink Model Version: 1.8.1

Nodes: 9,781,698

Edges: 46,296,048

Notes:
 - Only edited `edges.tsv` file from KG2.6.5 (and `nodes.tsv` to increase version)

Issues:

 - Issue [#78](https://github.com/RTXteam/RTX-KG2/issues/78)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`

# 2.6.5
**Date: 2021.6.20**

Biolink Model Version: 1.8.1

Nodes: 9,781,698

Edges: 46,296,048

Notes:
 - Of the source JSON files, only regenerated `kg2-ont.json` to minimize build time (to get build out quicker)

Issues:

 - Issue [#56](https://github.com/RTXteam/RTX-KG2/issues/56)
 - Issue [#49](https://github.com/RTXteam/RTX-KG2/issues/49)
 - Issue [#55](https://github.com/RTXteam/RTX-KG2/issues/55)
 - Issue [#47](https://github.com/RTXteam/RTX-KG2/issues/47)
 - Issue [#68](https://github.com/RTXteam/RTX-KG2/issues/68)
 - Issue [#9](https://github.com/RTXteam/RTX-KG2/issues/9)
 - Issue [#62](https://github.com/RTXteam/RTX-KG2/issues/62)
 - Issue [#14](https://github.com/RTXteam/RTX-KG2/issues/14)
 - Issue [#19](https://github.com/RTXteam/RTX-KG2/issues/19)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`

# 2.6.3

**Date: 2021.5.7**

Biolink Model Version: 1.8.1

Nodes: 10,694,772

Edges: 51,687,002

Notes: 
 - Built by modifying edges.tsv to address 1432 speedily. changes then incorporated into the whole build process.

Issues:
 
 - Issue [#1432](https://github.com/RTXteam/RTX/issues/1432)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`

# 2.6.2

**Date: 2021.5.1**

Biolink Model Version: 1.8.1

Nodes: 10,694,772

Edges: 51,687,002

Notes: 
 - Partial rebuild from Simplify on branch Ontobio507TempFix

Issues:
 
 - Issue [#1423](https://github.com/RTXteam/RTX/issues/1423)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`


# 2.6.1

**Date: 2021.4.28**

Biolink Model Version: 1.8.1

Nodes: 10,694,772

Edges: 51,687,002

Notes: 
 - this build was done from the branch Ontobio507TempFix,
 with an uncommitted workaround to add some of the KEGG nodes back in

Issues:
 
 - Issue [#1400](https://github.com/RTXteam/RTX/issues/1400)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`

# 2.6.0

**Date: 2021.4.23**

Biolink Model Version: 1.8.1

Nodes: 10,675,990

Edges: 49,342,413 

Notes: 
 - KG1 was dropped from this build, and with it KEGG
 - this build was done from the branch Ontobio507TempFix

Issues:
 
 - Issue [#1381](https://github.com/RTXteam/RTX/issues/1381)
 - Issue [#1374](https://github.com/RTXteam/RTX/issues/1374)
 - Issue [#1362](https://github.com/RTXteam/RTX/issues/1363)
 - Issue [#1362](https://github.com/RTXteam/RTX/issues/1362)
 - Issue [#1358](https://github.com/RTXteam/RTX/issues/1358)
 - Issue [#1345](https://github.com/RTXteam/RTX/issues/1345)
 - Issue [#1343](https://github.com/RTXteam/RTX/issues/1343)
 - Issue [#1335](https://github.com/RTXteam/RTX/issues/1335)
 - Issue [#1332](https://github.com/RTXteam/RTX/issues/1332)
 - Issue [#1322](https://github.com/RTXteam/RTX/issues/1322)
 - Issue [#1311](https://github.com/RTXteam/RTX/issues/1311)
 - Issue [#1292](https://github.com/RTXteam/RTX/issues/1292)
 - Issue [#1286](https://github.com/RTXteam/RTX/issues/1286)
 - Issue [#1278](https://github.com/RTXteam/RTX/issues/1278)
 - Issue [#1273](https://github.com/RTXteam/RTX/issues/1273)
 - Issue [#1247](https://github.com/RTXteam/RTX/issues/1247)
 - Issue [#1246](https://github.com/RTXteam/RTX/issues/1246)
 - Issue [#1245](https://github.com/RTXteam/RTX/issues/1245)
 - Issue [#1220](https://github.com/RTXteam/RTX/issues/1220)
 - Issue [#1213](https://github.com/RTXteam/RTX/issues/1213)
 - Issue [#1199](https://github.com/RTXteam/RTX/issues/1199)
 - Issue [#1189](https://github.com/RTXteam/RTX/issues/1189)
 - Issue [#1170](https://github.com/RTXteam/RTX/issues/1170)
 - Issue [#1125](https://github.com/RTXteam/RTX/issues/1125)
 - Issue [#1078](https://github.com/RTXteam/RTX/issues/1078)
 - Issue [#1027](https://github.com/RTXteam/RTX/issues/1027)
 - Issue [#636](https://github.com/RTXteam/RTX/issues/636)
 - Issue [#550](https://github.com/RTXteam/RTX/issues/550)
 - Issue [#545](https://github.com/RTXteam/RTX/issues/545)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`
Json file(s) stored on same host, `/home/ubuntu/kg2-build/KG2-6-0/`

# 2.5.2 

**Date: 2021.3.6**

Nodes: 10,546,338
Edges: 53,739,675

- Issue [#1283](https://github.com/RTXteam/RTX/issues/1283)
- Issue [#1271](https://github.com/RTXteam/RTX/issues/1271)
- Issue [#1270](https://github.com/RTXteam/RTX/issues/1270)
- Issue [#1267](https://github.com/RTXteam/RTX/issues/1267)
- Issue [#1266](https://github.com/RTXteam/RTX/issues/1266)
- Issue [#1264](https://github.com/RTXteam/RTX/issues/1264)
- Issue [#1263](https://github.com/RTXteam/RTX/issues/1263)
- Issue [#1259](https://github.com/RTXteam/RTX/issues/1259)
- Issue [#1253](https://github.com/RTXteam/RTX/issues/1253)
- Issue [#1249](https://github.com/RTXteam/RTX/issues/1249)
- Issue [#1243](https://github.com/RTXteam/RTX/issues/1243)
- Issue [#1230](https://github.com/RTXteam/RTX/issues/1230)
- Issue [#1219](https://github.com/RTXteam/RTX/issues/1219)
- Issue [#1216](https://github.com/RTXteam/RTX/issues/1216)
- Issue [#1214](https://github.com/RTXteam/RTX/issues/1214)
- Issue [#1175](https://github.com/RTXteam/RTX/issues/1175)
- Issue [#1171](https://github.com/RTXteam/RTX/issues/1171)
- Issue [#1160](https://github.com/RTXteam/RTX/issues/1160)
- Issue [#1128](https://github.com/RTXteam/RTX/issues/1128)
- Issue [#1114](https://github.com/RTXteam/RTX/issues/1114)
- Issue [#1050](https://github.com/RTXteam/RTX/issues/1050)
- Issue [#1025](https://github.com/RTXteam/RTX/issues/1025)
- Issue [#964](https://github.com/RTXteam/RTX/issues/964)
- Issue [#762](https://github.com/RTXteam/RTX/issues/762)

Build host: `kg2steve.rtx.ai` `/home/ubuntu/kg2-build/`

# 2.5.1 

**Date: 2021.1.24**

Nodes: 10,533,862

Edges: 53,474,162

- Issue [#1185](https://github.com/RTXteam/RTX/issues/1185)
- Issue [#1171 (tentative)](https://github.com/RTXteam/RTX/issues/1171)
- Issue [#1122](https://github.com/RTXteam/RTX/issues/1122)
- Issue [#1200](https://github.com/RTXteam/RTX/issues/1200)
- Issue [#1079](https://github.com/RTXteam/RTX/issues/1079)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`

# 2.5.0 

**Date: 2021.1.14**

Nodes: 10,533,862

Edges: 53,416,143

- Issue [#1173](https://github.com/RTXteam/RTX/issues/1173)
- Issue [#1180](https://github.com/RTXteam/RTX/issues/1180)
- Issue [#1155](https://github.com/RTXteam/RTX/issues/1155)
- Issue [#1083](https://github.com/RTXteam/RTX/issues/1083)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`

# 2.4.0 

**Date: 2020.12.11**

Nodes: 10,533,792

Edges: 53,415,986

- Issue [#1161](https://github.com/RTXteam/RTX/issues/1161)
- Issue [#1126](https://github.com/RTXteam/RTX/issues/1126)
- Issue [#1123](https://github.com/RTXteam/RTX/issues/1123)
- Issue [#1142](https://github.com/RTXteam/RTX/issues/1142)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build/`

# 2.3.5 

**Date: 2020.10.26**

Nodes: 10,543,712

Edges: 53,456,505

- Issue [#1091](https://github.com/RTXteam/RTX/issues/1091)
- Issue [#1103](https://github.com/RTXteam/RTX/issues/1103)
- Issue [#1102](https://github.com/RTXteam/RTX/issues/1102)
- Issue [#1107](https://github.com/RTXteam/RTX/issues/1107)
- Issue [#1115](https://github.com/RTXteam/RTX/issues/1115)
- Issue [#1053](https://github.com/RTXteam/RTX/issues/1053)
- Issue [#1076](https://github.com/RTXteam/RTX/issues/1076)
- Issue [#981](https://github.com/RTXteam/RTX/issues/981)
- Issue [#1098](https://github.com/RTXteam/RTX/issues/1098)
- Issue [#931](https://github.com/RTXteam/RTX/issues/931)
- Issue [#891](https://github.com/RTXteam/RTX/issues/891)

Build host: `kg2lindsey.rtx.ai` `/home/ubuntu/kg2-build-3.5/`

# 2.3.4 

**Date: 2020.09.04**

Nodes: 10,527,134

Edges: 53,589,306

- Issue [#1051](https://github.com/RTXteam/RTX/issues/1051)
- Issue [#1045(?)](https://github.com/RTXteam/RTX/issues/1045)
- Issue [#1027(?)](https://github.com/RTXteam/RTX/issues/1027)
- Issue [#931](https://github.com/RTXteam/RTX/issues/931)
- Issue [#999](https://github.com/RTXteam/RTX/issues/999)
- Issue [#762](https://github.com/RTXteam/RTX/issues/762)

Build host: `kg2steve.rtx.ai`.

# 2.3.1 

**Date: 2020.08.21**

Nodes: 9,633,671

Edges: 52,537,504

- Issue [#1031](https://github.com/RTXteam/RTX/issues/1031)
- Issue [#1033](https://github.com/RTXteam/RTX/issues/1033)
- Issue [#1019](https://github.com/RTXteam/RTX/issues/1019)
- Issue [#1024](https://github.com/RTXteam/RTX/issues/1024)
- Issue [#1016](https://github.com/RTXteam/RTX/issues/1016)
- Issue [#1000](https://github.com/RTXteam/RTX/issues/1000)
- Issue [#1006](https://github.com/RTXteam/RTX/issues/1006)
- Issue [#1007](https://github.com/RTXteam/RTX/issues/1007)
- Issue [#988](https://github.com/RTXteam/RTX/issues/988)

Build host: `kg2dev.rtx.ai`.

