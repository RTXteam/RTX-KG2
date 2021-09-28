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

Build info:
- Biolink Model version: 2.1.0
- Build host: `buildkg2.rtx.ai`
- Build directory: `/home/ubuntu/kg2-build`
- Build code branch: `master`
- Neo4j endpoint CNAME: `kg2endpoint-kg2-7-3.rtx.ai`

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

