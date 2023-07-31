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

**Relevant Issue Comments:** 

## Changes to `query_kegg.py`

**Reason:** The original structure for `query_kegg.py` had the script send a request for each KEGG id to the KEGG API, one at a time. However, this is very slow. Based on the above table, this serial structure takes over 20 hours. With a longer build process than even UMLS (at 6 hours for extraction plus 8.5 hours for conversion, UMLS takes roughly 14.5 hours), this makes it a constraining script on the build. This became even more challenging because of the updates to `semmeddb_mysql_to_tuplelist_jsonl.py` and `semmeddb_tuplelist_json_to_kg_jsonl.py` to fully utilize the serial structure of JSON Lines. With that update, the SemMedDB portion of the ETL takes less than 12 hours. Thus, it was important that we sped up this extraction.

**Method:** 

**Important Code Notes:**

**Important Considerations for Maintainers:** 

**Relevant Commits:** [`255cb89`](https://github.com/RTXteam/RTX-KG2/commit/255cb8959b93314cf7f8d6be1ecbf215476acc99), [`1e68baf`](https://github.com/RTXteam/RTX-KG2/commit/1e68baf7b8f9f52f300f77012c03552e3bc2ed27), [`de5d0a5`](https://github.com/RTXteam/RTX-KG2/commit/de5d0a57fc2bd81fff86eaf51c1bc9a5a949ca50), [`a177b29`](https://github.com/RTXteam/RTX-KG2/commit/a177b2927d07dff7c00ef1d4a2de16d8c7d6584f), [`2838b76`](https://github.com/RTXteam/RTX-KG2/commit/2838b76622eef76ea8288a99f09d4dd16ef99739), [`8ad64e5`](https://github.com/RTXteam/RTX-KG2/commit/8ad64e57fa94a7eaed5656bad3e2e7df40f49b49)

**Relevant Issue Comments:** [#321 (Comment)](https://github.com/RTXteam/RTX-KG2/issues/321#issuecomment-1646443209)

## Rename Files
**Reason:** 

**Method:** 

**Important Code Notes:** 

**Important Considerations for Maintainers:** 

**Relevant Commits:** 

**Relevant Issue Comments:** 

## Stop MySQL Binary Logging
**Reason:** 

**Method:** 

**Important Code Notes:** 

**Important Considerations for Maintainers:** 

**Relevant Commits:** 

**Relevant Issue Comments:** 


## Removing Deprecated Code
**Reason:** 

**Method:** 

**Important Code Notes:** 

**Important Considerations for Maintainers:** 

**Relevant Commits:** 

**Relevant Issue Comments:** 