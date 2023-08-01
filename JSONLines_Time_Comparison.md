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

```
+ echo '================= starting build-kg2-snakemake.sh =================='
================= starting build-kg2-snakemake.sh ==================
+ date
Mon Jul 31 00:46:50 UTC 2023
+ snakemake_config_file=/home/ubuntu/kg2-code/snakemake-config.yaml
+ snakefile=/home/ubuntu/kg2-code/Snakefile
+ /home/ubuntu/kg2-venv/bin/python3 -u /home/ubuntu/kg2-code/generate_snakemake_config_file.py ./master-config.shinc /home/ubuntu/kg2-code/snakemake-config-var.yaml /home/ubuntu/kg2-code/snakemake-config.yaml
+ export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/ubuntu/kg2-build
+ PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/ubuntu/kg2-build
+ graphic=
+ [[ all == \g\r\a\p\h\i\c ]]
+ [[ -F == \g\r\a\p\h\i\c ]]
+ [[ '' == \g\r\a\p\h\i\c ]]
+ echo configfile: '"/home/ubuntu/kg2-code/snakemake-config.yaml"'
+ cat /home/ubuntu/kg2-code/Snakefile-finish
+ echo 'include: "Snakefile-pre-etl"'
+ echo 'include: "Snakefile-conversion"'
+ echo 'include: "Snakefile-post-etl"'
+ [[ all == \a\l\l ]]
+ echo 'include: "Snakefile-extraction"'
+ cd /home/ubuntu
+ /home/ubuntu/kg2-venv/bin/snakemake --snakefile /home/ubuntu/kg2-code/Snakefile -F -R Finish -j 16
Building DAG of jobs...
Using shell: /usr/bin/bash
Provided cores: 16
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	ChEMBL
	1	ChEMBL_Conversion
	1	DGIdb
	1	DGIdb_Conversion
	1	DisGeNET
	1	DisGeNET_Conversion
	1	DrugBank
	1	DrugBank_Conversion
	1	DrugCentral
	1	DrugCentral_Conversion
	1	Ensembl
	1	Ensembl_Conversion
	1	Finish
	1	GO_Annotations
	1	GO_Annotations_Conversion
	1	HMDB
	1	HMDB_Conversion
	1	IntAct
	1	IntAct_Conversion
	1	JensenLab
	1	JensenLab_Conversion
	1	KEGG
	1	KEGG_Conversion
	1	Merge
	1	NCBIGene
	1	NCBIGene_Conversion
	1	Ontologies_and_TTL
	1	Reactome
	1	Reactome_Conversion
	1	RepoDB
	1	RepoDB_Conversion
	1	SMPDB
	1	SMPDB_Conversion
	1	SemMedDB
	1	SemMedDB_Conversion
	1	Simplify
	1	Simplify_Stats
	1	Slim
	1	Stats
	1	TSV
	1	UMLS
	1	UniChem
	1	UniChem_Conversion
	1	UniProtKB
	1	UniProtKB_Conversion
	1	ValidationTests
	1	miRBase
	1	miRBase_Conversion
	48

[Mon Jul 31 00:46:51 2023]
rule ValidationTests:
    output: /home/ubuntu/kg2-build/validation-placeholder.empty
    log: /home/ubuntu/kg2-build/run-validation-tests.log
    jobid: 28

[Mon Jul 31 00:47:26 2023]
Finished job 28.
1 of 48 steps (2%) done

[Mon Jul 31 00:47:26 2023]
rule miRBase:
    input: /home/ubuntu/kg2-code/extract-mirbase.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/miRNA.dat
    log: /home/ubuntu/kg2-build/extract-mirbase.log
    jobid: 42


[Mon Jul 31 00:47:26 2023]
rule UniProtKB:
    input: /home/ubuntu/kg2-code/extract-uniprotkb.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/uniprotkb/uniprot_sprot.dat
    log: /home/ubuntu/kg2-build/extract-uniprotkb.log
    jobid: 29


[Mon Jul 31 00:47:26 2023]
rule DisGeNET:
    input: /home/ubuntu/kg2-code/extract-disgenet.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/all_gene_disease_pmid_associations.tsv
    log: /home/ubuntu/kg2-build/extract-disgenet.log
    jobid: 46


[Mon Jul 31 00:47:26 2023]
rule NCBIGene:
    input: /home/ubuntu/kg2-code/extract-ncbigene.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/ncbigene/Homo_sapiens_gene_info.tsv
    log: /home/ubuntu/kg2-build/extract-ncbigene.log
    jobid: 34


[Mon Jul 31 00:47:26 2023]
rule SMPDB:
    input: /home/ubuntu/kg2-code/extract-smpdb.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/smpdb/pathbank_pathways.csv
    log: /home/ubuntu/kg2-build/extract-smpdb.log
    jobid: 38


[Mon Jul 31 00:47:27 2023]
rule UMLS:
    input: /home/ubuntu/kg2-code/extract-umls.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/umls_cuis.tsv
    log: /home/ubuntu/kg2-build/extract-umls.log
    jobid: 27


[Mon Jul 31 00:47:27 2023]
rule ChEMBL:
    input: /home/ubuntu/kg2-code/extract-chembl.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/chembl-placeholder.empty
    log: /home/ubuntu/kg2-build/extract-chembl.log
    jobid: 31


[Mon Jul 31 00:47:27 2023]
rule Reactome:
    input: /home/ubuntu/kg2-code/extract-reactome.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/reactome-placeholder.empty
    log: /home/ubuntu/kg2-build/extract-reactome.log
    jobid: 41


[Mon Jul 31 00:47:27 2023]
rule SemMedDB:
    input: /home/ubuntu/kg2-code/extract-semmeddb.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/semmeddb-tuplelist.jsonl, /home/ubuntu/kg2-build/semmed-exclude-list.yaml, /home/ubuntu/kg2-build/semmeddb-version.txt
    log: /home/ubuntu/kg2-build/extract-semmeddb.log
    jobid: 30


[Mon Jul 31 00:47:27 2023]
rule DrugCentral:
    input: /home/ubuntu/kg2-code/extract-drugcentral.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/drugcentral/drugcentral_psql_json.json
    log: /home/ubuntu/kg2-build/extract-drugcentral.log
    jobid: 44


[Mon Jul 31 00:47:27 2023]
rule Ensembl:
    input: /home/ubuntu/kg2-code/extract-ensembl.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/ensembl/ensembl_genes_homo_sapiens.json
    log: /home/ubuntu/kg2-build/extract-ensembl.log
    jobid: 32


[Mon Jul 31 00:47:27 2023]
rule IntAct:
    input: /home/ubuntu/kg2-code/extract-intact.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/intact.txt
    log: /home/ubuntu/kg2-build/extract-intact.log
    jobid: 45


[Mon Jul 31 00:47:28 2023]
rule UniChem:
    input: /home/ubuntu/kg2-code/extract-unichem.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/unichem/unichem-mappings.tsv
    log: /home/ubuntu/kg2-build/extract-unichem.log
    jobid: 33


[Mon Jul 31 00:47:28 2023]
rule GO_Annotations:
    input: /home/ubuntu/kg2-code/extract-go-annotations.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/goa_human.gpa
    log: /home/ubuntu/kg2-build/extract-go-annotations.log
    jobid: 40


[Mon Jul 31 00:47:28 2023]
rule DGIdb:
    input: /home/ubuntu/kg2-code/extract-dgidb.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/dgidb/interactions.tsv
    log: /home/ubuntu/kg2-build/extract-dgidb.log
    jobid: 35


[Mon Jul 31 00:47:28 2023]
rule JensenLab:
    input: /home/ubuntu/kg2-code/extract-jensenlab.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/jensenlab-placeholder.empty
    log: /home/ubuntu/kg2-build/extract-jensenlab.log
    jobid: 43

[Mon Jul 31 00:47:28 2023]
Finished job 35.
2 of 48 steps (4%) done

[Mon Jul 31 00:47:28 2023]
rule DGIdb_Conversion:
    input: /home/ubuntu/kg2-code/dgidb_tsv_to_kg_jsonl.py, /home/ubuntu/kg2-build/dgidb/interactions.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-dgidb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-dgidb-edges.jsonl
    log: /home/ubuntu/kg2-build/dgidb_tsv_to_kg_jsonl.log
    jobid: 14

[Mon Jul 31 00:47:29 2023]
Finished job 34.
3 of 48 steps (6%) done

[Mon Jul 31 00:47:29 2023]
rule NCBIGene_Conversion:
    input: /home/ubuntu/kg2-code/ncbigene_tsv_to_kg_jsonl.py, /home/ubuntu/kg2-build/ncbigene/Homo_sapiens_gene_info.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-ncbigene-nodes.jsonl, /home/ubuntu/kg2-build/kg2-ncbigene-edges.jsonl
    log: /home/ubuntu/kg2-build/ncbigene_tsv_to_kg_jsonl.log
    jobid: 13

[Mon Jul 31 00:47:32 2023]
Finished job 40.
4 of 48 steps (8%) done

[Mon Jul 31 00:47:32 2023]
rule GO_Annotations_Conversion:
    input: /home/ubuntu/kg2-code/go_gpa_to_kg_jsonl.py, /home/ubuntu/kg2-build/goa_human.gpa, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-go-annotations-nodes.jsonl, /home/ubuntu/kg2-build/kg2-go-annotations-edges.jsonl
    log: /home/ubuntu/kg2-build/go_gpa_to_kg_jsonl.log
    jobid: 19

[Mon Jul 31 00:47:34 2023]
Finished job 14.
5 of 48 steps (10%) done

[Mon Jul 31 00:47:34 2023]
rule DrugBank:
    input: /home/ubuntu/kg2-code/extract-drugbank.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/drugbank.xml
    log: /home/ubuntu/kg2-build/extract-drugbank.log
    jobid: 37

[Mon Jul 31 00:47:34 2023]
Finished job 46.
6 of 48 steps (12%) done

[Mon Jul 31 00:47:34 2023]
rule DisGeNET_Conversion:
    input: /home/ubuntu/kg2-code/disgenet_tsv_to_kg_jsonl.py, /home/ubuntu/kg2-build/all_gene_disease_pmid_associations.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-disgenet-nodes.jsonl, /home/ubuntu/kg2-build/kg2-disgenet-edges.jsonl
    log: /home/ubuntu/kg2-build/disgenet_tsv_to_kg_jsonl.log
    jobid: 25

[Mon Jul 31 00:47:39 2023]
Finished job 42.
7 of 48 steps (15%) done

[Mon Jul 31 00:47:39 2023]
rule miRBase_Conversion:
    input: /home/ubuntu/kg2-code/mirbase_dat_to_kg_jsonl.py, /home/ubuntu/kg2-build/miRNA.dat, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-mirbase-nodes.jsonl, /home/ubuntu/kg2-build/kg2-mirbase-edges.jsonl
    log: /home/ubuntu/kg2-build/mirbase_dat_to_kg_jsonl.log
    jobid: 21

[Mon Jul 31 00:47:45 2023]
Finished job 21.
8 of 48 steps (17%) done

[Mon Jul 31 00:47:45 2023]
rule HMDB:
    input: /home/ubuntu/kg2-code/extract-hmdb.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/hmdb_metabolites.xml
    log: /home/ubuntu/kg2-build/extract-hmdb.log
    jobid: 39

[Mon Jul 31 00:47:47 2023]
Finished job 13.
9 of 48 steps (19%) done

[Mon Jul 31 00:47:47 2023]
rule KEGG:
    input: /home/ubuntu/kg2-code/extract-kegg.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kegg.jsonl
    log: /home/ubuntu/kg2-build/extract-kegg.log
    jobid: 47

[Mon Jul 31 00:47:48 2023]
Finished job 37.
10 of 48 steps (21%) done

[Mon Jul 31 00:47:48 2023]
rule DrugBank_Conversion:
    input: /home/ubuntu/kg2-code/drugbank_xml_to_kg_jsonl.py, /home/ubuntu/kg2-build/drugbank.xml, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-drugbank-nodes.jsonl, /home/ubuntu/kg2-build/kg2-drugbank-edges.jsonl
    log: /home/ubuntu/kg2-build/drugbank_xml_to_kg_jsonl.log
    jobid: 16

[Mon Jul 31 00:47:52 2023]
Finished job 19.
11 of 48 steps (23%) done

[Mon Jul 31 00:47:52 2023]
rule RepoDB:
    input: /home/ubuntu/kg2-code/extract-repodb.sh, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/repodb/repodb.csv
    log: /home/ubuntu/kg2-build/extract-repodb.log
    jobid: 36

[Mon Jul 31 00:47:53 2023]
Finished job 36.
12 of 48 steps (25%) done

[Mon Jul 31 00:47:53 2023]
rule RepoDB_Conversion:
    input: /home/ubuntu/kg2-code/repodb_csv_to_kg_jsonl.py, /home/ubuntu/kg2-build/repodb/repodb.csv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-repodb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-repodb-edges.jsonl
    log: /home/ubuntu/kg2-build/repodb_csv_to_kg_jsonl.log
    jobid: 15

[Mon Jul 31 00:48:05 2023]
Finished job 25.
13 of 48 steps (27%) done
[Mon Jul 31 00:48:20 2023]
Finished job 15.
14 of 48 steps (29%) done
[Mon Jul 31 00:48:53 2023]
Finished job 45.
15 of 48 steps (31%) done

[Mon Jul 31 00:48:53 2023]
rule IntAct_Conversion:
    input: /home/ubuntu/kg2-code/intact_tsv_to_kg_jsonl.py, /home/ubuntu/kg2-build/intact.txt, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-intact-nodes.jsonl, /home/ubuntu/kg2-build/kg2-intact-edges.jsonl
    log: /home/ubuntu/kg2-build/intact_tsv_to_kg_jsonl.log
    jobid: 24

[Mon Jul 31 00:49:39 2023]
Finished job 24.
16 of 48 steps (33%) done
[Mon Jul 31 00:50:50 2023]
Finished job 39.
17 of 48 steps (35%) done

[Mon Jul 31 00:50:50 2023]
rule HMDB_Conversion:
    input: /home/ubuntu/kg2-code/hmdb_xml_to_kg_jsonl.py, /home/ubuntu/kg2-build/hmdb_metabolites.xml, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-hmdb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-hmdb-edges.jsonl
    log: /home/ubuntu/kg2-build/hmdb_xml_to_kg_jsonl.log
    jobid: 18

[Mon Jul 31 00:51:33 2023]
Finished job 32.
18 of 48 steps (38%) done

[Mon Jul 31 00:51:33 2023]
rule Ensembl_Conversion:
    input: /home/ubuntu/kg2-code/ensembl_json_to_kg_jsonl.py, /home/ubuntu/kg2-build/ensembl/ensembl_genes_homo_sapiens.json, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-ensembl-nodes.jsonl, /home/ubuntu/kg2-build/kg2-ensembl-edges.jsonl
    log: /home/ubuntu/kg2-build/ensembl_json_to_kg_jsonl.log
    jobid: 11

[Mon Jul 31 00:51:49 2023]
Finished job 44.
19 of 48 steps (40%) done

[Mon Jul 31 00:51:49 2023]
rule DrugCentral_Conversion:
    input: /home/ubuntu/kg2-code/drugcentral_json_to_kg_jsonl.py, /home/ubuntu/kg2-build/drugcentral/drugcentral_psql_json.json, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-drugcentral-nodes.jsonl, /home/ubuntu/kg2-build/kg2-drugcentral-edges.jsonl
    log: /home/ubuntu/kg2-build/drugcentral_json_to_kg_jsonl.log
    jobid: 23

[Mon Jul 31 00:52:06 2023]
Finished job 23.
20 of 48 steps (42%) done
[Mon Jul 31 00:54:38 2023]
Finished job 16.
21 of 48 steps (44%) done
[Mon Jul 31 00:54:44 2023]
Finished job 11.
22 of 48 steps (46%) done
[Mon Jul 31 00:55:03 2023]
Finished job 41.
23 of 48 steps (48%) done

[Mon Jul 31 00:55:03 2023]
rule Reactome_Conversion:
    input: /home/ubuntu/kg2-code/reactome_mysql_to_kg_jsonl.py, /home/ubuntu/kg2-build/reactome-placeholder.empty, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-reactome-nodes.jsonl, /home/ubuntu/kg2-build/kg2-reactome-edges.jsonl
    log: /home/ubuntu/kg2-build/reactome_mysql_to_kg_jsonl.log
    jobid: 20

[Mon Jul 31 00:56:44 2023]
Finished job 20.
24 of 48 steps (50%) done
[Mon Jul 31 00:57:29 2023]
Finished job 43.
25 of 48 steps (52%) done

[Mon Jul 31 00:57:29 2023]
rule JensenLab_Conversion:
    input: /home/ubuntu/kg2-code/jensenlab_tsv_to_kg_jsonl.py, /home/ubuntu/kg2-build/validation-placeholder.empty, /home/ubuntu/kg2-build/jensenlab-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-jensenlab-nodes.jsonl, /home/ubuntu/kg2-build/kg2-jensenlab-edges.jsonl
    log: /home/ubuntu/kg2-build/jensenlab_tsv_to_kg_jsonl.log
    jobid: 22

[Mon Jul 31 01:03:05 2023]
Finished job 33.
26 of 48 steps (54%) done

[Mon Jul 31 01:03:05 2023]
rule UniChem_Conversion:
    input: /home/ubuntu/kg2-code/unichem_tsv_to_kg_jsonl.py, /home/ubuntu/kg2-build/unichem/unichem-mappings.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-unichem-nodes.jsonl, /home/ubuntu/kg2-build/kg2-unichem-edges.jsonl
    log: /home/ubuntu/kg2-build/unichem_tsv_to_kg_jsonl.log
    jobid: 12

[Mon Jul 31 01:03:15 2023]
Finished job 12.
27 of 48 steps (56%) done
[Mon Jul 31 01:05:05 2023]
Finished job 38.
28 of 48 steps (58%) done

[Mon Jul 31 01:05:05 2023]
rule SMPDB_Conversion:
    input: /home/ubuntu/kg2-code/smpdb_csv_to_kg_jsonl.py, /home/ubuntu/kg2-build/smpdb/pathbank_pathways.csv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-smpdb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-smpdb-edges.jsonl
    log: /home/ubuntu/kg2-build/smpdb_csv_to_kg_jsonl.log
    jobid: 17

[Mon Jul 31 01:14:16 2023]
Finished job 18.
29 of 48 steps (60%) done
[Mon Jul 31 01:17:27 2023]
Finished job 22.
30 of 48 steps (62%) done
[Mon Jul 31 01:25:44 2023]
Finished job 29.
31 of 48 steps (65%) done

[Mon Jul 31 01:25:44 2023]
rule UniProtKB_Conversion:
    input: /home/ubuntu/kg2-code/uniprotkb_dat_to_kg_jsonl.py, /home/ubuntu/kg2-build/uniprotkb/uniprot_sprot.dat, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-uniprotkb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-uniprotkb-edges.jsonl
    log: /home/ubuntu/kg2-build/uniprotkb_dat_to_kg_jsonl.log
    jobid: 8

[Mon Jul 31 01:28:50 2023]
Finished job 8.
32 of 48 steps (67%) done
[Mon Jul 31 03:49:44 2023]
Finished job 17.
33 of 48 steps (69%) done
[Mon Jul 31 05:06:44 2023]
Finished job 31.
34 of 48 steps (71%) done

[Mon Jul 31 05:06:44 2023]
rule ChEMBL_Conversion:
    input: /home/ubuntu/kg2-code/chembl_mysql_to_kg_jsonl.py, /home/ubuntu/kg2-build/chembl-placeholder.empty, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-chembl-nodes.jsonl, /home/ubuntu/kg2-build/kg2-chembl-edges.jsonl
    log: /home/ubuntu/kg2-build/chembl_mysql_to_kg_jsonl.log
    jobid: 10

[Mon Jul 31 05:29:39 2023]
Finished job 47.
35 of 48 steps (73%) done

[Mon Jul 31 05:29:39 2023]
rule KEGG_Conversion:
    input: /home/ubuntu/kg2-code/kegg_jsonl_to_kg_jsonl.py, /home/ubuntu/kg2-build/kegg.jsonl, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-kegg-nodes.jsonl, /home/ubuntu/kg2-build/kg2-kegg-edges.jsonl
    log: /home/ubuntu/kg2-build/kegg_jsonl_to_kg_jsonl.log
    jobid: 26

[Mon Jul 31 05:29:59 2023]
Finished job 26.
36 of 48 steps (75%) done
[Mon Jul 31 05:35:52 2023]
Finished job 10.
37 of 48 steps (77%) done
[Mon Jul 31 06:31:24 2023]
Finished job 27.
38 of 48 steps (79%) done

[Mon Jul 31 06:31:24 2023]
rule Ontologies_and_TTL:
    input: /home/ubuntu/kg2-code/build-multi-ont-kg.sh, /home/ubuntu/kg2-build/umls_cuis.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-ont-nodes.jsonl, /home/ubuntu/kg2-build/kg2-ont-edges.jsonl
    log: /home/ubuntu/kg2-build/build-multi-ont-kg.log
    jobid: 7

[Mon Jul 31 12:02:08 2023]
Finished job 30.
39 of 48 steps (81%) done

[Mon Jul 31 12:02:08 2023]
rule SemMedDB_Conversion:
    input: /home/ubuntu/kg2-code/semmeddb_tuplelist_json_to_kg_jsonl.py, /home/ubuntu/kg2-build/semmeddb-tuplelist.jsonl, /home/ubuntu/kg2-build/umls_cuis.tsv, /home/ubuntu/kg2-build/semmed-exclude-list.yaml, /home/ubuntu/kg2-build/semmeddb-version.txt, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-semmeddb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-semmeddb-edges.jsonl
    log: /home/ubuntu/kg2-build/semmeddb_tuplelist_json_to_kg_jsonl.log
    jobid: 9

[Mon Jul 31 12:39:07 2023]
Finished job 9.
40 of 48 steps (83%) done
[Mon Jul 31 13:24:18 2023]
Finished job 7.
41 of 48 steps (85%) done

[Mon Jul 31 13:24:18 2023]
rule Merge:
    input: /home/ubuntu/kg2-code/merge_graphs.py, /home/ubuntu/kg2-build/kg2-ont-nodes.jsonl, /home/ubuntu/kg2-build/kg2-ont-edges.jsonl, /home/ubuntu/kg2-build/kg2-uniprotkb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-uniprotkb-edges.jsonl, /home/ubuntu/kg2-build/kg2-semmeddb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-semmeddb-edges.jsonl, /home/ubuntu/kg2-build/kg2-chembl-nodes.jsonl, /home/ubuntu/kg2-build/kg2-chembl-edges.jsonl, /home/ubuntu/kg2-build/kg2-ensembl-nodes.jsonl, /home/ubuntu/kg2-build/kg2-ensembl-edges.jsonl, /home/ubuntu/kg2-build/kg2-unichem-nodes.jsonl, /home/ubuntu/kg2-build/kg2-unichem-edges.jsonl, /home/ubuntu/kg2-build/kg2-ncbigene-nodes.jsonl, /home/ubuntu/kg2-build/kg2-ncbigene-edges.jsonl, /home/ubuntu/kg2-build/kg2-dgidb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-dgidb-edges.jsonl, /home/ubuntu/kg2-build/kg2-repodb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-repodb-edges.jsonl, /home/ubuntu/kg2-build/kg2-drugbank-nodes.jsonl, /home/ubuntu/kg2-build/kg2-drugbank-edges.jsonl, /home/ubuntu/kg2-build/kg2-smpdb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-smpdb-edges.jsonl, /home/ubuntu/kg2-build/kg2-hmdb-nodes.jsonl, /home/ubuntu/kg2-build/kg2-hmdb-edges.jsonl, /home/ubuntu/kg2-build/kg2-go-annotations-nodes.jsonl, /home/ubuntu/kg2-build/kg2-go-annotations-edges.jsonl, /home/ubuntu/kg2-build/kg2-reactome-nodes.jsonl, /home/ubuntu/kg2-build/kg2-reactome-edges.jsonl, /home/ubuntu/kg2-build/kg2-mirbase-nodes.jsonl, /home/ubuntu/kg2-build/kg2-mirbase-edges.jsonl, /home/ubuntu/kg2-build/kg2-jensenlab-nodes.jsonl, /home/ubuntu/kg2-build/kg2-jensenlab-edges.jsonl, /home/ubuntu/kg2-build/kg2-drugcentral-nodes.jsonl, /home/ubuntu/kg2-build/kg2-drugcentral-edges.jsonl, /home/ubuntu/kg2-build/kg2-intact-nodes.jsonl, /home/ubuntu/kg2-build/kg2-intact-edges.jsonl, /home/ubuntu/kg2-build/kg2-disgenet-nodes.jsonl, /home/ubuntu/kg2-build/kg2-disgenet-edges.jsonl, /home/ubuntu/kg2-build/kg2-kegg-nodes.jsonl, /home/ubuntu/kg2-build/kg2-kegg-edges.jsonl
    output: /home/ubuntu/kg2-build/kg2-merged-nodes.jsonl, /home/ubuntu/kg2-build/kg2-merged-edges.jsonl, /home/ubuntu/kg2-build/kg2-orphan-edges.jsonl
    log: /home/ubuntu/kg2-build/merge_graphs.log
    jobid: 1

[Mon Jul 31 21:54:19 2023]
Finished job 1.
42 of 48 steps (88%) done

[Mon Jul 31 21:54:19 2023]
rule Stats:
    input: /home/ubuntu/kg2-code/report_stats_on_kg_jsonl.py, /home/ubuntu/kg2-build/kg2-merged-nodes.jsonl, /home/ubuntu/kg2-build/kg2-merged-edges.jsonl
    output: /home/ubuntu/kg2-build/kg2-report.json
    log: /home/ubuntu/kg2-build/report_stats_on_kg_jsonl.log
    jobid: 2


[Mon Jul 31 21:54:19 2023]
rule Simplify:
    input: /home/ubuntu/kg2-code/run-simplify.sh, /home/ubuntu/kg2-build/kg2-merged-nodes.jsonl, /home/ubuntu/kg2-build/kg2-merged-edges.jsonl
    output: /home/ubuntu/kg2-build/kg2-simplified-nodes.jsonl, /home/ubuntu/kg2-build/kg2-simplified-edges.jsonl
    log: /home/ubuntu/kg2-build/run-simplify.log
    jobid: 3

[Mon Jul 31 22:14:38 2023]
Finished job 2.
43 of 48 steps (90%) done
[Mon Jul 31 22:46:55 2023]
Finished job 3.
44 of 48 steps (92%) done

[Mon Jul 31 22:46:55 2023]
rule Slim:
    input: /home/ubuntu/kg2-code/slim_kg2.py, /home/ubuntu/kg2-build/kg2-simplified-nodes.jsonl, /home/ubuntu/kg2-build/kg2-simplified-edges.jsonl
    output: /home/ubuntu/kg2-build/kg2-slim-nodes.jsonl, /home/ubuntu/kg2-build/kg2-slim-edges.jsonl
    log: /home/ubuntu/kg2-build/slim_kg2.log
    jobid: 5


[Mon Jul 31 22:46:55 2023]
rule TSV:
    input: /home/ubuntu/kg2-code/kg_json_to_tsv.py, /home/ubuntu/kg2-build/kg2-simplified-nodes.jsonl, /home/ubuntu/kg2-build/kg2-simplified-edges.jsonl, /home/ubuntu/kg2-code/kg2-provided-by-curie-to-infores-curie.yaml
    output: /home/ubuntu/kg2-build/tsv_placeholder.empty
    log: /home/ubuntu/kg2-build/kg_json_to_tsv.log
    jobid: 6

[Mon Jul 31 22:46:55 2023]
rule Simplify_Stats:
    input: /home/ubuntu/kg2-code/report_stats_on_kg_jsonl.py, /home/ubuntu/kg2-build/kg2-simplified-nodes.jsonl, /home/ubuntu/kg2-build/kg2-simplified-edges.jsonl
    output: /home/ubuntu/kg2-build/kg2-simplified-report.json
    log: /home/ubuntu/kg2-build/report_stats_on_kg_jsonl-simplified.log
    jobid: 4

Job counts:
	count	jobs
	1	TSV
	1
[Mon Jul 31 23:06:32 2023]
Finished job 4.
45 of 48 steps (94%) done
[Mon Jul 31 23:15:53 2023]
Finished job 5.
46 of 48 steps (96%) done
[Mon Jul 31 23:51:40 2023]
Finished job 6.
47 of 48 steps (98%) done

[Mon Jul 31 23:51:40 2023]
rule Finish:
    input: /home/ubuntu/kg2-build/kg2-merged-nodes.jsonl, /home/ubuntu/kg2-build/kg2-merged-edges.jsonl, /home/ubuntu/kg2-build/kg2-orphan-edges.jsonl, /home/ubuntu/kg2-build/kg2-report.json, /home/ubuntu/kg2-build/kg2-simplified-nodes.jsonl, /home/ubuntu/kg2-build/kg2-simplified-edges.jsonl, /home/ubuntu/kg2-build/kg2-simplified-report.json, /home/ubuntu/kg2-build/kg2-slim-nodes.jsonl, /home/ubuntu/kg2-build/kg2-slim-edges.jsonl, /home/ubuntu/kg2-build/tsv_placeholder.empty
    jobid: 0

+ [[ /home/ubuntu/kg2-build/kg2-merged-nodes.jsonl == \-\-\h\e\l\p ]]
+ [[ /home/ubuntu/kg2-build/kg2-merged-nodes.jsonl == \-\h ]]
+ final_output_nodes_file_full=/home/ubuntu/kg2-build/kg2-merged-nodes.jsonl
+ final_output_edges_file_full=/home/ubuntu/kg2-build/kg2-merged-edges.jsonl
+ output_file_orphan_edges=/home/ubuntu/kg2-build/kg2-orphan-edges.jsonl
+ report_file_full=/home/ubuntu/kg2-build/kg2-report.json
+ simplified_output_nodes_file_full=/home/ubuntu/kg2-build/kg2-simplified-nodes.jsonl
+ simplified_output_edges_file_full=/home/ubuntu/kg2-build/kg2-simplified-edges.jsonl
+ simplified_report_file_full=/home/ubuntu/kg2-build/kg2-simplified-report.json
+ slim_output_nodes_file_full=/home/ubuntu/kg2-build/kg2-slim-nodes.jsonl
+ slim_output_edges_file_full=/home/ubuntu/kg2-build/kg2-slim-edges.jsonl
+ kg2_tsv_dir=/home/ubuntu/kg2-build/TSV
+ s3_cp_cmd='aws s3 cp --no-progress --region us-west-2'
+ kg2_tsv_tarball=/home/ubuntu/kg2-build/kg2-tsv-for-neo4j.tar.gz
+ s3_bucket=rtx-kg2
+ s3_bucket_public=rtx-kg2-public
+ CODE_DIR=/home/ubuntu/kg2-code
+ s3_bucket_versioned=rtx-kg2-versioned
+ BUILD_DIR=/home/ubuntu/kg2-build
+ simplified_report_file_base=kg2-simplified-report.json
+ VENV_DIR=/home/ubuntu/kg2-venv
+ previous_simplified_report_base=previous-kg2-simplified-report.json
+ echo '================= starting finish-snakemake.sh =================='
================= starting finish-snakemake.sh ==================
+ date
Mon Jul 31 23:51:40 UTC 2023
+ gzip -fk /home/ubuntu/kg2-build/kg2-merged-nodes.jsonl
+ gzip -fk /home/ubuntu/kg2-build/kg2-merged-edges.jsonl
+ tar -C /home/ubuntu/kg2-build/TSV -czvf /home/ubuntu/kg2-build/kg2-tsv-for-neo4j.tar.gz nodes.tsv nodes_header.tsv edges.tsv edges_header.tsv
nodes.tsv
nodes_header.tsv
edges.tsv
edges_header.tsv
+ gzip -fk /home/ubuntu/kg2-build/kg2-simplified-nodes.jsonl
+ gzip -fk /home/ubuntu/kg2-build/kg2-simplified-edges.jsonl
+ gzip -fk /home/ubuntu/kg2-build/kg2-orphan-edges.jsonl
+ gzip -fk /home/ubuntu/kg2-build/kg2-slim-nodes.jsonl
+ gzip -fk /home/ubuntu/kg2-build/kg2-slim-edges.jsonl
+ aws s3 cp --no-progress --region us-west-2 s3://rtx-kg2-public/kg2-simplified-report.json /home/ubuntu/kg2-build/previous-kg2-simplified-report.json
download: s3://rtx-kg2-public/kg2-simplified-report.json to kg2-build/previous-kg2-simplified-report.json
+ '[' 0 -eq 0 ']'
+ /home/ubuntu/kg2-venv/bin/python3 -u /home/ubuntu/kg2-code/compare_edge_reports.py /home/ubuntu/kg2-build/previous-kg2-simplified-report.json /home/ubuntu/kg2-build/kg2-simplified-report.json
/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
+ date
Tue Aug  1 01:14:19 UTC 2023
+ echo '================ script finished ============================'
================ script finished ============================
[Tue Aug  1 01:14:19 2023]
Finished job 0.
48 of 48 steps (100%) done
Complete log: /home/ubuntu/.snakemake/log/2023-07-31T004651.281522.snakemake.log
+ date
Tue Aug  1 01:14:19 UTC 2023
+ echo '================ script finished ============================'
================ script finished ============================
```
</details>

## Instance Data Tracker for JSON Lines Build
<details>

```
================= starting primative-instance-data-tracker.sh =================
Time: 2023-07-31-00-46-36; Memory: 0%; Disk: 52.4% of 991.28GB
Time: 2023-07-31-00-47-37; Memory: 0%; Disk: 45.9% of 991.28GB
Time: 2023-07-31-00-48-38; Memory: 3%; Disk: 47.8% of 991.28GB
Time: 2023-07-31-00-49-39; Memory: 4%; Disk: 50.4% of 991.28GB
Time: 2023-07-31-00-50-40; Memory: 4%; Disk: 51.8% of 991.28GB
Time: 2023-07-31-00-51-41; Memory: 13%; Disk: 52.1% of 991.28GB
Time: 2023-07-31-00-52-42; Memory: 18%; Disk: 53.2% of 991.28GB
Time: 2023-07-31-00-53-43; Memory: 19%; Disk: 54.9% of 991.28GB
Time: 2023-07-31-00-54-44; Memory: 10%; Disk: 53.7% of 991.28GB
Time: 2023-07-31-00-55-45; Memory: 11%; Disk: 54.6% of 991.28GB
Time: 2023-07-31-00-56-46; Memory: 11%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-00-57-47; Memory: 13%; Disk: 56.0% of 991.28GB
Time: 2023-07-31-00-58-47; Memory: 18%; Disk: 56.9% of 991.28GB
Time: 2023-07-31-00-59-48; Memory: 22%; Disk: 57.8% of 991.28GB
Time: 2023-07-31-01-00-49; Memory: 22%; Disk: 57.8% of 991.28GB
Time: 2023-07-31-01-01-50; Memory: 22%; Disk: 55.1% of 991.28GB
Time: 2023-07-31-01-02-51; Memory: 23%; Disk: 49.7% of 991.28GB
Time: 2023-07-31-01-03-52; Memory: 23%; Disk: 48.9% of 991.28GB
Time: 2023-07-31-01-04-53; Memory: 24%; Disk: 48.0% of 991.28GB
Time: 2023-07-31-01-05-54; Memory: 24%; Disk: 45.8% of 991.28GB
Time: 2023-07-31-01-06-55; Memory: 25%; Disk: 45.9% of 991.28GB
Time: 2023-07-31-01-07-56; Memory: 25%; Disk: 46.0% of 991.28GB
Time: 2023-07-31-01-08-57; Memory: 26%; Disk: 46.0% of 991.28GB
Time: 2023-07-31-01-09-58; Memory: 26%; Disk: 46.1% of 991.28GB
Time: 2023-07-31-01-10-59; Memory: 27%; Disk: 46.2% of 991.28GB
Time: 2023-07-31-01-11-59; Memory: 19%; Disk: 46.3% of 991.28GB
Time: 2023-07-31-01-13-00; Memory: 20%; Disk: 46.5% of 991.28GB
Time: 2023-07-31-01-14-01; Memory: 20%; Disk: 46.6% of 991.28GB
Time: 2023-07-31-01-15-02; Memory: 11%; Disk: 46.7% of 991.28GB
Time: 2023-07-31-01-16-03; Memory: 11%; Disk: 46.7% of 991.28GB
Time: 2023-07-31-01-17-04; Memory: 11%; Disk: 46.8% of 991.28GB
Time: 2023-07-31-01-18-05; Memory: 3%; Disk: 46.9% of 991.28GB
Time: 2023-07-31-01-19-06; Memory: 3%; Disk: 46.9% of 991.28GB
Time: 2023-07-31-01-20-07; Memory: 3%; Disk: 47.0% of 991.28GB
Time: 2023-07-31-01-21-08; Memory: 3%; Disk: 47.1% of 991.28GB
Time: 2023-07-31-01-22-09; Memory: 3%; Disk: 47.1% of 991.28GB
Time: 2023-07-31-01-23-09; Memory: 3%; Disk: 47.2% of 991.28GB
Time: 2023-07-31-01-24-10; Memory: 3%; Disk: 47.3% of 991.28GB
Time: 2023-07-31-01-25-11; Memory: 3%; Disk: 47.5% of 991.28GB
Time: 2023-07-31-01-26-12; Memory: 3%; Disk: 48.1% of 991.28GB
Time: 2023-07-31-01-27-13; Memory: 3%; Disk: 48.2% of 991.28GB
Time: 2023-07-31-01-28-14; Memory: 3%; Disk: 48.3% of 991.28GB
Time: 2023-07-31-01-29-15; Memory: 3%; Disk: 48.3% of 991.28GB
Time: 2023-07-31-01-30-16; Memory: 3%; Disk: 48.4% of 991.28GB
Time: 2023-07-31-01-31-17; Memory: 3%; Disk: 48.5% of 991.28GB
Time: 2023-07-31-01-32-18; Memory: 3%; Disk: 48.5% of 991.28GB
Time: 2023-07-31-01-33-18; Memory: 3%; Disk: 48.6% of 991.28GB
Time: 2023-07-31-01-34-19; Memory: 3%; Disk: 48.7% of 991.28GB
Time: 2023-07-31-01-35-20; Memory: 3%; Disk: 48.8% of 991.28GB
Time: 2023-07-31-01-36-21; Memory: 3%; Disk: 48.8% of 991.28GB
Time: 2023-07-31-01-37-22; Memory: 3%; Disk: 48.9% of 991.28GB
Time: 2023-07-31-01-38-23; Memory: 3%; Disk: 48.9% of 991.28GB
Time: 2023-07-31-01-39-24; Memory: 3%; Disk: 49.0% of 991.28GB
Time: 2023-07-31-01-40-25; Memory: 3%; Disk: 49.1% of 991.28GB
Time: 2023-07-31-01-41-26; Memory: 3%; Disk: 49.1% of 991.28GB
Time: 2023-07-31-01-42-27; Memory: 3%; Disk: 49.2% of 991.28GB
Time: 2023-07-31-01-43-27; Memory: 3%; Disk: 49.3% of 991.28GB
Time: 2023-07-31-01-44-28; Memory: 3%; Disk: 49.3% of 991.28GB
Time: 2023-07-31-01-45-29; Memory: 3%; Disk: 49.4% of 991.28GB
Time: 2023-07-31-01-46-30; Memory: 3%; Disk: 49.5% of 991.28GB
Time: 2023-07-31-01-47-31; Memory: 3%; Disk: 49.5% of 991.28GB
Time: 2023-07-31-01-48-32; Memory: 3%; Disk: 49.6% of 991.28GB
Time: 2023-07-31-01-49-33; Memory: 3%; Disk: 49.6% of 991.28GB
Time: 2023-07-31-01-50-34; Memory: 3%; Disk: 49.7% of 991.28GB
Time: 2023-07-31-01-51-34; Memory: 3%; Disk: 49.8% of 991.28GB
Time: 2023-07-31-01-52-35; Memory: 3%; Disk: 49.8% of 991.28GB
Time: 2023-07-31-01-53-36; Memory: 3%; Disk: 49.9% of 991.28GB
Time: 2023-07-31-01-54-37; Memory: 3%; Disk: 49.9% of 991.28GB
Time: 2023-07-31-01-55-38; Memory: 3%; Disk: 50.0% of 991.28GB
Time: 2023-07-31-01-56-39; Memory: 3%; Disk: 50.1% of 991.28GB
Time: 2023-07-31-01-57-40; Memory: 3%; Disk: 50.1% of 991.28GB
Time: 2023-07-31-01-58-41; Memory: 3%; Disk: 50.2% of 991.28GB
Time: 2023-07-31-01-59-42; Memory: 3%; Disk: 50.2% of 991.28GB
Time: 2023-07-31-02-00-42; Memory: 3%; Disk: 50.3% of 991.28GB
Time: 2023-07-31-02-01-43; Memory: 3%; Disk: 50.4% of 991.28GB
Time: 2023-07-31-02-02-44; Memory: 3%; Disk: 50.4% of 991.28GB
Time: 2023-07-31-02-03-45; Memory: 3%; Disk: 50.5% of 991.28GB
Time: 2023-07-31-02-04-46; Memory: 3%; Disk: 50.6% of 991.28GB
Time: 2023-07-31-02-05-47; Memory: 3%; Disk: 50.5% of 991.28GB
Time: 2023-07-31-02-06-48; Memory: 3%; Disk: 50.6% of 991.28GB
Time: 2023-07-31-02-07-49; Memory: 3%; Disk: 50.6% of 991.28GB
Time: 2023-07-31-02-08-49; Memory: 3%; Disk: 50.7% of 991.28GB
Time: 2023-07-31-02-09-50; Memory: 3%; Disk: 50.8% of 991.28GB
Time: 2023-07-31-02-10-51; Memory: 3%; Disk: 50.8% of 991.28GB
Time: 2023-07-31-02-11-52; Memory: 3%; Disk: 50.9% of 991.28GB
Time: 2023-07-31-02-12-53; Memory: 3%; Disk: 50.9% of 991.28GB
Time: 2023-07-31-02-13-54; Memory: 3%; Disk: 51.0% of 991.28GB
Time: 2023-07-31-02-14-55; Memory: 3%; Disk: 51.0% of 991.28GB
Time: 2023-07-31-02-15-56; Memory: 3%; Disk: 51.1% of 991.28GB
Time: 2023-07-31-02-16-57; Memory: 3%; Disk: 51.1% of 991.28GB
Time: 2023-07-31-02-17-57; Memory: 3%; Disk: 51.2% of 991.28GB
Time: 2023-07-31-02-18-58; Memory: 3%; Disk: 51.3% of 991.28GB
Time: 2023-07-31-02-19-59; Memory: 3%; Disk: 51.3% of 991.28GB
Time: 2023-07-31-02-21-00; Memory: 3%; Disk: 51.4% of 991.28GB
Time: 2023-07-31-02-22-01; Memory: 3%; Disk: 51.4% of 991.28GB
Time: 2023-07-31-02-23-02; Memory: 3%; Disk: 51.5% of 991.28GB
Time: 2023-07-31-02-24-03; Memory: 3%; Disk: 51.5% of 991.28GB
Time: 2023-07-31-02-25-04; Memory: 3%; Disk: 51.6% of 991.28GB
Time: 2023-07-31-02-26-05; Memory: 3%; Disk: 51.6% of 991.28GB
Time: 2023-07-31-02-27-06; Memory: 3%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-02-28-06; Memory: 3%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-02-29-07; Memory: 3%; Disk: 51.8% of 991.28GB
Time: 2023-07-31-02-30-08; Memory: 3%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-02-31-09; Memory: 3%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-02-32-10; Memory: 3%; Disk: 52.0% of 991.28GB
Time: 2023-07-31-02-33-11; Memory: 3%; Disk: 52.0% of 991.28GB
Time: 2023-07-31-02-34-12; Memory: 3%; Disk: 52.1% of 991.28GB
Time: 2023-07-31-02-35-13; Memory: 3%; Disk: 52.1% of 991.28GB
Time: 2023-07-31-02-36-14; Memory: 3%; Disk: 52.2% of 991.28GB
Time: 2023-07-31-02-37-14; Memory: 3%; Disk: 52.3% of 991.28GB
Time: 2023-07-31-02-38-15; Memory: 3%; Disk: 52.3% of 991.28GB
Time: 2023-07-31-02-39-16; Memory: 3%; Disk: 52.4% of 991.28GB
Time: 2023-07-31-02-40-17; Memory: 4%; Disk: 52.4% of 991.28GB
Time: 2023-07-31-02-41-18; Memory: 4%; Disk: 52.5% of 991.28GB
Time: 2023-07-31-02-42-19; Memory: 4%; Disk: 52.7% of 991.28GB
Time: 2023-07-31-02-43-20; Memory: 4%; Disk: 53.0% of 991.28GB
Time: 2023-07-31-02-44-21; Memory: 4%; Disk: 53.0% of 991.28GB
Time: 2023-07-31-02-45-22; Memory: 4%; Disk: 52.9% of 991.28GB
Time: 2023-07-31-02-46-23; Memory: 4%; Disk: 52.9% of 991.28GB
Time: 2023-07-31-02-47-23; Memory: 4%; Disk: 53.0% of 991.28GB
Time: 2023-07-31-02-48-24; Memory: 4%; Disk: 53.1% of 991.28GB
Time: 2023-07-31-02-49-25; Memory: 4%; Disk: 52.8% of 991.28GB
Time: 2023-07-31-02-50-26; Memory: 4%; Disk: 52.9% of 991.28GB
Time: 2023-07-31-02-51-27; Memory: 4%; Disk: 52.9% of 991.28GB
Time: 2023-07-31-02-52-28; Memory: 4%; Disk: 53.0% of 991.28GB
Time: 2023-07-31-02-53-29; Memory: 4%; Disk: 53.1% of 991.28GB
Time: 2023-07-31-02-54-30; Memory: 4%; Disk: 53.1% of 991.28GB
Time: 2023-07-31-02-55-31; Memory: 4%; Disk: 53.2% of 991.28GB
Time: 2023-07-31-02-56-31; Memory: 4%; Disk: 53.2% of 991.28GB
Time: 2023-07-31-02-57-32; Memory: 4%; Disk: 53.3% of 991.28GB
Time: 2023-07-31-02-58-33; Memory: 4%; Disk: 53.3% of 991.28GB
Time: 2023-07-31-02-59-34; Memory: 4%; Disk: 53.4% of 991.28GB
Time: 2023-07-31-03-00-35; Memory: 4%; Disk: 53.5% of 991.28GB
Time: 2023-07-31-03-01-36; Memory: 4%; Disk: 53.5% of 991.28GB
Time: 2023-07-31-03-02-37; Memory: 4%; Disk: 53.6% of 991.28GB
Time: 2023-07-31-03-03-38; Memory: 4%; Disk: 53.6% of 991.28GB
Time: 2023-07-31-03-04-39; Memory: 4%; Disk: 53.7% of 991.28GB
Time: 2023-07-31-03-05-40; Memory: 4%; Disk: 53.8% of 991.28GB
Time: 2023-07-31-03-06-41; Memory: 4%; Disk: 53.8% of 991.28GB
Time: 2023-07-31-03-07-42; Memory: 4%; Disk: 53.8% of 991.28GB
Time: 2023-07-31-03-08-43; Memory: 4%; Disk: 54.0% of 991.28GB
Time: 2023-07-31-03-09-44; Memory: 4%; Disk: 54.0% of 991.28GB
Time: 2023-07-31-03-10-44; Memory: 4%; Disk: 54.1% of 991.28GB
Time: 2023-07-31-03-11-45; Memory: 4%; Disk: 54.1% of 991.28GB
Time: 2023-07-31-03-12-46; Memory: 4%; Disk: 54.2% of 991.28GB
Time: 2023-07-31-03-13-47; Memory: 4%; Disk: 54.2% of 991.28GB
Time: 2023-07-31-03-14-48; Memory: 4%; Disk: 54.3% of 991.28GB
Time: 2023-07-31-03-15-49; Memory: 4%; Disk: 54.4% of 991.28GB
Time: 2023-07-31-03-16-50; Memory: 4%; Disk: 54.8% of 991.28GB
Time: 2023-07-31-03-17-51; Memory: 4%; Disk: 55.0% of 991.28GB
Time: 2023-07-31-03-18-52; Memory: 4%; Disk: 55.1% of 991.28GB
Time: 2023-07-31-03-19-53; Memory: 4%; Disk: 55.1% of 991.28GB
Time: 2023-07-31-03-20-54; Memory: 4%; Disk: 54.8% of 991.28GB
Time: 2023-07-31-03-21-55; Memory: 4%; Disk: 54.9% of 991.28GB
Time: 2023-07-31-03-22-55; Memory: 4%; Disk: 55.0% of 991.28GB
Time: 2023-07-31-03-23-56; Memory: 4%; Disk: 55.1% of 991.28GB
Time: 2023-07-31-03-24-57; Memory: 4%; Disk: 55.1% of 991.28GB
Time: 2023-07-31-03-25-58; Memory: 4%; Disk: 55.2% of 991.28GB
Time: 2023-07-31-03-26-59; Memory: 4%; Disk: 55.3% of 991.28GB
Time: 2023-07-31-03-28-00; Memory: 4%; Disk: 55.1% of 991.28GB
Time: 2023-07-31-03-29-01; Memory: 4%; Disk: 55.2% of 991.28GB
Time: 2023-07-31-03-30-02; Memory: 4%; Disk: 55.2% of 991.28GB
Time: 2023-07-31-03-31-03; Memory: 4%; Disk: 55.3% of 991.28GB
Time: 2023-07-31-03-32-04; Memory: 4%; Disk: 55.3% of 991.28GB
Time: 2023-07-31-03-33-05; Memory: 4%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-03-34-05; Memory: 4%; Disk: 55.5% of 991.28GB
Time: 2023-07-31-03-35-06; Memory: 4%; Disk: 55.5% of 991.28GB
Time: 2023-07-31-03-36-07; Memory: 4%; Disk: 55.5% of 991.28GB
Time: 2023-07-31-03-37-08; Memory: 4%; Disk: 55.5% of 991.28GB
Time: 2023-07-31-03-38-09; Memory: 4%; Disk: 55.6% of 991.28GB
Time: 2023-07-31-03-39-10; Memory: 4%; Disk: 55.8% of 991.28GB
Time: 2023-07-31-03-40-11; Memory: 4%; Disk: 55.7% of 991.28GB
Time: 2023-07-31-03-41-12; Memory: 4%; Disk: 55.8% of 991.28GB
Time: 2023-07-31-03-42-13; Memory: 4%; Disk: 55.8% of 991.28GB
Time: 2023-07-31-03-43-14; Memory: 4%; Disk: 55.8% of 991.28GB
Time: 2023-07-31-03-44-15; Memory: 4%; Disk: 55.9% of 991.28GB
Time: 2023-07-31-03-45-16; Memory: 4%; Disk: 56.0% of 991.28GB
Time: 2023-07-31-03-46-16; Memory: 4%; Disk: 56.0% of 991.28GB
Time: 2023-07-31-03-47-17; Memory: 4%; Disk: 56.1% of 991.28GB
Time: 2023-07-31-03-48-18; Memory: 4%; Disk: 56.1% of 991.28GB
Time: 2023-07-31-03-49-19; Memory: 4%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-03-50-20; Memory: 4%; Disk: 56.3% of 991.28GB
Time: 2023-07-31-03-51-21; Memory: 4%; Disk: 56.4% of 991.28GB
Time: 2023-07-31-03-52-22; Memory: 4%; Disk: 56.4% of 991.28GB
Time: 2023-07-31-03-53-23; Memory: 4%; Disk: 56.4% of 991.28GB
Time: 2023-07-31-03-54-24; Memory: 4%; Disk: 56.5% of 991.28GB
Time: 2023-07-31-03-55-25; Memory: 4%; Disk: 56.6% of 991.28GB
Time: 2023-07-31-03-56-26; Memory: 4%; Disk: 56.8% of 991.28GB
Time: 2023-07-31-03-57-27; Memory: 4%; Disk: 56.9% of 991.28GB
Time: 2023-07-31-03-58-27; Memory: 4%; Disk: 57.1% of 991.28GB
Time: 2023-07-31-03-59-28; Memory: 4%; Disk: 57.2% of 991.28GB
Time: 2023-07-31-04-00-29; Memory: 4%; Disk: 57.4% of 991.28GB
Time: 2023-07-31-04-01-30; Memory: 4%; Disk: 57.7% of 991.28GB
Time: 2023-07-31-04-02-31; Memory: 4%; Disk: 57.9% of 991.28GB
Time: 2023-07-31-04-03-32; Memory: 4%; Disk: 58.0% of 991.28GB
Time: 2023-07-31-04-04-33; Memory: 4%; Disk: 58.0% of 991.28GB
Time: 2023-07-31-04-05-34; Memory: 4%; Disk: 58.0% of 991.28GB
Time: 2023-07-31-04-06-35; Memory: 4%; Disk: 58.1% of 991.28GB
Time: 2023-07-31-04-07-36; Memory: 4%; Disk: 58.1% of 991.28GB
Time: 2023-07-31-04-08-37; Memory: 4%; Disk: 57.8% of 991.28GB
Time: 2023-07-31-04-09-38; Memory: 4%; Disk: 57.8% of 991.28GB
Time: 2023-07-31-04-10-39; Memory: 4%; Disk: 57.9% of 991.28GB
Time: 2023-07-31-04-11-40; Memory: 4%; Disk: 57.9% of 991.28GB
Time: 2023-07-31-04-12-41; Memory: 4%; Disk: 58.0% of 991.28GB
Time: 2023-07-31-04-13-41; Memory: 4%; Disk: 58.0% of 991.28GB
Time: 2023-07-31-04-14-42; Memory: 4%; Disk: 58.1% of 991.28GB
Time: 2023-07-31-04-15-43; Memory: 4%; Disk: 58.1% of 991.28GB
Time: 2023-07-31-04-16-44; Memory: 4%; Disk: 58.2% of 991.28GB
Time: 2023-07-31-04-17-45; Memory: 4%; Disk: 58.2% of 991.28GB
Time: 2023-07-31-04-18-46; Memory: 4%; Disk: 58.3% of 991.28GB
Time: 2023-07-31-04-19-47; Memory: 4%; Disk: 58.4% of 991.28GB
Time: 2023-07-31-04-20-48; Memory: 4%; Disk: 58.5% of 991.28GB
Time: 2023-07-31-04-21-49; Memory: 4%; Disk: 58.7% of 991.28GB
Time: 2023-07-31-04-22-50; Memory: 4%; Disk: 58.7% of 991.28GB
Time: 2023-07-31-04-23-51; Memory: 4%; Disk: 58.8% of 991.28GB
Time: 2023-07-31-04-24-52; Memory: 4%; Disk: 58.9% of 991.28GB
Time: 2023-07-31-04-25-53; Memory: 4%; Disk: 59.0% of 991.28GB
Time: 2023-07-31-04-26-54; Memory: 4%; Disk: 58.9% of 991.28GB
Time: 2023-07-31-04-27-55; Memory: 4%; Disk: 59.0% of 991.28GB
Time: 2023-07-31-04-28-56; Memory: 4%; Disk: 59.1% of 991.28GB
Time: 2023-07-31-04-29-56; Memory: 4%; Disk: 59.2% of 991.28GB
Time: 2023-07-31-04-30-57; Memory: 4%; Disk: 59.1% of 991.28GB
Time: 2023-07-31-04-31-58; Memory: 4%; Disk: 57.9% of 991.28GB
Time: 2023-07-31-04-32-59; Memory: 4%; Disk: 58.0% of 991.28GB
Time: 2023-07-31-04-34-00; Memory: 4%; Disk: 58.0% of 991.28GB
Time: 2023-07-31-04-35-01; Memory: 4%; Disk: 58.1% of 991.28GB
Time: 2023-07-31-04-36-02; Memory: 4%; Disk: 58.2% of 991.28GB
Time: 2023-07-31-04-37-03; Memory: 4%; Disk: 58.4% of 991.28GB
Time: 2023-07-31-04-38-04; Memory: 4%; Disk: 58.5% of 991.28GB
Time: 2023-07-31-04-39-05; Memory: 4%; Disk: 58.6% of 991.28GB
Time: 2023-07-31-04-40-06; Memory: 4%; Disk: 58.6% of 991.28GB
Time: 2023-07-31-04-41-06; Memory: 4%; Disk: 58.7% of 991.28GB
Time: 2023-07-31-04-42-07; Memory: 4%; Disk: 58.7% of 991.28GB
Time: 2023-07-31-04-43-08; Memory: 4%; Disk: 58.7% of 991.28GB
Time: 2023-07-31-04-44-09; Memory: 4%; Disk: 58.9% of 991.28GB
Time: 2023-07-31-04-45-10; Memory: 4%; Disk: 59.1% of 991.28GB
Time: 2023-07-31-04-46-11; Memory: 4%; Disk: 59.1% of 991.28GB
Time: 2023-07-31-04-47-12; Memory: 4%; Disk: 59.2% of 991.28GB
Time: 2023-07-31-04-48-13; Memory: 4%; Disk: 59.2% of 991.28GB
Time: 2023-07-31-04-49-14; Memory: 4%; Disk: 59.3% of 991.28GB
Time: 2023-07-31-04-50-15; Memory: 4%; Disk: 59.4% of 991.28GB
Time: 2023-07-31-04-51-16; Memory: 4%; Disk: 59.4% of 991.28GB
Time: 2023-07-31-04-52-17; Memory: 4%; Disk: 59.6% of 991.28GB
Time: 2023-07-31-04-53-18; Memory: 4%; Disk: 59.9% of 991.28GB
Time: 2023-07-31-04-54-18; Memory: 4%; Disk: 60.2% of 991.28GB
Time: 2023-07-31-04-55-19; Memory: 4%; Disk: 60.5% of 991.28GB
Time: 2023-07-31-04-56-20; Memory: 4%; Disk: 60.8% of 991.28GB
Time: 2023-07-31-04-57-21; Memory: 4%; Disk: 61.2% of 991.28GB
Time: 2023-07-31-04-58-22; Memory: 4%; Disk: 61.2% of 991.28GB
Time: 2023-07-31-04-59-23; Memory: 4%; Disk: 61.2% of 991.28GB
Time: 2023-07-31-05-00-24; Memory: 4%; Disk: 61.3% of 991.28GB
Time: 2023-07-31-05-01-25; Memory: 4%; Disk: 61.3% of 991.28GB
Time: 2023-07-31-05-02-26; Memory: 4%; Disk: 61.3% of 991.28GB
Time: 2023-07-31-05-03-27; Memory: 4%; Disk: 61.4% of 991.28GB
Time: 2023-07-31-05-04-28; Memory: 4%; Disk: 61.4% of 991.28GB
Time: 2023-07-31-05-05-28; Memory: 4%; Disk: 60.8% of 991.28GB
Time: 2023-07-31-05-06-29; Memory: 4%; Disk: 61.0% of 991.28GB
Time: 2023-07-31-05-07-30; Memory: 4%; Disk: 60.8% of 991.28GB
Time: 2023-07-31-05-08-31; Memory: 4%; Disk: 60.9% of 991.28GB
Time: 2023-07-31-05-09-32; Memory: 4%; Disk: 60.9% of 991.28GB
Time: 2023-07-31-05-10-33; Memory: 4%; Disk: 61.0% of 991.28GB
Time: 2023-07-31-05-11-34; Memory: 4%; Disk: 61.0% of 991.28GB
Time: 2023-07-31-05-12-35; Memory: 4%; Disk: 61.0% of 991.28GB
Time: 2023-07-31-05-13-36; Memory: 4%; Disk: 61.1% of 991.28GB
Time: 2023-07-31-05-14-37; Memory: 4%; Disk: 61.3% of 991.28GB
Time: 2023-07-31-05-15-38; Memory: 4%; Disk: 61.5% of 991.28GB
Time: 2023-07-31-05-16-39; Memory: 4%; Disk: 61.6% of 991.28GB
Time: 2023-07-31-05-17-40; Memory: 4%; Disk: 61.6% of 991.28GB
Time: 2023-07-31-05-18-41; Memory: 4%; Disk: 61.6% of 991.28GB
Time: 2023-07-31-05-19-42; Memory: 4%; Disk: 61.8% of 991.28GB
Time: 2023-07-31-05-20-42; Memory: 4%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-05-21-43; Memory: 4%; Disk: 60.3% of 991.28GB
Time: 2023-07-31-05-22-44; Memory: 4%; Disk: 60.6% of 991.28GB
Time: 2023-07-31-05-23-45; Memory: 4%; Disk: 60.6% of 991.28GB
Time: 2023-07-31-05-24-46; Memory: 4%; Disk: 60.6% of 991.28GB
Time: 2023-07-31-05-25-47; Memory: 4%; Disk: 60.7% of 991.28GB
Time: 2023-07-31-05-26-48; Memory: 4%; Disk: 60.8% of 991.28GB
Time: 2023-07-31-05-27-49; Memory: 4%; Disk: 60.9% of 991.28GB
Time: 2023-07-31-05-28-50; Memory: 5%; Disk: 61.1% of 991.28GB
Time: 2023-07-31-05-29-51; Memory: 4%; Disk: 61.1% of 991.28GB
Time: 2023-07-31-05-30-52; Memory: 4%; Disk: 61.0% of 991.28GB
Time: 2023-07-31-05-31-52; Memory: 4%; Disk: 61.2% of 991.28GB
Time: 2023-07-31-05-32-53; Memory: 4%; Disk: 61.3% of 991.28GB
Time: 2023-07-31-05-33-54; Memory: 4%; Disk: 61.3% of 991.28GB
Time: 2023-07-31-05-34-55; Memory: 4%; Disk: 61.4% of 991.28GB
Time: 2023-07-31-05-35-56; Memory: 3%; Disk: 61.3% of 991.28GB
Time: 2023-07-31-05-36-57; Memory: 3%; Disk: 61.4% of 991.28GB
Time: 2023-07-31-05-37-58; Memory: 3%; Disk: 61.5% of 991.28GB
Time: 2023-07-31-05-38-59; Memory: 3%; Disk: 61.5% of 991.28GB
Time: 2023-07-31-05-40-00; Memory: 3%; Disk: 61.6% of 991.28GB
Time: 2023-07-31-05-41-00; Memory: 3%; Disk: 61.7% of 991.28GB
Time: 2023-07-31-05-42-01; Memory: 3%; Disk: 61.7% of 991.28GB
Time: 2023-07-31-05-43-02; Memory: 3%; Disk: 61.8% of 991.28GB
Time: 2023-07-31-05-44-03; Memory: 4%; Disk: 61.8% of 991.28GB
Time: 2023-07-31-05-45-04; Memory: 4%; Disk: 61.8% of 991.28GB
Time: 2023-07-31-05-46-05; Memory: 4%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-05-47-06; Memory: 3%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-05-48-06; Memory: 3%; Disk: 62.0% of 991.28GB
Time: 2023-07-31-05-49-07; Memory: 3%; Disk: 62.0% of 991.28GB
Time: 2023-07-31-05-50-08; Memory: 3%; Disk: 62.0% of 991.28GB
Time: 2023-07-31-05-51-09; Memory: 3%; Disk: 62.1% of 991.28GB
Time: 2023-07-31-05-52-10; Memory: 3%; Disk: 62.1% of 991.28GB
Time: 2023-07-31-05-53-11; Memory: 4%; Disk: 62.1% of 991.28GB
Time: 2023-07-31-05-54-12; Memory: 5%; Disk: 62.2% of 991.28GB
Time: 2023-07-31-05-55-12; Memory: 6%; Disk: 62.2% of 991.28GB
Time: 2023-07-31-05-56-13; Memory: 6%; Disk: 62.3% of 991.28GB
Time: 2023-07-31-05-57-14; Memory: 6%; Disk: 62.3% of 991.28GB
Time: 2023-07-31-05-58-15; Memory: 7%; Disk: 62.3% of 991.28GB
Time: 2023-07-31-05-59-16; Memory: 5%; Disk: 62.4% of 991.28GB
Time: 2023-07-31-06-00-17; Memory: 4%; Disk: 62.4% of 991.28GB
Time: 2023-07-31-06-01-18; Memory: 4%; Disk: 62.5% of 991.28GB
Time: 2023-07-31-06-02-18; Memory: 4%; Disk: 62.5% of 991.28GB
Time: 2023-07-31-06-03-19; Memory: 5%; Disk: 62.5% of 991.28GB
Time: 2023-07-31-06-04-20; Memory: 5%; Disk: 62.5% of 991.28GB
Time: 2023-07-31-06-05-21; Memory: 4%; Disk: 62.6% of 991.28GB
Time: 2023-07-31-06-06-22; Memory: 4%; Disk: 62.6% of 991.28GB
Time: 2023-07-31-06-07-23; Memory: 3%; Disk: 62.7% of 991.28GB
Time: 2023-07-31-06-08-24; Memory: 3%; Disk: 62.7% of 991.28GB
Time: 2023-07-31-06-09-25; Memory: 4%; Disk: 62.7% of 991.28GB
Time: 2023-07-31-06-10-25; Memory: 5%; Disk: 62.7% of 991.28GB
Time: 2023-07-31-06-11-26; Memory: 3%; Disk: 62.8% of 991.28GB
Time: 2023-07-31-06-12-27; Memory: 3%; Disk: 62.8% of 991.28GB
Time: 2023-07-31-06-13-28; Memory: 3%; Disk: 62.8% of 991.28GB
Time: 2023-07-31-06-14-29; Memory: 3%; Disk: 62.9% of 991.28GB
Time: 2023-07-31-06-15-30; Memory: 3%; Disk: 62.9% of 991.28GB
Time: 2023-07-31-06-16-31; Memory: 3%; Disk: 62.9% of 991.28GB
Time: 2023-07-31-06-17-32; Memory: 3%; Disk: 63.0% of 991.28GB
Time: 2023-07-31-06-18-33; Memory: 3%; Disk: 63.0% of 991.28GB
Time: 2023-07-31-06-19-34; Memory: 3%; Disk: 63.0% of 991.28GB
Time: 2023-07-31-06-20-34; Memory: 3%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-06-21-35; Memory: 3%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-06-22-36; Memory: 3%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-06-23-37; Memory: 3%; Disk: 63.2% of 991.28GB
Time: 2023-07-31-06-24-38; Memory: 3%; Disk: 63.2% of 991.28GB
Time: 2023-07-31-06-25-39; Memory: 3%; Disk: 63.3% of 991.28GB
Time: 2023-07-31-06-26-40; Memory: 3%; Disk: 63.3% of 991.28GB
Time: 2023-07-31-06-27-40; Memory: 3%; Disk: 63.4% of 991.28GB
Time: 2023-07-31-06-28-41; Memory: 3%; Disk: 63.4% of 991.28GB
Time: 2023-07-31-06-29-42; Memory: 3%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-06-30-43; Memory: 3%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-06-31-44; Memory: 4%; Disk: 62.8% of 991.28GB
Time: 2023-07-31-06-32-45; Memory: 5%; Disk: 62.8% of 991.28GB
Time: 2023-07-31-06-33-46; Memory: 4%; Disk: 62.9% of 991.28GB
Time: 2023-07-31-06-34-46; Memory: 3%; Disk: 62.9% of 991.28GB
Time: 2023-07-31-06-35-47; Memory: 3%; Disk: 63.0% of 991.28GB
Time: 2023-07-31-06-36-48; Memory: 5%; Disk: 63.0% of 991.28GB
Time: 2023-07-31-06-37-49; Memory: 4%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-06-38-50; Memory: 4%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-06-39-51; Memory: 4%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-06-40-52; Memory: 4%; Disk: 63.2% of 991.28GB
Time: 2023-07-31-06-41-52; Memory: 4%; Disk: 63.2% of 991.28GB
Time: 2023-07-31-06-42-53; Memory: 4%; Disk: 63.3% of 991.28GB
Time: 2023-07-31-06-43-54; Memory: 6%; Disk: 63.3% of 991.28GB
Time: 2023-07-31-06-44-55; Memory: 4%; Disk: 63.4% of 991.28GB
Time: 2023-07-31-06-45-56; Memory: 4%; Disk: 63.4% of 991.28GB
Time: 2023-07-31-06-46-57; Memory: 6%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-06-47-58; Memory: 4%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-06-48-59; Memory: 4%; Disk: 63.6% of 991.28GB
Time: 2023-07-31-06-49-59; Memory: 4%; Disk: 63.6% of 991.28GB
Time: 2023-07-31-06-51-00; Memory: 4%; Disk: 63.7% of 991.28GB
Time: 2023-07-31-06-52-01; Memory: 5%; Disk: 63.7% of 991.28GB
Time: 2023-07-31-06-53-02; Memory: 4%; Disk: 63.8% of 991.28GB
Time: 2023-07-31-06-54-03; Memory: 10%; Disk: 63.8% of 991.28GB
Time: 2023-07-31-06-55-04; Memory: 16%; Disk: 63.8% of 991.28GB
Time: 2023-07-31-06-56-05; Memory: 18%; Disk: 63.9% of 991.28GB
Time: 2023-07-31-06-57-06; Memory: 6%; Disk: 63.9% of 991.28GB
Time: 2023-07-31-06-58-06; Memory: 6%; Disk: 64.0% of 991.28GB
Time: 2023-07-31-06-59-07; Memory: 6%; Disk: 64.0% of 991.28GB
Time: 2023-07-31-07-00-08; Memory: 6%; Disk: 64.1% of 991.28GB
Time: 2023-07-31-07-01-09; Memory: 6%; Disk: 64.1% of 991.28GB
Time: 2023-07-31-07-02-10; Memory: 6%; Disk: 64.2% of 991.28GB
Time: 2023-07-31-07-03-11; Memory: 6%; Disk: 64.2% of 991.28GB
Time: 2023-07-31-07-04-12; Memory: 6%; Disk: 64.2% of 991.28GB
Time: 2023-07-31-07-05-12; Memory: 6%; Disk: 64.3% of 991.28GB
Time: 2023-07-31-07-06-13; Memory: 6%; Disk: 64.3% of 991.28GB
Time: 2023-07-31-07-07-14; Memory: 6%; Disk: 64.4% of 991.28GB
Time: 2023-07-31-07-08-15; Memory: 6%; Disk: 64.4% of 991.28GB
Time: 2023-07-31-07-09-16; Memory: 6%; Disk: 64.5% of 991.28GB
Time: 2023-07-31-07-10-17; Memory: 6%; Disk: 64.5% of 991.28GB
Time: 2023-07-31-07-11-18; Memory: 6%; Disk: 64.5% of 991.28GB
Time: 2023-07-31-07-12-18; Memory: 6%; Disk: 64.6% of 991.28GB
Time: 2023-07-31-07-13-19; Memory: 6%; Disk: 64.6% of 991.28GB
Time: 2023-07-31-07-14-20; Memory: 6%; Disk: 64.7% of 991.28GB
Time: 2023-07-31-07-15-21; Memory: 6%; Disk: 64.7% of 991.28GB
Time: 2023-07-31-07-16-22; Memory: 7%; Disk: 64.8% of 991.28GB
Time: 2023-07-31-07-17-23; Memory: 7%; Disk: 64.8% of 991.28GB
Time: 2023-07-31-07-18-23; Memory: 7%; Disk: 64.8% of 991.28GB
Time: 2023-07-31-07-19-24; Memory: 7%; Disk: 64.9% of 991.28GB
Time: 2023-07-31-07-20-25; Memory: 9%; Disk: 64.9% of 991.28GB
Time: 2023-07-31-07-21-26; Memory: 15%; Disk: 64.9% of 991.28GB
Time: 2023-07-31-07-22-27; Memory: 19%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-07-23-28; Memory: 7%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-07-24-29; Memory: 7%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-07-25-30; Memory: 7%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-07-26-31; Memory: 7%; Disk: 65.1% of 991.28GB
Time: 2023-07-31-07-27-31; Memory: 7%; Disk: 65.1% of 991.28GB
Time: 2023-07-31-07-28-32; Memory: 7%; Disk: 65.1% of 991.28GB
Time: 2023-07-31-07-29-33; Memory: 7%; Disk: 65.1% of 991.28GB
Time: 2023-07-31-07-30-34; Memory: 7%; Disk: 65.2% of 991.28GB
Time: 2023-07-31-07-31-35; Memory: 7%; Disk: 65.2% of 991.28GB
Time: 2023-07-31-07-32-36; Memory: 7%; Disk: 65.2% of 991.28GB
Time: 2023-07-31-07-33-36; Memory: 7%; Disk: 65.2% of 991.28GB
Time: 2023-07-31-07-34-37; Memory: 7%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-07-35-38; Memory: 8%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-07-36-39; Memory: 8%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-07-37-40; Memory: 8%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-07-38-41; Memory: 8%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-07-39-42; Memory: 8%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-07-40-42; Memory: 8%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-07-41-43; Memory: 8%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-07-42-44; Memory: 14%; Disk: 65.5% of 991.28GB
Time: 2023-07-31-07-43-45; Memory: 9%; Disk: 65.5% of 991.28GB
Time: 2023-07-31-07-44-46; Memory: 9%; Disk: 65.5% of 991.28GB
Time: 2023-07-31-07-45-47; Memory: 9%; Disk: 65.6% of 991.28GB
Time: 2023-07-31-07-46-48; Memory: 9%; Disk: 65.6% of 991.28GB
Time: 2023-07-31-07-47-49; Memory: 9%; Disk: 65.6% of 991.28GB
Time: 2023-07-31-07-48-50; Memory: 9%; Disk: 65.6% of 991.28GB
Time: 2023-07-31-07-49-50; Memory: 9%; Disk: 65.6% of 991.28GB
Time: 2023-07-31-07-50-51; Memory: 9%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-07-51-52; Memory: 9%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-07-52-53; Memory: 9%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-07-53-54; Memory: 9%; Disk: 65.8% of 991.28GB
Time: 2023-07-31-07-54-55; Memory: 9%; Disk: 65.8% of 991.28GB
Time: 2023-07-31-07-55-56; Memory: 9%; Disk: 65.8% of 991.28GB
Time: 2023-07-31-07-56-56; Memory: 9%; Disk: 65.9% of 991.28GB
Time: 2023-07-31-07-57-57; Memory: 9%; Disk: 65.9% of 991.28GB
Time: 2023-07-31-07-58-58; Memory: 9%; Disk: 65.9% of 991.28GB
Time: 2023-07-31-07-59-59; Memory: 9%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-08-01-00; Memory: 9%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-08-02-01; Memory: 9%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-08-03-02; Memory: 9%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-08-04-03; Memory: 9%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-08-05-04; Memory: 9%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-08-06-05; Memory: 9%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-08-07-06; Memory: 11%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-08-08-06; Memory: 10%; Disk: 66.2% of 991.28GB
Time: 2023-07-31-08-09-07; Memory: 10%; Disk: 66.2% of 991.28GB
Time: 2023-07-31-08-10-08; Memory: 10%; Disk: 66.2% of 991.28GB
Time: 2023-07-31-08-11-09; Memory: 10%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-08-12-10; Memory: 10%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-08-13-11; Memory: 10%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-08-14-12; Memory: 10%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-08-15-13; Memory: 10%; Disk: 66.4% of 991.28GB
Time: 2023-07-31-08-16-13; Memory: 14%; Disk: 66.4% of 991.28GB
Time: 2023-07-31-08-17-14; Memory: 11%; Disk: 66.4% of 991.28GB
Time: 2023-07-31-08-18-15; Memory: 11%; Disk: 66.5% of 991.28GB
Time: 2023-07-31-08-19-16; Memory: 11%; Disk: 66.5% of 991.28GB
Time: 2023-07-31-08-20-17; Memory: 11%; Disk: 66.5% of 991.28GB
Time: 2023-07-31-08-21-18; Memory: 11%; Disk: 66.5% of 991.28GB
Time: 2023-07-31-08-22-19; Memory: 11%; Disk: 66.6% of 991.28GB
Time: 2023-07-31-08-23-20; Memory: 11%; Disk: 66.6% of 991.28GB
Time: 2023-07-31-08-24-20; Memory: 12%; Disk: 66.6% of 991.28GB
Time: 2023-07-31-08-25-21; Memory: 11%; Disk: 66.6% of 991.28GB
Time: 2023-07-31-08-26-22; Memory: 11%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-08-27-23; Memory: 11%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-08-28-24; Memory: 11%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-08-29-25; Memory: 12%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-08-30-26; Memory: 12%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-08-31-27; Memory: 12%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-08-32-28; Memory: 12%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-08-33-29; Memory: 12%; Disk: 66.8% of 991.28GB
Time: 2023-07-31-08-34-29; Memory: 12%; Disk: 66.8% of 991.28GB
Time: 2023-07-31-08-35-31; Memory: 14%; Disk: 66.8% of 991.28GB
Time: 2023-07-31-08-36-31; Memory: 12%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-08-37-32; Memory: 13%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-08-38-33; Memory: 16%; Disk: 67.0% of 991.28GB
Time: 2023-07-31-08-39-34; Memory: 18%; Disk: 67.0% of 991.28GB
Time: 2023-07-31-08-40-35; Memory: 13%; Disk: 67.1% of 991.28GB
Time: 2023-07-31-08-41-36; Memory: 13%; Disk: 67.1% of 991.28GB
Time: 2023-07-31-08-42-37; Memory: 13%; Disk: 67.1% of 991.28GB
Time: 2023-07-31-08-43-38; Memory: 13%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-08-44-38; Memory: 13%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-08-45-39; Memory: 13%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-08-46-40; Memory: 14%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-08-47-41; Memory: 14%; Disk: 67.4% of 991.28GB
Time: 2023-07-31-08-48-42; Memory: 14%; Disk: 67.4% of 991.28GB
Time: 2023-07-31-08-49-43; Memory: 18%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-08-50-44; Memory: 14%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-08-51-44; Memory: 14%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-08-52-45; Memory: 14%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-08-53-46; Memory: 14%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-08-54-47; Memory: 14%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-08-55-48; Memory: 14%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-08-56-49; Memory: 14%; Disk: 67.8% of 991.28GB
Time: 2023-07-31-08-57-50; Memory: 14%; Disk: 67.8% of 991.28GB
Time: 2023-07-31-08-58-50; Memory: 15%; Disk: 67.9% of 991.28GB
Time: 2023-07-31-08-59-51; Memory: 15%; Disk: 67.9% of 991.28GB
Time: 2023-07-31-09-00-52; Memory: 15%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-09-01-53; Memory: 15%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-09-02-54; Memory: 15%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-09-03-55; Memory: 15%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-09-04-56; Memory: 15%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-09-05-56; Memory: 15%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-09-06-57; Memory: 15%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-09-07-58; Memory: 15%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-09-08-59; Memory: 15%; Disk: 68.3% of 991.28GB
Time: 2023-07-31-09-10-00; Memory: 15%; Disk: 68.3% of 991.28GB
Time: 2023-07-31-09-11-01; Memory: 15%; Disk: 68.4% of 991.28GB
Time: 2023-07-31-09-12-02; Memory: 15%; Disk: 68.4% of 991.28GB
Time: 2023-07-31-09-13-02; Memory: 15%; Disk: 68.5% of 991.28GB
Time: 2023-07-31-09-14-03; Memory: 15%; Disk: 68.5% of 991.28GB
Time: 2023-07-31-09-15-04; Memory: 15%; Disk: 68.6% of 991.28GB
Time: 2023-07-31-09-16-05; Memory: 15%; Disk: 68.6% of 991.28GB
Time: 2023-07-31-09-17-06; Memory: 15%; Disk: 68.6% of 991.28GB
Time: 2023-07-31-09-18-07; Memory: 15%; Disk: 68.7% of 991.28GB
Time: 2023-07-31-09-19-08; Memory: 15%; Disk: 68.7% of 991.28GB
Time: 2023-07-31-09-20-08; Memory: 15%; Disk: 64.4% of 991.28GB
Time: 2023-07-31-09-21-09; Memory: 15%; Disk: 64.4% of 991.28GB
Time: 2023-07-31-09-22-10; Memory: 15%; Disk: 64.5% of 991.28GB
Time: 2023-07-31-09-23-11; Memory: 15%; Disk: 64.7% of 991.28GB
Time: 2023-07-31-09-24-12; Memory: 15%; Disk: 64.8% of 991.28GB
Time: 2023-07-31-09-25-13; Memory: 15%; Disk: 64.9% of 991.28GB
Time: 2023-07-31-09-26-13; Memory: 15%; Disk: 65.1% of 991.28GB
Time: 2023-07-31-09-27-14; Memory: 15%; Disk: 65.2% of 991.28GB
Time: 2023-07-31-09-28-15; Memory: 15%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-09-29-16; Memory: 15%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-09-30-17; Memory: 15%; Disk: 65.5% of 991.28GB
Time: 2023-07-31-09-31-18; Memory: 15%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-09-32-19; Memory: 15%; Disk: 65.8% of 991.28GB
Time: 2023-07-31-09-33-19; Memory: 15%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-09-34-20; Memory: 15%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-09-35-21; Memory: 15%; Disk: 66.2% of 991.28GB
Time: 2023-07-31-09-36-22; Memory: 15%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-09-37-23; Memory: 15%; Disk: 66.5% of 991.28GB
Time: 2023-07-31-09-38-24; Memory: 15%; Disk: 66.6% of 991.28GB
Time: 2023-07-31-09-39-25; Memory: 15%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-09-40-25; Memory: 15%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-09-41-26; Memory: 15%; Disk: 67.0% of 991.28GB
Time: 2023-07-31-09-42-27; Memory: 15%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-09-43-28; Memory: 15%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-09-44-29; Memory: 15%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-09-45-30; Memory: 15%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-09-46-31; Memory: 15%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-09-47-31; Memory: 15%; Disk: 67.9% of 991.28GB
Time: 2023-07-31-09-48-32; Memory: 15%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-09-49-33; Memory: 16%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-09-50-34; Memory: 16%; Disk: 68.3% of 991.28GB
Time: 2023-07-31-09-51-35; Memory: 16%; Disk: 68.4% of 991.28GB
Time: 2023-07-31-09-52-36; Memory: 16%; Disk: 68.5% of 991.28GB
Time: 2023-07-31-09-53-37; Memory: 16%; Disk: 68.7% of 991.28GB
Time: 2023-07-31-09-54-37; Memory: 16%; Disk: 68.8% of 991.28GB
Time: 2023-07-31-09-55-38; Memory: 16%; Disk: 68.9% of 991.28GB
Time: 2023-07-31-09-56-39; Memory: 16%; Disk: 69.1% of 991.28GB
Time: 2023-07-31-09-57-40; Memory: 16%; Disk: 69.2% of 991.28GB
Time: 2023-07-31-09-58-41; Memory: 16%; Disk: 69.3% of 991.28GB
Time: 2023-07-31-09-59-42; Memory: 16%; Disk: 69.5% of 991.28GB
Time: 2023-07-31-10-00-42; Memory: 16%; Disk: 69.6% of 991.28GB
Time: 2023-07-31-10-01-43; Memory: 16%; Disk: 69.7% of 991.28GB
Time: 2023-07-31-10-02-44; Memory: 16%; Disk: 69.9% of 991.28GB
Time: 2023-07-31-10-03-45; Memory: 16%; Disk: 70.0% of 991.28GB
Time: 2023-07-31-10-04-46; Memory: 16%; Disk: 70.1% of 991.28GB
Time: 2023-07-31-10-05-47; Memory: 16%; Disk: 70.3% of 991.28GB
Time: 2023-07-31-10-06-48; Memory: 16%; Disk: 70.4% of 991.28GB
Time: 2023-07-31-10-07-48; Memory: 16%; Disk: 70.6% of 991.28GB
Time: 2023-07-31-10-08-49; Memory: 16%; Disk: 70.8% of 991.28GB
Time: 2023-07-31-10-09-50; Memory: 16%; Disk: 71.0% of 991.28GB
Time: 2023-07-31-10-10-51; Memory: 16%; Disk: 71.1% of 991.28GB
Time: 2023-07-31-10-11-52; Memory: 16%; Disk: 71.3% of 991.28GB
Time: 2023-07-31-10-12-53; Memory: 16%; Disk: 71.5% of 991.28GB
Time: 2023-07-31-10-13-54; Memory: 16%; Disk: 71.7% of 991.28GB
Time: 2023-07-31-10-14-54; Memory: 16%; Disk: 71.8% of 991.28GB
Time: 2023-07-31-10-15-55; Memory: 16%; Disk: 72.0% of 991.28GB
Time: 2023-07-31-10-16-56; Memory: 16%; Disk: 72.2% of 991.28GB
Time: 2023-07-31-10-17-57; Memory: 16%; Disk: 72.4% of 991.28GB
Time: 2023-07-31-10-18-58; Memory: 16%; Disk: 72.5% of 991.28GB
Time: 2023-07-31-10-19-59; Memory: 16%; Disk: 72.7% of 991.28GB
Time: 2023-07-31-10-21-00; Memory: 16%; Disk: 72.8% of 991.28GB
Time: 2023-07-31-10-22-00; Memory: 16%; Disk: 72.9% of 991.28GB
Time: 2023-07-31-10-23-01; Memory: 16%; Disk: 73.0% of 991.28GB
Time: 2023-07-31-10-24-02; Memory: 16%; Disk: 73.1% of 991.28GB
Time: 2023-07-31-10-25-03; Memory: 16%; Disk: 73.2% of 991.28GB
Time: 2023-07-31-10-26-04; Memory: 16%; Disk: 73.3% of 991.28GB
Time: 2023-07-31-10-27-05; Memory: 16%; Disk: 73.4% of 991.28GB
Time: 2023-07-31-10-28-06; Memory: 16%; Disk: 73.5% of 991.28GB
Time: 2023-07-31-10-29-06; Memory: 16%; Disk: 73.6% of 991.28GB
Time: 2023-07-31-10-30-07; Memory: 16%; Disk: 73.7% of 991.28GB
Time: 2023-07-31-10-31-08; Memory: 16%; Disk: 73.8% of 991.28GB
Time: 2023-07-31-10-32-09; Memory: 16%; Disk: 73.9% of 991.28GB
Time: 2023-07-31-10-33-10; Memory: 16%; Disk: 74.0% of 991.28GB
Time: 2023-07-31-10-34-11; Memory: 16%; Disk: 74.3% of 991.28GB
Time: 2023-07-31-10-35-12; Memory: 16%; Disk: 74.8% of 991.28GB
Time: 2023-07-31-10-36-12; Memory: 16%; Disk: 75.4% of 991.28GB
Time: 2023-07-31-10-37-13; Memory: 16%; Disk: 76.0% of 991.28GB
Time: 2023-07-31-10-38-14; Memory: 16%; Disk: 76.6% of 991.28GB
Time: 2023-07-31-10-39-15; Memory: 16%; Disk: 77.2% of 991.28GB
Time: 2023-07-31-10-40-16; Memory: 16%; Disk: 77.8% of 991.28GB
Time: 2023-07-31-10-41-17; Memory: 16%; Disk: 78.4% of 991.28GB
Time: 2023-07-31-10-42-18; Memory: 16%; Disk: 79.0% of 991.28GB
Time: 2023-07-31-10-43-18; Memory: 16%; Disk: 79.6% of 991.28GB
Time: 2023-07-31-10-44-19; Memory: 16%; Disk: 80.2% of 991.28GB
Time: 2023-07-31-10-45-20; Memory: 16%; Disk: 80.8% of 991.28GB
Time: 2023-07-31-10-46-21; Memory: 16%; Disk: 81.4% of 991.28GB
Time: 2023-07-31-10-47-22; Memory: 16%; Disk: 82.0% of 991.28GB
Time: 2023-07-31-10-48-23; Memory: 16%; Disk: 82.6% of 991.28GB
Time: 2023-07-31-10-49-24; Memory: 16%; Disk: 83.2% of 991.28GB
Time: 2023-07-31-10-50-24; Memory: 16%; Disk: 83.7% of 991.28GB
Time: 2023-07-31-10-51-25; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-10-52-26; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-10-53-27; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-10-54-28; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-10-55-29; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-10-56-30; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-10-57-30; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-10-58-31; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-10-59-32; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-00-33; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-01-34; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-02-35; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-03-36; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-04-37; Memory: 16%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-05-37; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-06-38; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-07-39; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-08-40; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-09-41; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-10-42; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-11-43; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-12-44; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-13-44; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-14-45; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-15-46; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-16-47; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-17-48; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-18-49; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-19-50; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-20-50; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-21-51; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-22-52; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-23-53; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-24-54; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-25-55; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-26-56; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-27-56; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-28-57; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-29-58; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-30-59; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-32-00; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-33-01; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-34-02; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-35-03; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-36-04; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-37-05; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-38-05; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-39-06; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-40-07; Memory: 17%; Disk: 83.9% of 991.28GB
Time: 2023-07-31-11-41-08; Memory: 17%; Disk: 76.9% of 991.28GB
Time: 2023-07-31-11-42-09; Memory: 17%; Disk: 74.7% of 991.28GB
Time: 2023-07-31-11-43-10; Memory: 17%; Disk: 77.3% of 991.28GB
Time: 2023-07-31-11-44-11; Memory: 17%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-45-12; Memory: 19%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-46-12; Memory: 21%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-47-13; Memory: 23%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-48-14; Memory: 24%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-49-15; Memory: 26%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-50-16; Memory: 27%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-51-17; Memory: 29%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-52-18; Memory: 31%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-53-18; Memory: 32%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-11-54-19; Memory: 31%; Disk: 64.6% of 991.28GB
Time: 2023-07-31-11-55-20; Memory: 31%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-11-56-21; Memory: 31%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-11-57-22; Memory: 31%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-11-58-23; Memory: 31%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-11-59-23; Memory: 31%; Disk: 66.4% of 991.28GB
Time: 2023-07-31-12-00-24; Memory: 31%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-12-01-25; Memory: 31%; Disk: 67.0% of 991.28GB
Time: 2023-07-31-12-02-26; Memory: 15%; Disk: 62.4% of 991.28GB
Time: 2023-07-31-12-03-27; Memory: 15%; Disk: 62.5% of 991.28GB
Time: 2023-07-31-12-04-28; Memory: 16%; Disk: 62.6% of 991.28GB
Time: 2023-07-31-12-05-29; Memory: 16%; Disk: 62.7% of 991.28GB
Time: 2023-07-31-12-06-29; Memory: 16%; Disk: 62.9% of 991.28GB
Time: 2023-07-31-12-07-30; Memory: 16%; Disk: 63.0% of 991.28GB
Time: 2023-07-31-12-08-31; Memory: 16%; Disk: 63.2% of 991.28GB
Time: 2023-07-31-12-09-32; Memory: 16%; Disk: 63.3% of 991.28GB
Time: 2023-07-31-12-10-33; Memory: 16%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-12-11-34; Memory: 16%; Disk: 63.6% of 991.28GB
Time: 2023-07-31-12-12-35; Memory: 16%; Disk: 63.8% of 991.28GB
Time: 2023-07-31-12-13-35; Memory: 16%; Disk: 63.9% of 991.28GB
Time: 2023-07-31-12-14-36; Memory: 16%; Disk: 64.1% of 991.28GB
Time: 2023-07-31-12-15-37; Memory: 16%; Disk: 64.2% of 991.28GB
Time: 2023-07-31-12-16-38; Memory: 16%; Disk: 64.3% of 991.28GB
Time: 2023-07-31-12-17-39; Memory: 16%; Disk: 64.5% of 991.28GB
Time: 2023-07-31-12-18-40; Memory: 16%; Disk: 64.6% of 991.28GB
Time: 2023-07-31-12-19-41; Memory: 16%; Disk: 64.8% of 991.28GB
Time: 2023-07-31-12-20-41; Memory: 16%; Disk: 64.9% of 991.28GB
Time: 2023-07-31-12-21-42; Memory: 16%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-12-22-43; Memory: 16%; Disk: 65.2% of 991.28GB
Time: 2023-07-31-12-23-44; Memory: 16%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-12-24-45; Memory: 16%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-12-25-46; Memory: 16%; Disk: 65.6% of 991.28GB
Time: 2023-07-31-12-26-46; Memory: 16%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-12-27-47; Memory: 16%; Disk: 65.8% of 991.28GB
Time: 2023-07-31-12-28-48; Memory: 16%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-12-29-49; Memory: 17%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-12-30-50; Memory: 17%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-12-31-51; Memory: 18%; Disk: 66.4% of 991.28GB
Time: 2023-07-31-12-32-52; Memory: 18%; Disk: 66.5% of 991.28GB
Time: 2023-07-31-12-33-52; Memory: 18%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-12-34-53; Memory: 18%; Disk: 66.8% of 991.28GB
Time: 2023-07-31-12-35-54; Memory: 18%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-12-36-55; Memory: 18%; Disk: 67.1% of 991.28GB
Time: 2023-07-31-12-37-56; Memory: 18%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-12-38-57; Memory: 18%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-39-58; Memory: 18%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-40-58; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-41-59; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-43-00; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-44-01; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-45-02; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-46-03; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-47-03; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-48-04; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-49-05; Memory: 19%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-50-06; Memory: 20%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-51-07; Memory: 20%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-52-08; Memory: 20%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-53-09; Memory: 20%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-54-09; Memory: 20%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-55-10; Memory: 20%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-56-11; Memory: 20%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-57-12; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-58-13; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-12-59-14; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-00-14; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-01-15; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-02-16; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-03-17; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-04-18; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-05-19; Memory: 21%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-06-20; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-07-20; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-08-21; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-09-22; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-10-23; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-11-24; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-12-25; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-13-25; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-14-26; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-15-27; Memory: 22%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-16-28; Memory: 23%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-17-29; Memory: 23%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-18-30; Memory: 23%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-13-19-31; Memory: 23%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-13-20-31; Memory: 23%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-13-21-32; Memory: 23%; Disk: 67.9% of 991.28GB
Time: 2023-07-31-13-22-33; Memory: 23%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-13-23-34; Memory: 17%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-13-24-35; Memory: 2%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-25-36; Memory: 5%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-26-36; Memory: 9%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-27-37; Memory: 10%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-28-38; Memory: 10%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-29-39; Memory: 10%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-30-40; Memory: 10%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-31-41; Memory: 10%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-32-42; Memory: 10%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-33-42; Memory: 10%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-34-43; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-35-44; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-36-45; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-37-46; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-38-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-39-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-40-48; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-41-49; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-42-50; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-43-51; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-44-52; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-45-53; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-46-53; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-47-54; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-48-55; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-49-56; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-50-57; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-51-58; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-52-58; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-53-59; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-55-00; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-56-01; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-57-02; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-58-03; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-13-59-03; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-00-04; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-01-05; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-02-06; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-03-07; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-04-08; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-05-09; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-06-09; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-07-10; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-08-11; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-09-12; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-10-13; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-11-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-12-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-13-15; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-14-16; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-15-17; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-16-18; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-17-19; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-18-20; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-19-20; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-20-21; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-21-22; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-22-23; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-23-24; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-24-25; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-25-25; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-26-26; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-27-27; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-28-28; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-29-29; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-30-30; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-31-30; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-32-31; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-33-32; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-34-33; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-35-34; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-36-35; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-37-36; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-38-36; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-39-37; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-40-38; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-41-39; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-42-40; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-43-41; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-44-41; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-45-42; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-46-43; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-47-44; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-48-45; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-49-46; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-50-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-51-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-52-48; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-53-49; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-54-50; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-55-51; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-56-52; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-57-52; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-58-53; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-14-59-54; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-00-55; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-01-56; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-02-57; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-03-57; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-04-58; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-05-59; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-07-00; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-08-01; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-09-02; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-10-03; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-11-03; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-12-04; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-13-05; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-14-06; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-15-07; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-16-08; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-17-08; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-18-09; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-19-10; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-20-11; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-21-12; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-22-13; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-23-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-24-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-25-15; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-26-16; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-27-17; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-28-18; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-29-19; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-30-19; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-31-20; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-32-21; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-33-22; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-34-23; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-35-24; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-36-25; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-37-25; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-38-26; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-39-27; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-40-28; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-41-29; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-42-30; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-43-30; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-44-31; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-45-32; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-46-33; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-47-34; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-48-35; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-49-36; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-50-36; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-51-37; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-52-38; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-53-39; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-54-40; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-55-41; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-56-41; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-57-42; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-58-43; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-15-59-44; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-00-45; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-01-46; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-02-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-03-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-04-48; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-05-49; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-06-50; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-07-51; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-08-52; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-09-52; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-10-53; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-11-54; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-12-55; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-13-56; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-14-57; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-15-58; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-16-58; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-17-59; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-19-00; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-20-01; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-21-02; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-22-03; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-23-03; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-24-04; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-25-05; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-26-06; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-27-07; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-28-08; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-29-08; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-30-09; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-31-10; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-32-11; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-33-12; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-34-13; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-35-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-36-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-37-15; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-38-16; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-39-17; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-40-18; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-41-19; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-42-19; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-43-20; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-44-21; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-45-22; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-46-23; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-47-24; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-48-25; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-49-25; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-50-26; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-51-27; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-52-28; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-53-29; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-54-30; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-55-30; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-56-31; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-57-32; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-58-33; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-16-59-34; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-00-35; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-01-36; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-02-36; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-03-37; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-04-38; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-05-39; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-06-40; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-07-41; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-08-41; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-09-42; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-10-43; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-11-44; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-12-45; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-13-46; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-14-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-15-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-16-48; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-17-49; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-18-50; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-19-51; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-20-52; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-21-52; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-22-53; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-23-54; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-24-55; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-25-56; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-26-57; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-27-58; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-28-58; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-29-59; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-31-00; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-32-01; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-33-02; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-34-03; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-35-03; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-36-04; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-37-05; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-38-06; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-39-07; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-40-08; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-41-09; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-42-09; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-43-10; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-44-11; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-45-12; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-46-13; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-47-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-48-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-49-15; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-50-16; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-51-17; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-52-18; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-53-19; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-54-19; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-55-20; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-56-21; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-57-22; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-58-23; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-17-59-24; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-00-25; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-01-25; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-02-26; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-03-27; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-04-28; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-05-29; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-06-30; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-07-30; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-08-31; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-09-32; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-10-33; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-11-34; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-12-35; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-13-36; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-14-36; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-15-37; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-16-38; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-17-39; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-18-40; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-19-41; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-20-41; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-21-42; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-22-43; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-23-44; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-24-45; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-25-46; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-26-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-27-47; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-28-48; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-29-49; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-30-50; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-31-51; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-32-52; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-33-53; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-34-53; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-35-54; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-36-55; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-37-56; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-38-57; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-39-58; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-40-58; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-41-59; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-43-00; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-44-01; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-45-02; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-46-03; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-47-04; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-48-04; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-49-05; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-50-06; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-51-07; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-52-08; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-53-09; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-54-10; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-55-10; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-56-11; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-57-12; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-58-13; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-18-59-14; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-00-15; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-01-15; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-02-16; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-03-17; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-04-18; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-05-19; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-06-20; Memory: 11%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-07-21; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-08-21; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-09-22; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-10-23; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-11-24; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-12-25; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-13-26; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-14-26; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-15-27; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-16-28; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-17-29; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-18-30; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-19-31; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-20-32; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-21-32; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-22-33; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-23-34; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-24-35; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-25-36; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-26-37; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-27-37; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-28-38; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-29-39; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-30-40; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-31-41; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-32-42; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-33-43; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-34-43; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-35-44; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-36-45; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-37-46; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-38-47; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-39-48; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-40-48; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-41-49; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-42-50; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-43-51; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-44-52; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-45-53; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-46-54; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-47-54; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-48-55; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-49-56; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-50-57; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-51-58; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-52-59; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-54-00; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-55-00; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-56-01; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-57-02; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-58-03; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-19-59-04; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-00-05; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-01-05; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-02-06; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-03-07; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-04-08; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-05-09; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-06-10; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-07-11; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-08-11; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-09-12; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-10-13; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-11-14; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-12-15; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-13-16; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-14-16; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-15-17; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-16-18; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-17-19; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-18-20; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-19-21; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-20-22; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-21-22; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-22-23; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-23-24; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-24-25; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-25-26; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-26-27; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-27-28; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-28-28; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-29-29; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-30-30; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-31-31; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-32-32; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-33-33; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-34-33; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-35-34; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-36-35; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-37-36; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-38-37; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-39-38; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-40-39; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-41-39; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-42-40; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-43-41; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-44-42; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-45-43; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-46-44; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-47-44; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-48-45; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-49-46; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-50-47; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-51-48; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-52-49; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-53-50; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-54-50; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-55-51; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-56-52; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-57-53; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-58-54; Memory: 12%; Disk: 61.9% of 991.28GB
Time: 2023-07-31-20-59-55; Memory: 12%; Disk: 62.1% of 991.28GB
Time: 2023-07-31-21-00-55; Memory: 12%; Disk: 62.4% of 991.28GB
Time: 2023-07-31-21-01-56; Memory: 12%; Disk: 62.6% of 991.28GB
Time: 2023-07-31-21-02-57; Memory: 12%; Disk: 62.7% of 991.28GB
Time: 2023-07-31-21-03-58; Memory: 12%; Disk: 62.8% of 991.28GB
Time: 2023-07-31-21-04-59; Memory: 13%; Disk: 62.9% of 991.28GB
Time: 2023-07-31-21-06-00; Memory: 13%; Disk: 63.0% of 991.28GB
Time: 2023-07-31-21-07-01; Memory: 13%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-21-08-01; Memory: 13%; Disk: 63.2% of 991.28GB
Time: 2023-07-31-21-09-02; Memory: 13%; Disk: 63.3% of 991.28GB
Time: 2023-07-31-21-10-03; Memory: 13%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-21-11-04; Memory: 13%; Disk: 63.6% of 991.28GB
Time: 2023-07-31-21-12-05; Memory: 13%; Disk: 63.8% of 991.28GB
Time: 2023-07-31-21-13-06; Memory: 13%; Disk: 63.9% of 991.28GB
Time: 2023-07-31-21-14-07; Memory: 13%; Disk: 64.0% of 991.28GB
Time: 2023-07-31-21-15-07; Memory: 13%; Disk: 64.2% of 991.28GB
Time: 2023-07-31-21-16-08; Memory: 13%; Disk: 64.3% of 991.28GB
Time: 2023-07-31-21-17-09; Memory: 13%; Disk: 64.5% of 991.28GB
Time: 2023-07-31-21-18-10; Memory: 14%; Disk: 64.6% of 991.28GB
Time: 2023-07-31-21-19-11; Memory: 14%; Disk: 64.7% of 991.28GB
Time: 2023-07-31-21-20-12; Memory: 14%; Disk: 64.9% of 991.28GB
Time: 2023-07-31-21-21-12; Memory: 14%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-21-22-13; Memory: 14%; Disk: 65.1% of 991.28GB
Time: 2023-07-31-21-23-14; Memory: 14%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-21-24-15; Memory: 14%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-21-25-16; Memory: 14%; Disk: 65.5% of 991.28GB
Time: 2023-07-31-21-26-17; Memory: 14%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-21-27-18; Memory: 14%; Disk: 65.8% of 991.28GB
Time: 2023-07-31-21-28-18; Memory: 14%; Disk: 65.9% of 991.28GB
Time: 2023-07-31-21-29-19; Memory: 14%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-21-30-20; Memory: 14%; Disk: 66.2% of 991.28GB
Time: 2023-07-31-21-31-21; Memory: 14%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-21-32-22; Memory: 14%; Disk: 66.4% of 991.28GB
Time: 2023-07-31-21-33-23; Memory: 14%; Disk: 66.6% of 991.28GB
Time: 2023-07-31-21-34-23; Memory: 14%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-21-35-24; Memory: 14%; Disk: 66.8% of 991.28GB
Time: 2023-07-31-21-36-25; Memory: 15%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-21-37-26; Memory: 15%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-21-38-27; Memory: 15%; Disk: 67.0% of 991.28GB
Time: 2023-07-31-21-39-28; Memory: 15%; Disk: 67.1% of 991.28GB
Time: 2023-07-31-21-40-29; Memory: 15%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-21-41-29; Memory: 15%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-21-42-30; Memory: 15%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-21-43-31; Memory: 15%; Disk: 67.4% of 991.28GB
Time: 2023-07-31-21-44-32; Memory: 15%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-21-45-33; Memory: 15%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-21-46-34; Memory: 15%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-21-47-34; Memory: 16%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-21-48-35; Memory: 16%; Disk: 67.8% of 991.28GB
Time: 2023-07-31-21-49-36; Memory: 16%; Disk: 67.9% of 991.28GB
Time: 2023-07-31-21-50-37; Memory: 16%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-21-51-38; Memory: 16%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-21-52-39; Memory: 16%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-21-53-40; Memory: 8%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-21-54-40; Memory: 2%; Disk: 62.4% of 991.28GB
Time: 2023-07-31-21-55-41; Memory: 2%; Disk: 62.5% of 991.28GB
Time: 2023-07-31-21-56-42; Memory: 2%; Disk: 62.6% of 991.28GB
Time: 2023-07-31-21-57-43; Memory: 2%; Disk: 62.7% of 991.28GB
Time: 2023-07-31-21-58-44; Memory: 2%; Disk: 62.9% of 991.28GB
Time: 2023-07-31-21-59-45; Memory: 2%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-22-00-46; Memory: 2%; Disk: 63.1% of 991.28GB
Time: 2023-07-31-22-01-46; Memory: 2%; Disk: 63.2% of 991.28GB
Time: 2023-07-31-22-02-47; Memory: 2%; Disk: 63.3% of 991.28GB
Time: 2023-07-31-22-03-48; Memory: 2%; Disk: 63.4% of 991.28GB
Time: 2023-07-31-22-04-49; Memory: 2%; Disk: 63.4% of 991.28GB
Time: 2023-07-31-22-05-50; Memory: 2%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-22-06-51; Memory: 2%; Disk: 63.7% of 991.28GB
Time: 2023-07-31-22-07-52; Memory: 2%; Disk: 63.8% of 991.28GB
Time: 2023-07-31-22-08-52; Memory: 2%; Disk: 64.0% of 991.28GB
Time: 2023-07-31-22-09-53; Memory: 2%; Disk: 64.1% of 991.28GB
Time: 2023-07-31-22-10-54; Memory: 2%; Disk: 64.3% of 991.28GB
Time: 2023-07-31-22-11-55; Memory: 2%; Disk: 64.4% of 991.28GB
Time: 2023-07-31-22-12-56; Memory: 2%; Disk: 64.6% of 991.28GB
Time: 2023-07-31-22-13-57; Memory: 2%; Disk: 64.7% of 991.28GB
Time: 2023-07-31-22-14-57; Memory: 2%; Disk: 64.9% of 991.28GB
Time: 2023-07-31-22-15-58; Memory: 2%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-22-16-59; Memory: 2%; Disk: 65.1% of 991.28GB
Time: 2023-07-31-22-18-00; Memory: 2%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-22-19-01; Memory: 2%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-22-20-02; Memory: 2%; Disk: 65.5% of 991.28GB
Time: 2023-07-31-22-21-03; Memory: 2%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-22-22-03; Memory: 2%; Disk: 65.8% of 991.28GB
Time: 2023-07-31-22-23-04; Memory: 2%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-22-24-05; Memory: 2%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-22-25-06; Memory: 2%; Disk: 66.2% of 991.28GB
Time: 2023-07-31-22-26-07; Memory: 2%; Disk: 66.4% of 991.28GB
Time: 2023-07-31-22-27-08; Memory: 2%; Disk: 66.5% of 991.28GB
Time: 2023-07-31-22-28-09; Memory: 2%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-22-29-09; Memory: 2%; Disk: 66.8% of 991.28GB
Time: 2023-07-31-22-30-10; Memory: 2%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-22-31-11; Memory: 2%; Disk: 67.0% of 991.28GB
Time: 2023-07-31-22-32-12; Memory: 2%; Disk: 67.0% of 991.28GB
Time: 2023-07-31-22-33-13; Memory: 2%; Disk: 67.1% of 991.28GB
Time: 2023-07-31-22-34-14; Memory: 2%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-22-35-14; Memory: 2%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-22-36-15; Memory: 2%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-22-37-16; Memory: 2%; Disk: 67.4% of 991.28GB
Time: 2023-07-31-22-38-17; Memory: 2%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-22-39-18; Memory: 2%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-22-40-19; Memory: 2%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-22-41-20; Memory: 2%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-22-42-20; Memory: 2%; Disk: 67.8% of 991.28GB
Time: 2023-07-31-22-43-21; Memory: 2%; Disk: 67.9% of 991.28GB
Time: 2023-07-31-22-44-22; Memory: 2%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-22-45-23; Memory: 2%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-22-46-24; Memory: 2%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-22-47-25; Memory: 2%; Disk: 63.4% of 991.28GB
Time: 2023-07-31-22-48-26; Memory: 2%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-22-49-26; Memory: 2%; Disk: 63.5% of 991.28GB
Time: 2023-07-31-22-50-27; Memory: 2%; Disk: 63.6% of 991.28GB
Time: 2023-07-31-22-51-28; Memory: 2%; Disk: 63.7% of 991.28GB
Time: 2023-07-31-22-52-29; Memory: 2%; Disk: 63.8% of 991.28GB
Time: 2023-07-31-22-53-30; Memory: 2%; Disk: 63.9% of 991.28GB
Time: 2023-07-31-22-54-31; Memory: 2%; Disk: 64.0% of 991.28GB
Time: 2023-07-31-22-55-31; Memory: 2%; Disk: 64.1% of 991.28GB
Time: 2023-07-31-22-56-32; Memory: 2%; Disk: 64.1% of 991.28GB
Time: 2023-07-31-22-57-33; Memory: 2%; Disk: 64.2% of 991.28GB
Time: 2023-07-31-22-58-34; Memory: 2%; Disk: 64.3% of 991.28GB
Time: 2023-07-31-22-59-35; Memory: 3%; Disk: 64.3% of 991.28GB
Time: 2023-07-31-23-00-36; Memory: 3%; Disk: 64.4% of 991.28GB
Time: 2023-07-31-23-01-36; Memory: 3%; Disk: 64.5% of 991.28GB
Time: 2023-07-31-23-02-37; Memory: 3%; Disk: 64.6% of 991.28GB
Time: 2023-07-31-23-03-38; Memory: 3%; Disk: 64.7% of 991.28GB
Time: 2023-07-31-23-04-39; Memory: 3%; Disk: 64.8% of 991.28GB
Time: 2023-07-31-23-05-40; Memory: 3%; Disk: 64.9% of 991.28GB
Time: 2023-07-31-23-06-41; Memory: 2%; Disk: 65.0% of 991.28GB
Time: 2023-07-31-23-07-41; Memory: 2%; Disk: 65.1% of 991.28GB
Time: 2023-07-31-23-08-42; Memory: 2%; Disk: 65.2% of 991.28GB
Time: 2023-07-31-23-09-43; Memory: 2%; Disk: 65.3% of 991.28GB
Time: 2023-07-31-23-10-44; Memory: 2%; Disk: 65.4% of 991.28GB
Time: 2023-07-31-23-11-45; Memory: 2%; Disk: 65.6% of 991.28GB
Time: 2023-07-31-23-12-46; Memory: 2%; Disk: 65.7% of 991.28GB
Time: 2023-07-31-23-13-47; Memory: 2%; Disk: 65.8% of 991.28GB
Time: 2023-07-31-23-14-47; Memory: 3%; Disk: 65.9% of 991.28GB
Time: 2023-07-31-23-15-48; Memory: 3%; Disk: 66.0% of 991.28GB
Time: 2023-07-31-23-16-49; Memory: 2%; Disk: 66.1% of 991.28GB
Time: 2023-07-31-23-17-50; Memory: 2%; Disk: 66.2% of 991.28GB
Time: 2023-07-31-23-18-51; Memory: 2%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-23-19-52; Memory: 3%; Disk: 66.3% of 991.28GB
Time: 2023-07-31-23-20-52; Memory: 3%; Disk: 66.4% of 991.28GB
Time: 2023-07-31-23-21-53; Memory: 3%; Disk: 66.5% of 991.28GB
Time: 2023-07-31-23-22-54; Memory: 3%; Disk: 66.6% of 991.28GB
Time: 2023-07-31-23-23-55; Memory: 3%; Disk: 66.6% of 991.28GB
Time: 2023-07-31-23-24-56; Memory: 3%; Disk: 66.7% of 991.28GB
Time: 2023-07-31-23-25-57; Memory: 3%; Disk: 66.8% of 991.28GB
Time: 2023-07-31-23-26-58; Memory: 3%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-23-27-58; Memory: 3%; Disk: 66.9% of 991.28GB
Time: 2023-07-31-23-28-59; Memory: 3%; Disk: 67.0% of 991.28GB
Time: 2023-07-31-23-30-00; Memory: 3%; Disk: 67.1% of 991.28GB
Time: 2023-07-31-23-31-01; Memory: 3%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-23-32-02; Memory: 3%; Disk: 67.2% of 991.28GB
Time: 2023-07-31-23-33-03; Memory: 3%; Disk: 67.3% of 991.28GB
Time: 2023-07-31-23-34-04; Memory: 3%; Disk: 67.4% of 991.28GB
Time: 2023-07-31-23-35-04; Memory: 3%; Disk: 67.4% of 991.28GB
Time: 2023-07-31-23-36-05; Memory: 3%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-23-37-06; Memory: 3%; Disk: 67.5% of 991.28GB
Time: 2023-07-31-23-38-07; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-23-39-08; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-23-40-09; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-23-41-09; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-23-42-10; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-07-31-23-43-11; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-07-31-23-44-12; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-07-31-23-45-13; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-07-31-23-46-14; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-07-31-23-47-15; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-23-48-15; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-07-31-23-49-16; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-23-50-17; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-23-51-18; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-23-52-19; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-07-31-23-53-20; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-23-54-20; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-07-31-23-55-21; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-23-56-22; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-23-57-23; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-23-58-24; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-07-31-23-59-25; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-00-25; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-01-26; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-02-27; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-03-28; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-04-29; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-05-30; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-06-31; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-00-07-31; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-00-08-32; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-00-09-33; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-00-10-34; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-00-11-35; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-00-12-36; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-00-13-37; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-00-14-37; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-00-15-38; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-00-16-39; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-17-40; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-18-41; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-19-42; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-20-42; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-08-01-00-21-43; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-08-01-00-22-44; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-08-01-00-23-45; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-08-01-00-24-46; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-25-47; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-26-48; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-27-48; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-28-49; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-29-50; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-30-51; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-31-52; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-00-32-53; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-00-33-53; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-00-34-54; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-00-35-55; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-00-36-56; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-00-37-57; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-00-38-58; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-00-39-59; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-00-40-59; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-00-42-00; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-43-01; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-44-02; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-45-03; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-46-04; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-00-47-04; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-08-01-00-48-05; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-08-01-00-49-06; Memory: 3%; Disk: 67.6% of 991.28GB
Time: 2023-08-01-00-50-07; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-51-08; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-52-09; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-53-10; Memory: 3%; Disk: 67.7% of 991.28GB
Time: 2023-08-01-00-54-10; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-55-11; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-56-12; Memory: 3%; Disk: 67.8% of 991.28GB
Time: 2023-08-01-00-57-13; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-00-58-14; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-00-59-15; Memory: 3%; Disk: 67.9% of 991.28GB
Time: 2023-08-01-01-00-15; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-01-01-16; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-01-02-17; Memory: 3%; Disk: 68.0% of 991.28GB
Time: 2023-08-01-01-03-18; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-01-04-19; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-01-05-20; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-01-06-21; Memory: 3%; Disk: 68.1% of 991.28GB
Time: 2023-08-01-01-07-21; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-01-08-22; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-01-09-23; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-01-10-24; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-01-11-25; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-01-12-26; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-01-13-27; Memory: 3%; Disk: 68.2% of 991.28GB
Time: 2023-08-01-01-14-27; Memory: 3%; Disk: 68.2% of 991.28GB
```
</details>

## Snakemake Log File for JSON Lines Build
<details>

</details>

## Instance Data Tracker for JSON Lines Build
<details>

</details>
