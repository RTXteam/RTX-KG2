## Time Comparison

All times come from Snakemake log for consistency, since this includes any lag time.

Everything that runs in parallel ran in parallel for these calculations.

For the JSON Lines test, there was a failure at Simplify and a failure at TSV that required a restart at those respective places. However, any files that were created in parallel were deleted so that the scripts that run in parallel to them would run in parallel for all testing, in order to accurately assess the time each stage takes.

Snakemake Rule|JSON Lines Run Time|KG2.8.4 Run Time|JSON Lines Start Time|JSON Lines End Time|KG2.8.4 Start Time|KG2.8.4 End Time
--|--|--|--|--|--|-- 
ChEMBL|04:15:33|04:16:43|Sat Jul 29 20:45:28 2023|Sun Jul 30 01:01:01 2023|Sun Jul 30 23:16:14 2023|Mon Jul 31 03:32:57 2023
ChEMBL_Conversion|00:28:55|00:25:31|Sun Jul 30 01:01:01 2023|Sun Jul 30 01:29:56 2023|Mon Jul 31 03:32:57 2023|Mon Jul 31 03:58:28 2023
DGIdb|00:00:00|00:00:00|Sat Jul 29 20:45:29 2023|Sat Jul 29 20:45:29 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:15:55 2023
DGIdb_Conversion|00:00:07|00:00:08|Sat Jul 29 20:45:29 2023|Sat Jul 29 20:45:36 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:16:04 2023
DisGeNET|00:00:07|00:02:07|Sat Jul 29 20:45:28 2023|Sat Jul 29 20:45:35 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:18:02 2023
DisGeNET_Conversion|00:00:33|00:00:42|Sat Jul 29 20:45:35 2023|Sat Jul 29 20:46:08 2023|Sun Jul 30 23:18:02 2023|Sun Jul 30 23:18:44 2023
DrugBank|00:00:14|00:00:12|Sat Jul 29 20:45:36 2023|Sat Jul 29 20:45:50 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:16:07 2023
DrugBank_Conversion|00:06:47|00:09:04|Sat Jul 29 20:45:50 2023|Sat Jul 29 20:52:37 2023|Sun Jul 30 23:16:07 2023|Sun Jul 30 23:25:11 2023
DrugCentral|00:04:09|00:04:05|Sat Jul 29 20:45:28 2023|Sat Jul 29 20:49:37 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:20:20 2023
DrugCentral_Conversion|00:00:17|00:00:29|Sat Jul 29 20:49:37 2023|Sat Jul 29 20:49:54 2023|Sun Jul 30 23:20:20 2023|Sun Jul 30 23:20:49 2023
Ensembl|00:03:24|00:03:32|Sat Jul 29 20:45:28 2023|Sat Jul 29 20:48:52 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:19:28 2023
Ensembl_Conversion|00:03:12|00:04:59|Sat Jul 29 20:48:52 2023|Sat Jul 29 20:52:04 2023|Sun Jul 30 23:19:28 2023|Sun Jul 30 23:24:29 2023
Finish|01:22:29|00:00:00|Sun Jul 30 21:41:55 2023|Sun Jul 30 23:04:24 2023| | 
GO_Annotations|00:00:05|00:00:05|Sat Jul 29 20:45:28 2023|Sat Jul 29 20:45:33 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:16:00 2023
GO_Annotations_Conversion|00:00:23|00:00:50|Sat Jul 29 20:45:33 2023|Sat Jul 29 20:45:56 2023|Sun Jul 30 23:16:00 2023|Sun Jul 30 23:16:50 2023
HMDB|00:04:46|00:01:52|Sat Jul 29 20:45:48 2023|Sat Jul 29 20:50:34 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:17:47 2023
HMDB_Conversion|00:23:43|00:24:01|Sat Jul 29 20:50:34 2023|Sat Jul 29 21:14:17 2023|Sun Jul 30 23:17:47 2023|Sun Jul 30 23:41:48 2023
IntAct|00:01:23|00:01:22|Sat Jul 29 20:45:28 2023|Sat Jul 29 20:46:51 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:17:18 2023
IntAct_Conversion|00:00:44|00:01:01|Sat Jul 29 20:46:51 2023|Sat Jul 29 20:47:35 2023|Sun Jul 30 23:17:18 2023|Sun Jul 30 23:18:19 2023
JensenLab|00:09:52|00:12:30|Sat Jul 29 20:45:28 2023|Sat Jul 29 20:55:20 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:28:25 2023
JensenLab_Conversion|00:21:13|00:19:57|Sat Jul 29 20:55:20 2023|Sat Jul 29 21:16:33 2023|Sun Jul 30 23:28:25 2023|Sun Jul 30 23:48:22 2023
KEGG|04:41:17|20:06:05|Sat Jul 29 20:45:49 2023|Sun Jul 30 01:27:16 2023|Sun Jul 30 23:15:56 2023|Mon Jul 31 19:22:01 2023
KEGG_Conversion|00:00:23|00:00:33|Sun Jul 30 01:27:16 2023|Sun Jul 30 01:27:39 2023|Mon Jul 31 19:22:01 2023|Mon Jul 31 19:22:34 2023
Merge|08:34:45|00:00:00|Sun Jul 30 09:15:15 2023|Sun Jul 30 17:50:00 2023| | 
NCBIGene|00:00:03|00:00:02|Sat Jul 29 20:45:28 2023|Sat Jul 29 20:45:31 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:15:57 2023
NCBIGene_Conversion|00:00:18|00:00:42|Sat Jul 29 20:45:31 2023|Sat Jul 29 20:45:49 2023|Sun Jul 30 23:15:57 2023|Sun Jul 30 23:16:39 2023
Ontologies_and_TTL|06:47:19|08:26:09|Sun Jul 30 02:26:56 2023|Sun Jul 30 09:15:15 2023|Mon Jul 31 05:17:33 2023|Mon Jul 31 13:43:42 2023
Reactome|00:08:01|00:11:33|Sat Jul 29 20:45:29 2023|Sat Jul 29 20:53:30 2023|Sun Jul 30 23:16:04 2023|Sun Jul 30 23:27:37 2023
Reactome_Conversion|00:01:44|00:01:58|Sat Jul 29 20:53:30 2023|Sat Jul 29 20:55:14 2023|Sun Jul 30 23:27:37 2023|Sun Jul 30 23:29:35 2023
RepoDB|00:00:01|00:00:01|Sat Jul 29 20:45:56 2023|Sat Jul 29 20:45:57 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:15:56 2023
RepoDB_Conversion|00:00:28|00:00:26|Sat Jul 29 20:45:57 2023|Sat Jul 29 20:46:25 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:16:22 2023
SMPDB|00:17:59|00:17:02|Sat Jul 29 20:45:29 2023|Sat Jul 29 21:03:28 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:32:58 2023
SMPDB_Conversion|02:39:28|02:44:33|Sat Jul 29 21:03:28 2023|Sat Jul 29 23:42:56 2023|Sun Jul 30 23:32:58 2023|Mon Jul 31 02:27:31 2023
SemMedDB|11:18:44|10:46:16|Sat Jul 29 20:45:28 2023|Sun Jul 30 08:04:12 2023|Sun Jul 30 23:15:56 2023|Mon Jul 31 10:02:12 2023
SemMedDB_Conversion|00:35:48|00:00:00|Sun Jul 30 08:04:12 2023|Sun Jul 30 08:40:00 2023|Mon Jul 31 10:02:12 2023| 
Simplify|00:51:37|00:00:00|Sun Jul 30 19:20:11 2023|Sun Jul 30 20:11:48 2023| | 
Simplify_Stats|00:19:34|00:00:00|Sun Jul 30 20:37:49 2023|Sun Jul 30 20:57:23 2023| | 
Slim|00:29:09|00:00:00|Sun Jul 30 20:37:49 2023|Sun Jul 30 21:06:58 2023| | 
Stats|00:20:13|00:00:00|Sun Jul 30 19:20:11 2023|Sun Jul 30 19:40:24 2023| | 
TSV|01:04:06|00:00:00|Sun Jul 30 20:37:49 2023|Sun Jul 30 21:41:55 2023| | 
UMLS|05:41:27|06:01:11|Sat Jul 29 20:45:29 2023|Sun Jul 30 02:26:56 2023|Sun Jul 30 23:16:22 2023|Mon Jul 31 05:17:33 2023
UniChem|00:15:43|00:17:07|Sat Jul 29 20:45:28 2023|Sat Jul 29 21:01:11 2023|Sun Jul 30 23:16:39 2023|Sun Jul 30 23:33:46 2023
UniChem_Conversion|00:00:09|00:00:13|Sat Jul 29 21:01:11 2023|Sat Jul 29 21:01:20 2023|Sun Jul 30 23:33:46 2023|Sun Jul 30 23:33:59 2023
UniProtKB|00:41:08|00:39:07|Sat Jul 29 20:45:29 2023|Sat Jul 29 21:26:37 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:55:02 2023
UniProtKB_Conversion|00:03:05|00:03:10|Sat Jul 29 21:26:37 2023|Sat Jul 29 21:29:42 2023|Sun Jul 30 23:55:02 2023|Sun Jul 30 23:58:12 2023
ValidationTests|00:00:35|00:00:34|Sat Jul 29 20:44:53 2023|Sat Jul 29 20:45:28 2023|Sun Jul 30 23:15:21 2023|Sun Jul 30 23:15:55 2023
miRBase|00:00:13|00:00:12|Sat Jul 29 20:45:29 2023|Sat Jul 29 20:45:42 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:16:08 2023
miRBase_Conversion|00:00:06|00:00:06|Sat Jul 29 20:45:42 2023|Sat Jul 29 20:45:48 2023|Sun Jul 30 23:16:08 2023|Sun Jul 30 23:16:14 2023
--|--|--|--|--|--|-- 
Build Stage Times:| | | | | |  
Pre-ETL|00:00:35|00:00:34|Sat Jul 29 20:44:53 2023|Sat Jul 29 20:45:28 2023|Sun Jul 30 23:15:21 2023|Sun Jul 30 23:15:55 2023
ETL|12:42:11|00:00:00|Sat Jul 29 20:45:28 2023|Sun Jul 30 09:15:15 2023| | 
Post-ETL|10:30:28|00:00:00|Merge: Sun Jul 30 09:15:15 2023<br>Simplify: Sun Jul 30 19:20:11 2023<br>TSV: Sun Jul 30 20:37:49 2023|Merge: Sun Jul 30 17:50:00 2023<br>Simplify: Sun Jul 30 20:11:48 2023<br>TSV: Sun Jul 30 21:41:55 2023| | 
Finish|01:22:29|00:00:00|Sun Jul 30 21:41:55 2023|Sun Jul 30 23:04:24 2023| | 
--|--|--|--|--|--|-- 
Total Build Times:| | | | | |  
Total|24:33:40|00:00:00||| | 


# Notable Changes from [KG2.8.4](https://github.com/RTXteam/RTX-KG2/releases/tag/KG2.8.4):

## Streaming SemMedDB
**Reason:** 

**Method:** 

**Important Code Notes:** 

**Important Considerations for Maintainers:** 

**Relevant Commits:**
- [`b4537b2`](https://github.com/RTXteam/RTX-KG2/commit/b4537b29765350424cb1052224452dc1048c7ce6)
- [`d501be7`](https://github.com/RTXteam/RTX-KG2/commit/d501be7b8980aca0a1c3b5a0d7fbcf7582ce78ed)
- [`02da59a`](https://github.com/RTXteam/RTX-KG2/commit/02da59a5e5c162d7036d561989003a6db0f18aa7)
- [`08133c1`](https://github.com/RTXteam/RTX-KG2/commit/08133c11ed426dfba47f0e1f66c754ad8faddb43)
- [`c4ea737`](https://github.com/RTXteam/RTX-KG2/commit/c4ea7376547d8861c7a9dfa076bd84e9de8579b8)
- [`243c462`](https://github.com/RTXteam/RTX-KG2/commit/243c4620acb6fe4fdf1669a8e242487d3515137f)
- [`d76afc0`](https://github.com/RTXteam/RTX-KG2/commit/d76afc0cc9f20b3a1bc0467493c1e2815b88f599)
- [`639065e`](https://github.com/RTXteam/RTX-KG2/commit/639065e459fb157e6ce5332d40882de6f8962a5c)
- [`c77f67e`](https://github.com/RTXteam/RTX-KG2/commit/c77f67ed0d2a92ad9e49a1505978cb181f3173c9)
- [`b03b2ad`](https://github.com/RTXteam/RTX-KG2/commit/b03b2ad2459222c164bab0d3ec6aa2c1d47940e8)
- [`b425236`](https://github.com/RTXteam/RTX-KG2/commit/b425236571b2d44a28f1e7d23656f0cac4e92121)
- [`36309ce`](https://github.com/RTXteam/RTX-KG2/commit/36309ce978e55528e029989ab300ddc6108059a6)
- [`80f689d`](https://github.com/RTXteam/RTX-KG2/commit/80f689df9c74967bb3e11f64f55269fee809256f)
- [`e5a66d4`](https://github.com/RTXteam/RTX-KG2/commit/e5a66d47b2067476131c00b631bb00f39da1c7cc)
- [`5ab1a20`](https://github.com/RTXteam/RTX-KG2/commit/5ab1a20a068623ef5e7c36ee404373efaa44c8fe)
- [`12073c6`](https://github.com/RTXteam/RTX-KG2/commit/12073c6a22f4eaf6219f39f4f0a2071b2cbd4ad5)
- [`b89d75c`](https://github.com/RTXteam/RTX-KG2/commit/b89d75c8e3eb356930bf8de38e268d891b8f991b)

**Relevant Issue Comments:**
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1646443209): This comment documents the original request for this feature.
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1648690706): This comment documents the issue with disk space that arises when `pymyql` is saving its temp file with the query result, this led to determining the issue with the binary log files, since much of the instance's disk space was taken up by that. It also resulted in commit [`12073c6`](https://github.com/RTXteam/RTX-KG2/commit/12073c6a22f4eaf6219f39f4f0a2071b2cbd4ad5) which deleted the files that are loaded into MySQL to make space. In general, you need the disk space (with 1 TB of space) to not be over 65% in use to avoid this error. 
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1649057345): This comment documents the error that occurs when the `GROUP_CONCAT` gets truncated after running into MySQL's limit. This error led to several commits ([`b4537b2`](https://github.com/RTXteam/RTX-KG2/commit/b4537b29765350424cb1052224452dc1048c7ce6), [`d501be7`](https://github.com/RTXteam/RTX-KG2/commit/d501be7b8980aca0a1c3b5a0d7fbcf7582ce78ed), [`c4ea737`](https://github.com/RTXteam/RTX-KG2/commit/c4ea7376547d8861c7a9dfa076bd84e9de8579b8), [`80f689d`](https://github.com/RTXteam/RTX-KG2/commit/80f689df9c74967bb3e11f64f55269fee809256f), [`b89d75c`](https://github.com/RTXteam/RTX-KG2/commit/b89d75c8e3eb356930bf8de38e268d891b8f991b)) in an attempt to curb this issue. This issue was finally eliminated with [`b89d75c`](https://github.com/RTXteam/RTX-KG2/commit/b89d75c8e3eb356930bf8de38e268d891b8f991b). No heuristics were used to set this parameter, only a guess-and-check strategy. The current value is a little less than half of the max integer, so hopefully this doesn't have to increase.
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1649208855): This comment provides an update on the issue regarding the max `GROUP_CONCAT` length, particularly giving it scope.
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1649268508): This comment reports on the timing improvement with this new structure.

## Changes to `query_kegg.py`

**Reason:** The original structure for `query_kegg.py` had the script send a request for each KEGG id to the KEGG API, one at a time. However, this is very slow. Based on the above table, this serial structure takes over 20 hours. With a longer build process than even UMLS (at 6 hours for extraction plus 8.5 hours for conversion, UMLS takes roughly 14.5 hours), this makes it a constraining script on the build. This became even more challenging because of the updates to `semmeddb_mysql_to_tuplelist_jsonl.py` and `semmeddb_tuplelist_json_to_kg_jsonl.py` to fully utilize the serial structure of JSON Lines. With that update, the SemMedDB portion of the ETL takes less than 12 hours. Thus, it was important that we sped up this extraction.

**Method:** 

**Important Code Notes:**

**Important Considerations for Maintainers:** 

**Relevant Commits:**
- [`255cb89`](https://github.com/RTXteam/RTX-KG2/commit/255cb8959b93314cf7f8d6be1ecbf215476acc99)
- [`1e68baf`](https://github.com/RTXteam/RTX-KG2/commit/1e68baf7b8f9f52f300f77012c03552e3bc2ed27)
- [`de5d0a5`](https://github.com/RTXteam/RTX-KG2/commit/de5d0a57fc2bd81fff86eaf51c1bc9a5a949ca50)
- [`a177b29`](https://github.com/RTXteam/RTX-KG2/commit/a177b2927d07dff7c00ef1d4a2de16d8c7d6584f)
- [`2838b76`](https://github.com/RTXteam/RTX-KG2/commit/2838b76622eef76ea8288a99f09d4dd16ef99739)
- [`8ad64e5`](https://github.com/RTXteam/RTX-KG2/commit/8ad64e57fa94a7eaed5656bad3e2e7df40f49b49)
- [`344c5e5`](https://github.com/RTXteam/RTX-KG2/commit/344c5e5f352f9bc968d838ff264147bb2e423017)

**Relevant Issue Comments:** [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1646443209)

## Rename Files
**Reason:** 

**Method:** 

**Important Code Notes:** 

**Important Considerations for Maintainers:** 

**Relevant Commits:**
- [`b03b2ad`](https://github.com/RTXteam/RTX-KG2/commit/b03b2ad2459222c164bab0d3ec6aa2c1d47940e8)
- [`ddba16b`](https://github.com/RTXteam/RTX-KG2/commit/ddba16b50a89bc80f1e6357b6533acd30800e3a4)
- [`4346127`](https://github.com/RTXteam/RTX-KG2/commit/43461270be69710fa32d37e220b71323dbffe9ee)
- [`b0b2303`](https://github.com/RTXteam/RTX-KG2/commit/b0b2303e60668c26ff484bde5bf36e474d86ca08)
- [`3ef738c`](https://github.com/RTXteam/RTX-KG2/commit/3ef738cc9d6788c12285b570c229f79ed5f1e055)
- [`ea8ab0a`](https://github.com/RTXteam/RTX-KG2/commit/ea8ab0abc1d02d9932449df5d76e39d32b90cc2a)
- [`ac46119`](https://github.com/RTXteam/RTX-KG2/commit/ac46119d00d7b043d45bfa9aceb5fcc2714b2415)
- [`1eadc46`](https://github.com/RTXteam/RTX-KG2/commit/1eadc4660d4514a450a5316d287bd4756a89e7cf)
- [`9bf1e8f`](https://github.com/RTXteam/RTX-KG2/commit/9bf1e8fa13bd76daec0ae52637dfee3a98cb82e0)
- [`a6944d7`](https://github.com/RTXteam/RTX-KG2/commit/a6944d7fc5eea05498db0e6a8ec45afad13dd170)
- [`9f53310`](https://github.com/RTXteam/RTX-KG2/commit/9f5331094d1ebd64aa32db93c89e8c120ed72a43)
- [`7e0eed5`](https://github.com/RTXteam/RTX-KG2/commit/7e0eed5c4db53170be6661fbca62c396c24ac630)
- [`de4d28c`](https://github.com/RTXteam/RTX-KG2/commit/de4d28cc4656f2de1c6fcb09791954577d86f28b)
- [`8a3c8ec`](https://github.com/RTXteam/RTX-KG2/commit/8a3c8ecc6a567f797a8d2679c59b6f9cada29328)
- [`7707691`](https://github.com/RTXteam/RTX-KG2/commit/77076912944ee7a9f7a05252e78e5f65f8c2b0bd)
- [`78a928b`](https://github.com/RTXteam/RTX-KG2/commit/78a928b5f858b767cfcd601291a8597cc2658021)
- [`7f7b320`](https://github.com/RTXteam/RTX-KG2/commit/7f7b320f91f01f0d4d7b9a066332ca1fddb41f44)
- [`2a4223e`](https://github.com/RTXteam/RTX-KG2/commit/2a4223e13654e238b81fca9e6ebb59405e62ec4a)
- [`286a3e6`](https://github.com/RTXteam/RTX-KG2/commit/286a3e605602ac2ffd24de8d99af81e7d56eb53c)
- [`a6799b5`](https://github.com/RTXteam/RTX-KG2/commit/a6799b51c037304855c4827b3397da38a44d483b)
- [`b425236`](https://github.com/RTXteam/RTX-KG2/commit/b425236571b2d44a28f1e7d23656f0cac4e92121)
- [`36309ce`](https://github.com/RTXteam/RTX-KG2/commit/36309ce978e55528e029989ab300ddc6108059a6)
- [`f094382`](https://github.com/RTXteam/RTX-KG2/commit/f094382846abc8006b6a88143618883654b5230a)
- [`6bfa52e`](https://github.com/RTXteam/RTX-KG2/commit/6bfa52e5fbcc01a7de05fd43032326beacd104c7)
- [`5720118`](https://github.com/RTXteam/RTX-KG2/commit/5720118d601445af3e7dcac4d25ec0b7811f9798)
- [`58f29ce`](https://github.com/RTXteam/RTX-KG2/commit/58f29cebbf211994d0b07d3f4a47500e3d8c9eba)
- [`3e07421`](https://github.com/RTXteam/RTX-KG2/commit/3e074217ef1e4e0e5800ea847c22cb76a73df106)
- [`ee87a9d`](https://github.com/RTXteam/RTX-KG2/commit/ee87a9dbbe6816e92010334dee12b7b6c8c12899)
- [`fce7423`](https://github.com/RTXteam/RTX-KG2/commit/fce7423569f1f0754a49be27ddb4a52bdce21e4e)
- [`a7bb6dc`](https://github.com/RTXteam/RTX-KG2/commit/a7bb6dc18516929435363db11bbc7b6cced33784)
- [`39c8cbd`](https://github.com/RTXteam/RTX-KG2/commit/39c8cbd498e03219036f7a80359fbf302d9f9178)
- [`34bef3d`](https://github.com/RTXteam/RTX-KG2/commit/34bef3dc302f367b5ae6da7f55eccd60c6ff1858)
- [`19f622d`](https://github.com/RTXteam/RTX-KG2/commit/19f622de5f5292068c37e553c4856eaee2e432f3)
- [`67be18b`](https://github.com/RTXteam/RTX-KG2/commit/67be18b5e4f1ec53c169c0c39d35ffc01935e710)
- [`5f85bbe`](https://github.com/RTXteam/RTX-KG2/commit/5f85bbe6ec2f1bd8edeba74fdcb44b6197736302)
- [`cc290ff`](https://github.com/RTXteam/RTX-KG2/commit/cc290fff069dba8c55d8e4c90e5afd6ad80f78bb)
- [`ee5a963`](https://github.com/RTXteam/RTX-KG2/commit/ee5a963586c167aadb109a4af96335885e8c50ae)
- [`d87e3b5`](https://github.com/RTXteam/RTX-KG2/commit/d87e3b5061234d2eaa64c02d7545ed0cc0b0a79d)
- [`7f1ccb0`](https://github.com/RTXteam/RTX-KG2/commit/7f1ccb0a32d748bed899a6768d58ec17077d2cc4)

**Relevant Issue Comments:**
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1646443209)
- [#332 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/332#issue-1819530418)

## Stop MySQL Binary Logging
**Reason:** While most of the `binlog.*` files are only 101M each, this quickly adds up when there are hundreds of files.

**Method:** 

**Impacted Files:**
- `setup-kg2-build.sh`
- `mysql-config.conf`

**Important Code Notes:** 

**Important Considerations for Maintainers:** Please note that this change occurs in `setup-kg2-build.sh`. This script only runs once, when an instance is being set up. Thus, if you are operating on an instance that has already been setup, you will have to manually add
```
[mysqld]
skip-log-bin
```
to your `mysql-config.conf` to prevent binary logging. Additionally, you should run the following commands:

This command will allow you to make changes to the `/var/lib/mysql` directory and run `du` there. (Warning: this enters you into superuser mode and you can do real damage with it):
```
sudo -i
```

This command takes you to where all of the MySQL data is stored on the instance:
```
cd /var/lib/mysql/
```

This command will show you all of the files that MySQL is keeping. If you have a binary logging issue, you will see many files that start with `binlog`:
```
ls
```

This command will show you the space taken up by each file MySQL is keeping: 
```
du -h *
```

This command will show you how much disk space the entire directory is taking up:
```
du -sh
```

This command will remove all of the binary logging files:
```
rm binlog.*
```

This command will show you how much disk space the entire directory is taking up. You should see a marked difference from the first time you execute this command:
```
du -sh
```

This command will take you out of superuser mode (ending the effects of the first command):
```
exit
```

**Relevant Commits:**
- [`ee3884f`](https://github.com/RTXteam/RTX-KG2/commit/ee3884ff47b0df3a17845b0f8cc1af8009189081)
- [`3c42962`](https://github.com/RTXteam/RTX-KG2/commit/3c42962f2bd14658a9c655945d43eb7bbec3de15)

**Relevant Issue Comments:** 
- [#336 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/336#issue-1827603175)

## Remove Code That Is No Longer In Use
**Reason:** 

**Method:** 

**Impacted Files:**
- `build-kg2-DEPRECATED.sh`
- `Snakefile-DEPRECATED.sh`
- `filter_kg_and_remap_predicates_DEPRECATED.sh`
- `predicate-remap_DEPRECATED.sh`
- `slim_kg2_DEPRECATED.sh`
- `Snakefile-semmeddb-extraction`
- `Snakefile-generate-nodes`
- `build-kg2-snakemake.sh`
- `Snakemake-finish`

**Important Code Notes:** 

**Important Considerations for Maintainers:** 

**Relevant Commits:**
- [`fa3bb43`](https://github.com/RTXteam/RTX-KG2/commit/fa3bb4312e1de887e1a7c7e115a0210ed98455ad)
- [`d76afc0`](https://github.com/RTXteam/RTX-KG2/commit/d76afc0cc9f20b3a1bc0467493c1e2815b88f599)
- [`da425af`](https://github.com/RTXteam/RTX-KG2/commit/da425afd272ece812a8f4fb21885c75a9bc69fff)
- [`639065e`](https://github.com/RTXteam/RTX-KG2/commit/639065e459fb157e6ce5332d40882de6f8962a5c)
- [`56341a8`](https://github.com/RTXteam/RTX-KG2/commit/56341a88b77b866e78f083ab5697891a68aef64a)

**Relevant Issue Comments:**
- [#323 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/323#issue-1808635632)
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1650689925)

## Memory Tracker
**Reason:** AWS offers many graphs that allow you to see instance activity. However, memory is not tracked by default and is quite challenging to set up. In order to assess the memory usage by this JSON Lines update, we needed a simple way to get memory usage at many different points in time.

**Method:** Everytime you log into an AWS instance, there is a dashboard with instance statistics, including memory and disk space usage. In addition to showing up on login, it can be accessed with the command `landscape-sysinfo`. Since this returns a predictable, text-based block, I opted to use `grep` to find the correct line in the block and `sed` to strip off all other information.

**Impacted Files:**
- `primative-instance-data-tracker.sh`

**Important Code Notes:** 

**Important Considerations for Maintainers:** The format that this script assumes for the return value of `landscape-sysinfo` is only guaranteed to be correct for the AWS EC2 Ubuntu 22.04 instances. On my personal, Ubuntu 20.04, laptop, the output of `landscape-sysinfo` looks slightly different and thus, the parsing that `primative-instance-data-tracker.sh` performs does not apply. If you are looking to test this file, make sure to do so on an AWS EC2 Ubuntu 22.04 instance.

**Relevant Commits:**
- [`4dab16b`](https://github.com/RTXteam/RTX-KG2/commit/4dab16b91a68d7b8ef32d036305b68fc5b00f930)
- [`886aebd`](https://github.com/RTXteam/RTX-KG2/commit/886aebd0783e51f94fcf4034dbd6fc9b5487cbac)
- [`e41f8e2`](https://github.com/RTXteam/RTX-KG2/commit/e41f8e29a8fe2c56305cc116c6392515e56464f6)

**Relevant Issue Comments:**
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1652691766)
- [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1657291102)

# Looking Forward

- [#316](https://github.com/RTXteam/RTX-KG2/issues/316)
- [#335](https://github.com/RTXteam/RTX-KG2/issues/335)
- [#337](https://github.com/RTXteam/RTX-KG2/issues/337)

# Appendix
## Snakemake Log File for JSON Lines Build
<details>

</details>

## Instance Data Tracker for JSON Lines Build
<details>

</details>

## Snakemake Log File for JSON Lines Build
<details>

</details>

## Instance Data Tracker for JSON Lines Build
<details>

</details>
