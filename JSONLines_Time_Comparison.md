# JSON Lines vs KG2.8.4 Build Process
## Time Comparison

All times come from Snakemake log for consistency, since this includes any lag time.

Everything that runs in parallel ran in parallel for these calculations. The scripts ran end-to-end without any gaps.

The log file for JSON Lines is in the Appendix [here](#snakemake-log-file-for-json-lines-build).

The modified log file for KG2.8.4's build is in the Appendix [here](#snakemake-log-file-for-kg284-build). It was modified to remove thousands of logging lines that made the file unviewable as Markdown in GitHub.

Snakemake Rule|JSON Lines Run Time|KG2.8.4 Run Time|JSON Lines Start Time|JSON Lines End Time|KG2.8.4 Start Time|KG2.8.4 End Time
--|--|--|--|--|--|-- 
`ChEMBL`                   |04:19:17|04:16:43|Mon Jul 31 00:47:27 2023|Mon Jul 31 05:06:44 2023|Sun Jul 30 23:16:14 2023|Mon Jul 31 03:32:57 2023
`ChEMBL_Conversion`        |00:29:08|00:25:31|Mon Jul 31 05:06:44 2023|Mon Jul 31 05:35:52 2023|Mon Jul 31 03:32:57 2023|Mon Jul 31 03:58:28 2023
`DGIdb`                    |00:00:00|00:00:00|Mon Jul 31 00:47:28 2023|Mon Jul 31 00:47:28 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:15:55 2023
`DGIdb_Conversion`         |00:00:04|00:00:08|Mon Jul 31 00:47:28 2023|Mon Jul 31 00:47:34 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:16:04 2023
`DisGeNET`                 |00:00:08|00:02:07|Mon Jul 31 00:47:26 2023|Mon Jul 31 00:47:34 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:18:02 2023
`DisGeNET_Conversion`      |00:00:31|00:00:42|Mon Jul 31 00:47:34 2023|Mon Jul 31 00:48:05 2023|Sun Jul 30 23:18:02 2023|Sun Jul 30 23:18:44 2023
`DrugBank`                 |00:00:14|00:00:12|Mon Jul 31 00:47:34 2023|Mon Jul 31 00:47:48 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:16:07 2023
`DrugBank_Conversion`      |00:06:50|00:09:04|Mon Jul 31 00:47:48 2023|Mon Jul 31 00:54:38 2023|Sun Jul 30 23:16:07 2023|Sun Jul 30 23:25:11 2023
`DrugCentral`              |00:04:22|00:04:05|Mon Jul 31 00:47:27 2023|Mon Jul 31 00:51:49 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:20:20 2023
`DrugCentral_Conversion`   |00:00:17|00:00:29|Mon Jul 31 00:51:49 2023|Mon Jul 31 00:52:06 2023|Sun Jul 30 23:20:20 2023|Sun Jul 30 23:20:49 2023
`Ensembl`                  |00:04:06|00:03:32|Mon Jul 31 00:47:27 2023|Mon Jul 31 00:51:33 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:19:28 2023
`Ensembl_Conversion`       |00:03:11|00:04:59|Mon Jul 31 00:51:33 2023|Mon Jul 31 00:54:44 2023|Sun Jul 30 23:19:28 2023|Sun Jul 30 23:24:29 2023
`Finish`                   |01:22:39|01:45:57|Mon Jul 31 23:51:40 2023|Tue Aug  1 01:14:19 2023|Wed Aug  2 22:19:39 2023|Thu Aug  3 00:05:36 2023
`GO_Annotations`           |00:00:04|00:00:05|Mon Jul 31 00:47:28 2023|Mon Jul 31 00:47:32 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:16:00 2023
`GO_Annotations_Conversion`|00:00:20|00:00:50|Mon Jul 31 00:47:32 2023|Mon Jul 31 00:47:52 2023|Sun Jul 30 23:16:00 2023|Sun Jul 30 23:16:50 2023
`HMDB`                     |00:03:05|00:01:52|Mon Jul 31 00:47:45 2023|Mon Jul 31 00:50:50 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:17:47 2023
`HMDB_Conversion`          |00:23:26|00:24:01|Mon Jul 31 00:50:50 2023|Mon Jul 31 01:14:16 2023|Sun Jul 30 23:17:47 2023|Sun Jul 30 23:41:48 2023
`IntAct`                   |00:01:26|00:01:22|Mon Jul 31 00:47:27 2023|Mon Jul 31 00:48:53 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:17:18 2023
`IntAct_Conversion`        |00:00:46|00:01:01|Mon Jul 31 00:48:53 2023|Mon Jul 31 00:49:39 2023|Sun Jul 30 23:17:18 2023|Sun Jul 30 23:18:19 2023
`JensenLab`                |00:10:01|00:12:30|Mon Jul 31 00:47:28 2023|Mon Jul 31 00:57:29 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:28:25 2023
`JensenLab_Conversion`     |00:19:58|00:19:57|Mon Jul 31 00:57:29 2023|Mon Jul 31 01:17:27 2023|Sun Jul 30 23:28:25 2023|Sun Jul 30 23:48:22 2023
`KEGG`                     |04:42:52|20:06:05|Mon Jul 31 00:47:47 2023|Mon Jul 31 05:29:39 2023|Sun Jul 30 23:15:56 2023|Mon Jul 31 19:22:01 2023
`KEGG_Conversion`          |00:00:20|00:00:33|Mon Jul 31 05:29:39 2023|Mon Jul 31 05:29:59 2023|Mon Jul 31 19:22:01 2023|Mon Jul 31 19:22:34 2023
`Merge`                    |08:30:01|10:39:43|Mon Jul 31 13:24:18 2023|Mon Jul 31 21:54:19 2023|Tue Aug  1 18:22:08 2023|Wed Aug  2 05:01:51 2023
`NCBIGene`                 |00:00:03|00:00:02|Mon Jul 31 00:47:26 2023|Mon Jul 31 00:47:29 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:15:57 2023
`NCBIGene_Conversion`      |00:00:16|00:00:42|Mon Jul 31 00:47:29 2023|Mon Jul 31 00:47:47 2023|Sun Jul 30 23:15:57 2023|Sun Jul 30 23:16:39 2023
`Ontologies_and_TTL`       |06:52:54|08:26:09|Mon Jul 31 06:31:24 2023|Mon Jul 31 13:24:18 2023|Mon Jul 31 05:17:33 2023|Mon Jul 31 13:43:42 2023
`Reactome`                 |00:07:36|00:11:33|Mon Jul 31 00:47:27 2023|Mon Jul 31 00:55:03 2023|Sun Jul 30 23:16:04 2023|Sun Jul 30 23:27:37 2023
`Reactome_Conversion`      |00:01:41|00:01:58|Mon Jul 31 00:55:03 2023|Mon Jul 31 00:56:44 2023|Sun Jul 30 23:27:37 2023|Sun Jul 30 23:29:35 2023
`RepoDB`                   |00:00:01|00:00:01|Mon Jul 31 00:47:52 2023|Mon Jul 31 00:47:53 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:15:56 2023
`RepoDB_Conversion`        |00:00:27|00:00:26|Mon Jul 31 00:47:53 2023|Mon Jul 31 00:48:20 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:16:22 2023
`SMPDB`                    |00:17:39|00:17:02|Mon Jul 31 00:47:26 2023|Mon Jul 31 01:05:05 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:32:58 2023
`SMPDB_Conversion`         |02:44:39|02:44:33|Mon Jul 31 01:05:05 2023|Mon Jul 31 03:49:44 2023|Sun Jul 30 23:32:58 2023|Mon Jul 31 02:27:31 2023
`SemMedDB`                 |11:14:41|10:46:16|Mon Jul 31 00:47:27 2023|Mon Jul 31 12:02:08 2023|Sun Jul 30 23:15:56 2023|Mon Jul 31 10:02:12 2023
`SemMedDB_Conversion`      |00:36:59|32:19:56|Mon Jul 31 12:02:08 2023|Mon Jul 31 12:39:07 2023|Mon Jul 31 10:02:12 2023|Tue Aug  1 18:22:08 2023
`Simplify`                 |00:52:36|02:38:45|Mon Jul 31 21:54:19 2023|Mon Jul 31 22:46:55 2023|Wed Aug  2 07:30:44 2023|Wed Aug  2 10:09:29 2023
`Simplify_Stats`           |00:19:37|02:28:59|Mon Jul 31 22:46:55 2023|Mon Jul 31 23:06:32 2023|Wed Aug  2 18:21:45 2023|Wed Aug  2 20:50:44 2023
`Slim`                     |00:28:58|08:12:16|Mon Jul 31 22:46:55 2023|Mon Jul 31 23:15:53 2023|Wed Aug  2 10:09:29 2023|Wed Aug  2 18:21:45 2023
`Stats`                    |00:20:19|02:28:53|Mon Jul 31 21:54:19 2023|Mon Jul 31 22:14:38 2023|Wed Aug  2 05:01:51 2023|Wed Aug  2 07:30:44 2023
`TSV`                      |01:04:45|01:28:55|Mon Jul 31 22:46:55 2023|Mon Jul 31 23:51:40 2023|Wed Aug  2 20:50:44 2023|Wed Aug  2 22:19:39 2023
`UMLS`                     |05:43:57|06:01:11|Mon Jul 31 00:47:27 2023|Mon Jul 31 06:31:24 2023|Sun Jul 30 23:16:22 2023|Mon Jul 31 05:17:33 2023
`UniChem`                  |00:15:37|00:17:07|Mon Jul 31 00:47:28 2023|Mon Jul 31 01:03:05 2023|Sun Jul 30 23:16:39 2023|Sun Jul 30 23:33:46 2023
`UniChem_Conversion`       |00:00:10|00:00:13|Mon Jul 31 01:03:05 2023|Mon Jul 31 01:03:15 2023|Sun Jul 30 23:33:46 2023|Sun Jul 30 23:33:59 2023
`UniProtKB`                |00:38:18|00:39:07|Mon Jul 31 00:47:26 2023|Mon Jul 31 01:25:44 2023|Sun Jul 30 23:15:55 2023|Sun Jul 30 23:55:02 2023
`UniProtKB_Conversion`     |00:03:06|00:03:10|Mon Jul 31 01:25:44 2023|Mon Jul 31 01:28:50 2023|Sun Jul 30 23:55:02 2023|Sun Jul 30 23:58:12 2023
`ValidationTests`          |00:00:35|00:00:34|Mon Jul 31 00:46:51 2023|Mon Jul 31 00:47:26 2023|Sun Jul 30 23:15:21 2023|Sun Jul 30 23:15:55 2023
`miRBase`                  |00:00:13|00:00:12|Mon Jul 31 00:47:26 2023|Mon Jul 31 00:47:39 2023|Sun Jul 30 23:15:56 2023|Sun Jul 30 23:16:08 2023
`miRBase_Conversion`       |00:00:06|00:00:06|Mon Jul 31 00:47:39 2023|Mon Jul 31 00:47:45 2023|Sun Jul 30 23:16:08 2023|Sun Jul 30 23:16:14 2023
--|--|--|--|--|--|-- 
Build Stage Times:         | | | | | |  
Pre-ETL                    |00:00:35|00:00:34|Mon Jul 31 00:46:51 2023|Mon Jul 31 00:47:26 2023|Sun Jul 30 23:15:21 2023|Sun Jul 30 23:15:55 2023
ETL                        |12:36:52|43:06:13|Mon Jul 31 00:47:26 2023|Mon Jul 31 13:24:18 2023|Sun Jul 30 23:15:55 2023|Tue Aug  1 18:22:08 2023
Post-ETL                   |10:27:22|27:47:31|Mon Jul 31 13:24:18 2023|Mon Jul 31 23:51:40 2023|Tue Aug  1 18:22:08 2023|Wed Aug  2 22:19:39 2023
Finish                     |01:22:39|01:45:57|Mon Jul 31 23:51:40 2023|Tue Aug  1 01:14:19 2023|Wed Aug  2 22:19:39 2023|Thu Aug  3 00:05:36 2023
--|--|--|--|--|--|-- 
Total Build Times:         | | | | | |  
Total                      |24:27:28|72:40:15|Mon Jul 31 00:46:51 2023|Tue Aug  1 01:14:19 2023|Sun Jul 30 23:15:21 2023|Thu Aug  3 00:05:36 2023

## Memory Comparison

All memory results came from the output of `primative-instance-data-tracker.sh`. For an explanation of how this works, please see [here](#memory-tracker).

Everything that runs in parallel ran in parallel for these calculations. The scripts ran end-to-end without any gaps.

The instance data file for JSON Lines is in the Appendix [here](#instance-data-tracker-for-json-lines-build).

The instance data file for KG2.8.4's build is in the Appendix [here](#instance-data-tracker-for-kg284-build).

Here is a graph of the memory usage by the JSON Lines code. This grpah also shows the memory available on an `r5a.2xlarge` and `r5a.4xlarge` instance for context on these memory values. The values were collected as percentages of the available memory on the `r5a.8xlarge` instance used for the build. This graph shows clearly that we will be able to swtich to an `r5a.4xlarge` instance with the JSON Lines code. It also suggests that we, with more optimization, could even switch to an `r5a.2xlarge` instance in the future. Note that would come will unwanted side effects, since we would have less cores, so less Snakemake rules could run at once. we currently have 5 extraction/conversion pairs that take over an hour based on the above table. With only 8 cores, this could be more of a bottleneck. Regardless, switching to an `r5a.4xlarge` should pose no problems, though there might not be enough cores to run `primative-instance-data-tracker.sh` in parallel with the build process.

![image](https://github.com/RTXteam/RTX-KG2/assets/36611732/c8d482d3-f520-42d5-b656-aeb031e64158)

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

## Snakemake Log File for KG2.8.4 Build
<details>

```
+ echo '================= starting build-kg2-snakemake.sh =================='
================= starting build-kg2-snakemake.sh ==================
+ date
Sun Jul 30 23:15:21 UTC 2023
+ snakemake_config_file=/home/ubuntu/kg2-code/snakemake-config.yaml
+ snakefile=/home/ubuntu/kg2-code/Snakefile
+ /home/ubuntu/kg2-venv/bin/python3 -u /home/ubuntu/kg2-code/generate_snakemake_config_file.py ./master-config.shinc /home/ubuntu/kg2-code/snakemake-config-var.yaml /home/ubuntu/kg2-code/snakemake-config.yaml
+ export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/ubuntu/kg2-build
+ PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/ubuntu/kg2-build
+ nodes_flag=
+ [[ '' == \t\e\s\t ]]
+ [[ all == \n\o\d\e\s ]]
+ [[ -F == \n\o\d\e\s ]]
+ [[ '' == \n\o\d\e\s ]]
+ [[ '' == \n\o\d\e\s ]]
+ graphic=
+ [[ all == \g\r\a\p\h\i\c ]]
+ [[ -F == \g\r\a\p\h\i\c ]]
+ [[ '' == \g\r\a\p\h\i\c ]]
+ [[ '' != \n\o\d\e\s ]]
+ sed -i '/\        placeholder = config\['\''SIMPLIFIED_OUTPUT_NODES_FILE_FULL'\''\]/d' /home/ubuntu/kg2-code/Snakefile-post-etl
+ sed -i '/\        slim_real = config\['\''SIMPLIFIED_OUTPUT_FILE_FULL'\''\],/c\        slim_real = config['\''SIMPLIFIED_OUTPUT_FILE_FULL'\'']' /home/ubuntu/kg2-code/Snakefile-post-etl
+ sed -i '/\        simplified_output_nodes_file_full = config\['\''SIMPLIFIED_OUTPUT_NODES_FILE_FULL'\''\],/d' /home/ubuntu/kg2-code/Snakefile-finish
+ sed -i '/\        shell("gzip -fk {input.simplified_output_nodes_file_full}")/d' /home/ubuntu/kg2-code/Snakefile-finish
+ sed -i '/\        shell(config\['\''S3_CP_CMD'\''\] + '\'' {input.simplified_output_nodes_file_full}.gz s3:\/\/'\'' + config\['\''S3_BUCKET'\''\])/d' /home/ubuntu/kg2-code/Snakefile-finish
+ echo configfile: '"/home/ubuntu/kg2-code/snakemake-config.yaml"'
+ cat /home/ubuntu/kg2-code/Snakefile-finish
+ echo 'include: "Snakefile-pre-etl"'
+ echo 'include: "Snakefile-conversion"'
+ echo 'include: "Snakefile-post-etl"'
+ [[ all == \a\l\l ]]
+ echo 'include: "Snakefile-semmeddb-extraction"'
+ [[ all == \a\l\l ]]
+ echo 'include: "Snakefile-extraction"'
+ [[ '' == \n\o\d\e\s ]]
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
	1	Jensenlab_Conversion
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

[Sun Jul 30 23:15:21 2023]
rule ValidationTests:
    output: /home/ubuntu/kg2-build/validation-placeholder.empty
    log: /home/ubuntu/kg2-build/run-validation-tests.log
    jobid: 28

[Sun Jul 30 23:15:55 2023]
Finished job 28.
1 of 48 steps (2%) done

[Sun Jul 30 23:15:55 2023]
rule DGIdb:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/dgidb/interactions.tsv
    log: /home/ubuntu/kg2-build/extract-dgidb.log
    jobid: 35


[Sun Jul 30 23:15:55 2023]
rule NCBIGene:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/ncbigene/Homo_sapiens_gene_info.tsv
    log: /home/ubuntu/kg2-build/extract-ncbigene.log
    jobid: 34


[Sun Jul 30 23:15:55 2023]
rule RepoDB:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/repodb/repodb.csv
    log: /home/ubuntu/kg2-build/download-repodb-csv.log
    jobid: 36


[Sun Jul 30 23:15:55 2023]
rule DisGeNET:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/all_gene_disease_pmid_associations.tsv
    log: /home/ubuntu/kg2-build/extract-disgenet.log
    jobid: 46


[Sun Jul 30 23:15:55 2023]
rule HMDB:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/hmdb_metabolites.xml
    log: /home/ubuntu/kg2-build/extract-hmdb.log
    jobid: 39


[Sun Jul 30 23:15:55 2023]
rule DrugCentral:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/drugcentral/drugcentral_psql_json.json
    log: /home/ubuntu/kg2-build/extract-drugcentral.log
    jobid: 44


[Sun Jul 30 23:15:55 2023]
rule GO_Annotations:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/goa_human.gpa
    log: /home/ubuntu/kg2-build/extract-go-annotations.log
    jobid: 40


[Sun Jul 30 23:15:55 2023]
rule UniProtKB:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/uniprotkb/uniprot_sprot.dat
    log: /home/ubuntu/kg2-build/extract-uniprotkb.log
    jobid: 29


[Sun Jul 30 23:15:55 2023]
rule JensenLab:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/jensenlab-placeholder.empty
    log: /home/ubuntu/kg2-build/extract-jensenlab.log
    jobid: 43


[Sun Jul 30 23:15:55 2023]
rule DrugBank:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/drugbank.xml
    log: /home/ubuntu/kg2-build/extract-drugbank.log
    jobid: 37

[Sun Jul 30 23:15:55 2023]
Finished job 35.
2 of 48 steps (4%) done

[Sun Jul 30 23:15:56 2023]
rule SMPDB:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/smpdb/pathbank_pathways.csv
    log: /home/ubuntu/kg2-build/extract-smpdb.log
    jobid: 38


[Sun Jul 30 23:15:56 2023]
rule IntAct:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/intact.txt
    log: /home/ubuntu/kg2-build/extract-intact.log
    jobid: 45


[Sun Jul 30 23:15:56 2023]
rule SemMedDB:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/semmeddb/kg2-semmeddb-tuplelist.json, /home/ubuntu/kg2-build/semmed-exclude-list.yaml
    log: /home/ubuntu/kg2-build/extract-semmeddb.log
    jobid: 30


[Sun Jul 30 23:15:56 2023]
rule KEGG:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kegg.json
    log: /home/ubuntu/kg2-build/extract-kegg.log
    jobid: 47


[Sun Jul 30 23:15:56 2023]
rule Ensembl:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/ensembl/ensembl_genes_homo_sapiens.json
    log: /home/ubuntu/kg2-build/extract-ensembl.log
    jobid: 32


[Sun Jul 30 23:15:56 2023]
rule miRBase:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/miRNA.dat
    log: /home/ubuntu/kg2-build/extract-mirbase.log
    jobid: 42


[Sun Jul 30 23:15:56 2023]
rule DGIdb_Conversion:
    input: /home/ubuntu/kg2-build/dgidb/interactions.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-dgidb.json
    log: /home/ubuntu/kg2-build/dgidb/dgidb-tsv-to-kg-json-stderr.log
    jobid: 14

[Sun Jul 30 23:15:56 2023]
Finished job 36.
3 of 48 steps (6%) done

[Sun Jul 30 23:15:56 2023]
rule RepoDB_Conversion:
    input: /home/ubuntu/kg2-build/repodb/repodb.csv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-repodb.json
    jobid: 15

[Sun Jul 30 23:15:57 2023]
Finished job 34.
4 of 48 steps (8%) done

[Sun Jul 30 23:15:57 2023]
rule NCBIGene_Conversion:
    input: /home/ubuntu/kg2-build/ncbigene/Homo_sapiens_gene_info.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-ncbigene.json
    jobid: 13

/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
[Sun Jul 30 23:16:00 2023]
Finished job 40.
5 of 48 steps (10%) done

[Sun Jul 30 23:16:00 2023]
rule GO_Annotations_Conversion:
    input: /home/ubuntu/kg2-build/goa_human.gpa, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-go-annotation.json
    log: /home/ubuntu/kg2-build/go-gpa-to-kg-json.log
    jobid: 19

[Sun Jul 30 23:16:04 2023]
Finished job 14.
6 of 48 steps (12%) done

[Sun Jul 30 23:16:04 2023]
rule Reactome:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/reactome-placeholder.empty
    log: /home/ubuntu/kg2-build/extract-reactome.log
    jobid: 41

[Sun Jul 30 23:16:07 2023]
Finished job 37.
7 of 48 steps (15%) done

[Sun Jul 30 23:16:07 2023]
rule DrugBank_Conversion:
    input: /home/ubuntu/kg2-build/drugbank.xml, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-drugbank.json
    log: /home/ubuntu/kg2-build/drugbank-xml-to-kg-json.log
    jobid: 16

[Sun Jul 30 23:16:08 2023]
Finished job 42.
8 of 48 steps (17%) done

[Sun Jul 30 23:16:08 2023]
rule miRBase_Conversion:
    input: /home/ubuntu/kg2-build/miRNA.dat, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-mirbase.json
    jobid: 21

/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
[Sun Jul 30 23:16:14 2023]
Finished job 21.
9 of 48 steps (19%) done

[Sun Jul 30 23:16:14 2023]
rule ChEMBL:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/chembl-placeholder.empty
    log: /home/ubuntu/kg2-build/extract-chembl.log
    jobid: 31

[Sun Jul 30 23:16:22 2023]
Finished job 15.
10 of 48 steps (21%) done

[Sun Jul 30 23:16:22 2023]
rule UMLS:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/umls_cuis.tsv
    log: /home/ubuntu/kg2-build/extract-umls.log
    jobid: 27

[Sun Jul 30 23:16:39 2023]
Finished job 13.
11 of 48 steps (23%) done

[Sun Jul 30 23:16:39 2023]
rule UniChem:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/unichem/unichem-mappings.tsv
    log: /home/ubuntu/kg2-build/extract-unichem.log
    jobid: 33

[Sun Jul 30 23:16:50 2023]
Finished job 19.
12 of 48 steps (25%) done
[Sun Jul 30 23:17:18 2023]
Finished job 45.
13 of 48 steps (27%) done

[Sun Jul 30 23:17:18 2023]
rule IntAct_Conversion:
    input: /home/ubuntu/kg2-build/intact.txt, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-intact.json
    jobid: 24

/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
[Sun Jul 30 23:17:47 2023]
Finished job 39.
14 of 48 steps (29%) done

[Sun Jul 30 23:17:47 2023]
rule HMDB_Conversion:
    input: /home/ubuntu/kg2-build/hmdb_metabolites.xml, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-hmdb.json
    log: /home/ubuntu/kg2-build/hmdb-xml-to-kg-json.log
    jobid: 18

[Sun Jul 30 23:18:02 2023]
Finished job 46.
15 of 48 steps (31%) done

[Sun Jul 30 23:18:02 2023]
rule DisGeNET_Conversion:
    input: /home/ubuntu/kg2-build/all_gene_disease_pmid_associations.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-disgenet.json
    jobid: 25

/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
[Sun Jul 30 23:18:19 2023]
Finished job 24.
16 of 48 steps (33%) done
[Sun Jul 30 23:18:44 2023]
Finished job 25.
17 of 48 steps (35%) done
[Sun Jul 30 23:19:28 2023]
Finished job 32.
18 of 48 steps (38%) done

[Sun Jul 30 23:19:28 2023]
rule Ensembl_Conversion:
    input: /home/ubuntu/kg2-build/ensembl/ensembl_genes_homo_sapiens.json, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-ensembl.json
    jobid: 11

/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
[Sun Jul 30 23:20:20 2023]
Finished job 44.
19 of 48 steps (40%) done

[Sun Jul 30 23:20:20 2023]
rule DrugCentral_Conversion:
    input: /home/ubuntu/kg2-build/drugcentral/drugcentral_psql_json.json, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-drugcentral.json
    log: /home/ubuntu/kg2-build/drugcentral/drugcentral-mysql-to-kg-json.log
    jobid: 23

[Sun Jul 30 23:20:49 2023]
Finished job 23.
20 of 48 steps (42%) done
[Sun Jul 30 23:24:29 2023]
Finished job 11.
21 of 48 steps (44%) done
[Sun Jul 30 23:25:11 2023]
Finished job 16.
22 of 48 steps (46%) done
[Sun Jul 30 23:27:37 2023]
Finished job 41.
23 of 48 steps (48%) done

[Sun Jul 30 23:27:37 2023]
rule Reactome_Conversion:
    input: /home/ubuntu/kg2-build/reactome-placeholder.empty, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-reactome.json
    log: /home/ubuntu/kg2-build/reactome-mysql-to-kg-json.log
    jobid: 20

[Sun Jul 30 23:28:25 2023]
Finished job 43.
24 of 48 steps (50%) done

[Sun Jul 30 23:28:25 2023]
rule Jensenlab_Conversion:
    input: /home/ubuntu/kg2-build/validation-placeholder.empty, /home/ubuntu/kg2-build/jensenlab-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-jensenlab.json
    jobid: 22

/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
[Sun Jul 30 23:29:35 2023]
Finished job 20.
25 of 48 steps (52%) done
[Sun Jul 30 23:32:58 2023]
Finished job 38.
26 of 48 steps (54%) done

[Sun Jul 30 23:32:58 2023]
rule SMPDB_Conversion:
    input: /home/ubuntu/kg2-build/smpdb/pathbank_pathways.csv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-smpdb.json
    log: /home/ubuntu/kg2-build/smpdb/smpdb-csv-to-kg-json.log
    jobid: 17

[Sun Jul 30 23:33:46 2023]
Finished job 33.
27 of 48 steps (56%) done

[Sun Jul 30 23:33:46 2023]
rule UniChem_Conversion:
    input: /home/ubuntu/kg2-build/unichem/unichem-mappings.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-unichem.json
    jobid: 12

/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
[Sun Jul 30 23:33:59 2023]
Finished job 12.
28 of 48 steps (58%) done
[Sun Jul 30 23:41:48 2023]
Finished job 18.
29 of 48 steps (60%) done
Skipped 6668 rows for lack of kg2 gene ids.
Found 21268 used kg2 gene ids.
Added 1002606 edges.
[Sun Jul 30 23:48:22 2023]
Finished job 22.
30 of 48 steps (62%) done
[Sun Jul 30 23:55:02 2023]
Finished job 29.
31 of 48 steps (65%) done

[Sun Jul 30 23:55:02 2023]
rule UniProtKB_Conversion:
    input: /home/ubuntu/kg2-build/uniprotkb/uniprot_sprot.dat, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-uniprotkb.json
    log: /home/ubuntu/kg2-build/uniprotkb-dat-to-json.log
    jobid: 8

[Sun Jul 30 23:58:12 2023]
Finished job 8.
32 of 48 steps (67%) done
[Mon Jul 31 02:27:31 2023]
Finished job 17.
33 of 48 steps (69%) done
[Mon Jul 31 03:32:57 2023]
Finished job 31.
34 of 48 steps (71%) done

[Mon Jul 31 03:32:57 2023]
rule ChEMBL_Conversion:
    input: /home/ubuntu/kg2-build/chembl-placeholder.empty, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-chembl.json
    log: /home/ubuntu/kg2-build/chembl-mysql-to-kg-json.log
    jobid: 10

[Mon Jul 31 03:58:28 2023]
Finished job 10.
35 of 48 steps (73%) done
[Mon Jul 31 05:17:33 2023]
Finished job 27.
36 of 48 steps (75%) done

[Mon Jul 31 05:17:33 2023]
rule Ontologies_and_TTL:
    input: /home/ubuntu/kg2-build/umls_cuis.tsv, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-ont.json
    log: /home/ubuntu/kg2-build/build-multi-ont-kg.log
    jobid: 7

[Mon Jul 31 10:02:12 2023]
Finished job 30.
37 of 48 steps (77%) done

[Mon Jul 31 10:02:12 2023]
rule SemMedDB_Conversion:
    input: /home/ubuntu/kg2-build/semmeddb/kg2-semmeddb-tuplelist.json, /home/ubuntu/kg2-build/umls_cuis.tsv, /home/ubuntu/kg2-build/semmed-exclude-list.yaml, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-semmeddb-edges.json
    log: /home/ubuntu/kg2-build/semmeddb-tuple-list-json-to-kg-json.log
    jobid: 9

[Mon Jul 31 13:43:42 2023]
Finished job 7.
38 of 48 steps (79%) done
[Mon Jul 31 19:22:01 2023]
Finished job 47.
39 of 48 steps (81%) done

[Mon Jul 31 19:22:01 2023]
rule KEGG_Conversion:
    input: /home/ubuntu/kg2-build/kegg.json, /home/ubuntu/kg2-build/validation-placeholder.empty
    output: /home/ubuntu/kg2-build/kg2-kegg.json
    log: /home/ubuntu/kg2-build/kegg_json_to_kg_json.log
    jobid: 26

[Mon Jul 31 19:22:34 2023]
Finished job 26.
40 of 48 steps (83%) done
[Tue Aug  1 18:22:08 2023]
Finished job 9.
41 of 48 steps (85%) done

[Tue Aug  1 18:22:08 2023]
rule Merge:
    input: /home/ubuntu/kg2-build/kg2-ont.json, /home/ubuntu/kg2-build/kg2-uniprotkb.json, /home/ubuntu/kg2-build/kg2-semmeddb-edges.json, /home/ubuntu/kg2-build/kg2-chembl.json, /home/ubuntu/kg2-build/kg2-ensembl.json, /home/ubuntu/kg2-build/kg2-unichem.json, /home/ubuntu/kg2-build/kg2-ncbigene.json, /home/ubuntu/kg2-build/kg2-dgidb.json, /home/ubuntu/kg2-build/kg2-repodb.json, /home/ubuntu/kg2-build/kg2-drugbank.json, /home/ubuntu/kg2-build/kg2-smpdb.json, /home/ubuntu/kg2-build/kg2-hmdb.json, /home/ubuntu/kg2-build/kg2-go-annotation.json, /home/ubuntu/kg2-build/kg2-reactome.json, /home/ubuntu/kg2-build/kg2-mirbase.json, /home/ubuntu/kg2-build/kg2-jensenlab.json, /home/ubuntu/kg2-build/kg2-drugcentral.json, /home/ubuntu/kg2-build/kg2-intact.json, /home/ubuntu/kg2-build/kg2-disgenet.json, /home/ubuntu/kg2-build/kg2-kegg.json
    output: /home/ubuntu/kg2-build/kg2.json, /home/ubuntu/kg2-build/kg2-orphans-edges.json
    jobid: 1

/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
[/home/ubuntu/kg2-build/kg2-ont.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-ont.json] number of nodes added: 4603676
[/home/ubuntu/kg2-build/kg2-semmeddb-edges.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-semmeddb-edges.json] number of nodes added: 38
[/home/ubuntu/kg2-build/kg2-uniprotkb.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-uniprotkb.json] number of nodes added: 26745
[/home/ubuntu/kg2-build/kg2-ensembl.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-ensembl.json] number of nodes added: 339282
[/home/ubuntu/kg2-build/kg2-unichem.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-unichem.json] number of nodes added: 1
[/home/ubuntu/kg2-build/kg2-chembl.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-chembl.json] number of nodes added: 2417027
[/home/ubuntu/kg2-build/kg2-ncbigene.json] reading nodes from file
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:9890; keeping first value: http://identifiers.org/ncbigene/9890
Warning: for NCBIGene:9890 original name of LPPR4 (human) is being overwriten to PLPPR4
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:50810; keeping first value: http://identifiers.org/ncbigene/50810
Warning: for NCBIGene:50810 original name of HDGFRP3 (human) is being overwriten to HDGFL3
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:51714; keeping first value: http://identifiers.org/ncbigene/51714
Warning: for NCBIGene:51714 original name of SELT (human) is being overwriten to SELENOT
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:54886; keeping first value: http://identifiers.org/ncbigene/54886
Warning: for NCBIGene:54886 original name of LPPR1 (human) is being overwriten to PLPPR1
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:58515; keeping first value: http://identifiers.org/ncbigene/58515
Warning: for NCBIGene:58515 original name of SELK (human) is being overwriten to SELENOK
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:64748; keeping first value: http://identifiers.org/ncbigene/64748
Warning: for NCBIGene:64748 original name of LPPR2 (human) is being overwriten to PLPPR2
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:79948; keeping first value: http://identifiers.org/ncbigene/79948
Warning: for NCBIGene:79948 original name of LPPR3 (human) is being overwriten to PLPPR3
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:83642; keeping first value: http://identifiers.org/ncbigene/83642
Warning: for NCBIGene:83642 original name of SELO (human) is being overwriten to SELENOO
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:84717; keeping first value: http://identifiers.org/ncbigene/84717
Warning: for NCBIGene:84717 original name of HDGFRP2 (human) is being overwriten to HDGFL2
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:140606; keeping first value: http://identifiers.org/ncbigene/140606
Warning: for NCBIGene:140606 original name of SELM (human) is being overwriten to SELENOM
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:157285; keeping first value: http://identifiers.org/ncbigene/157285
Warning: for NCBIGene:157285 original name of SGK223 (human) is being overwriten to PRAG1
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:163404; keeping first value: http://identifiers.org/ncbigene/163404
Warning: for NCBIGene:163404 original name of LPPR5 (human) is being overwriten to PLPPR5
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:390928; keeping first value: http://identifiers.org/ncbigene/390928
Warning: for NCBIGene:390928 original name of PAPL (human) is being overwriten to ACP7
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:100129307; keeping first value: http://identifiers.org/ncbigene/100129307
Warning: for NCBIGene:100129307 original name of LOC100129307 (human) is being overwriten to LOC100129307
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:100131107; keeping first value: http://identifiers.org/ncbigene/100131107
Warning: for NCBIGene:100131107 original name of LOC100131107 (human) is being overwriten to LOC100131107
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:101927789; keeping first value: http://identifiers.org/ncbigene/101927789
Warning: for NCBIGene:101927789 original name of LOC101927789 (human) is being overwriten to FAUP4
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:105373297; keeping first value: http://identifiers.org/ncbigene/105373297
Warning: for NCBIGene:105373297 original name of ERVFC1 (human) is being overwriten to ERVFC1
warning:  for key: iri, dropping second value: https://identifiers.org/ncbigene:107987235; keeping first value: http://identifiers.org/ncbigene/107987235
Warning: for NCBIGene:107987235 original name of LOC107987235 (human) is being overwriten to LOC107987235
[/home/ubuntu/kg2-build/kg2-ncbigene.json] number of nodes added: 191171
[/home/ubuntu/kg2-build/kg2-dgidb.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-dgidb.json] number of nodes added: 8657
[/home/ubuntu/kg2-build/kg2-repodb.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-repodb.json] number of nodes added: 1
[/home/ubuntu/kg2-build/kg2-smpdb.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-smpdb.json] number of nodes added: 3698755
[/home/ubuntu/kg2-build/kg2-drugbank.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-drugbank.json] number of nodes added: 15236
[/home/ubuntu/kg2-build/kg2-hmdb.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-hmdb.json] number of nodes added: 217921
[/home/ubuntu/kg2-build/kg2-go-annotation.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-go-annotation.json] number of nodes added: 1
[/home/ubuntu/kg2-build/kg2-reactome.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-reactome.json] number of nodes added: 74151
[/home/ubuntu/kg2-build/kg2-mirbase.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-mirbase.json] number of nodes added: 1918
[/home/ubuntu/kg2-build/kg2-jensenlab.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-jensenlab.json] number of nodes added: 1
[/home/ubuntu/kg2-build/kg2-drugcentral.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-drugcentral.json] number of nodes added: 4928
[/home/ubuntu/kg2-build/kg2-intact.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-intact.json] number of nodes added: 1
[/home/ubuntu/kg2-build/kg2-disgenet.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-disgenet.json] number of nodes added: 1
[/home/ubuntu/kg2-build/kg2-kegg.json] reading nodes from file
[/home/ubuntu/kg2-build/kg2-kegg.json] number of nodes added: 83344
[/home/ubuntu/kg2-build/kg2-ont.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-ont.json] number of edges added: 11589821
[/home/ubuntu/kg2-build/kg2-ont.json] number of orphan edges: 0
[/home/ubuntu/kg2-build/kg2-semmeddb-edges.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-semmeddb-edges.json] number of edges added: 22507763
[/home/ubuntu/kg2-build/kg2-semmeddb-edges.json] number of orphan edges: 2262909
[/home/ubuntu/kg2-build/kg2-uniprotkb.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-uniprotkb.json] number of edges added: 108640
[/home/ubuntu/kg2-build/kg2-uniprotkb.json] number of orphan edges: 29652
[/home/ubuntu/kg2-build/kg2-ensembl.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-ensembl.json] number of edges added: 2495473
[/home/ubuntu/kg2-build/kg2-ensembl.json] number of orphan edges: 1766
[/home/ubuntu/kg2-build/kg2-unichem.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-unichem.json] number of edges added: 105585
[/home/ubuntu/kg2-build/kg2-unichem.json] number of orphan edges: 71206
[/home/ubuntu/kg2-build/kg2-chembl.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-chembl.json] number of edges added: 141020
[/home/ubuntu/kg2-build/kg2-chembl.json] number of orphan edges: 6403
[/home/ubuntu/kg2-build/kg2-ncbigene.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-ncbigene.json] number of edges added: 290556
[/home/ubuntu/kg2-build/kg2-ncbigene.json] number of orphan edges: 43637
[/home/ubuntu/kg2-build/kg2-dgidb.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-dgidb.json] number of edges added: 66682
[/home/ubuntu/kg2-build/kg2-dgidb.json] number of orphan edges: 521
[/home/ubuntu/kg2-build/kg2-repodb.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-repodb.json] number of edges added: 9514
[/home/ubuntu/kg2-build/kg2-repodb.json] number of orphan edges: 1048
[/home/ubuntu/kg2-build/kg2-smpdb.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-smpdb.json] number of edges added: 27873650
[/home/ubuntu/kg2-build/kg2-smpdb.json] number of orphan edges: 2687222
[/home/ubuntu/kg2-build/kg2-drugbank.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-drugbank.json] number of edges added: 3012176
[/home/ubuntu/kg2-build/kg2-drugbank.json] number of orphan edges: 6110
[/home/ubuntu/kg2-build/kg2-hmdb.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-hmdb.json] number of edges added: 1848226
[/home/ubuntu/kg2-build/kg2-hmdb.json] number of orphan edges: 21480
[/home/ubuntu/kg2-build/kg2-go-annotation.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-go-annotation.json] number of edges added: 632266
[/home/ubuntu/kg2-build/kg2-go-annotation.json] number of orphan edges: 248
[/home/ubuntu/kg2-build/kg2-reactome.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-reactome.json] number of edges added: 274202
[/home/ubuntu/kg2-build/kg2-reactome.json] number of orphan edges: 1338
[/home/ubuntu/kg2-build/kg2-mirbase.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-mirbase.json] number of edges added: 3976
[/home/ubuntu/kg2-build/kg2-mirbase.json] number of orphan edges: 21
[/home/ubuntu/kg2-build/kg2-jensenlab.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-jensenlab.json] number of edges added: 1001829
[/home/ubuntu/kg2-build/kg2-jensenlab.json] number of orphan edges: 777
[/home/ubuntu/kg2-build/kg2-drugcentral.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-drugcentral.json] number of edges added: 91546
[/home/ubuntu/kg2-build/kg2-drugcentral.json] number of orphan edges: 329391
[/home/ubuntu/kg2-build/kg2-intact.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-intact.json] number of edges added: 483073
[/home/ubuntu/kg2-build/kg2-intact.json] number of orphan edges: 163544
[/home/ubuntu/kg2-build/kg2-disgenet.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-disgenet.json] number of edges added: 536116
[/home/ubuntu/kg2-build/kg2-disgenet.json] number of orphan edges: 5128
[/home/ubuntu/kg2-build/kg2-kegg.json] reading edges from file
[/home/ubuntu/kg2-build/kg2-kegg.json] number of edges added: 273900
[/home/ubuntu/kg2-build/kg2-kegg.json] number of orphan edges: 35178
[Wed Aug  2 05:01:51 2023]
Finished job 1.
42 of 48 steps (88%) done

[Wed Aug  2 05:01:51 2023]
rule Stats:
    input: /home/ubuntu/kg2-build/kg2.json
    output: /home/ubuntu/kg2-build/kg2-report.json
    log: /home/ubuntu/kg2-build/report_stats_on_json_kg.log
    jobid: 2

[Wed Aug  2 07:30:44 2023]
Finished job 2.
43 of 48 steps (90%) done

[Wed Aug  2 07:30:44 2023]
rule Simplify:
    input: /home/ubuntu/kg2-build/kg2.json, /home/ubuntu/kg2-build/kg2-report.json
    output: /home/ubuntu/kg2-build/kg2-simplified.json
    log: /home/ubuntu/kg2-build/filter_kg_and_remap_predicates.log
    jobid: 3

[Wed Aug  2 10:09:29 2023]
Finished job 3.
44 of 48 steps (92%) done

[Wed Aug  2 10:09:29 2023]
rule Slim:
    input: /home/ubuntu/kg2-build/kg2-simplified.json
    output: /home/ubuntu/kg2-build/kg2-slim.json
    log: /home/ubuntu/kg2-build/slim_kg2.log
    jobid: 5

[Wed Aug  2 18:21:45 2023]
Finished job 5.
45 of 48 steps (94%) done

[Wed Aug  2 18:21:45 2023]
rule Simplify_Stats:
    input: /home/ubuntu/kg2-build/kg2-simplified.json, /home/ubuntu/kg2-build/kg2-slim.json
    output: /home/ubuntu/kg2-build/kg2-simplified-report.json
    log: /home/ubuntu/kg2-build/report_stats_on_json_kg_simplified.log
    jobid: 4

[Wed Aug  2 20:50:44 2023]
Finished job 4.
46 of 48 steps (96%) done

[Wed Aug  2 20:50:44 2023]
rule TSV:
    input: /home/ubuntu/kg2-build/kg2-simplified.json, /home/ubuntu/kg2-build/kg2-simplified-report.json
    output: /home/ubuntu/kg2-build/tsv_placeholder.empty
    jobid: 6

[33mJob counts:
	count	jobs
	1	TSV
	1[0m
Start time: 2023-08-02 20:50:44
Start nodes:  2023-08-02 20:50:44
Processing node: 1000000
Processing node: 2000000
Processing node: 3000000
Processing node: 4000000
Processing node: 5000000
Processing node: 6000000
Processing node: 7000000
warning: truncating 'description field on node PathWhiz.Compound:1134 because it's too big for neo4j
warning: truncating 'description field on node PathWhiz.Compound:1099 because it's too big for neo4j
warning: truncating 'description field on node PathWhiz.Compound:3906 because it's too big for neo4j
warning: truncating 'description field on node PathWhiz.Compound:170 because it's too big for neo4j
warning: truncating 'description field on node PathWhiz.Compound:1031 because it's too big for neo4j
warning: truncating 'description field on node PathWhiz.Compound:8389 because it's too big for neo4j
warning: truncating 'description field on node PathWhiz.Compound:6578 because it's too big for neo4j
warning: truncating 'description field on node PathWhiz.Compound:65 because it's too big for neo4j
warning: truncating 'description field on node PathWhiz.Compound:749 because it's too big for neo4j
Processing node: 8000000
Finish nodes:  2023-08-02 21:15:51
Start edges:  2023-08-02 21:15:51
Processing edge: 1000000
Processing edge: 2000000
Processing edge: 3000000
Processing edge: 4000000
Processing edge: 5000000
Processing edge: 6000000
Processing edge: 7000000
Processing edge: 8000000
Processing edge: 9000000
Processing edge: 10000000
Processing edge: 11000000
Processing edge: 12000000
Processing edge: 13000000
Processing edge: 14000000
Processing edge: 15000000
Processing edge: 16000000
Processing edge: 17000000
Processing edge: 18000000
Processing edge: 19000000
Processing edge: 20000000
Processing edge: 21000000
Processing edge: 22000000
Processing edge: 23000000
Processing edge: 24000000
Processing edge: 25000000
Processing edge: 26000000
Processing edge: 27000000
Processing edge: 28000000
Processing edge: 29000000
Processing edge: 30000000
Processing edge: 31000000
Processing edge: 32000000
Processing edge: 33000000
Processing edge: 34000000
Processing edge: 35000000
Processing edge: 36000000
Processing edge: 37000000
Processing edge: 38000000
Processing edge: 39000000
Processing edge: 40000000
Processing edge: 41000000
Processing edge: 42000000
Processing edge: 43000000
Processing edge: 44000000
Processing edge: 45000000
Processing edge: 46000000
Processing edge: 47000000
Processing edge: 48000000
Processing edge: 49000000
Processing edge: 50000000
Processing edge: 51000000
Processing edge: 52000000
Processing edge: 53000000
Processing edge: 54000000
Finish edges:  2023-08-02 22:19:39
Finish time:  2023-08-02 22:19:39
[Wed Aug  2 22:19:39 2023]
Finished job 6.
47 of 48 steps (98%) done

[Wed Aug  2 22:19:39 2023]
rule Finish:
    input: /home/ubuntu/kg2-build/kg2.json, /home/ubuntu/kg2-build/kg2-orphans-edges.json, /home/ubuntu/kg2-build/kg2-report.json, /home/ubuntu/kg2-build/kg2-simplified.json, /home/ubuntu/kg2-build/kg2-simplified-report.json, /home/ubuntu/kg2-build/kg2-slim.json, /home/ubuntu/kg2-build/tsv_placeholder.empty
    jobid: 0

[33mJob counts:
	count	jobs
	1	Finish
	1[0m
+ [[ /home/ubuntu/kg2-build/kg2.json == \-\-\h\e\l\p ]]
+ [[ /home/ubuntu/kg2-build/kg2.json == \-\h ]]
+ final_output_file_full=/home/ubuntu/kg2-build/kg2.json
+ output_file_orphan_edges=/home/ubuntu/kg2-build/kg2-orphans-edges.json
+ report_file_full=/home/ubuntu/kg2-build/kg2-report.json
+ simplified_output_file_full=/home/ubuntu/kg2-build/kg2-simplified.json
+ simplified_report_file_full=/home/ubuntu/kg2-build/kg2-simplified-report.json
+ slim_output_file_full=/home/ubuntu/kg2-build/kg2-slim.json
+ kg2_tsv_dir=/home/ubuntu/kg2-build/TSV
+ s3_cp_cmd='aws s3 cp --no-progress --region us-west-2'
+ kg2_tsv_tarball=/home/ubuntu/kg2-build/kg2-tsv-for-neo4j.tar.gz
+ s3_bucket=rtx-kg2
+ s3_bucket_public=rtx-kg2-public
+ output_file_base=kg2-ont.json
+ CODE_DIR=/home/ubuntu/kg2-code
+ s3_bucket_versioned=rtx-kg2-versioned
+ BUILD_DIR=/home/ubuntu/kg2-build
+ simplified_report_file_base=kg2-simplified-report.json
+ VENV_DIR=/home/ubuntu/kg2-venv
+ previous_simplified_report_base=previous-kg2-simplified-report.json
+ echo '================= starting finish-snakemake.sh =================='
================= starting finish-snakemake.sh ==================
+ date
Wed Aug  2 22:19:39 UTC 2023
+ gzip -fk /home/ubuntu/kg2-build/kg2.json
+ tar -C /home/ubuntu/kg2-build/TSV -czvf /home/ubuntu/kg2-build/kg2-tsv-for-neo4j.tar.gz nodes.tsv nodes_header.tsv edges.tsv edges_header.tsv
nodes.tsv
nodes_header.tsv
edges.tsv
edges_header.tsv
+ gzip -fk /home/ubuntu/kg2-build/kg2-simplified.json
+ gzip -fk /home/ubuntu/kg2-build/kg2-orphans-edges.json
+ gzip -fk /home/ubuntu/kg2-build/kg2-slim.json
+ aws s3 cp --no-progress --region us-west-2 s3://rtx-kg2-public/kg2-simplified-report.json /home/ubuntu/kg2-build/previous-kg2-simplified-report.json
download: s3://rtx-kg2-public/kg2-simplified-report.json to kg2-build/previous-kg2-simplified-report.json
+ '[' 0 -eq 0 ']'
+ /home/ubuntu/kg2-venv/bin/python3 -u /home/ubuntu/kg2-code/compare_edge_reports.py /home/ubuntu/kg2-build/previous-kg2-simplified-report.json /home/ubuntu/kg2-build/kg2-simplified-report.json
/home/ubuntu/kg2-venv/lib/python3.7/site-packages/rdflib_jsonld/__init__.py:12: DeprecationWarning: The rdflib-jsonld package has been integrated into rdflib as of rdflib==6.0.0.  Please remove rdflib-jsonld from your project's dependencies.
  DeprecationWarning,
+ date
Thu Aug  3 00:05:36 UTC 2023
+ echo '================ script finished ============================'
================ script finished ============================
[Thu Aug  3 00:05:36 2023]
Finished job 0.
48 of 48 steps (100%) done
Complete log: /home/ubuntu/.snakemake/log/2023-07-30T231521.751582.snakemake.log
+ date
Thu Aug  3 00:05:36 UTC 2023
+ echo '================ script finished ============================'
================ script finished ============================

```
</details>

## Instance Data Tracker for KG2.8.4 Build
<details>

```
================= starting primative-instance-data-tracker.sh =================
Time: 2023-07-30-23-14-22; Memory: 0%; Disk: 0.6% of 991.28GB
Time: 2023-07-30-23-15-23; Memory: 0%; Disk: 0.6% of 991.28GB
Time: 2023-07-30-23-16-24; Memory: 2%; Disk: 1.6% of 991.28GB
Time: 2023-07-30-23-17-25; Memory: 2%; Disk: 4.8% of 991.28GB
Time: 2023-07-30-23-18-26; Memory: 10%; Disk: 7.9% of 991.28GB
Time: 2023-07-30-23-19-27; Memory: 8%; Disk: 9.5% of 991.28GB
Time: 2023-07-30-23-20-28; Memory: 13%; Disk: 10.6% of 991.28GB
Time: 2023-07-30-23-21-29; Memory: 14%; Disk: 12.1% of 991.28GB
Time: 2023-07-30-23-22-30; Memory: 14%; Disk: 13.4% of 991.28GB
Time: 2023-07-30-23-23-31; Memory: 15%; Disk: 14.6% of 991.28GB
Time: 2023-07-30-23-24-32; Memory: 10%; Disk: 15.6% of 991.28GB
Time: 2023-07-30-23-25-33; Memory: 8%; Disk: 16.3% of 991.28GB
Time: 2023-07-30-23-26-34; Memory: 9%; Disk: 16.9% of 991.28GB
Time: 2023-07-30-23-27-35; Memory: 9%; Disk: 17.5% of 991.28GB
Time: 2023-07-30-23-28-35; Memory: 10%; Disk: 17.7% of 991.28GB
Time: 2023-07-30-23-29-36; Memory: 13%; Disk: 17.8% of 991.28GB
Time: 2023-07-30-23-30-37; Memory: 16%; Disk: 16.4% of 991.28GB
Time: 2023-07-30-23-31-38; Memory: 16%; Disk: 16.5% of 991.28GB
Time: 2023-07-30-23-32-39; Memory: 16%; Disk: 16.6% of 991.28GB
Time: 2023-07-30-23-33-40; Memory: 17%; Disk: 16.7% of 991.28GB
Time: 2023-07-30-23-34-41; Memory: 17%; Disk: 16.8% of 991.28GB
Time: 2023-07-30-23-35-42; Memory: 17%; Disk: 16.9% of 991.28GB
Time: 2023-07-30-23-36-43; Memory: 18%; Disk: 16.9% of 991.28GB
Time: 2023-07-30-23-37-44; Memory: 14%; Disk: 17.0% of 991.28GB
Time: 2023-07-30-23-38-45; Memory: 14%; Disk: 17.2% of 991.28GB
Time: 2023-07-30-23-39-46; Memory: 15%; Disk: 17.3% of 991.28GB
Time: 2023-07-30-23-40-47; Memory: 15%; Disk: 17.4% of 991.28GB
Time: 2023-07-30-23-41-48; Memory: 9%; Disk: 17.5% of 991.28GB
Time: 2023-07-30-23-42-49; Memory: 9%; Disk: 17.6% of 991.28GB
Time: 2023-07-30-23-43-50; Memory: 9%; Disk: 17.7% of 991.28GB
Time: 2023-07-30-23-44-51; Memory: 9%; Disk: 17.8% of 991.28GB
Time: 2023-07-30-23-45-52; Memory: 9%; Disk: 17.9% of 991.28GB
Time: 2023-07-30-23-46-53; Memory: 9%; Disk: 18.1% of 991.28GB
Time: 2023-07-30-23-47-54; Memory: 9%; Disk: 18.2% of 991.28GB
Time: 2023-07-30-23-48-54; Memory: 3%; Disk: 18.3% of 991.28GB
Time: 2023-07-30-23-49-55; Memory: 3%; Disk: 18.4% of 991.28GB
Time: 2023-07-30-23-50-56; Memory: 4%; Disk: 18.5% of 991.28GB
Time: 2023-07-30-23-51-57; Memory: 4%; Disk: 18.6% of 991.28GB
Time: 2023-07-30-23-52-58; Memory: 4%; Disk: 18.7% of 991.28GB
Time: 2023-07-30-23-53-59; Memory: 4%; Disk: 18.8% of 991.28GB
Time: 2023-07-30-23-55-00; Memory: 4%; Disk: 19.5% of 991.28GB
Time: 2023-07-30-23-56-01; Memory: 4%; Disk: 19.6% of 991.28GB
Time: 2023-07-30-23-57-02; Memory: 4%; Disk: 19.7% of 991.28GB
Time: 2023-07-30-23-58-03; Memory: 5%; Disk: 19.8% of 991.28GB
Time: 2023-07-30-23-59-04; Memory: 4%; Disk: 19.9% of 991.28GB
Time: 2023-07-31-00-00-05; Memory: 5%; Disk: 20.0% of 991.28GB
Time: 2023-07-31-00-01-06; Memory: 5%; Disk: 20.1% of 991.28GB
Time: 2023-07-31-00-02-07; Memory: 5%; Disk: 20.2% of 991.28GB
Time: 2023-07-31-00-03-08; Memory: 5%; Disk: 20.2% of 991.28GB
Time: 2023-07-31-00-04-08; Memory: 5%; Disk: 20.3% of 991.28GB
Time: 2023-07-31-00-05-09; Memory: 5%; Disk: 20.4% of 991.28GB
Time: 2023-07-31-00-06-10; Memory: 5%; Disk: 20.4% of 991.28GB
Time: 2023-07-31-00-07-11; Memory: 5%; Disk: 20.5% of 991.28GB
Time: 2023-07-31-00-08-12; Memory: 5%; Disk: 20.6% of 991.28GB
Time: 2023-07-31-00-09-13; Memory: 5%; Disk: 20.7% of 991.28GB
Time: 2023-07-31-00-10-14; Memory: 6%; Disk: 20.7% of 991.28GB
Time: 2023-07-31-00-11-15; Memory: 6%; Disk: 20.8% of 991.28GB
Time: 2023-07-31-00-12-16; Memory: 6%; Disk: 20.9% of 991.28GB
Time: 2023-07-31-00-13-17; Memory: 6%; Disk: 21.0% of 991.28GB
Time: 2023-07-31-00-14-18; Memory: 6%; Disk: 21.0% of 991.28GB
Time: 2023-07-31-00-15-19; Memory: 6%; Disk: 21.1% of 991.28GB
Time: 2023-07-31-00-16-19; Memory: 6%; Disk: 21.2% of 991.28GB
Time: 2023-07-31-00-17-20; Memory: 6%; Disk: 21.2% of 991.28GB
Time: 2023-07-31-00-18-21; Memory: 6%; Disk: 21.3% of 991.28GB
Time: 2023-07-31-00-19-22; Memory: 7%; Disk: 21.4% of 991.28GB
Time: 2023-07-31-00-20-23; Memory: 7%; Disk: 21.4% of 991.28GB
Time: 2023-07-31-00-21-24; Memory: 7%; Disk: 21.5% of 991.28GB
Time: 2023-07-31-00-22-25; Memory: 7%; Disk: 21.6% of 991.28GB
Time: 2023-07-31-00-23-26; Memory: 7%; Disk: 21.6% of 991.28GB
Time: 2023-07-31-00-24-27; Memory: 7%; Disk: 21.7% of 991.28GB
Time: 2023-07-31-00-25-28; Memory: 7%; Disk: 21.8% of 991.28GB
Time: 2023-07-31-00-26-29; Memory: 7%; Disk: 21.9% of 991.28GB
Time: 2023-07-31-00-27-30; Memory: 7%; Disk: 21.9% of 991.28GB
Time: 2023-07-31-00-28-31; Memory: 7%; Disk: 22.0% of 991.28GB
Time: 2023-07-31-00-29-31; Memory: 8%; Disk: 22.1% of 991.28GB
Time: 2023-07-31-00-30-32; Memory: 8%; Disk: 22.1% of 991.28GB
Time: 2023-07-31-00-31-33; Memory: 8%; Disk: 22.2% of 991.28GB
Time: 2023-07-31-00-32-34; Memory: 8%; Disk: 22.2% of 991.28GB
Time: 2023-07-31-00-33-35; Memory: 8%; Disk: 22.3% of 991.28GB
Time: 2023-07-31-00-34-36; Memory: 8%; Disk: 22.3% of 991.28GB
Time: 2023-07-31-00-35-37; Memory: 8%; Disk: 22.4% of 991.28GB
Time: 2023-07-31-00-36-38; Memory: 8%; Disk: 22.5% of 991.28GB
Time: 2023-07-31-00-37-39; Memory: 8%; Disk: 22.5% of 991.28GB
Time: 2023-07-31-00-38-40; Memory: 9%; Disk: 22.6% of 991.28GB
Time: 2023-07-31-00-39-41; Memory: 9%; Disk: 22.7% of 991.28GB
Time: 2023-07-31-00-40-42; Memory: 9%; Disk: 22.7% of 991.28GB
Time: 2023-07-31-00-41-43; Memory: 9%; Disk: 22.8% of 991.28GB
Time: 2023-07-31-00-42-43; Memory: 9%; Disk: 22.8% of 991.28GB
Time: 2023-07-31-00-43-44; Memory: 9%; Disk: 22.9% of 991.28GB
Time: 2023-07-31-00-44-45; Memory: 9%; Disk: 23.0% of 991.28GB
Time: 2023-07-31-00-45-46; Memory: 9%; Disk: 23.0% of 991.28GB
Time: 2023-07-31-00-46-47; Memory: 9%; Disk: 23.1% of 991.28GB
Time: 2023-07-31-00-47-48; Memory: 9%; Disk: 23.2% of 991.28GB
Time: 2023-07-31-00-48-49; Memory: 9%; Disk: 23.2% of 991.28GB
Time: 2023-07-31-00-49-50; Memory: 10%; Disk: 23.3% of 991.28GB
Time: 2023-07-31-00-50-51; Memory: 10%; Disk: 23.4% of 991.28GB
Time: 2023-07-31-00-51-52; Memory: 10%; Disk: 23.4% of 991.28GB
Time: 2023-07-31-00-52-53; Memory: 10%; Disk: 23.3% of 991.28GB
Time: 2023-07-31-00-53-54; Memory: 10%; Disk: 23.4% of 991.28GB
Time: 2023-07-31-00-54-54; Memory: 10%; Disk: 23.5% of 991.28GB
Time: 2023-07-31-00-55-55; Memory: 10%; Disk: 23.5% of 991.28GB
Time: 2023-07-31-00-56-56; Memory: 10%; Disk: 23.6% of 991.28GB
Time: 2023-07-31-00-57-57; Memory: 10%; Disk: 23.7% of 991.28GB
Time: 2023-07-31-00-58-58; Memory: 10%; Disk: 23.7% of 991.28GB
Time: 2023-07-31-00-59-59; Memory: 11%; Disk: 23.8% of 991.28GB
Time: 2023-07-31-01-01-00; Memory: 11%; Disk: 23.9% of 991.28GB
Time: 2023-07-31-01-02-01; Memory: 11%; Disk: 23.9% of 991.28GB
Time: 2023-07-31-01-03-02; Memory: 11%; Disk: 24.0% of 991.28GB
Time: 2023-07-31-01-04-03; Memory: 11%; Disk: 24.1% of 991.28GB
Time: 2023-07-31-01-05-04; Memory: 11%; Disk: 24.1% of 991.28GB
Time: 2023-07-31-01-06-05; Memory: 11%; Disk: 24.2% of 991.28GB
Time: 2023-07-31-01-07-06; Memory: 11%; Disk: 24.2% of 991.28GB
Time: 2023-07-31-01-08-06; Memory: 11%; Disk: 24.3% of 991.28GB
Time: 2023-07-31-01-09-07; Memory: 11%; Disk: 24.4% of 991.28GB
Time: 2023-07-31-01-10-08; Memory: 12%; Disk: 24.4% of 991.28GB
Time: 2023-07-31-01-11-09; Memory: 12%; Disk: 24.5% of 991.28GB
Time: 2023-07-31-01-12-10; Memory: 12%; Disk: 24.5% of 991.28GB
Time: 2023-07-31-01-13-11; Memory: 12%; Disk: 24.6% of 991.28GB
Time: 2023-07-31-01-14-12; Memory: 12%; Disk: 24.6% of 991.28GB
Time: 2023-07-31-01-15-13; Memory: 12%; Disk: 24.7% of 991.28GB
Time: 2023-07-31-01-16-14; Memory: 12%; Disk: 24.7% of 991.28GB
Time: 2023-07-31-01-17-15; Memory: 12%; Disk: 24.8% of 991.28GB
Time: 2023-07-31-01-18-16; Memory: 12%; Disk: 24.9% of 991.28GB
Time: 2023-07-31-01-19-16; Memory: 12%; Disk: 24.9% of 991.28GB
Time: 2023-07-31-01-20-17; Memory: 13%; Disk: 25.0% of 991.28GB
Time: 2023-07-31-01-21-18; Memory: 13%; Disk: 25.0% of 991.28GB
Time: 2023-07-31-01-22-19; Memory: 13%; Disk: 25.1% of 991.28GB
Time: 2023-07-31-01-23-20; Memory: 13%; Disk: 25.2% of 991.28GB
Time: 2023-07-31-01-24-21; Memory: 13%; Disk: 25.2% of 991.28GB
Time: 2023-07-31-01-25-22; Memory: 13%; Disk: 25.3% of 991.28GB
Time: 2023-07-31-01-26-23; Memory: 13%; Disk: 25.3% of 991.28GB
Time: 2023-07-31-01-27-24; Memory: 13%; Disk: 25.4% of 991.28GB
Time: 2023-07-31-01-28-25; Memory: 13%; Disk: 25.5% of 991.28GB
Time: 2023-07-31-01-29-26; Memory: 13%; Disk: 25.5% of 991.28GB
Time: 2023-07-31-01-30-27; Memory: 14%; Disk: 25.6% of 991.28GB
Time: 2023-07-31-01-31-28; Memory: 14%; Disk: 25.7% of 991.28GB
Time: 2023-07-31-01-32-28; Memory: 14%; Disk: 25.7% of 991.28GB
Time: 2023-07-31-01-33-29; Memory: 14%; Disk: 25.8% of 991.28GB
Time: 2023-07-31-01-34-30; Memory: 14%; Disk: 25.9% of 991.28GB
Time: 2023-07-31-01-35-31; Memory: 14%; Disk: 26.1% of 991.28GB
Time: 2023-07-31-01-36-32; Memory: 14%; Disk: 26.3% of 991.28GB
Time: 2023-07-31-01-37-33; Memory: 14%; Disk: 26.2% of 991.28GB
Time: 2023-07-31-01-38-34; Memory: 14%; Disk: 26.2% of 991.28GB
Time: 2023-07-31-01-39-35; Memory: 15%; Disk: 26.3% of 991.28GB
Time: 2023-07-31-01-40-36; Memory: 15%; Disk: 26.4% of 991.28GB
Time: 2023-07-31-01-41-37; Memory: 15%; Disk: 26.5% of 991.28GB
Time: 2023-07-31-01-42-38; Memory: 15%; Disk: 26.2% of 991.28GB
Time: 2023-07-31-01-43-39; Memory: 15%; Disk: 26.2% of 991.28GB
Time: 2023-07-31-01-44-40; Memory: 15%; Disk: 26.3% of 991.28GB
Time: 2023-07-31-01-45-41; Memory: 15%; Disk: 26.3% of 991.28GB
Time: 2023-07-31-01-46-42; Memory: 15%; Disk: 26.4% of 991.28GB
Time: 2023-07-31-01-47-43; Memory: 15%; Disk: 26.4% of 991.28GB
Time: 2023-07-31-01-48-43; Memory: 15%; Disk: 26.5% of 991.28GB
Time: 2023-07-31-01-49-44; Memory: 16%; Disk: 26.5% of 991.28GB
Time: 2023-07-31-01-50-45; Memory: 16%; Disk: 26.6% of 991.28GB
Time: 2023-07-31-01-51-46; Memory: 16%; Disk: 26.6% of 991.28GB
Time: 2023-07-31-01-52-47; Memory: 16%; Disk: 26.6% of 991.28GB
Time: 2023-07-31-01-53-48; Memory: 16%; Disk: 26.7% of 991.28GB
Time: 2023-07-31-01-54-49; Memory: 16%; Disk: 26.8% of 991.28GB
Time: 2023-07-31-01-55-50; Memory: 16%; Disk: 27.0% of 991.28GB
Time: 2023-07-31-01-56-51; Memory: 16%; Disk: 27.1% of 991.28GB
Time: 2023-07-31-01-57-52; Memory: 16%; Disk: 27.2% of 991.28GB
Time: 2023-07-31-01-58-53; Memory: 16%; Disk: 27.4% of 991.28GB
Time: 2023-07-31-01-59-54; Memory: 16%; Disk: 27.5% of 991.28GB
Time: 2023-07-31-02-00-55; Memory: 16%; Disk: 27.6% of 991.28GB
Time: 2023-07-31-02-01-56; Memory: 16%; Disk: 27.7% of 991.28GB
Time: 2023-07-31-02-02-56; Memory: 16%; Disk: 27.9% of 991.28GB
Time: 2023-07-31-02-03-58; Memory: 16%; Disk: 27.9% of 991.28GB
Time: 2023-07-31-02-04-58; Memory: 16%; Disk: 28.1% of 991.28GB
Time: 2023-07-31-02-05-59; Memory: 16%; Disk: 28.2% of 991.28GB
Time: 2023-07-31-02-07-00; Memory: 16%; Disk: 28.3% of 991.28GB
Time: 2023-07-31-02-08-01; Memory: 16%; Disk: 28.4% of 991.28GB
Time: 2023-07-31-02-09-02; Memory: 16%; Disk: 28.5% of 991.28GB
Time: 2023-07-31-02-10-03; Memory: 16%; Disk: 28.6% of 991.28GB
Time: 2023-07-31-02-11-04; Memory: 16%; Disk: 29.0% of 991.28GB
Time: 2023-07-31-02-12-05; Memory: 16%; Disk: 29.5% of 991.28GB
Time: 2023-07-31-02-13-06; Memory: 16%; Disk: 29.6% of 991.28GB
Time: 2023-07-31-02-14-07; Memory: 16%; Disk: 29.6% of 991.28GB
Time: 2023-07-31-02-15-08; Memory: 16%; Disk: 29.4% of 991.28GB
Time: 2023-07-31-02-16-09; Memory: 16%; Disk: 29.5% of 991.28GB
Time: 2023-07-31-02-17-10; Memory: 16%; Disk: 29.7% of 991.28GB
Time: 2023-07-31-02-18-11; Memory: 16%; Disk: 29.8% of 991.28GB
Time: 2023-07-31-02-19-12; Memory: 16%; Disk: 30.0% of 991.28GB
Time: 2023-07-31-02-20-13; Memory: 16%; Disk: 30.2% of 991.28GB
Time: 2023-07-31-02-21-13; Memory: 16%; Disk: 30.4% of 991.28GB
Time: 2023-07-31-02-22-14; Memory: 16%; Disk: 30.3% of 991.28GB
Time: 2023-07-31-02-23-15; Memory: 16%; Disk: 30.4% of 991.28GB
Time: 2023-07-31-02-24-16; Memory: 16%; Disk: 30.4% of 991.28GB
Time: 2023-07-31-02-25-17; Memory: 16%; Disk: 30.5% of 991.28GB
Time: 2023-07-31-02-26-18; Memory: 16%; Disk: 30.6% of 991.28GB
Time: 2023-07-31-02-27-19; Memory: 11%; Disk: 30.7% of 991.28GB
Time: 2023-07-31-02-28-20; Memory: 3%; Disk: 30.8% of 991.28GB
Time: 2023-07-31-02-29-21; Memory: 3%; Disk: 30.9% of 991.28GB
Time: 2023-07-31-02-30-22; Memory: 3%; Disk: 31.1% of 991.28GB
Time: 2023-07-31-02-31-23; Memory: 3%; Disk: 31.1% of 991.28GB
Time: 2023-07-31-02-32-24; Memory: 3%; Disk: 31.2% of 991.28GB
Time: 2023-07-31-02-33-25; Memory: 3%; Disk: 31.2% of 991.28GB
Time: 2023-07-31-02-34-26; Memory: 3%; Disk: 31.3% of 991.28GB
Time: 2023-07-31-02-35-27; Memory: 3%; Disk: 31.5% of 991.28GB
Time: 2023-07-31-02-36-27; Memory: 3%; Disk: 31.6% of 991.28GB
Time: 2023-07-31-02-37-28; Memory: 3%; Disk: 31.7% of 991.28GB
Time: 2023-07-31-02-38-29; Memory: 3%; Disk: 31.7% of 991.28GB
Time: 2023-07-31-02-39-30; Memory: 3%; Disk: 31.8% of 991.28GB
Time: 2023-07-31-02-40-31; Memory: 3%; Disk: 32.0% of 991.28GB
Time: 2023-07-31-02-41-32; Memory: 3%; Disk: 32.0% of 991.28GB
Time: 2023-07-31-02-42-33; Memory: 3%; Disk: 32.0% of 991.28GB
Time: 2023-07-31-02-43-34; Memory: 3%; Disk: 32.1% of 991.28GB
Time: 2023-07-31-02-44-35; Memory: 3%; Disk: 32.1% of 991.28GB
Time: 2023-07-31-02-45-36; Memory: 3%; Disk: 32.3% of 991.28GB
Time: 2023-07-31-02-46-37; Memory: 3%; Disk: 32.4% of 991.28GB
Time: 2023-07-31-02-47-38; Memory: 3%; Disk: 32.5% of 991.28GB
Time: 2023-07-31-02-48-39; Memory: 3%; Disk: 32.7% of 991.28GB
Time: 2023-07-31-02-49-39; Memory: 3%; Disk: 32.8% of 991.28GB
Time: 2023-07-31-02-50-40; Memory: 3%; Disk: 33.0% of 991.28GB
Time: 2023-07-31-02-51-41; Memory: 3%; Disk: 33.2% of 991.28GB
Time: 2023-07-31-02-52-42; Memory: 3%; Disk: 33.5% of 991.28GB
Time: 2023-07-31-02-53-43; Memory: 3%; Disk: 33.7% of 991.28GB
Time: 2023-07-31-02-54-44; Memory: 3%; Disk: 33.7% of 991.28GB
Time: 2023-07-31-02-55-45; Memory: 3%; Disk: 33.7% of 991.28GB
Time: 2023-07-31-02-56-46; Memory: 3%; Disk: 33.7% of 991.28GB
Time: 2023-07-31-02-57-47; Memory: 3%; Disk: 33.8% of 991.28GB
Time: 2023-07-31-02-58-48; Memory: 3%; Disk: 33.8% of 991.28GB
Time: 2023-07-31-02-59-49; Memory: 3%; Disk: 33.5% of 991.28GB
Time: 2023-07-31-03-00-50; Memory: 3%; Disk: 33.7% of 991.28GB
Time: 2023-07-31-03-01-51; Memory: 3%; Disk: 33.9% of 991.28GB
Time: 2023-07-31-03-02-52; Memory: 3%; Disk: 33.9% of 991.28GB
Time: 2023-07-31-03-03-53; Memory: 3%; Disk: 34.0% of 991.28GB
Time: 2023-07-31-03-04-54; Memory: 3%; Disk: 34.1% of 991.28GB
Time: 2023-07-31-03-05-55; Memory: 3%; Disk: 34.2% of 991.28GB
Time: 2023-07-31-03-06-56; Memory: 3%; Disk: 34.3% of 991.28GB
Time: 2023-07-31-03-07-57; Memory: 3%; Disk: 34.4% of 991.28GB
Time: 2023-07-31-03-08-58; Memory: 3%; Disk: 34.5% of 991.28GB
Time: 2023-07-31-03-09-59; Memory: 3%; Disk: 34.6% of 991.28GB
Time: 2023-07-31-03-11-00; Memory: 3%; Disk: 34.7% of 991.28GB
Time: 2023-07-31-03-12-01; Memory: 3%; Disk: 34.7% of 991.28GB
Time: 2023-07-31-03-13-02; Memory: 3%; Disk: 34.8% of 991.28GB
Time: 2023-07-31-03-14-03; Memory: 3%; Disk: 34.9% of 991.28GB
Time: 2023-07-31-03-15-04; Memory: 3%; Disk: 35.0% of 991.28GB
Time: 2023-07-31-03-16-05; Memory: 3%; Disk: 35.2% of 991.28GB
Time: 2023-07-31-03-17-06; Memory: 3%; Disk: 35.3% of 991.28GB
Time: 2023-07-31-03-18-07; Memory: 3%; Disk: 35.4% of 991.28GB
Time: 2023-07-31-03-19-07; Memory: 3%; Disk: 35.5% of 991.28GB
Time: 2023-07-31-03-20-08; Memory: 3%; Disk: 35.6% of 991.28GB
Time: 2023-07-31-03-21-09; Memory: 3%; Disk: 35.7% of 991.28GB
Time: 2023-07-31-03-22-10; Memory: 3%; Disk: 35.7% of 991.28GB
Time: 2023-07-31-03-23-11; Memory: 3%; Disk: 35.8% of 991.28GB
Time: 2023-07-31-03-24-12; Memory: 3%; Disk: 35.9% of 991.28GB
Time: 2023-07-31-03-25-13; Memory: 3%; Disk: 36.1% of 991.28GB
Time: 2023-07-31-03-26-14; Memory: 3%; Disk: 36.2% of 991.28GB
Time: 2023-07-31-03-27-15; Memory: 3%; Disk: 36.2% of 991.28GB
Time: 2023-07-31-03-28-16; Memory: 3%; Disk: 34.9% of 991.28GB
Time: 2023-07-31-03-29-17; Memory: 3%; Disk: 35.1% of 991.28GB
Time: 2023-07-31-03-30-18; Memory: 3%; Disk: 35.2% of 991.28GB
Time: 2023-07-31-03-31-19; Memory: 3%; Disk: 35.2% of 991.28GB
Time: 2023-07-31-03-32-20; Memory: 3%; Disk: 35.3% of 991.28GB
Time: 2023-07-31-03-33-21; Memory: 3%; Disk: 35.6% of 991.28GB
Time: 2023-07-31-03-34-22; Memory: 3%; Disk: 35.6% of 991.28GB
Time: 2023-07-31-03-35-23; Memory: 4%; Disk: 35.7% of 991.28GB
Time: 2023-07-31-03-36-24; Memory: 4%; Disk: 35.7% of 991.28GB
Time: 2023-07-31-03-37-25; Memory: 4%; Disk: 35.7% of 991.28GB
Time: 2023-07-31-03-38-26; Memory: 4%; Disk: 35.7% of 991.28GB
Time: 2023-07-31-03-39-26; Memory: 4%; Disk: 35.9% of 991.28GB
Time: 2023-07-31-03-40-27; Memory: 4%; Disk: 36.0% of 991.28GB
Time: 2023-07-31-03-41-28; Memory: 4%; Disk: 36.1% of 991.28GB
Time: 2023-07-31-03-42-29; Memory: 4%; Disk: 36.1% of 991.28GB
Time: 2023-07-31-03-43-30; Memory: 4%; Disk: 36.1% of 991.28GB
Time: 2023-07-31-03-44-31; Memory: 4%; Disk: 36.1% of 991.28GB
Time: 2023-07-31-03-45-32; Memory: 4%; Disk: 36.5% of 991.28GB
Time: 2023-07-31-03-46-33; Memory: 4%; Disk: 37.0% of 991.28GB
Time: 2023-07-31-03-47-34; Memory: 4%; Disk: 37.4% of 991.28GB
Time: 2023-07-31-03-48-35; Memory: 4%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-03-49-36; Memory: 4%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-03-50-37; Memory: 4%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-03-51-38; Memory: 5%; Disk: 38.0% of 991.28GB
Time: 2023-07-31-03-52-39; Memory: 5%; Disk: 38.0% of 991.28GB
Time: 2023-07-31-03-53-40; Memory: 5%; Disk: 38.0% of 991.28GB
Time: 2023-07-31-03-54-41; Memory: 5%; Disk: 38.1% of 991.28GB
Time: 2023-07-31-03-55-42; Memory: 5%; Disk: 38.1% of 991.28GB
Time: 2023-07-31-03-56-42; Memory: 5%; Disk: 37.7% of 991.28GB
Time: 2023-07-31-03-57-43; Memory: 5%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-03-58-44; Memory: 3%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-03-59-45; Memory: 3%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-04-00-46; Memory: 3%; Disk: 38.0% of 991.28GB
Time: 2023-07-31-04-01-47; Memory: 3%; Disk: 38.0% of 991.28GB
Time: 2023-07-31-04-02-48; Memory: 3%; Disk: 38.1% of 991.28GB
Time: 2023-07-31-04-03-49; Memory: 3%; Disk: 38.1% of 991.28GB
Time: 2023-07-31-04-04-50; Memory: 3%; Disk: 38.1% of 991.28GB
Time: 2023-07-31-04-05-51; Memory: 3%; Disk: 38.2% of 991.28GB
Time: 2023-07-31-04-06-52; Memory: 3%; Disk: 38.3% of 991.28GB
Time: 2023-07-31-04-07-53; Memory: 3%; Disk: 38.4% of 991.28GB
Time: 2023-07-31-04-08-54; Memory: 3%; Disk: 38.6% of 991.28GB
Time: 2023-07-31-04-09-54; Memory: 3%; Disk: 38.7% of 991.28GB
Time: 2023-07-31-04-10-55; Memory: 3%; Disk: 38.8% of 991.28GB
Time: 2023-07-31-04-11-56; Memory: 3%; Disk: 38.8% of 991.28GB
Time: 2023-07-31-04-12-57; Memory: 3%; Disk: 38.8% of 991.28GB
Time: 2023-07-31-04-13-58; Memory: 3%; Disk: 39.0% of 991.28GB
Time: 2023-07-31-04-14-59; Memory: 3%; Disk: 39.1% of 991.28GB
Time: 2023-07-31-04-16-00; Memory: 3%; Disk: 37.6% of 991.28GB
Time: 2023-07-31-04-17-01; Memory: 3%; Disk: 37.8% of 991.28GB
Time: 2023-07-31-04-18-02; Memory: 3%; Disk: 37.8% of 991.28GB
Time: 2023-07-31-04-19-03; Memory: 3%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-04-20-04; Memory: 3%; Disk: 37.8% of 991.28GB
Time: 2023-07-31-04-21-05; Memory: 3%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-04-22-06; Memory: 3%; Disk: 37.9% of 991.28GB
Time: 2023-07-31-04-23-07; Memory: 3%; Disk: 38.1% of 991.28GB
Time: 2023-07-31-04-24-08; Memory: 3%; Disk: 38.3% of 991.28GB
Time: 2023-07-31-04-25-09; Memory: 3%; Disk: 38.4% of 991.28GB
Time: 2023-07-31-04-26-09; Memory: 3%; Disk: 38.4% of 991.28GB
Time: 2023-07-31-04-27-10; Memory: 3%; Disk: 38.3% of 991.28GB
Time: 2023-07-31-04-28-11; Memory: 3%; Disk: 38.5% of 991.28GB
Time: 2023-07-31-04-29-12; Memory: 3%; Disk: 38.6% of 991.28GB
Time: 2023-07-31-04-30-13; Memory: 3%; Disk: 38.6% of 991.28GB
Time: 2023-07-31-04-31-14; Memory: 3%; Disk: 38.6% of 991.28GB
Time: 2023-07-31-04-32-15; Memory: 3%; Disk: 38.7% of 991.28GB
Time: 2023-07-31-04-33-16; Memory: 3%; Disk: 38.8% of 991.28GB
Time: 2023-07-31-04-34-17; Memory: 3%; Disk: 38.9% of 991.28GB
Time: 2023-07-31-04-35-18; Memory: 3%; Disk: 39.0% of 991.28GB
Time: 2023-07-31-04-36-19; Memory: 3%; Disk: 39.0% of 991.28GB
Time: 2023-07-31-04-37-20; Memory: 3%; Disk: 39.1% of 991.28GB
Time: 2023-07-31-04-38-21; Memory: 3%; Disk: 39.2% of 991.28GB
Time: 2023-07-31-04-39-22; Memory: 3%; Disk: 39.3% of 991.28GB
Time: 2023-07-31-04-40-22; Memory: 3%; Disk: 39.3% of 991.28GB
Time: 2023-07-31-04-41-23; Memory: 3%; Disk: 39.4% of 991.28GB
Time: 2023-07-31-04-42-24; Memory: 3%; Disk: 39.5% of 991.28GB
Time: 2023-07-31-04-43-25; Memory: 3%; Disk: 39.5% of 991.28GB
Time: 2023-07-31-04-44-26; Memory: 4%; Disk: 39.6% of 991.28GB
Time: 2023-07-31-04-45-27; Memory: 3%; Disk: 39.7% of 991.28GB
Time: 2023-07-31-04-46-28; Memory: 3%; Disk: 39.7% of 991.28GB
Time: 2023-07-31-04-47-29; Memory: 3%; Disk: 39.8% of 991.28GB
Time: 2023-07-31-04-48-30; Memory: 3%; Disk: 39.8% of 991.28GB
Time: 2023-07-31-04-49-31; Memory: 3%; Disk: 39.9% of 991.28GB
Time: 2023-07-31-04-50-32; Memory: 3%; Disk: 39.9% of 991.28GB
Time: 2023-07-31-04-51-33; Memory: 3%; Disk: 39.9% of 991.28GB
Time: 2023-07-31-04-52-34; Memory: 4%; Disk: 40.0% of 991.28GB
Time: 2023-07-31-04-53-35; Memory: 4%; Disk: 40.1% of 991.28GB
Time: 2023-07-31-04-54-35; Memory: 5%; Disk: 40.1% of 991.28GB
Time: 2023-07-31-04-55-36; Memory: 5%; Disk: 40.1% of 991.28GB
Time: 2023-07-31-04-56-37; Memory: 5%; Disk: 40.2% of 991.28GB
Time: 2023-07-31-04-57-38; Memory: 5%; Disk: 40.2% of 991.28GB
Time: 2023-07-31-04-58-39; Memory: 5%; Disk: 40.3% of 991.28GB
Time: 2023-07-31-04-59-40; Memory: 5%; Disk: 40.3% of 991.28GB
Time: 2023-07-31-05-00-41; Memory: 3%; Disk: 40.4% of 991.28GB
Time: 2023-07-31-05-01-42; Memory: 3%; Disk: 40.4% of 991.28GB
Time: 2023-07-31-05-02-43; Memory: 3%; Disk: 40.5% of 991.28GB
Time: 2023-07-31-05-03-44; Memory: 4%; Disk: 40.5% of 991.28GB
Time: 2023-07-31-05-04-45; Memory: 4%; Disk: 40.5% of 991.28GB
Time: 2023-07-31-05-05-46; Memory: 4%; Disk: 40.6% of 991.28GB
Time: 2023-07-31-05-06-47; Memory: 4%; Disk: 40.7% of 991.28GB
Time: 2023-07-31-05-07-47; Memory: 4%; Disk: 40.8% of 991.28GB
Time: 2023-07-31-05-08-48; Memory: 3%; Disk: 40.8% of 991.28GB
Time: 2023-07-31-05-09-49; Memory: 4%; Disk: 40.9% of 991.28GB
Time: 2023-07-31-05-10-50; Memory: 4%; Disk: 40.9% of 991.28GB
Time: 2023-07-31-05-11-51; Memory: 3%; Disk: 40.9% of 991.28GB
Time: 2023-07-31-05-12-52; Memory: 4%; Disk: 41.0% of 991.28GB
Time: 2023-07-31-05-13-53; Memory: 3%; Disk: 41.0% of 991.28GB
Time: 2023-07-31-05-14-54; Memory: 3%; Disk: 41.1% of 991.28GB
Time: 2023-07-31-05-15-55; Memory: 3%; Disk: 41.1% of 991.28GB
Time: 2023-07-31-05-16-56; Memory: 3%; Disk: 41.2% of 991.28GB
Time: 2023-07-31-05-17-57; Memory: 4%; Disk: 41.3% of 991.28GB
Time: 2023-07-31-05-18-58; Memory: 4%; Disk: 41.4% of 991.28GB
Time: 2023-07-31-05-19-59; Memory: 3%; Disk: 41.4% of 991.28GB
Time: 2023-07-31-05-21-00; Memory: 3%; Disk: 41.5% of 991.28GB
Time: 2023-07-31-05-22-00; Memory: 3%; Disk: 41.6% of 991.28GB
Time: 2023-07-31-05-23-01; Memory: 5%; Disk: 41.6% of 991.28GB
Time: 2023-07-31-05-24-02; Memory: 3%; Disk: 41.7% of 991.28GB
Time: 2023-07-31-05-25-03; Memory: 3%; Disk: 41.8% of 991.28GB
Time: 2023-07-31-05-26-04; Memory: 3%; Disk: 41.8% of 991.28GB
Time: 2023-07-31-05-27-05; Memory: 4%; Disk: 41.9% of 991.28GB
Time: 2023-07-31-05-28-06; Memory: 4%; Disk: 42.0% of 991.28GB
Time: 2023-07-31-05-29-07; Memory: 4%; Disk: 42.0% of 991.28GB
Time: 2023-07-31-05-30-08; Memory: 4%; Disk: 42.1% of 991.28GB
Time: 2023-07-31-05-31-09; Memory: 4%; Disk: 42.2% of 991.28GB
Time: 2023-07-31-05-32-10; Memory: 4%; Disk: 42.2% of 991.28GB
Time: 2023-07-31-05-33-10; Memory: 4%; Disk: 42.3% of 991.28GB
Time: 2023-07-31-05-34-11; Memory: 4%; Disk: 42.4% of 991.28GB
Time: 2023-07-31-05-35-12; Memory: 4%; Disk: 42.4% of 991.28GB
Time: 2023-07-31-05-36-13; Memory: 4%; Disk: 42.5% of 991.28GB
Time: 2023-07-31-05-37-14; Memory: 4%; Disk: 42.5% of 991.28GB
Time: 2023-07-31-05-38-15; Memory: 4%; Disk: 42.6% of 991.28GB
Time: 2023-07-31-05-39-16; Memory: 9%; Disk: 42.7% of 991.28GB
Time: 2023-07-31-05-40-17; Memory: 12%; Disk: 42.7% of 991.28GB
Time: 2023-07-31-05-41-18; Memory: 14%; Disk: 42.8% of 991.28GB
Time: 2023-07-31-05-42-19; Memory: 5%; Disk: 42.9% of 991.28GB
Time: 2023-07-31-05-43-20; Memory: 5%; Disk: 43.0% of 991.28GB
Time: 2023-07-31-05-44-21; Memory: 5%; Disk: 43.1% of 991.28GB
Time: 2023-07-31-05-45-22; Memory: 5%; Disk: 43.1% of 991.28GB
Time: 2023-07-31-05-46-23; Memory: 5%; Disk: 43.2% of 991.28GB
Time: 2023-07-31-05-47-24; Memory: 5%; Disk: 43.3% of 991.28GB
Time: 2023-07-31-05-48-25; Memory: 5%; Disk: 43.3% of 991.28GB
Time: 2023-07-31-05-49-26; Memory: 5%; Disk: 43.4% of 991.28GB
Time: 2023-07-31-05-50-27; Memory: 5%; Disk: 43.4% of 991.28GB
Time: 2023-07-31-05-51-28; Memory: 5%; Disk: 43.5% of 991.28GB
Time: 2023-07-31-05-52-29; Memory: 5%; Disk: 43.6% of 991.28GB
Time: 2023-07-31-05-53-30; Memory: 5%; Disk: 43.6% of 991.28GB
Time: 2023-07-31-05-54-31; Memory: 5%; Disk: 43.7% of 991.28GB
Time: 2023-07-31-05-55-32; Memory: 5%; Disk: 43.8% of 991.28GB
Time: 2023-07-31-05-56-33; Memory: 5%; Disk: 43.8% of 991.28GB
Time: 2023-07-31-05-57-34; Memory: 5%; Disk: 43.9% of 991.28GB
Time: 2023-07-31-05-58-35; Memory: 5%; Disk: 44.0% of 991.28GB
Time: 2023-07-31-05-59-36; Memory: 5%; Disk: 44.0% of 991.28GB
Time: 2023-07-31-06-00-36; Memory: 5%; Disk: 44.1% of 991.28GB
Time: 2023-07-31-06-01-37; Memory: 5%; Disk: 44.1% of 991.28GB
Time: 2023-07-31-06-02-38; Memory: 6%; Disk: 44.2% of 991.28GB
Time: 2023-07-31-06-03-39; Memory: 7%; Disk: 44.2% of 991.28GB
Time: 2023-07-31-06-04-40; Memory: 10%; Disk: 44.3% of 991.28GB
Time: 2023-07-31-06-05-41; Memory: 14%; Disk: 44.4% of 991.28GB
Time: 2023-07-31-06-06-42; Memory: 6%; Disk: 44.5% of 991.28GB
Time: 2023-07-31-06-07-43; Memory: 6%; Disk: 44.5% of 991.28GB
Time: 2023-07-31-06-08-44; Memory: 6%; Disk: 44.6% of 991.28GB
Time: 2023-07-31-06-09-45; Memory: 6%; Disk: 44.7% of 991.28GB
Time: 2023-07-31-06-10-46; Memory: 6%; Disk: 44.7% of 991.28GB
Time: 2023-07-31-06-11-47; Memory: 6%; Disk: 44.8% of 991.28GB
Time: 2023-07-31-06-12-48; Memory: 6%; Disk: 44.8% of 991.28GB
Time: 2023-07-31-06-13-49; Memory: 6%; Disk: 44.9% of 991.28GB
Time: 2023-07-31-06-14-50; Memory: 6%; Disk: 45.0% of 991.28GB
Time: 2023-07-31-06-15-51; Memory: 6%; Disk: 45.0% of 991.28GB
Time: 2023-07-31-06-16-52; Memory: 6%; Disk: 45.1% of 991.28GB
Time: 2023-07-31-06-17-53; Memory: 6%; Disk: 45.2% of 991.28GB
Time: 2023-07-31-06-18-54; Memory: 6%; Disk: 45.2% of 991.28GB
Time: 2023-07-31-06-19-55; Memory: 6%; Disk: 45.3% of 991.28GB
Time: 2023-07-31-06-20-56; Memory: 6%; Disk: 45.4% of 991.28GB
Time: 2023-07-31-06-21-57; Memory: 6%; Disk: 45.4% of 991.28GB
Time: 2023-07-31-06-22-58; Memory: 6%; Disk: 45.5% of 991.28GB
Time: 2023-07-31-06-23-59; Memory: 10%; Disk: 45.5% of 991.28GB
Time: 2023-07-31-06-25-00; Memory: 7%; Disk: 45.6% of 991.28GB
Time: 2023-07-31-06-26-00; Memory: 7%; Disk: 45.6% of 991.28GB
Time: 2023-07-31-06-27-01; Memory: 7%; Disk: 45.6% of 991.28GB
Time: 2023-07-31-06-28-02; Memory: 7%; Disk: 45.7% of 991.28GB
Time: 2023-07-31-06-29-03; Memory: 7%; Disk: 45.7% of 991.28GB
Time: 2023-07-31-06-30-04; Memory: 7%; Disk: 45.7% of 991.28GB
Time: 2023-07-31-06-31-05; Memory: 7%; Disk: 45.8% of 991.28GB
Time: 2023-07-31-06-32-06; Memory: 7%; Disk: 45.8% of 991.28GB
Time: 2023-07-31-06-33-07; Memory: 7%; Disk: 45.9% of 991.28GB
Time: 2023-07-31-06-34-08; Memory: 7%; Disk: 45.9% of 991.28GB
Time: 2023-07-31-06-35-09; Memory: 7%; Disk: 45.9% of 991.28GB
Time: 2023-07-31-06-36-10; Memory: 7%; Disk: 46.0% of 991.28GB
Time: 2023-07-31-06-37-11; Memory: 7%; Disk: 46.0% of 991.28GB
Time: 2023-07-31-06-38-12; Memory: 7%; Disk: 46.0% of 991.28GB
Time: 2023-07-31-06-39-13; Memory: 7%; Disk: 46.1% of 991.28GB
Time: 2023-07-31-06-40-14; Memory: 7%; Disk: 46.1% of 991.28GB
Time: 2023-07-31-06-41-15; Memory: 7%; Disk: 46.2% of 991.28GB
Time: 2023-07-31-06-42-16; Memory: 7%; Disk: 46.2% of 991.28GB
Time: 2023-07-31-06-43-17; Memory: 7%; Disk: 46.2% of 991.28GB
Time: 2023-07-31-06-44-18; Memory: 7%; Disk: 46.3% of 991.28GB
Time: 2023-07-31-06-45-19; Memory: 7%; Disk: 46.3% of 991.28GB
Time: 2023-07-31-06-46-20; Memory: 7%; Disk: 46.3% of 991.28GB
Time: 2023-07-31-06-47-21; Memory: 11%; Disk: 46.4% of 991.28GB
Time: 2023-07-31-06-48-22; Memory: 8%; Disk: 46.4% of 991.28GB
Time: 2023-07-31-06-49-23; Memory: 8%; Disk: 46.5% of 991.28GB
Time: 2023-07-31-06-50-23; Memory: 8%; Disk: 46.5% of 991.28GB
Time: 2023-07-31-06-51-24; Memory: 8%; Disk: 46.6% of 991.28GB
Time: 2023-07-31-06-52-25; Memory: 8%; Disk: 46.6% of 991.28GB
Time: 2023-07-31-06-53-26; Memory: 8%; Disk: 46.6% of 991.28GB
Time: 2023-07-31-06-54-27; Memory: 8%; Disk: 46.7% of 991.28GB
Time: 2023-07-31-06-55-28; Memory: 8%; Disk: 46.7% of 991.28GB
Time: 2023-07-31-06-56-29; Memory: 8%; Disk: 46.7% of 991.28GB
Time: 2023-07-31-06-57-30; Memory: 8%; Disk: 46.8% of 991.28GB
Time: 2023-07-31-06-58-31; Memory: 8%; Disk: 46.8% of 991.28GB
Time: 2023-07-31-06-59-32; Memory: 8%; Disk: 46.9% of 991.28GB
Time: 2023-07-31-07-00-33; Memory: 8%; Disk: 46.9% of 991.28GB
Time: 2023-07-31-07-01-34; Memory: 8%; Disk: 47.0% of 991.28GB
Time: 2023-07-31-07-02-34; Memory: 8%; Disk: 47.0% of 991.28GB
Time: 2023-07-31-07-03-35; Memory: 8%; Disk: 47.0% of 991.28GB
Time: 2023-07-31-07-04-36; Memory: 8%; Disk: 47.1% of 991.28GB
Time: 2023-07-31-07-05-37; Memory: 8%; Disk: 47.1% of 991.28GB
Time: 2023-07-31-07-06-38; Memory: 8%; Disk: 47.2% of 991.28GB
Time: 2023-07-31-07-07-39; Memory: 8%; Disk: 47.2% of 991.28GB
Time: 2023-07-31-07-08-40; Memory: 8%; Disk: 47.2% of 991.28GB
Time: 2023-07-31-07-09-41; Memory: 8%; Disk: 47.3% of 991.28GB
Time: 2023-07-31-07-10-42; Memory: 8%; Disk: 47.3% of 991.28GB
Time: 2023-07-31-07-11-43; Memory: 8%; Disk: 47.4% of 991.28GB
Time: 2023-07-31-07-12-44; Memory: 8%; Disk: 47.4% of 991.28GB
Time: 2023-07-31-07-13-44; Memory: 8%; Disk: 47.4% of 991.28GB
Time: 2023-07-31-07-14-45; Memory: 8%; Disk: 47.5% of 991.28GB
Time: 2023-07-31-07-15-46; Memory: 8%; Disk: 47.5% of 991.28GB
Time: 2023-07-31-07-16-47; Memory: 8%; Disk: 47.5% of 991.28GB
Time: 2023-07-31-07-17-48; Memory: 8%; Disk: 47.6% of 991.28GB
Time: 2023-07-31-07-18-49; Memory: 8%; Disk: 47.6% of 991.28GB
Time: 2023-07-31-07-19-50; Memory: 8%; Disk: 47.7% of 991.28GB
Time: 2023-07-31-07-20-51; Memory: 8%; Disk: 47.7% of 991.28GB
Time: 2023-07-31-07-21-52; Memory: 8%; Disk: 47.7% of 991.28GB
Time: 2023-07-31-07-22-53; Memory: 9%; Disk: 47.9% of 991.28GB
Time: 2023-07-31-07-23-53; Memory: 11%; Disk: 47.9% of 991.28GB
Time: 2023-07-31-07-24-54; Memory: 8%; Disk: 48.0% of 991.28GB
Time: 2023-07-31-07-25-55; Memory: 8%; Disk: 48.0% of 991.28GB
Time: 2023-07-31-07-26-56; Memory: 8%; Disk: 48.0% of 991.28GB
Time: 2023-07-31-07-27-57; Memory: 8%; Disk: 48.1% of 991.28GB
Time: 2023-07-31-07-28-58; Memory: 8%; Disk: 48.1% of 991.28GB
Time: 2023-07-31-07-29-59; Memory: 9%; Disk: 48.2% of 991.28GB
Time: 2023-07-31-07-31-00; Memory: 9%; Disk: 48.2% of 991.28GB
Time: 2023-07-31-07-32-01; Memory: 9%; Disk: 48.3% of 991.28GB
Time: 2023-07-31-07-33-02; Memory: 9%; Disk: 48.3% of 991.28GB
Time: 2023-07-31-07-34-03; Memory: 9%; Disk: 48.3% of 991.28GB
Time: 2023-07-31-07-35-04; Memory: 9%; Disk: 48.4% of 991.28GB
Time: 2023-07-31-07-36-05; Memory: 9%; Disk: 48.4% of 991.28GB
Time: 2023-07-31-07-37-06; Memory: 9%; Disk: 48.4% of 991.28GB
Time: 2023-07-31-07-38-07; Memory: 9%; Disk: 48.5% of 991.28GB
Time: 2023-07-31-07-39-08; Memory: 9%; Disk: 48.5% of 991.28GB
Time: 2023-07-31-07-40-09; Memory: 9%; Disk: 48.5% of 991.28GB
Time: 2023-07-31-07-41-10; Memory: 9%; Disk: 48.6% of 991.28GB
Time: 2023-07-31-07-42-11; Memory: 9%; Disk: 48.6% of 991.28GB
Time: 2023-07-31-07-43-12; Memory: 10%; Disk: 48.6% of 991.28GB
Time: 2023-07-31-07-44-13; Memory: 9%; Disk: 48.7% of 991.28GB
Time: 2023-07-31-07-45-14; Memory: 9%; Disk: 48.8% of 991.28GB
Time: 2023-07-31-07-46-15; Memory: 9%; Disk: 48.8% of 991.28GB
Time: 2023-07-31-07-47-16; Memory: 9%; Disk: 48.9% of 991.28GB
Time: 2023-07-31-07-48-16; Memory: 9%; Disk: 49.0% of 991.28GB
Time: 2023-07-31-07-49-17; Memory: 9%; Disk: 49.0% of 991.28GB
Time: 2023-07-31-07-50-18; Memory: 9%; Disk: 49.1% of 991.28GB
Time: 2023-07-31-07-51-19; Memory: 9%; Disk: 49.2% of 991.28GB
Time: 2023-07-31-07-52-20; Memory: 9%; Disk: 49.2% of 991.28GB
Time: 2023-07-31-07-53-21; Memory: 9%; Disk: 49.3% of 991.28GB
Time: 2023-07-31-07-54-22; Memory: 9%; Disk: 49.3% of 991.28GB
Time: 2023-07-31-07-55-23; Memory: 9%; Disk: 49.4% of 991.28GB
Time: 2023-07-31-07-56-24; Memory: 9%; Disk: 49.5% of 991.28GB
Time: 2023-07-31-07-57-25; Memory: 9%; Disk: 49.5% of 991.28GB
Time: 2023-07-31-07-58-26; Memory: 9%; Disk: 49.6% of 991.28GB
Time: 2023-07-31-07-59-27; Memory: 9%; Disk: 49.7% of 991.28GB
Time: 2023-07-31-08-00-27; Memory: 9%; Disk: 49.7% of 991.28GB
Time: 2023-07-31-08-01-28; Memory: 9%; Disk: 49.8% of 991.28GB
Time: 2023-07-31-08-02-29; Memory: 9%; Disk: 49.9% of 991.28GB
Time: 2023-07-31-08-03-30; Memory: 9%; Disk: 49.9% of 991.28GB
Time: 2023-07-31-08-04-31; Memory: 9%; Disk: 50.0% of 991.28GB
Time: 2023-07-31-08-05-32; Memory: 9%; Disk: 50.0% of 991.28GB
Time: 2023-07-31-08-06-33; Memory: 9%; Disk: 50.1% of 991.28GB
Time: 2023-07-31-08-07-34; Memory: 9%; Disk: 50.1% of 991.28GB
Time: 2023-07-31-08-08-35; Memory: 9%; Disk: 50.2% of 991.28GB
Time: 2023-07-31-08-09-36; Memory: 9%; Disk: 50.2% of 991.28GB
Time: 2023-07-31-08-10-37; Memory: 9%; Disk: 50.3% of 991.28GB
Time: 2023-07-31-08-11-38; Memory: 9%; Disk: 50.4% of 991.28GB
Time: 2023-07-31-08-12-38; Memory: 9%; Disk: 50.4% of 991.28GB
Time: 2023-07-31-08-13-39; Memory: 10%; Disk: 50.5% of 991.28GB
Time: 2023-07-31-08-14-40; Memory: 10%; Disk: 50.5% of 991.28GB
Time: 2023-07-31-08-15-41; Memory: 10%; Disk: 50.6% of 991.28GB
Time: 2023-07-31-08-16-42; Memory: 10%; Disk: 50.6% of 991.28GB
Time: 2023-07-31-08-17-43; Memory: 10%; Disk: 50.7% of 991.28GB
Time: 2023-07-31-08-18-44; Memory: 10%; Disk: 50.8% of 991.28GB
Time: 2023-07-31-08-19-45; Memory: 10%; Disk: 50.8% of 991.28GB
Time: 2023-07-31-08-20-46; Memory: 10%; Disk: 50.9% of 991.28GB
Time: 2023-07-31-08-21-47; Memory: 10%; Disk: 50.9% of 991.28GB
Time: 2023-07-31-08-22-48; Memory: 10%; Disk: 51.0% of 991.28GB
Time: 2023-07-31-08-23-49; Memory: 10%; Disk: 51.1% of 991.28GB
Time: 2023-07-31-08-24-49; Memory: 10%; Disk: 51.1% of 991.28GB
Time: 2023-07-31-08-25-50; Memory: 10%; Disk: 51.2% of 991.28GB
Time: 2023-07-31-08-26-51; Memory: 10%; Disk: 51.2% of 991.28GB
Time: 2023-07-31-08-27-52; Memory: 10%; Disk: 51.3% of 991.28GB
Time: 2023-07-31-08-28-53; Memory: 10%; Disk: 51.4% of 991.28GB
Time: 2023-07-31-08-29-54; Memory: 10%; Disk: 51.4% of 991.28GB
Time: 2023-07-31-08-30-55; Memory: 10%; Disk: 51.5% of 991.28GB
Time: 2023-07-31-08-31-56; Memory: 10%; Disk: 51.5% of 991.28GB
Time: 2023-07-31-08-32-57; Memory: 10%; Disk: 51.6% of 991.28GB
Time: 2023-07-31-08-33-58; Memory: 10%; Disk: 51.6% of 991.28GB
Time: 2023-07-31-08-34-59; Memory: 10%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-36-00; Memory: 10%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-37-01; Memory: 10%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-38-01; Memory: 11%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-39-02; Memory: 11%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-40-03; Memory: 12%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-41-04; Memory: 12%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-42-05; Memory: 12%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-43-06; Memory: 13%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-44-07; Memory: 13%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-45-08; Memory: 14%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-46-09; Memory: 14%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-47-10; Memory: 15%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-48-11; Memory: 15%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-49-12; Memory: 15%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-50-12; Memory: 16%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-51-13; Memory: 16%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-52-14; Memory: 17%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-53-15; Memory: 18%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-54-16; Memory: 18%; Disk: 51.7% of 991.28GB
Time: 2023-07-31-08-55-17; Memory: 20%; Disk: 51.8% of 991.28GB
Time: 2023-07-31-08-56-18; Memory: 23%; Disk: 51.8% of 991.28GB
Time: 2023-07-31-08-57-19; Memory: 26%; Disk: 51.8% of 991.28GB
Time: 2023-07-31-08-58-20; Memory: 20%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-08-59-21; Memory: 21%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-00-22; Memory: 22%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-01-23; Memory: 22%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-02-24; Memory: 23%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-03-25; Memory: 23%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-04-25; Memory: 24%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-05-26; Memory: 25%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-06-27; Memory: 28%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-07-28; Memory: 26%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-08-29; Memory: 26%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-09-30; Memory: 27%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-10-31; Memory: 28%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-11-32; Memory: 28%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-12-33; Memory: 29%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-13-34; Memory: 29%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-14-35; Memory: 30%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-15-36; Memory: 31%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-16-37; Memory: 31%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-17-37; Memory: 32%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-18-38; Memory: 33%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-19-39; Memory: 33%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-20-40; Memory: 34%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-21-41; Memory: 34%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-22-42; Memory: 35%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-23-43; Memory: 35%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-24-44; Memory: 36%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-25-45; Memory: 36%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-26-46; Memory: 37%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-27-47; Memory: 37%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-28-48; Memory: 38%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-29-48; Memory: 39%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-30-49; Memory: 39%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-31-50; Memory: 40%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-32-51; Memory: 40%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-33-52; Memory: 41%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-34-53; Memory: 41%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-35-54; Memory: 42%; Disk: 51.9% of 991.28GB
Time: 2023-07-31-09-36-55; Memory: 42%; Disk: 52.1% of 991.28GB
Time: 2023-07-31-09-37-56; Memory: 42%; Disk: 52.2% of 991.28GB
Time: 2023-07-31-09-38-57; Memory: 42%; Disk: 52.4% of 991.28GB
Time: 2023-07-31-09-39-58; Memory: 42%; Disk: 52.5% of 991.28GB
Time: 2023-07-31-09-40-58; Memory: 42%; Disk: 52.7% of 991.28GB
Time: 2023-07-31-09-41-59; Memory: 42%; Disk: 52.8% of 991.28GB
Time: 2023-07-31-09-43-00; Memory: 42%; Disk: 53.0% of 991.28GB
Time: 2023-07-31-09-44-01; Memory: 42%; Disk: 53.1% of 991.28GB
Time: 2023-07-31-09-45-02; Memory: 42%; Disk: 53.2% of 991.28GB
Time: 2023-07-31-09-46-03; Memory: 41%; Disk: 53.4% of 991.28GB
Time: 2023-07-31-09-47-04; Memory: 41%; Disk: 53.5% of 991.28GB
Time: 2023-07-31-09-48-05; Memory: 41%; Disk: 53.7% of 991.28GB
Time: 2023-07-31-09-49-06; Memory: 41%; Disk: 53.8% of 991.28GB
Time: 2023-07-31-09-50-07; Memory: 41%; Disk: 53.9% of 991.28GB
Time: 2023-07-31-09-51-08; Memory: 41%; Disk: 54.0% of 991.28GB
Time: 2023-07-31-09-52-08; Memory: 41%; Disk: 54.2% of 991.28GB
Time: 2023-07-31-09-53-09; Memory: 41%; Disk: 54.3% of 991.28GB
Time: 2023-07-31-09-54-10; Memory: 41%; Disk: 54.4% of 991.28GB
Time: 2023-07-31-09-55-11; Memory: 41%; Disk: 54.6% of 991.28GB
Time: 2023-07-31-09-56-12; Memory: 41%; Disk: 54.7% of 991.28GB
Time: 2023-07-31-09-57-13; Memory: 41%; Disk: 54.9% of 991.28GB
Time: 2023-07-31-09-58-14; Memory: 41%; Disk: 55.0% of 991.28GB
Time: 2023-07-31-09-59-15; Memory: 41%; Disk: 55.1% of 991.28GB
Time: 2023-07-31-10-00-16; Memory: 41%; Disk: 55.3% of 991.28GB
Time: 2023-07-31-10-01-17; Memory: 39%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-02-18; Memory: 11%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-03-18; Memory: 15%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-04-19; Memory: 19%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-05-20; Memory: 20%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-06-21; Memory: 24%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-07-22; Memory: 28%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-08-23; Memory: 31%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-09-24; Memory: 34%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-10-25; Memory: 38%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-11-26; Memory: 42%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-12-27; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-13-28; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-14-29; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-15-30; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-16-30; Memory: 44%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-17-31; Memory: 44%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-18-32; Memory: 45%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-19-33; Memory: 45%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-20-34; Memory: 45%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-21-35; Memory: 45%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-22-36; Memory: 45%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-23-37; Memory: 45%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-24-38; Memory: 45%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-25-39; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-26-40; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-27-41; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-28-41; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-29-42; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-30-43; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-31-44; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-32-45; Memory: 46%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-33-46; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-34-47; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-35-48; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-36-49; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-37-50; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-38-51; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-39-51; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-40-52; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-41-53; Memory: 47%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-42-54; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-43-55; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-44-56; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-45-57; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-46-58; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-47-59; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-49-00; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-50-01; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-51-02; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-52-02; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-53-03; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-54-04; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-55-05; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-56-06; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-57-07; Memory: 48%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-58-08; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-10-59-09; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-00-10; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-01-11; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-02-12; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-03-12; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-04-13; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-05-14; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-06-15; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-07-16; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-08-17; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-09-18; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-10-19; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-11-20; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-12-21; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-13-22; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-14-22; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-15-23; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-16-24; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-17-25; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-18-26; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-19-27; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-20-28; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-21-29; Memory: 49%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-22-30; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-23-31; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-24-32; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-25-32; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-26-33; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-27-34; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-28-35; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-29-36; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-30-37; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-31-38; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-32-39; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-33-40; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-34-41; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-35-42; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-36-42; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-37-43; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-38-44; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-39-45; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-40-46; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-41-47; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-42-48; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-43-49; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-44-50; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-45-51; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-46-52; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-47-52; Memory: 50%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-48-53; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-49-54; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-50-55; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-51-56; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-52-57; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-53-58; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-54-59; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-56-00; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-57-01; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-58-02; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-11-59-02; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-00-03; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-01-04; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-02-05; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-03-06; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-04-07; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-05-08; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-06-09; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-07-10; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-08-11; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-09-12; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-10-12; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-11-13; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-12-14; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-13-15; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-14-16; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-15-17; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-16-18; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-17-19; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-18-20; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-19-21; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-20-22; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-21-23; Memory: 51%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-22-23; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-23-24; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-24-25; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-25-26; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-26-27; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-27-28; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-28-29; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-29-30; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-30-31; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-31-32; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-32-33; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-33-33; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-34-34; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-35-35; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-36-36; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-37-37; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-38-38; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-39-39; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-40-40; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-41-41; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-42-42; Memory: 52%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-43-43; Memory: 53%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-44-43; Memory: 53%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-45-44; Memory: 53%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-46-45; Memory: 53%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-47-46; Memory: 53%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-48-47; Memory: 53%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-49-48; Memory: 53%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-50-49; Memory: 54%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-51-50; Memory: 54%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-52-51; Memory: 54%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-53-52; Memory: 54%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-54-53; Memory: 54%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-55-53; Memory: 54%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-56-54; Memory: 54%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-57-55; Memory: 54%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-58-56; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-12-59-57; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-00-58; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-01-59; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-03-00; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-04-01; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-05-02; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-06-03; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-07-03; Memory: 55%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-08-04; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-09-05; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-10-06; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-11-07; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-12-08; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-13-09; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-14-10; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-15-11; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-16-12; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-17-13; Memory: 56%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-18-13; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-19-14; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-20-15; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-21-16; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-22-17; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-23-18; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-24-19; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-25-20; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-26-21; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-27-22; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-28-23; Memory: 57%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-29-23; Memory: 58%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-30-24; Memory: 58%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-31-25; Memory: 58%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-32-26; Memory: 58%; Disk: 55.4% of 991.28GB
Time: 2023-07-31-13-33-27; Memory: 58%; Disk: 55.5% of 991.28GB
Time: 2023-07-31-13-34-28; Memory: 58%; Disk: 55.6% of 991.28GB
Time: 2023-07-31-13-35-29; Memory: 58%; Disk: 55.7% of 991.28GB
Time: 2023-07-31-13-36-30; Memory: 58%; Disk: 55.8% of 991.28GB
Time: 2023-07-31-13-37-31; Memory: 58%; Disk: 55.9% of 991.28GB
Time: 2023-07-31-13-38-32; Memory: 58%; Disk: 55.9% of 991.28GB
Time: 2023-07-31-13-39-33; Memory: 58%; Disk: 56.0% of 991.28GB
Time: 2023-07-31-13-40-34; Memory: 58%; Disk: 56.1% of 991.28GB
Time: 2023-07-31-13-41-34; Memory: 58%; Disk: 56.1% of 991.28GB
Time: 2023-07-31-13-42-35; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-43-36; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-44-37; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-45-38; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-46-39; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-47-40; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-48-41; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-49-42; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-50-43; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-51-44; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-52-44; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-53-45; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-54-46; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-55-47; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-56-48; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-57-49; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-58-50; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-13-59-51; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-00-52; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-01-53; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-02-54; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-03-54; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-04-55; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-05-56; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-06-57; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-07-58; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-08-59; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-10-00; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-11-01; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-12-02; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-13-03; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-14-04; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-15-04; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-16-05; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-17-06; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-18-07; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-19-08; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-20-09; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-21-10; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-22-11; Memory: 44%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-23-12; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-24-13; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-25-14; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-26-14; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-27-15; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-28-16; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-29-17; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-30-18; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-31-19; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-32-20; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-33-21; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-34-22; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-35-23; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-36-24; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-37-24; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-38-25; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-39-26; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-40-27; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-41-28; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-42-29; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-43-30; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-44-31; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-45-32; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-46-33; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-47-34; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-48-34; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-49-35; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-50-36; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-51-37; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-52-38; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-53-39; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-54-40; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-55-41; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-56-42; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-57-43; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-58-44; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-14-59-44; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-00-45; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-01-46; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-02-47; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-03-48; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-04-49; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-05-50; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-06-51; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-07-52; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-08-53; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-09-54; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-10-54; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-11-55; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-12-56; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-13-57; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-14-58; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-15-59; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-17-00; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-18-01; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-19-02; Memory: 45%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-20-03; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-21-04; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-22-05; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-23-05; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-24-06; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-25-07; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-26-08; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-27-09; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-28-10; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-29-11; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-30-12; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-31-13; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-32-14; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-33-14; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-34-15; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-35-16; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-36-17; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-37-18; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-38-19; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-39-20; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-40-21; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-41-22; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-42-23; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-43-24; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-44-24; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-45-25; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-46-26; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-47-27; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-48-28; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-49-29; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-50-30; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-51-31; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-52-32; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-53-33; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-54-34; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-55-35; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-56-35; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-57-36; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-58-37; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-15-59-38; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-00-39; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-01-40; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-02-41; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-03-42; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-04-43; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-05-44; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-06-45; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-07-45; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-08-46; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-09-47; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-10-48; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-11-49; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-12-50; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-13-51; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-14-52; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-15-53; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-16-54; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-17-55; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-18-55; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-19-56; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-20-57; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-21-58; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-22-59; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-24-00; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-25-01; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-26-02; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-27-03; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-28-04; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-29-05; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-30-05; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-31-06; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-32-07; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-33-08; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-34-09; Memory: 46%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-35-10; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-36-11; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-37-12; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-38-13; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-39-14; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-40-14; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-41-15; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-42-16; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-43-17; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-44-18; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-45-19; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-46-20; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-47-21; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-48-22; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-49-23; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-50-24; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-51-24; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-52-25; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-53-26; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-54-27; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-55-28; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-56-29; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-57-30; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-58-31; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-16-59-32; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-00-33; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-01-34; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-02-34; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-03-35; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-04-36; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-05-37; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-06-38; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-07-39; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-08-40; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-09-41; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-10-42; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-11-43; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-12-44; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-13-44; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-14-45; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-15-46; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-16-47; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-17-48; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-18-49; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-19-50; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-20-51; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-21-52; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-22-53; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-23-53; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-24-54; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-25-55; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-26-56; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-27-57; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-28-58; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-29-59; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-31-00; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-32-01; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-33-02; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-34-03; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-35-03; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-36-04; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-37-05; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-38-06; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-39-07; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-40-08; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-41-09; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-42-10; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-43-11; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-44-12; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-45-13; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-46-13; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-47-14; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-48-15; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-49-16; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-50-17; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-51-18; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-52-19; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-53-20; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-54-21; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-55-22; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-56-23; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-57-23; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-58-24; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-17-59-25; Memory: 47%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-00-26; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-01-27; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-02-28; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-03-29; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-04-30; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-05-31; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-06-32; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-07-33; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-08-33; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-09-34; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-10-35; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-11-36; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-12-37; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-13-38; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-14-39; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-15-40; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-16-41; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-17-42; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-18-42; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-19-43; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-20-44; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-21-45; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-22-46; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-23-47; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-24-48; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-25-49; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-26-50; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-27-51; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-28-52; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-29-52; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-30-53; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-31-54; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-32-55; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-33-56; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-34-57; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-35-58; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-36-59; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-38-00; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-39-01; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-40-02; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-41-02; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-42-03; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-43-04; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-44-05; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-45-06; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-46-07; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-47-08; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-48-09; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-49-10; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-50-11; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-51-11; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-52-12; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-53-13; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-54-14; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-55-15; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-56-16; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-57-17; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-58-18; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-18-59-19; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-00-20; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-01-21; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-02-21; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-03-22; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-04-23; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-05-24; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-06-25; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-07-26; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-08-27; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-09-28; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-10-29; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-11-30; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-12-31; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-13-31; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-14-32; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-15-33; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-16-34; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-17-35; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-18-36; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-19-37; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-20-38; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-21-39; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-22-40; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-23-41; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-24-41; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-25-42; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-26-43; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-27-44; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-28-45; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-29-46; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-30-47; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-31-48; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-32-49; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-33-50; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-34-51; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-35-51; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-36-52; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-37-53; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-38-54; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-39-55; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-40-56; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-41-57; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-42-58; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-43-59; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-45-00; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-46-01; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-47-01; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-48-02; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-49-03; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-50-04; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-51-05; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-52-06; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-53-07; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-54-08; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-55-09; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-56-10; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-57-10; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-58-11; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-19-59-12; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-00-13; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-01-14; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-02-15; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-03-16; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-04-17; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-05-18; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-06-19; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-07-20; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-08-20; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-09-21; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-10-22; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-11-23; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-12-24; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-13-25; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-14-26; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-15-27; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-16-28; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-17-29; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-18-30; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-19-30; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-20-31; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-21-32; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-22-33; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-23-34; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-24-35; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-25-36; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-26-37; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-27-38; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-28-39; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-29-40; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-30-40; Memory: 48%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-31-41; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-32-42; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-33-43; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-34-44; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-35-45; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-36-46; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-37-47; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-38-48; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-39-49; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-40-49; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-41-50; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-42-51; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-43-52; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-44-53; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-45-54; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-46-55; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-47-56; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-48-57; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-49-58; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-50-59; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-51-59; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-53-00; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-54-01; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-55-02; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-56-03; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-57-04; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-58-05; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-20-59-06; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-00-07; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-01-08; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-02-08; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-03-09; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-04-10; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-05-11; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-06-12; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-07-13; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-08-14; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-09-15; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-10-16; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-11-17; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-12-18; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-13-18; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-14-19; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-15-20; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-16-21; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-17-22; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-18-23; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-19-24; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-20-25; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-21-26; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-22-27; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-23-28; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-24-28; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-25-29; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-26-30; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-27-31; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-28-32; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-29-33; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-30-34; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-31-35; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-32-36; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-33-37; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-34-37; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-35-38; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-36-39; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-37-40; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-38-41; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-39-42; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-40-43; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-41-44; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-42-45; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-43-46; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-44-47; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-45-47; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-46-48; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-47-49; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-48-50; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-49-51; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-50-52; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-51-53; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-52-54; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-53-55; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-54-56; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-55-56; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-56-57; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-57-58; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-21-58-59; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-00-00; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-01-01; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-02-02; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-03-03; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-04-04; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-05-05; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-06-06; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-07-06; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-08-07; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-09-08; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-10-09; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-11-10; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-12-11; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-13-12; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-14-13; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-15-14; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-16-15; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-17-15; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-18-16; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-19-17; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-20-18; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-21-19; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-22-20; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-23-21; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-24-22; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-25-23; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-26-24; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-27-25; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-28-25; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-29-26; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-30-27; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-31-28; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-32-29; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-33-30; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-34-31; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-35-32; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-36-33; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-37-34; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-38-35; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-39-35; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-40-36; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-41-37; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-42-38; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-43-39; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-44-40; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-45-41; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-46-42; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-47-43; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-48-44; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-49-44; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-50-45; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-51-46; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-52-47; Memory: 49%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-53-48; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-54-49; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-55-50; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-56-51; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-57-52; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-58-53; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-22-59-54; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-00-54; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-01-55; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-02-56; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-03-57; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-04-58; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-05-59; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-07-00; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-08-01; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-09-02; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-10-03; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-11-04; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-12-04; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-13-05; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-14-06; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-15-07; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-16-08; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-17-09; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-18-10; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-19-11; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-20-12; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-21-13; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-22-14; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-23-14; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-24-15; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-25-16; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-26-17; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-27-18; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-28-19; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-29-20; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-30-21; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-31-22; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-32-23; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-33-23; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-34-24; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-35-25; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-36-26; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-37-27; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-38-28; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-39-29; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-40-30; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-41-31; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-42-32; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-43-33; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-44-33; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-45-34; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-46-35; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-47-36; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-48-37; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-49-38; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-50-39; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-51-40; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-52-41; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-53-42; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-54-43; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-55-43; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-56-44; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-57-45; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-58-46; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-07-31-23-59-47; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-00-48; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-01-49; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-02-50; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-03-51; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-04-52; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-05-53; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-06-53; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-07-54; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-08-55; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-09-56; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-10-57; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-11-58; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-12-59; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-14-00; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-15-01; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-16-02; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-17-02; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-18-03; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-19-04; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-20-05; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-21-06; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-22-07; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-23-08; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-24-09; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-25-10; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-26-11; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-27-12; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-28-12; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-29-13; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-30-14; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-31-15; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-32-16; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-33-17; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-34-18; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-35-19; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-36-20; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-37-21; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-38-22; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-39-22; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-40-23; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-41-24; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-42-25; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-43-26; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-44-27; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-45-28; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-46-29; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-47-30; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-48-31; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-49-31; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-50-32; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-51-33; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-52-34; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-53-35; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-54-36; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-55-37; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-56-38; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-57-39; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-58-40; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-00-59-41; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-00-41; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-01-42; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-02-43; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-03-44; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-04-45; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-05-46; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-06-47; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-07-48; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-08-49; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-09-50; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-10-51; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-11-51; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-12-52; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-13-53; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-14-54; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-15-55; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-16-56; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-17-57; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-18-58; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-19-59; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-21-00; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-22-01; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-23-01; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-24-02; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-25-03; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-26-04; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-27-05; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-28-06; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-29-07; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-30-08; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-31-09; Memory: 50%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-32-10; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-33-10; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-34-11; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-35-12; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-36-13; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-37-14; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-38-15; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-39-16; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-40-17; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-41-18; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-42-19; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-43-20; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-44-20; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-45-21; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-46-22; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-47-23; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-48-24; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-49-25; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-50-26; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-51-27; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-52-28; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-53-29; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-54-29; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-55-30; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-56-31; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-57-32; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-58-33; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-01-59-34; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-00-35; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-01-36; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-02-37; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-03-38; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-04-39; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-05-39; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-06-40; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-07-41; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-08-42; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-09-43; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-10-44; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-11-45; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-12-46; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-13-47; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-14-48; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-15-49; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-16-49; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-17-50; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-18-51; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-19-52; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-20-53; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-21-54; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-22-55; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-23-56; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-24-57; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-25-58; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-26-59; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-27-59; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-29-00; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-30-01; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-31-02; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-32-03; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-33-04; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-34-05; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-35-06; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-36-07; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-37-08; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-38-09; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-39-09; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-40-10; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-41-11; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-42-12; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-43-13; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-44-14; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-45-15; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-46-16; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-47-17; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-48-18; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-49-19; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-50-19; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-51-20; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-52-21; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-53-22; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-54-23; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-55-24; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-56-25; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-57-26; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-58-27; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-02-59-28; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-00-29; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-01-29; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-02-30; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-03-31; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-04-32; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-05-33; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-06-34; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-07-35; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-08-36; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-09-37; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-10-38; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-11-39; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-12-39; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-13-40; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-14-41; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-15-42; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-16-43; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-17-44; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-18-45; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-19-46; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-20-47; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-21-48; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-22-49; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-23-49; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-24-50; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-25-51; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-26-52; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-27-53; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-28-54; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-29-55; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-30-56; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-31-57; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-32-58; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-33-59; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-34-59; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-36-00; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-37-01; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-38-02; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-39-03; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-40-04; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-41-05; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-42-06; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-43-07; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-44-08; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-45-09; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-46-09; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-47-10; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-48-11; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-49-12; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-50-13; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-51-14; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-52-15; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-53-16; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-54-17; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-55-18; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-56-18; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-57-19; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-58-20; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-03-59-21; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-00-22; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-01-23; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-02-24; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-03-25; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-04-26; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-05-27; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-06-28; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-07-28; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-08-29; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-09-30; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-10-31; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-11-32; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-12-33; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-13-34; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-14-35; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-15-36; Memory: 51%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-16-37; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-17-38; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-18-38; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-19-39; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-20-40; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-21-41; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-22-42; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-23-43; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-24-44; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-25-45; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-26-46; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-27-47; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-28-48; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-29-48; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-30-49; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-31-50; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-32-51; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-33-52; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-34-53; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-35-54; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-36-55; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-37-56; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-38-57; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-39-57; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-40-58; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-41-59; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-43-00; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-44-01; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-45-02; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-46-03; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-47-04; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-48-05; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-49-06; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-50-07; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-51-07; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-52-08; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-53-09; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-54-10; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-55-11; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-56-12; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-57-13; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-58-14; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-04-59-15; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-00-16; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-01-16; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-02-17; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-03-18; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-04-19; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-05-20; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-06-21; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-07-22; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-08-23; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-09-24; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-10-25; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-11-26; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-12-26; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-13-27; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-14-28; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-15-29; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-16-30; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-17-31; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-18-32; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-19-33; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-20-34; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-21-35; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-22-36; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-23-36; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-24-37; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-25-38; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-26-39; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-27-40; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-28-41; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-29-42; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-30-43; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-31-44; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-32-45; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-33-45; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-34-46; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-35-47; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-36-48; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-37-49; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-38-50; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-39-51; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-40-52; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-41-53; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-42-54; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-43-55; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-44-56; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-45-56; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-46-57; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-47-58; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-48-59; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-50-00; Memory: 52%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-51-01; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-52-02; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-53-03; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-54-04; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-55-05; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-56-05; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-57-06; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-58-07; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-05-59-08; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-00-09; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-01-10; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-02-11; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-03-12; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-04-13; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-05-14; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-06-15; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-07-16; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-08-16; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-09-17; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-10-18; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-11-19; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-12-20; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-13-21; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-14-22; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-15-23; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-16-24; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-17-25; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-18-26; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-19-26; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-20-27; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-21-28; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-22-29; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-23-30; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-24-31; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-25-32; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-26-33; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-27-34; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-28-35; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-29-36; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-30-37; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-31-37; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-32-38; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-33-39; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-34-40; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-35-41; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-36-42; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-37-43; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-38-44; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-39-45; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-40-46; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-41-47; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-42-47; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-43-48; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-44-49; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-45-50; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-46-51; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-47-52; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-48-53; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-49-54; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-50-55; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-51-56; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-52-57; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-53-58; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-54-58; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-55-59; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-57-00; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-58-01; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-06-59-02; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-00-03; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-01-04; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-02-05; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-03-06; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-04-07; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-05-08; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-06-08; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-07-09; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-08-10; Memory: 53%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-09-11; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-10-12; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-11-13; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-12-14; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-13-15; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-14-16; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-15-17; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-16-18; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-17-18; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-18-19; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-19-20; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-20-21; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-21-22; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-22-23; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-23-24; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-24-25; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-25-26; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-26-27; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-27-28; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-28-28; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-29-29; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-30-30; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-31-31; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-32-32; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-33-33; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-34-34; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-35-35; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-36-36; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-37-37; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-38-38; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-39-39; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-40-39; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-41-40; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-42-41; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-43-42; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-44-43; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-45-44; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-46-45; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-47-46; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-48-47; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-49-48; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-50-49; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-51-49; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-52-50; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-53-51; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-54-52; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-55-53; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-56-54; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-57-55; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-58-56; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-07-59-57; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-00-58; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-01-59; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-02-59; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-04-00; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-05-01; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-06-02; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-07-03; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-08-04; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-09-05; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-10-06; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-11-07; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-12-08; Memory: 54%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-13-09; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-14-10; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-15-10; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-16-11; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-17-12; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-18-13; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-19-14; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-20-15; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-21-16; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-22-17; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-23-18; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-24-19; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-25-20; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-26-20; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-27-21; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-28-22; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-29-23; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-30-24; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-31-25; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-32-26; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-33-27; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-34-28; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-35-29; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-36-30; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-37-31; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-38-31; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-39-32; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-40-33; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-41-34; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-42-35; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-43-36; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-44-37; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-45-38; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-46-39; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-47-40; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-48-41; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-49-41; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-50-42; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-51-43; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-52-44; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-53-45; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-54-46; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-55-47; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-56-48; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-57-49; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-58-50; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-08-59-51; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-00-51; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-01-52; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-02-53; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-03-54; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-04-55; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-05-56; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-06-57; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-07-58; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-08-59; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-10-00; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-11-01; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-12-02; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-13-02; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-14-03; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-15-04; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-16-05; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-17-06; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-18-07; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-19-08; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-20-09; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-21-10; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-22-11; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-23-12; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-24-12; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-25-13; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-26-14; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-27-15; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-28-16; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-29-17; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-30-18; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-31-19; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-32-20; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-33-21; Memory: 55%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-34-22; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-35-22; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-36-23; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-37-24; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-38-25; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-39-26; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-40-27; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-41-28; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-42-29; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-43-30; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-44-31; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-45-32; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-46-33; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-47-33; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-48-34; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-49-35; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-50-36; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-51-37; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-52-38; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-53-39; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-54-40; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-55-41; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-56-42; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-57-43; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-58-43; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-09-59-44; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-00-45; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-01-46; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-02-47; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-03-48; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-04-49; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-05-50; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-06-51; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-07-52; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-08-53; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-09-53; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-10-54; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-11-55; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-12-56; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-13-57; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-14-58; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-15-59; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-17-00; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-18-01; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-19-02; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-20-03; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-21-04; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-22-04; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-23-05; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-24-06; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-25-07; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-26-08; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-27-09; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-28-10; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-29-11; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-30-12; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-31-13; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-32-14; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-33-14; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-34-15; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-35-16; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-36-17; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-37-18; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-38-19; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-39-20; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-40-21; Memory: 56%; Disk: 56.2% of 991.28GB
Time: 2023-08-01-10-41-22; Memory: 56%; Disk: 56.3% of 991.28GB
Time: 2023-08-01-10-42-23; Memory: 56%; Disk: 56.4% of 991.28GB
Time: 2023-08-01-10-43-24; Memory: 56%; Disk: 56.4% of 991.28GB
Time: 2023-08-01-10-44-24; Memory: 56%; Disk: 56.5% of 991.28GB
Time: 2023-08-01-10-45-25; Memory: 56%; Disk: 56.6% of 991.28GB
Time: 2023-08-01-10-46-26; Memory: 56%; Disk: 56.6% of 991.28GB
Time: 2023-08-01-10-47-27; Memory: 56%; Disk: 56.7% of 991.28GB
Time: 2023-08-01-10-48-28; Memory: 56%; Disk: 56.8% of 991.28GB
Time: 2023-08-01-10-49-29; Memory: 56%; Disk: 56.8% of 991.28GB
Time: 2023-08-01-10-50-30; Memory: 56%; Disk: 56.9% of 991.28GB
Time: 2023-08-01-10-51-31; Memory: 56%; Disk: 57.0% of 991.28GB
Time: 2023-08-01-10-52-32; Memory: 56%; Disk: 57.1% of 991.28GB
Time: 2023-08-01-10-53-33; Memory: 56%; Disk: 57.2% of 991.28GB
Time: 2023-08-01-10-54-34; Memory: 56%; Disk: 57.2% of 991.28GB
Time: 2023-08-01-10-55-35; Memory: 56%; Disk: 57.3% of 991.28GB
Time: 2023-08-01-10-56-35; Memory: 56%; Disk: 57.3% of 991.28GB
Time: 2023-08-01-10-57-36; Memory: 56%; Disk: 57.4% of 991.28GB
Time: 2023-08-01-10-58-37; Memory: 56%; Disk: 57.5% of 991.28GB
Time: 2023-08-01-10-59-38; Memory: 56%; Disk: 57.6% of 991.28GB
Time: 2023-08-01-11-00-39; Memory: 56%; Disk: 57.6% of 991.28GB
Time: 2023-08-01-11-01-40; Memory: 56%; Disk: 57.7% of 991.28GB
Time: 2023-08-01-11-02-41; Memory: 56%; Disk: 57.8% of 991.28GB
Time: 2023-08-01-11-03-42; Memory: 56%; Disk: 57.8% of 991.28GB
Time: 2023-08-01-11-04-43; Memory: 56%; Disk: 57.9% of 991.28GB
Time: 2023-08-01-11-05-44; Memory: 56%; Disk: 58.0% of 991.28GB
Time: 2023-08-01-11-06-45; Memory: 56%; Disk: 58.0% of 991.28GB
Time: 2023-08-01-11-07-45; Memory: 56%; Disk: 58.1% of 991.28GB
Time: 2023-08-01-11-08-46; Memory: 56%; Disk: 58.2% of 991.28GB
Time: 2023-08-01-11-09-47; Memory: 56%; Disk: 58.2% of 991.28GB
Time: 2023-08-01-11-10-48; Memory: 56%; Disk: 58.3% of 991.28GB
Time: 2023-08-01-11-11-49; Memory: 56%; Disk: 58.4% of 991.28GB
Time: 2023-08-01-11-12-50; Memory: 56%; Disk: 58.5% of 991.28GB
Time: 2023-08-01-11-13-51; Memory: 56%; Disk: 58.5% of 991.28GB
Time: 2023-08-01-11-14-52; Memory: 56%; Disk: 58.6% of 991.28GB
Time: 2023-08-01-11-15-53; Memory: 56%; Disk: 58.7% of 991.28GB
Time: 2023-08-01-11-16-54; Memory: 56%; Disk: 58.7% of 991.28GB
Time: 2023-08-01-11-17-55; Memory: 56%; Disk: 58.8% of 991.28GB
Time: 2023-08-01-11-18-56; Memory: 56%; Disk: 58.9% of 991.28GB
Time: 2023-08-01-11-19-56; Memory: 56%; Disk: 59.0% of 991.28GB
Time: 2023-08-01-11-20-57; Memory: 56%; Disk: 59.0% of 991.28GB
Time: 2023-08-01-11-21-58; Memory: 56%; Disk: 59.1% of 991.28GB
Time: 2023-08-01-11-22-59; Memory: 56%; Disk: 59.2% of 991.28GB
Time: 2023-08-01-11-24-00; Memory: 56%; Disk: 59.2% of 991.28GB
Time: 2023-08-01-11-25-01; Memory: 56%; Disk: 59.3% of 991.28GB
Time: 2023-08-01-11-26-02; Memory: 56%; Disk: 59.4% of 991.28GB
Time: 2023-08-01-11-27-03; Memory: 56%; Disk: 59.4% of 991.28GB
Time: 2023-08-01-11-28-04; Memory: 56%; Disk: 59.5% of 991.28GB
Time: 2023-08-01-11-29-05; Memory: 56%; Disk: 59.6% of 991.28GB
Time: 2023-08-01-11-30-06; Memory: 56%; Disk: 59.7% of 991.28GB
Time: 2023-08-01-11-31-06; Memory: 56%; Disk: 59.7% of 991.28GB
Time: 2023-08-01-11-32-07; Memory: 56%; Disk: 59.8% of 991.28GB
Time: 2023-08-01-11-33-08; Memory: 56%; Disk: 59.9% of 991.28GB
Time: 2023-08-01-11-34-09; Memory: 56%; Disk: 59.9% of 991.28GB
Time: 2023-08-01-11-35-10; Memory: 56%; Disk: 60.0% of 991.28GB
Time: 2023-08-01-11-36-11; Memory: 56%; Disk: 60.1% of 991.28GB
Time: 2023-08-01-11-37-12; Memory: 56%; Disk: 60.2% of 991.28GB
Time: 2023-08-01-11-38-13; Memory: 56%; Disk: 60.2% of 991.28GB
Time: 2023-08-01-11-39-14; Memory: 56%; Disk: 60.3% of 991.28GB
Time: 2023-08-01-11-40-15; Memory: 56%; Disk: 60.4% of 991.28GB
Time: 2023-08-01-11-41-16; Memory: 56%; Disk: 60.5% of 991.28GB
Time: 2023-08-01-11-42-16; Memory: 56%; Disk: 60.5% of 991.28GB
Time: 2023-08-01-11-43-17; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-44-18; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-45-19; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-46-20; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-47-21; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-48-22; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-49-23; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-50-24; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-51-25; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-52-26; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-53-26; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-54-27; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-55-28; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-56-29; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-57-30; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-58-31; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-11-59-32; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-00-33; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-01-34; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-02-35; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-03-36; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-04-37; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-05-37; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-06-38; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-07-39; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-08-40; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-09-41; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-10-42; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-11-43; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-12-44; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-13-45; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-14-46; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-15-47; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-16-47; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-17-48; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-18-49; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-19-50; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-20-51; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-21-52; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-22-53; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-23-54; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-24-55; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-25-56; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-26-57; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-27-57; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-28-58; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-29-59; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-31-00; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-32-01; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-33-02; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-34-03; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-35-04; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-36-05; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-37-06; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-38-07; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-39-08; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-40-08; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-41-09; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-42-10; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-43-11; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-44-12; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-45-13; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-46-14; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-47-15; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-48-16; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-49-17; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-50-18; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-51-18; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-52-19; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-53-20; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-54-21; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-55-22; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-56-23; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-57-24; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-58-25; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-12-59-26; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-00-27; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-01-28; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-02-28; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-03-29; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-04-30; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-05-31; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-06-32; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-07-33; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-08-34; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-09-35; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-10-36; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-11-37; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-12-38; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-13-38; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-14-39; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-15-40; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-16-41; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-17-42; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-18-43; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-19-44; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-20-45; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-21-46; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-22-47; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-23-48; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-24-48; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-25-49; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-26-50; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-27-51; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-28-52; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-29-53; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-30-54; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-31-55; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-32-56; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-33-57; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-34-58; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-35-58; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-36-59; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-38-00; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-39-01; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-40-02; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-41-03; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-42-04; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-43-05; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-44-06; Memory: 56%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-45-07; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-46-08; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-47-09; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-48-09; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-49-10; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-50-11; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-51-12; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-52-13; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-53-14; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-54-15; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-55-16; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-56-17; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-57-18; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-58-19; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-13-59-19; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-00-20; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-01-21; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-02-22; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-03-23; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-04-24; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-05-25; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-06-26; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-07-27; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-08-28; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-09-29; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-10-29; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-11-30; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-12-31; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-13-32; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-14-33; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-15-34; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-16-35; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-17-36; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-18-37; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-19-38; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-20-39; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-21-39; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-22-40; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-23-41; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-24-42; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-25-43; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-26-44; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-27-45; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-28-46; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-29-47; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-30-48; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-31-49; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-32-50; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-33-50; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-34-51; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-35-52; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-36-53; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-37-54; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-38-55; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-39-56; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-40-57; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-41-58; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-42-59; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-44-00; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-45-00; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-46-01; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-47-02; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-48-03; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-49-04; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-50-05; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-51-06; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-52-07; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-53-08; Memory: 53%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-54-09; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-55-10; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-56-10; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-57-11; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-58-12; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-14-59-13; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-00-14; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-01-15; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-02-16; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-03-17; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-04-18; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-05-19; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-06-20; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-07-21; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-08-21; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-09-22; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-10-23; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-11-24; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-12-25; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-13-26; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-14-27; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-15-28; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-16-29; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-17-30; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-18-31; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-19-32; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-20-32; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-21-33; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-22-34; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-23-35; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-24-36; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-25-37; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-26-38; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-27-39; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-28-40; Memory: 50%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-29-41; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-30-42; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-31-42; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-32-43; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-33-44; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-34-45; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-35-46; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-36-47; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-37-48; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-38-49; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-39-50; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-40-51; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-41-52; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-42-53; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-43-53; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-44-54; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-45-55; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-46-56; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-47-57; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-48-58; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-49-59; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-51-00; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-52-01; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-53-02; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-54-03; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-55-03; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-56-04; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-57-05; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-58-06; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-15-59-07; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-00-08; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-01-09; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-02-10; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-03-11; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-04-12; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-05-13; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-06-13; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-07-14; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-08-15; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-09-16; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-10-17; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-11-18; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-12-19; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-13-20; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-14-21; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-15-22; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-16-23; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-17-24; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-18-24; Memory: 45%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-19-25; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-20-26; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-21-27; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-22-28; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-23-29; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-24-30; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-25-31; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-26-32; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-27-33; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-28-34; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-29-34; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-30-35; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-31-36; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-32-37; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-33-38; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-34-39; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-35-40; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-36-41; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-37-42; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-38-43; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-39-44; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-40-45; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-41-45; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-42-46; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-43-47; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-44-48; Memory: 41%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-45-49; Memory: 41%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-46-50; Memory: 41%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-47-51; Memory: 41%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-48-52; Memory: 41%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-49-53; Memory: 41%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-50-54; Memory: 41%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-51-55; Memory: 41%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-52-55; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-53-56; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-54-57; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-55-58; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-56-59; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-58-00; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-16-59-01; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-00-02; Memory: 39%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-01-03; Memory: 39%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-02-04; Memory: 39%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-03-05; Memory: 39%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-04-05; Memory: 39%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-05-06; Memory: 39%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-06-07; Memory: 39%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-07-08; Memory: 39%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-08-09; Memory: 38%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-09-10; Memory: 38%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-10-11; Memory: 38%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-11-12; Memory: 38%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-12-13; Memory: 38%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-13-14; Memory: 38%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-14-15; Memory: 37%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-15-15; Memory: 37%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-16-16; Memory: 37%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-17-17; Memory: 37%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-18-18; Memory: 37%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-19-19; Memory: 36%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-20-20; Memory: 36%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-21-21; Memory: 36%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-22-22; Memory: 36%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-23-23; Memory: 36%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-24-24; Memory: 35%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-25-25; Memory: 35%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-26-25; Memory: 35%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-27-26; Memory: 35%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-28-27; Memory: 35%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-29-28; Memory: 34%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-30-29; Memory: 34%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-31-30; Memory: 34%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-32-31; Memory: 34%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-33-32; Memory: 34%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-34-33; Memory: 33%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-35-34; Memory: 33%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-36-35; Memory: 33%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-37-36; Memory: 33%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-38-36; Memory: 33%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-39-37; Memory: 32%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-40-38; Memory: 32%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-41-39; Memory: 32%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-42-40; Memory: 32%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-43-41; Memory: 31%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-44-42; Memory: 31%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-45-43; Memory: 31%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-46-44; Memory: 31%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-47-45; Memory: 30%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-48-46; Memory: 30%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-49-47; Memory: 30%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-50-47; Memory: 30%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-51-48; Memory: 30%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-52-49; Memory: 29%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-53-50; Memory: 29%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-54-51; Memory: 29%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-55-52; Memory: 29%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-56-53; Memory: 29%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-57-54; Memory: 28%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-58-55; Memory: 28%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-17-59-56; Memory: 28%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-00-57; Memory: 28%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-01-57; Memory: 28%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-02-58; Memory: 27%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-03-59; Memory: 27%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-05-00; Memory: 27%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-06-01; Memory: 27%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-07-02; Memory: 27%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-08-03; Memory: 26%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-09-04; Memory: 26%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-10-05; Memory: 26%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-11-06; Memory: 26%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-12-07; Memory: 25%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-13-08; Memory: 25%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-14-08; Memory: 25%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-15-09; Memory: 24%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-16-10; Memory: 24%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-17-11; Memory: 23%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-18-12; Memory: 23%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-19-13; Memory: 22%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-20-14; Memory: 21%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-21-15; Memory: 18%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-22-16; Memory: 3%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-23-17; Memory: 6%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-24-18; Memory: 9%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-25-18; Memory: 14%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-26-19; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-27-20; Memory: 23%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-28-21; Memory: 27%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-29-22; Memory: 31%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-30-23; Memory: 34%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-31-24; Memory: 37%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-32-25; Memory: 37%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-33-26; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-34-27; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-35-28; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-36-29; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-37-29; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-38-30; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-39-31; Memory: 49%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-40-32; Memory: 35%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-41-33; Memory: 25%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-42-34; Memory: 9%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-43-35; Memory: 11%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-44-36; Memory: 14%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-45-37; Memory: 17%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-46-38; Memory: 19%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-47-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-48-40; Memory: 22%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-49-40; Memory: 23%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-50-41; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-51-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-52-43; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-53-44; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-54-45; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-55-46; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-56-47; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-57-48; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-58-49; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-18-59-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-00-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-01-51; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-02-52; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-03-53; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-04-54; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-05-55; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-06-56; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-07-57; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-08-58; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-09-59; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-11-00; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-12-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-13-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-14-02; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-15-03; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-16-04; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-17-05; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-18-06; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-19-07; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-20-08; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-21-09; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-22-10; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-23-11; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-24-12; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-25-12; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-26-13; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-27-14; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-28-15; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-29-16; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-30-17; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-31-18; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-32-19; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-33-20; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-34-21; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-35-22; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-36-23; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-37-24; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-38-24; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-39-25; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-40-26; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-41-27; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-42-28; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-43-29; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-44-30; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-45-31; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-46-32; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-47-33; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-48-34; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-49-35; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-50-35; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-51-36; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-52-37; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-53-38; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-54-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-55-40; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-56-41; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-57-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-58-43; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-19-59-44; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-00-45; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-01-45; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-02-46; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-03-47; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-04-48; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-05-49; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-06-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-07-51; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-08-52; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-09-53; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-10-54; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-11-55; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-12-56; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-13-56; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-14-57; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-15-58; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-16-59; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-18-00; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-19-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-20-02; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-21-03; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-22-04; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-23-05; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-24-06; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-25-07; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-26-07; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-27-08; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-28-09; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-29-10; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-30-11; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-31-12; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-32-13; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-33-14; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-34-15; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-35-16; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-36-17; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-37-18; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-38-18; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-39-19; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-40-20; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-41-21; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-42-22; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-43-23; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-44-24; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-45-25; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-46-26; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-47-27; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-48-28; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-49-28; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-50-29; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-51-30; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-52-31; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-53-32; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-54-33; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-55-34; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-56-35; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-57-36; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-58-37; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-20-59-38; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-00-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-01-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-02-40; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-03-41; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-04-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-05-43; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-06-44; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-07-45; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-08-46; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-09-47; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-10-48; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-11-49; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-12-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-13-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-14-51; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-15-52; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-16-53; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-17-54; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-18-55; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-19-56; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-20-57; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-21-58; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-22-59; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-24-00; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-25-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-26-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-27-02; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-28-03; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-29-04; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-30-05; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-31-06; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-32-07; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-33-08; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-34-09; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-35-10; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-36-11; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-37-11; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-38-12; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-39-13; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-40-14; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-41-15; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-42-16; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-43-17; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-44-18; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-45-19; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-46-20; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-47-21; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-48-22; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-49-22; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-50-23; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-51-24; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-52-25; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-53-26; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-54-27; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-55-28; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-56-29; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-57-30; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-58-31; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-21-59-32; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-00-33; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-01-33; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-02-34; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-03-35; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-04-36; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-05-37; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-06-38; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-07-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-08-40; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-09-41; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-10-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-11-43; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-12-43; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-13-44; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-14-45; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-15-46; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-16-47; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-17-48; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-18-49; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-19-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-20-51; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-21-52; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-22-53; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-23-54; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-24-54; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-25-55; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-26-56; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-27-57; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-28-58; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-29-59; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-31-00; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-32-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-33-02; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-34-03; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-35-04; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-36-05; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-37-05; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-38-06; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-39-07; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-40-08; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-41-09; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-42-10; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-43-11; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-44-12; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-45-13; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-46-14; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-47-15; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-48-16; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-49-16; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-50-17; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-51-18; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-52-19; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-53-20; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-54-21; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-55-22; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-56-23; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-57-24; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-58-25; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-22-59-26; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-00-27; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-01-27; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-02-28; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-03-29; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-04-30; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-05-31; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-06-32; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-07-33; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-08-34; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-09-35; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-10-36; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-11-37; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-12-38; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-13-38; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-14-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-15-40; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-16-41; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-17-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-18-43; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-19-44; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-20-45; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-21-46; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-22-47; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-23-48; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-24-48; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-25-49; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-26-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-27-51; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-28-52; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-29-53; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-30-54; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-31-55; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-32-56; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-33-57; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-34-58; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-35-59; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-36-59; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-38-00; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-39-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-40-02; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-41-03; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-42-04; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-43-05; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-44-06; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-45-07; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-46-08; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-47-09; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-48-10; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-49-10; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-50-11; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-51-12; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-52-13; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-53-14; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-54-15; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-55-16; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-56-17; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-57-18; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-58-19; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-01-23-59-20; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-00-21; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-01-21; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-02-22; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-03-23; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-04-24; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-05-25; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-06-26; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-07-27; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-08-28; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-09-29; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-10-30; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-11-31; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-12-32; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-13-32; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-14-33; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-15-34; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-16-35; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-17-36; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-18-37; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-19-38; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-20-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-21-40; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-22-41; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-23-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-24-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-25-43; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-26-44; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-27-45; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-28-46; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-29-47; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-30-48; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-31-49; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-32-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-33-51; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-34-52; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-35-53; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-36-53; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-37-54; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-38-55; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-39-56; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-40-57; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-41-58; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-42-59; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-44-00; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-45-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-46-02; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-47-03; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-48-04; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-49-04; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-50-05; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-51-06; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-52-07; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-53-08; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-54-09; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-55-10; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-56-11; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-57-12; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-58-13; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-00-59-14; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-00-15; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-01-15; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-02-16; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-03-17; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-04-18; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-05-19; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-06-20; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-07-21; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-08-22; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-09-23; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-10-24; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-11-25; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-12-26; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-13-26; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-14-27; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-15-28; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-16-29; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-17-30; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-18-31; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-19-32; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-20-33; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-21-34; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-22-35; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-23-36; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-24-37; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-25-37; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-26-38; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-27-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-28-40; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-29-41; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-30-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-31-43; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-32-44; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-33-45; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-34-46; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-35-47; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-36-47; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-37-48; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-38-49; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-39-50; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-40-51; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-41-52; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-42-53; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-43-54; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-44-55; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-45-56; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-46-57; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-47-58; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-48-58; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-49-59; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-51-00; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-52-01; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-53-02; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-54-03; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-55-04; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-56-05; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-57-06; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-58-07; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-01-59-08; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-00-09; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-01-09; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-02-10; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-03-11; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-04-12; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-05-13; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-06-14; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-07-15; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-08-16; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-09-17; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-10-18; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-11-19; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-12-20; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-13-20; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-14-21; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-15-22; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-16-23; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-17-24; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-18-25; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-19-26; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-20-27; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-21-28; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-22-29; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-23-30; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-24-31; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-25-31; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-26-32; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-27-33; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-28-34; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-29-35; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-30-36; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-31-37; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-32-38; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-33-39; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-34-40; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-35-41; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-36-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-37-42; Memory: 20%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-38-43; Memory: 22%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-39-44; Memory: 14%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-40-45; Memory: 13%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-41-46; Memory: 15%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-42-47; Memory: 17%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-43-48; Memory: 16%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-44-49; Memory: 32%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-45-50; Memory: 29%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-46-51; Memory: 32%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-47-52; Memory: 35%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-48-53; Memory: 36%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-49-53; Memory: 38%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-50-54; Memory: 40%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-51-55; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-52-56; Memory: 43%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-53-57; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-54-58; Memory: 46%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-55-59; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-57-00; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-58-01; Memory: 52%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-02-59-02; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-00-03; Memory: 55%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-01-04; Memory: 47%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-02-04; Memory: 42%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-03-05; Memory: 44%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-04-06; Memory: 48%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-05-07; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-06-08; Memory: 51%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-07-09; Memory: 54%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-08-10; Memory: 57%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-09-11; Memory: 59%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-10-12; Memory: 59%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-11-13; Memory: 59%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-12-14; Memory: 62%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-13-15; Memory: 58%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-14-15; Memory: 58%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-15-16; Memory: 58%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-16-17; Memory: 58%; Disk: 60.6% of 991.28GB
Time: 2023-08-02-03-17-18; Memory: 58%; Disk: 60.7% of 991.28GB
Time: 2023-08-02-03-18-19; Memory: 58%; Disk: 60.7% of 991.28GB
Time: 2023-08-02-03-19-20; Memory: 58%; Disk: 60.8% of 991.28GB
Time: 2023-08-02-03-20-21; Memory: 58%; Disk: 60.9% of 991.28GB
Time: 2023-08-02-03-21-22; Memory: 58%; Disk: 61.0% of 991.28GB
Time: 2023-08-02-03-22-23; Memory: 58%; Disk: 61.2% of 991.28GB
Time: 2023-08-02-03-23-24; Memory: 58%; Disk: 61.3% of 991.28GB
Time: 2023-08-02-03-24-25; Memory: 58%; Disk: 61.4% of 991.28GB
Time: 2023-08-02-03-25-25; Memory: 58%; Disk: 61.5% of 991.28GB
Time: 2023-08-02-03-26-26; Memory: 58%; Disk: 61.5% of 991.28GB
Time: 2023-08-02-03-27-27; Memory: 58%; Disk: 61.6% of 991.28GB
Time: 2023-08-02-03-28-28; Memory: 58%; Disk: 61.7% of 991.28GB
Time: 2023-08-02-03-29-29; Memory: 58%; Disk: 61.8% of 991.28GB
Time: 2023-08-02-03-30-30; Memory: 58%; Disk: 61.9% of 991.28GB
Time: 2023-08-02-03-31-31; Memory: 58%; Disk: 62.0% of 991.28GB
Time: 2023-08-02-03-32-32; Memory: 58%; Disk: 62.1% of 991.28GB
Time: 2023-08-02-03-33-33; Memory: 58%; Disk: 62.2% of 991.28GB
Time: 2023-08-02-03-34-34; Memory: 58%; Disk: 62.3% of 991.28GB
Time: 2023-08-02-03-35-35; Memory: 58%; Disk: 62.4% of 991.28GB
Time: 2023-08-02-03-36-36; Memory: 58%; Disk: 62.5% of 991.28GB
Time: 2023-08-02-03-37-36; Memory: 58%; Disk: 62.6% of 991.28GB
Time: 2023-08-02-03-38-37; Memory: 58%; Disk: 62.7% of 991.28GB
Time: 2023-08-02-03-39-38; Memory: 58%; Disk: 62.8% of 991.28GB
Time: 2023-08-02-03-40-39; Memory: 58%; Disk: 62.9% of 991.28GB
Time: 2023-08-02-03-41-40; Memory: 58%; Disk: 63.0% of 991.28GB
Time: 2023-08-02-03-42-41; Memory: 58%; Disk: 63.1% of 991.28GB
Time: 2023-08-02-03-43-42; Memory: 58%; Disk: 63.2% of 991.28GB
Time: 2023-08-02-03-44-43; Memory: 58%; Disk: 63.3% of 991.28GB
Time: 2023-08-02-03-45-44; Memory: 58%; Disk: 63.4% of 991.28GB
Time: 2023-08-02-03-46-45; Memory: 58%; Disk: 63.4% of 991.28GB
Time: 2023-08-02-03-47-46; Memory: 58%; Disk: 63.5% of 991.28GB
Time: 2023-08-02-03-48-47; Memory: 58%; Disk: 63.6% of 991.28GB
Time: 2023-08-02-03-49-48; Memory: 58%; Disk: 63.7% of 991.28GB
Time: 2023-08-02-03-50-49; Memory: 58%; Disk: 63.8% of 991.28GB
Time: 2023-08-02-03-51-49; Memory: 58%; Disk: 63.9% of 991.28GB
Time: 2023-08-02-03-52-50; Memory: 58%; Disk: 64.0% of 991.28GB
Time: 2023-08-02-03-53-51; Memory: 58%; Disk: 64.1% of 991.28GB
Time: 2023-08-02-03-54-52; Memory: 58%; Disk: 64.2% of 991.28GB
Time: 2023-08-02-03-55-53; Memory: 58%; Disk: 64.3% of 991.28GB
Time: 2023-08-02-03-56-54; Memory: 58%; Disk: 64.4% of 991.28GB
Time: 2023-08-02-03-57-55; Memory: 58%; Disk: 64.5% of 991.28GB
Time: 2023-08-02-03-58-56; Memory: 58%; Disk: 64.5% of 991.28GB
Time: 2023-08-02-03-59-57; Memory: 58%; Disk: 64.6% of 991.28GB
Time: 2023-08-02-04-00-58; Memory: 58%; Disk: 64.7% of 991.28GB
Time: 2023-08-02-04-01-59; Memory: 58%; Disk: 64.8% of 991.28GB
Time: 2023-08-02-04-03-00; Memory: 58%; Disk: 64.9% of 991.28GB
Time: 2023-08-02-04-04-00; Memory: 58%; Disk: 65.0% of 991.28GB
Time: 2023-08-02-04-05-01; Memory: 58%; Disk: 65.1% of 991.28GB
Time: 2023-08-02-04-06-02; Memory: 58%; Disk: 65.2% of 991.28GB
Time: 2023-08-02-04-07-03; Memory: 58%; Disk: 65.2% of 991.28GB
Time: 2023-08-02-04-08-04; Memory: 58%; Disk: 65.3% of 991.28GB
Time: 2023-08-02-04-09-05; Memory: 58%; Disk: 65.4% of 991.28GB
Time: 2023-08-02-04-10-06; Memory: 58%; Disk: 65.5% of 991.28GB
Time: 2023-08-02-04-11-07; Memory: 58%; Disk: 65.6% of 991.28GB
Time: 2023-08-02-04-12-08; Memory: 58%; Disk: 65.7% of 991.28GB
Time: 2023-08-02-04-13-09; Memory: 58%; Disk: 65.8% of 991.28GB
Time: 2023-08-02-04-14-10; Memory: 58%; Disk: 65.9% of 991.28GB
Time: 2023-08-02-04-15-11; Memory: 58%; Disk: 66.0% of 991.28GB
Time: 2023-08-02-04-16-11; Memory: 58%; Disk: 66.0% of 991.28GB
Time: 2023-08-02-04-17-12; Memory: 58%; Disk: 66.1% of 991.28GB
Time: 2023-08-02-04-18-13; Memory: 58%; Disk: 66.2% of 991.28GB
Time: 2023-08-02-04-19-14; Memory: 58%; Disk: 66.3% of 991.28GB
Time: 2023-08-02-04-20-15; Memory: 58%; Disk: 66.4% of 991.28GB
Time: 2023-08-02-04-21-16; Memory: 58%; Disk: 66.4% of 991.28GB
Time: 2023-08-02-04-22-17; Memory: 58%; Disk: 66.5% of 991.28GB
Time: 2023-08-02-04-23-18; Memory: 58%; Disk: 66.6% of 991.28GB
Time: 2023-08-02-04-24-19; Memory: 58%; Disk: 66.7% of 991.28GB
Time: 2023-08-02-04-25-20; Memory: 58%; Disk: 66.8% of 991.28GB
Time: 2023-08-02-04-26-21; Memory: 58%; Disk: 66.9% of 991.28GB
Time: 2023-08-02-04-27-21; Memory: 58%; Disk: 67.0% of 991.28GB
Time: 2023-08-02-04-28-22; Memory: 58%; Disk: 67.1% of 991.28GB
Time: 2023-08-02-04-29-23; Memory: 58%; Disk: 67.1% of 991.28GB
Time: 2023-08-02-04-30-24; Memory: 58%; Disk: 67.2% of 991.28GB
Time: 2023-08-02-04-31-25; Memory: 58%; Disk: 67.3% of 991.28GB
Time: 2023-08-02-04-32-26; Memory: 58%; Disk: 67.4% of 991.28GB
Time: 2023-08-02-04-33-27; Memory: 58%; Disk: 67.5% of 991.28GB
Time: 2023-08-02-04-34-28; Memory: 58%; Disk: 67.5% of 991.28GB
Time: 2023-08-02-04-35-29; Memory: 58%; Disk: 67.6% of 991.28GB
Time: 2023-08-02-04-36-30; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-37-31; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-38-32; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-39-32; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-40-33; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-41-34; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-42-35; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-43-36; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-44-37; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-45-38; Memory: 57%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-46-39; Memory: 57%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-47-40; Memory: 56%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-48-41; Memory: 55%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-49-42; Memory: 55%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-50-42; Memory: 55%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-51-43; Memory: 54%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-52-44; Memory: 53%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-53-45; Memory: 51%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-54-46; Memory: 48%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-55-47; Memory: 44%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-56-48; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-57-49; Memory: 37%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-58-50; Memory: 33%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-04-59-51; Memory: 29%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-00-52; Memory: 22%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-01-53; Memory: 1%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-02-53; Memory: 5%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-03-54; Memory: 15%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-04-55; Memory: 28%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-05-56; Memory: 20%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-06-57; Memory: 24%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-07-58; Memory: 27%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-08-59; Memory: 30%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-10-00; Memory: 33%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-11-01; Memory: 37%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-12-02; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-13-03; Memory: 41%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-14-04; Memory: 42%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-15-05; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-16-05; Memory: 47%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-17-06; Memory: 50%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-18-07; Memory: 50%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-19-08; Memory: 51%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-20-09; Memory: 54%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-21-10; Memory: 56%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-22-11; Memory: 57%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-23-12; Memory: 60%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-24-13; Memory: 62%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-25-14; Memory: 62%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-26-15; Memory: 66%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-27-16; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-28-17; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-29-17; Memory: 50%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-30-18; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-31-19; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-32-20; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-33-21; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-34-22; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-35-23; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-36-24; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-37-25; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-38-26; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-39-27; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-40-28; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-41-29; Memory: 48%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-42-29; Memory: 48%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-43-30; Memory: 48%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-44-31; Memory: 48%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-45-32; Memory: 48%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-46-33; Memory: 47%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-47-34; Memory: 47%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-48-35; Memory: 46%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-49-36; Memory: 46%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-50-37; Memory: 46%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-51-38; Memory: 46%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-52-39; Memory: 46%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-53-40; Memory: 46%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-54-40; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-55-41; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-56-42; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-57-43; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-58-44; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-05-59-45; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-00-46; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-01-47; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-02-48; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-03-49; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-04-50; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-05-51; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-06-51; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-07-52; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-08-53; Memory: 44%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-09-54; Memory: 44%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-10-55; Memory: 44%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-11-56; Memory: 44%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-12-57; Memory: 44%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-13-58; Memory: 44%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-14-59; Memory: 43%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-16-00; Memory: 43%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-17-01; Memory: 43%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-18-02; Memory: 43%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-19-02; Memory: 43%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-20-03; Memory: 43%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-21-04; Memory: 42%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-22-05; Memory: 42%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-23-06; Memory: 42%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-24-07; Memory: 41%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-25-08; Memory: 41%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-26-09; Memory: 41%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-27-10; Memory: 41%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-28-11; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-29-12; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-30-12; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-31-13; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-32-14; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-33-15; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-34-16; Memory: 39%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-35-17; Memory: 39%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-36-18; Memory: 39%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-37-19; Memory: 39%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-38-20; Memory: 39%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-39-21; Memory: 38%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-40-22; Memory: 38%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-41-23; Memory: 38%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-42-23; Memory: 38%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-43-24; Memory: 38%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-44-25; Memory: 37%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-45-26; Memory: 37%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-46-27; Memory: 37%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-47-28; Memory: 37%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-48-29; Memory: 37%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-49-30; Memory: 37%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-50-31; Memory: 36%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-51-32; Memory: 36%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-52-33; Memory: 36%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-53-34; Memory: 36%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-54-34; Memory: 36%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-55-35; Memory: 35%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-56-36; Memory: 35%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-57-37; Memory: 35%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-58-38; Memory: 35%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-06-59-39; Memory: 35%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-00-40; Memory: 34%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-01-41; Memory: 34%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-02-42; Memory: 34%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-03-43; Memory: 33%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-04-44; Memory: 33%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-05-45; Memory: 33%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-06-45; Memory: 32%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-07-46; Memory: 32%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-08-47; Memory: 32%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-09-48; Memory: 31%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-10-49; Memory: 31%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-11-50; Memory: 31%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-12-51; Memory: 30%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-13-52; Memory: 30%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-14-53; Memory: 30%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-15-54; Memory: 29%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-16-55; Memory: 29%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-17-55; Memory: 29%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-18-56; Memory: 28%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-19-57; Memory: 28%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-20-58; Memory: 28%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-21-59; Memory: 27%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-23-00; Memory: 27%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-24-01; Memory: 26%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-25-02; Memory: 26%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-26-03; Memory: 25%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-27-04; Memory: 24%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-28-05; Memory: 23%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-29-06; Memory: 22%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-30-06; Memory: 19%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-31-07; Memory: 2%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-32-08; Memory: 4%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-33-09; Memory: 6%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-34-10; Memory: 7%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-35-11; Memory: 7%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-36-12; Memory: 7%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-37-13; Memory: 7%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-38-14; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-39-15; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-40-16; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-41-17; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-42-17; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-43-18; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-44-19; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-45-20; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-46-21; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-47-22; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-48-23; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-49-24; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-50-25; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-51-26; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-52-27; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-53-28; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-54-28; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-55-29; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-56-30; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-57-31; Memory: 8%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-58-32; Memory: 9%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-07-59-33; Memory: 10%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-00-34; Memory: 12%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-01-35; Memory: 13%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-02-36; Memory: 16%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-03-37; Memory: 20%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-04-38; Memory: 24%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-05-39; Memory: 28%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-06-39; Memory: 31%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-07-40; Memory: 33%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-08-41; Memory: 35%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-09-42; Memory: 38%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-10-43; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-11-44; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-12-45; Memory: 40%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-13-46; Memory: 42%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-14-47; Memory: 45%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-15-48; Memory: 47%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-16-49; Memory: 47%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-17-50; Memory: 49%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-18-51; Memory: 51%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-19-51; Memory: 54%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-20-52; Memory: 56%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-21-53; Memory: 56%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-22-54; Memory: 56%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-23-55; Memory: 58%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-24-56; Memory: 59%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-25-57; Memory: 61%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-26-58; Memory: 62%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-27-59; Memory: 64%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-29-00; Memory: 65%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-30-01; Memory: 66%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-31-02; Memory: 66%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-32-03; Memory: 66%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-33-04; Memory: 67%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-34-05; Memory: 69%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-35-05; Memory: 70%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-36-06; Memory: 72%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-37-07; Memory: 74%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-38-08; Memory: 74%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-39-09; Memory: 74%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-40-10; Memory: 74%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-41-11; Memory: 74%; Disk: 67.7% of 991.28GB
Time: 2023-08-02-08-42-12; Memory: 74%; Disk: 67.8% of 991.28GB
Time: 2023-08-02-08-43-13; Memory: 74%; Disk: 67.8% of 991.28GB
Time: 2023-08-02-08-44-14; Memory: 74%; Disk: 67.9% of 991.28GB
Time: 2023-08-02-08-45-15; Memory: 74%; Disk: 68.0% of 991.28GB
Time: 2023-08-02-08-46-16; Memory: 74%; Disk: 68.1% of 991.28GB
Time: 2023-08-02-08-47-17; Memory: 74%; Disk: 68.3% of 991.28GB
Time: 2023-08-02-08-48-17; Memory: 74%; Disk: 68.4% of 991.28GB
Time: 2023-08-02-08-49-18; Memory: 74%; Disk: 68.5% of 991.28GB
Time: 2023-08-02-08-50-19; Memory: 74%; Disk: 68.6% of 991.28GB
Time: 2023-08-02-08-51-20; Memory: 74%; Disk: 68.7% of 991.28GB
Time: 2023-08-02-08-52-21; Memory: 74%; Disk: 68.8% of 991.28GB
Time: 2023-08-02-08-53-22; Memory: 74%; Disk: 68.8% of 991.28GB
Time: 2023-08-02-08-54-23; Memory: 74%; Disk: 68.9% of 991.28GB
Time: 2023-08-02-08-55-24; Memory: 74%; Disk: 69.0% of 991.28GB
Time: 2023-08-02-08-56-25; Memory: 74%; Disk: 69.1% of 991.28GB
Time: 2023-08-02-08-57-26; Memory: 74%; Disk: 69.2% of 991.28GB
Time: 2023-08-02-08-58-27; Memory: 74%; Disk: 69.4% of 991.28GB
Time: 2023-08-02-08-59-28; Memory: 74%; Disk: 69.5% of 991.28GB
Time: 2023-08-02-09-00-29; Memory: 74%; Disk: 69.6% of 991.28GB
Time: 2023-08-02-09-01-30; Memory: 74%; Disk: 69.7% of 991.28GB
Time: 2023-08-02-09-02-31; Memory: 74%; Disk: 69.8% of 991.28GB
Time: 2023-08-02-09-03-31; Memory: 74%; Disk: 69.9% of 991.28GB
Time: 2023-08-02-09-04-32; Memory: 74%; Disk: 70.0% of 991.28GB
Time: 2023-08-02-09-05-33; Memory: 74%; Disk: 70.1% of 991.28GB
Time: 2023-08-02-09-06-34; Memory: 74%; Disk: 70.2% of 991.28GB
Time: 2023-08-02-09-07-35; Memory: 74%; Disk: 70.3% of 991.28GB
Time: 2023-08-02-09-08-36; Memory: 74%; Disk: 70.4% of 991.28GB
Time: 2023-08-02-09-09-37; Memory: 74%; Disk: 70.5% of 991.28GB
Time: 2023-08-02-09-10-38; Memory: 74%; Disk: 70.6% of 991.28GB
Time: 2023-08-02-09-11-39; Memory: 74%; Disk: 70.7% of 991.28GB
Time: 2023-08-02-09-12-40; Memory: 74%; Disk: 70.8% of 991.28GB
Time: 2023-08-02-09-13-41; Memory: 74%; Disk: 70.9% of 991.28GB
Time: 2023-08-02-09-14-42; Memory: 74%; Disk: 71.0% of 991.28GB
Time: 2023-08-02-09-15-43; Memory: 74%; Disk: 71.1% of 991.28GB
Time: 2023-08-02-09-16-44; Memory: 74%; Disk: 71.2% of 991.28GB
Time: 2023-08-02-09-17-45; Memory: 74%; Disk: 71.3% of 991.28GB
Time: 2023-08-02-09-18-46; Memory: 74%; Disk: 71.4% of 991.28GB
Time: 2023-08-02-09-19-46; Memory: 74%; Disk: 71.4% of 991.28GB
Time: 2023-08-02-09-20-47; Memory: 74%; Disk: 71.5% of 991.28GB
Time: 2023-08-02-09-21-48; Memory: 74%; Disk: 71.6% of 991.28GB
Time: 2023-08-02-09-22-49; Memory: 74%; Disk: 71.7% of 991.28GB
Time: 2023-08-02-09-23-50; Memory: 74%; Disk: 71.8% of 991.28GB
Time: 2023-08-02-09-24-51; Memory: 74%; Disk: 71.9% of 991.28GB
Time: 2023-08-02-09-25-52; Memory: 74%; Disk: 72.0% of 991.28GB
Time: 2023-08-02-09-26-53; Memory: 74%; Disk: 72.1% of 991.28GB
Time: 2023-08-02-09-27-54; Memory: 74%; Disk: 72.2% of 991.28GB
Time: 2023-08-02-09-28-55; Memory: 74%; Disk: 72.3% of 991.28GB
Time: 2023-08-02-09-29-56; Memory: 74%; Disk: 72.3% of 991.28GB
Time: 2023-08-02-09-30-57; Memory: 74%; Disk: 72.4% of 991.28GB
Time: 2023-08-02-09-31-58; Memory: 74%; Disk: 72.5% of 991.28GB
Time: 2023-08-02-09-32-59; Memory: 74%; Disk: 72.6% of 991.28GB
Time: 2023-08-02-09-34-00; Memory: 74%; Disk: 72.7% of 991.28GB
Time: 2023-08-02-09-35-01; Memory: 74%; Disk: 72.8% of 991.28GB
Time: 2023-08-02-09-36-02; Memory: 74%; Disk: 72.9% of 991.28GB
Time: 2023-08-02-09-37-03; Memory: 74%; Disk: 73.0% of 991.28GB
Time: 2023-08-02-09-38-04; Memory: 74%; Disk: 73.1% of 991.28GB
Time: 2023-08-02-09-39-05; Memory: 74%; Disk: 73.2% of 991.28GB
Time: 2023-08-02-09-40-06; Memory: 74%; Disk: 73.3% of 991.28GB
Time: 2023-08-02-09-41-07; Memory: 74%; Disk: 73.3% of 991.28GB
Time: 2023-08-02-09-42-07; Memory: 74%; Disk: 73.4% of 991.28GB
Time: 2023-08-02-09-43-08; Memory: 74%; Disk: 73.5% of 991.28GB
Time: 2023-08-02-09-44-09; Memory: 74%; Disk: 73.6% of 991.28GB
Time: 2023-08-02-09-45-10; Memory: 74%; Disk: 73.7% of 991.28GB
Time: 2023-08-02-09-46-11; Memory: 74%; Disk: 73.8% of 991.28GB
Time: 2023-08-02-09-47-12; Memory: 74%; Disk: 73.9% of 991.28GB
Time: 2023-08-02-09-48-13; Memory: 74%; Disk: 74.0% of 991.28GB
Time: 2023-08-02-09-49-14; Memory: 74%; Disk: 74.1% of 991.28GB
Time: 2023-08-02-09-50-15; Memory: 74%; Disk: 74.1% of 991.28GB
Time: 2023-08-02-09-51-16; Memory: 74%; Disk: 74.2% of 991.28GB
Time: 2023-08-02-09-52-17; Memory: 74%; Disk: 74.3% of 991.28GB
Time: 2023-08-02-09-53-18; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-09-54-19; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-09-55-20; Memory: 70%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-09-56-21; Memory: 67%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-09-57-22; Memory: 66%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-09-58-23; Memory: 64%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-09-59-23; Memory: 61%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-00-24; Memory: 57%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-01-25; Memory: 53%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-02-26; Memory: 49%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-03-27; Memory: 44%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-04-28; Memory: 38%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-05-29; Memory: 33%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-06-30; Memory: 28%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-07-31; Memory: 22%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-08-32; Memory: 16%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-09-33; Memory: 1%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-10-33; Memory: 3%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-11-34; Memory: 6%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-12-35; Memory: 6%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-13-36; Memory: 6%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-14-37; Memory: 6%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-15-38; Memory: 6%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-16-39; Memory: 8%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-17-40; Memory: 10%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-18-41; Memory: 13%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-19-42; Memory: 17%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-20-43; Memory: 21%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-21-44; Memory: 25%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-22-44; Memory: 27%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-23-45; Memory: 31%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-24-46; Memory: 34%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-25-47; Memory: 38%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-26-48; Memory: 39%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-27-49; Memory: 39%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-28-50; Memory: 43%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-29-51; Memory: 46%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-30-52; Memory: 46%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-31-53; Memory: 49%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-32-54; Memory: 53%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-33-55; Memory: 56%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-34-55; Memory: 56%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-35-56; Memory: 57%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-36-57; Memory: 60%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-37-58; Memory: 63%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-38-59; Memory: 66%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-40-00; Memory: 66%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-41-01; Memory: 66%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-42-02; Memory: 69%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-43-03; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-44-04; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-45-05; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-46-06; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-47-07; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-48-08; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-49-09; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-50-10; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-51-11; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-52-12; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-53-13; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-54-13; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-55-14; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-56-15; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-57-16; Memory: 78%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-58-17; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-10-59-18; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-00-19; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-01-20; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-02-21; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-03-22; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-04-23; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-05-24; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-06-25; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-07-26; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-08-27; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-09-27; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-10-28; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-11-29; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-12-30; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-13-31; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-14-32; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-15-33; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-16-34; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-17-35; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-18-36; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-19-37; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-20-38; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-21-38; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-22-39; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-23-40; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-24-41; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-25-42; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-26-43; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-27-44; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-28-45; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-29-46; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-30-47; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-31-48; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-32-48; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-33-49; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-34-50; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-35-51; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-36-52; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-37-53; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-38-54; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-39-55; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-40-56; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-41-57; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-42-58; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-43-59; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-44-59; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-46-00; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-47-01; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-48-02; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-49-03; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-50-04; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-51-05; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-52-06; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-53-07; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-54-08; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-55-09; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-56-10; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-57-11; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-58-11; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-11-59-12; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-00-13; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-01-14; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-02-15; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-03-16; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-04-17; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-05-18; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-06-19; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-07-20; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-08-21; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-09-22; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-10-22; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-11-23; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-12-24; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-13-25; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-14-26; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-15-27; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-16-28; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-17-29; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-18-30; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-19-31; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-20-32; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-21-32; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-22-33; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-23-34; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-24-35; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-25-36; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-26-37; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-27-38; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-28-39; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-29-40; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-30-41; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-31-42; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-32-43; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-33-43; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-34-44; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-35-45; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-36-46; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-37-47; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-38-48; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-39-49; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-40-50; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-41-51; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-42-52; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-43-53; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-44-53; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-45-54; Memory: 77%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-46-55; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-47-56; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-48-57; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-49-58; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-50-59; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-52-00; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-53-01; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-54-02; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-55-03; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-56-03; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-57-04; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-58-05; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-12-59-06; Memory: 76%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-00-07; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-01-08; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-02-09; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-03-10; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-04-11; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-05-12; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-06-13; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-07-13; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-08-14; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-09-15; Memory: 75%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-10-16; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-11-17; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-12-18; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-13-19; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-14-20; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-15-21; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-16-22; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-17-23; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-18-23; Memory: 74%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-19-24; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-20-25; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-21-26; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-22-27; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-23-28; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-24-29; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-25-30; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-26-31; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-27-32; Memory: 73%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-28-33; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-29-34; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-30-34; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-31-35; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-32-36; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-33-37; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-34-38; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-35-39; Memory: 72%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-36-40; Memory: 71%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-37-41; Memory: 71%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-38-42; Memory: 71%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-39-43; Memory: 71%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-40-44; Memory: 71%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-41-44; Memory: 71%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-42-45; Memory: 71%; Disk: 74.4% of 991.28GB
Time: 2023-08-02-13-43-46; Memory: 71%; Disk: 74.5% of 991.28GB
Time: 2023-08-02-13-44-47; Memory: 71%; Disk: 74.6% of 991.28GB
Time: 2023-08-02-13-45-48; Memory: 71%; Disk: 74.6% of 991.28GB
Time: 2023-08-02-13-46-49; Memory: 71%; Disk: 74.7% of 991.28GB
Time: 2023-08-02-13-47-50; Memory: 71%; Disk: 74.8% of 991.28GB
Time: 2023-08-02-13-48-51; Memory: 71%; Disk: 74.8% of 991.28GB
Time: 2023-08-02-13-49-52; Memory: 71%; Disk: 74.9% of 991.28GB
Time: 2023-08-02-13-50-53; Memory: 71%; Disk: 74.9% of 991.28GB
Time: 2023-08-02-13-51-54; Memory: 71%; Disk: 75.0% of 991.28GB
Time: 2023-08-02-13-52-55; Memory: 71%; Disk: 75.1% of 991.28GB
Time: 2023-08-02-13-53-55; Memory: 71%; Disk: 75.1% of 991.28GB
Time: 2023-08-02-13-54-56; Memory: 71%; Disk: 75.2% of 991.28GB
Time: 2023-08-02-13-55-57; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-13-56-58; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-13-57-59; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-13-59-00; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-00-01; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-01-02; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-02-03; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-03-04; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-04-05; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-05-06; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-06-07; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-07-08; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-08-09; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-09-10; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-10-11; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-11-12; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-12-13; Memory: 71%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-13-14; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-14-15; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-15-16; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-16-17; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-17-18; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-18-19; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-19-20; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-20-20; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-21-21; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-22-22; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-23-23; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-24-24; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-25-25; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-26-26; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-27-27; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-28-28; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-29-29; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-30-30; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-31-31; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-32-32; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-33-33; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-34-34; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-35-35; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-36-36; Memory: 70%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-37-37; Memory: 69%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-38-38; Memory: 69%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-39-38; Memory: 69%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-40-39; Memory: 69%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-41-40; Memory: 69%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-42-41; Memory: 69%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-43-42; Memory: 69%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-44-43; Memory: 68%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-45-44; Memory: 68%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-46-45; Memory: 68%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-47-46; Memory: 68%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-48-47; Memory: 68%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-49-48; Memory: 68%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-50-49; Memory: 68%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-51-50; Memory: 67%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-52-51; Memory: 67%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-53-52; Memory: 67%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-54-53; Memory: 67%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-55-54; Memory: 67%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-56-55; Memory: 67%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-57-56; Memory: 67%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-58-56; Memory: 66%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-14-59-57; Memory: 66%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-00-58; Memory: 66%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-01-59; Memory: 66%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-03-00; Memory: 66%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-04-01; Memory: 66%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-05-02; Memory: 66%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-06-03; Memory: 65%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-07-04; Memory: 65%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-08-05; Memory: 65%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-09-06; Memory: 65%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-10-07; Memory: 65%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-11-07; Memory: 65%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-12-08; Memory: 65%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-13-09; Memory: 64%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-14-10; Memory: 64%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-15-11; Memory: 64%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-16-12; Memory: 64%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-17-13; Memory: 64%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-18-14; Memory: 64%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-19-15; Memory: 64%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-20-16; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-21-17; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-22-18; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-23-18; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-24-19; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-25-20; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-26-21; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-27-22; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-28-23; Memory: 62%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-29-24; Memory: 62%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-30-25; Memory: 62%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-31-26; Memory: 62%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-32-27; Memory: 62%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-33-28; Memory: 62%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-34-29; Memory: 62%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-35-29; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-36-30; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-37-31; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-38-32; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-39-33; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-40-34; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-41-35; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-42-36; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-43-37; Memory: 60%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-44-38; Memory: 60%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-45-39; Memory: 60%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-46-40; Memory: 60%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-47-41; Memory: 60%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-48-41; Memory: 60%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-49-42; Memory: 60%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-50-43; Memory: 59%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-51-44; Memory: 59%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-52-45; Memory: 59%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-53-46; Memory: 59%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-54-47; Memory: 59%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-55-48; Memory: 59%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-56-49; Memory: 59%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-57-50; Memory: 59%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-58-51; Memory: 58%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-15-59-52; Memory: 58%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-00-52; Memory: 58%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-01-53; Memory: 58%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-02-54; Memory: 58%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-03-55; Memory: 58%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-04-56; Memory: 58%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-05-57; Memory: 57%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-06-58; Memory: 57%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-07-59; Memory: 57%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-09-00; Memory: 57%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-10-01; Memory: 57%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-11-02; Memory: 57%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-12-03; Memory: 57%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-13-03; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-14-04; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-15-05; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-16-06; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-17-07; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-18-08; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-19-09; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-20-10; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-21-11; Memory: 55%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-22-12; Memory: 55%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-23-13; Memory: 55%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-24-14; Memory: 55%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-25-14; Memory: 55%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-26-15; Memory: 55%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-27-16; Memory: 55%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-28-17; Memory: 54%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-29-18; Memory: 54%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-30-19; Memory: 54%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-31-20; Memory: 54%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-32-21; Memory: 54%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-33-22; Memory: 54%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-34-23; Memory: 54%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-35-24; Memory: 53%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-36-25; Memory: 53%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-37-25; Memory: 53%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-38-26; Memory: 53%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-39-27; Memory: 53%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-40-28; Memory: 53%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-41-29; Memory: 52%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-42-30; Memory: 52%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-43-31; Memory: 52%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-44-32; Memory: 52%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-45-33; Memory: 52%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-46-34; Memory: 52%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-47-35; Memory: 51%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-48-36; Memory: 51%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-49-36; Memory: 51%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-50-37; Memory: 51%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-51-38; Memory: 51%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-52-39; Memory: 50%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-53-40; Memory: 50%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-54-41; Memory: 50%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-55-42; Memory: 50%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-56-43; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-57-44; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-58-45; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-16-59-46; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-00-47; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-01-47; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-02-48; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-03-49; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-04-50; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-05-51; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-06-52; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-07-53; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-08-54; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-09-55; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-10-56; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-11-57; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-12-58; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-13-59; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-14-59; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-16-00; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-17-01; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-18-02; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-19-03; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-20-04; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-21-05; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-22-06; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-23-07; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-24-08; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-25-09; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-26-10; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-27-10; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-28-11; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-29-12; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-30-13; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-31-14; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-32-15; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-33-16; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-34-17; Memory: 41%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-35-18; Memory: 41%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-36-19; Memory: 41%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-37-20; Memory: 41%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-38-21; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-39-22; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-40-22; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-41-23; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-42-24; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-43-25; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-44-26; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-45-27; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-46-28; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-47-29; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-48-30; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-49-31; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-50-32; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-51-33; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-52-33; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-53-34; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-54-35; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-55-36; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-56-37; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-57-38; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-58-39; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-17-59-40; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-00-41; Memory: 34%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-01-42; Memory: 34%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-02-43; Memory: 34%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-03-44; Memory: 33%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-04-45; Memory: 33%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-05-45; Memory: 33%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-06-46; Memory: 32%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-07-47; Memory: 32%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-08-48; Memory: 32%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-09-49; Memory: 31%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-10-50; Memory: 31%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-11-51; Memory: 30%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-12-52; Memory: 30%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-13-53; Memory: 29%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-14-54; Memory: 29%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-15-55; Memory: 28%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-16-56; Memory: 28%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-17-57; Memory: 27%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-18-57; Memory: 26%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-19-58; Memory: 24%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-20-59; Memory: 18%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-22-00; Memory: 5%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-23-01; Memory: 11%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-24-02; Memory: 16%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-25-03; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-26-04; Memory: 20%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-27-05; Memory: 24%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-28-06; Memory: 26%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-29-07; Memory: 29%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-30-08; Memory: 33%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-31-09; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-32-10; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-33-10; Memory: 41%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-34-11; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-35-12; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-36-13; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-37-14; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-38-15; Memory: 50%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-39-16; Memory: 51%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-40-17; Memory: 55%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-41-18; Memory: 56%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-42-19; Memory: 57%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-43-20; Memory: 61%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-44-21; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-45-22; Memory: 63%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-46-22; Memory: 65%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-47-23; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-48-24; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-49-25; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-50-26; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-51-27; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-52-28; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-53-29; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-54-30; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-55-31; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-56-32; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-57-33; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-58-33; Memory: 49%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-18-59-34; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-00-35; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-01-36; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-02-37; Memory: 48%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-03-38; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-04-39; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-05-40; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-06-41; Memory: 47%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-07-42; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-08-43; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-09-44; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-10-44; Memory: 46%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-11-45; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-12-46; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-13-47; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-14-48; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-15-49; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-16-50; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-17-51; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-18-52; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-19-53; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-20-54; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-21-55; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-22-55; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-23-56; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-24-57; Memory: 45%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-25-58; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-26-59; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-28-00; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-29-01; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-30-02; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-31-03; Memory: 44%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-32-04; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-33-05; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-34-06; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-35-07; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-36-07; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-37-08; Memory: 43%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-38-09; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-39-10; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-40-11; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-41-12; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-42-13; Memory: 42%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-43-14; Memory: 41%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-44-15; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-45-16; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-46-17; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-47-18; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-48-18; Memory: 40%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-49-19; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-50-20; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-51-21; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-52-22; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-53-23; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-54-24; Memory: 39%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-55-25; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-56-26; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-57-27; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-58-28; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-19-59-29; Memory: 38%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-00-29; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-01-30; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-02-31; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-03-32; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-04-33; Memory: 37%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-05-34; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-06-35; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-07-36; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-08-37; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-09-38; Memory: 36%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-10-39; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-11-40; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-12-40; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-13-41; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-14-42; Memory: 35%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-15-43; Memory: 34%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-16-44; Memory: 34%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-17-45; Memory: 34%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-18-46; Memory: 34%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-19-47; Memory: 33%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-20-48; Memory: 33%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-21-49; Memory: 33%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-22-50; Memory: 33%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-23-51; Memory: 32%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-24-51; Memory: 32%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-25-52; Memory: 32%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-26-53; Memory: 31%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-27-54; Memory: 31%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-28-55; Memory: 31%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-29-56; Memory: 30%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-30-57; Memory: 30%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-31-58; Memory: 30%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-32-59; Memory: 29%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-34-00; Memory: 29%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-35-01; Memory: 29%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-36-02; Memory: 28%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-37-02; Memory: 28%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-38-03; Memory: 28%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-39-04; Memory: 27%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-40-05; Memory: 27%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-41-06; Memory: 26%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-42-07; Memory: 26%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-43-08; Memory: 25%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-44-09; Memory: 25%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-45-10; Memory: 24%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-46-11; Memory: 24%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-47-12; Memory: 23%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-48-13; Memory: 22%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-49-13; Memory: 20%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-50-14; Memory: 17%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-51-15; Memory: 0%; Disk: 75.3% of 991.28GB
Time: 2023-08-02-20-52-16; Memory: 0%; Disk: 75.4% of 991.28GB
Time: 2023-08-02-20-53-17; Memory: 0%; Disk: 75.4% of 991.28GB
Time: 2023-08-02-20-54-18; Memory: 0%; Disk: 75.4% of 991.28GB
Time: 2023-08-02-20-55-19; Memory: 0%; Disk: 75.5% of 991.28GB
Time: 2023-08-02-20-56-20; Memory: 0%; Disk: 75.6% of 991.28GB
Time: 2023-08-02-20-57-21; Memory: 0%; Disk: 75.6% of 991.28GB
Time: 2023-08-02-20-58-22; Memory: 0%; Disk: 75.6% of 991.28GB
Time: 2023-08-02-20-59-23; Memory: 0%; Disk: 75.6% of 991.28GB
Time: 2023-08-02-21-00-24; Memory: 0%; Disk: 75.6% of 991.28GB
Time: 2023-08-02-21-01-25; Memory: 0%; Disk: 75.6% of 991.28GB
Time: 2023-08-02-21-02-25; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-03-26; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-04-27; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-05-28; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-06-29; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-07-30; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-08-31; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-09-32; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-10-33; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-11-34; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-12-35; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-13-36; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-14-36; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-15-37; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-16-38; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-17-39; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-18-40; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-19-41; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-20-42; Memory: 0%; Disk: 75.7% of 991.28GB
Time: 2023-08-02-21-21-43; Memory: 0%; Disk: 75.8% of 991.28GB
Time: 2023-08-02-21-22-44; Memory: 0%; Disk: 75.8% of 991.28GB
Time: 2023-08-02-21-23-45; Memory: 1%; Disk: 75.9% of 991.28GB
Time: 2023-08-02-21-24-46; Memory: 1%; Disk: 75.9% of 991.28GB
Time: 2023-08-02-21-25-47; Memory: 1%; Disk: 75.9% of 991.28GB
Time: 2023-08-02-21-26-47; Memory: 1%; Disk: 76.0% of 991.28GB
Time: 2023-08-02-21-27-48; Memory: 1%; Disk: 76.0% of 991.28GB
Time: 2023-08-02-21-28-49; Memory: 1%; Disk: 76.1% of 991.28GB
Time: 2023-08-02-21-29-50; Memory: 1%; Disk: 76.1% of 991.28GB
Time: 2023-08-02-21-30-51; Memory: 1%; Disk: 76.2% of 991.28GB
Time: 2023-08-02-21-31-52; Memory: 1%; Disk: 76.3% of 991.28GB
Time: 2023-08-02-21-32-53; Memory: 1%; Disk: 76.4% of 991.28GB
Time: 2023-08-02-21-33-54; Memory: 1%; Disk: 76.6% of 991.28GB
Time: 2023-08-02-21-34-55; Memory: 1%; Disk: 76.7% of 991.28GB
Time: 2023-08-02-21-35-56; Memory: 1%; Disk: 76.8% of 991.28GB
Time: 2023-08-02-21-36-57; Memory: 1%; Disk: 76.9% of 991.28GB
Time: 2023-08-02-21-37-58; Memory: 1%; Disk: 77.0% of 991.28GB
Time: 2023-08-02-21-38-58; Memory: 1%; Disk: 77.1% of 991.28GB
Time: 2023-08-02-21-39-59; Memory: 1%; Disk: 77.2% of 991.28GB
Time: 2023-08-02-21-41-00; Memory: 1%; Disk: 77.2% of 991.28GB
Time: 2023-08-02-21-42-01; Memory: 1%; Disk: 77.3% of 991.28GB
Time: 2023-08-02-21-43-02; Memory: 1%; Disk: 77.4% of 991.28GB
Time: 2023-08-02-21-44-03; Memory: 1%; Disk: 77.5% of 991.28GB
Time: 2023-08-02-21-45-04; Memory: 1%; Disk: 77.6% of 991.28GB
Time: 2023-08-02-21-46-05; Memory: 1%; Disk: 77.7% of 991.28GB
Time: 2023-08-02-21-47-06; Memory: 1%; Disk: 77.7% of 991.28GB
Time: 2023-08-02-21-48-07; Memory: 1%; Disk: 77.8% of 991.28GB
Time: 2023-08-02-21-49-08; Memory: 1%; Disk: 77.9% of 991.28GB
Time: 2023-08-02-21-50-09; Memory: 1%; Disk: 77.9% of 991.28GB
Time: 2023-08-02-21-51-09; Memory: 1%; Disk: 78.0% of 991.28GB
Time: 2023-08-02-21-52-10; Memory: 1%; Disk: 78.1% of 991.28GB
Time: 2023-08-02-21-53-11; Memory: 1%; Disk: 78.1% of 991.28GB
Time: 2023-08-02-21-54-12; Memory: 1%; Disk: 78.2% of 991.28GB
Time: 2023-08-02-21-55-13; Memory: 1%; Disk: 78.3% of 991.28GB
Time: 2023-08-02-21-56-14; Memory: 1%; Disk: 78.3% of 991.28GB
Time: 2023-08-02-21-57-15; Memory: 1%; Disk: 78.4% of 991.28GB
Time: 2023-08-02-21-58-16; Memory: 1%; Disk: 78.5% of 991.28GB
Time: 2023-08-02-21-59-17; Memory: 1%; Disk: 78.5% of 991.28GB
Time: 2023-08-02-22-00-18; Memory: 1%; Disk: 78.6% of 991.28GB
Time: 2023-08-02-22-01-19; Memory: 1%; Disk: 78.7% of 991.28GB
Time: 2023-08-02-22-02-20; Memory: 1%; Disk: 78.8% of 991.28GB
Time: 2023-08-02-22-03-20; Memory: 1%; Disk: 78.8% of 991.28GB
Time: 2023-08-02-22-04-21; Memory: 1%; Disk: 78.9% of 991.28GB
Time: 2023-08-02-22-05-22; Memory: 1%; Disk: 78.9% of 991.28GB
Time: 2023-08-02-22-06-23; Memory: 1%; Disk: 79.0% of 991.28GB
Time: 2023-08-02-22-07-24; Memory: 1%; Disk: 79.0% of 991.28GB
Time: 2023-08-02-22-08-25; Memory: 1%; Disk: 79.1% of 991.28GB
Time: 2023-08-02-22-09-26; Memory: 1%; Disk: 79.1% of 991.28GB
Time: 2023-08-02-22-10-27; Memory: 1%; Disk: 79.2% of 991.28GB
Time: 2023-08-02-22-11-28; Memory: 1%; Disk: 79.2% of 991.28GB
Time: 2023-08-02-22-12-29; Memory: 1%; Disk: 79.3% of 991.28GB
Time: 2023-08-02-22-13-30; Memory: 1%; Disk: 79.3% of 991.28GB
Time: 2023-08-02-22-14-31; Memory: 1%; Disk: 79.4% of 991.28GB
Time: 2023-08-02-22-15-31; Memory: 1%; Disk: 79.4% of 991.28GB
Time: 2023-08-02-22-16-32; Memory: 1%; Disk: 79.5% of 991.28GB
Time: 2023-08-02-22-17-33; Memory: 1%; Disk: 79.5% of 991.28GB
Time: 2023-08-02-22-18-34; Memory: 1%; Disk: 79.6% of 991.28GB
Time: 2023-08-02-22-19-35; Memory: 1%; Disk: 79.7% of 991.28GB
Time: 2023-08-02-22-20-36; Memory: 1%; Disk: 79.7% of 991.28GB
Time: 2023-08-02-22-21-37; Memory: 1%; Disk: 79.7% of 991.28GB
Time: 2023-08-02-22-22-38; Memory: 1%; Disk: 79.7% of 991.28GB
Time: 2023-08-02-22-23-39; Memory: 1%; Disk: 79.7% of 991.28GB
Time: 2023-08-02-22-24-40; Memory: 1%; Disk: 79.8% of 991.28GB
Time: 2023-08-02-22-25-41; Memory: 1%; Disk: 79.8% of 991.28GB
Time: 2023-08-02-22-26-41; Memory: 1%; Disk: 79.8% of 991.28GB
Time: 2023-08-02-22-27-42; Memory: 1%; Disk: 79.8% of 991.28GB
Time: 2023-08-02-22-28-43; Memory: 1%; Disk: 79.9% of 991.28GB
Time: 2023-08-02-22-29-44; Memory: 1%; Disk: 79.9% of 991.28GB
Time: 2023-08-02-22-30-45; Memory: 1%; Disk: 79.9% of 991.28GB
Time: 2023-08-02-22-31-46; Memory: 1%; Disk: 80.0% of 991.28GB
Time: 2023-08-02-22-32-47; Memory: 1%; Disk: 80.0% of 991.28GB
Time: 2023-08-02-22-33-48; Memory: 1%; Disk: 80.0% of 991.28GB
Time: 2023-08-02-22-34-49; Memory: 1%; Disk: 80.0% of 991.28GB
Time: 2023-08-02-22-35-50; Memory: 1%; Disk: 80.1% of 991.28GB
Time: 2023-08-02-22-36-51; Memory: 1%; Disk: 80.1% of 991.28GB
Time: 2023-08-02-22-37-52; Memory: 1%; Disk: 80.1% of 991.28GB
Time: 2023-08-02-22-38-52; Memory: 1%; Disk: 80.2% of 991.28GB
Time: 2023-08-02-22-39-53; Memory: 1%; Disk: 80.2% of 991.28GB
Time: 2023-08-02-22-40-54; Memory: 1%; Disk: 80.2% of 991.28GB
Time: 2023-08-02-22-41-55; Memory: 1%; Disk: 80.2% of 991.28GB
Time: 2023-08-02-22-42-56; Memory: 1%; Disk: 80.3% of 991.28GB
Time: 2023-08-02-22-43-57; Memory: 1%; Disk: 80.3% of 991.28GB
Time: 2023-08-02-22-44-58; Memory: 1%; Disk: 80.3% of 991.28GB
Time: 2023-08-02-22-45-59; Memory: 1%; Disk: 80.4% of 991.28GB
Time: 2023-08-02-22-47-00; Memory: 1%; Disk: 80.4% of 991.28GB
Time: 2023-08-02-22-48-01; Memory: 1%; Disk: 80.4% of 991.28GB
Time: 2023-08-02-22-49-02; Memory: 1%; Disk: 80.5% of 991.28GB
Time: 2023-08-02-22-50-02; Memory: 1%; Disk: 80.5% of 991.28GB
Time: 2023-08-02-22-51-03; Memory: 1%; Disk: 80.5% of 991.28GB
Time: 2023-08-02-22-52-04; Memory: 1%; Disk: 80.5% of 991.28GB
Time: 2023-08-02-22-53-05; Memory: 1%; Disk: 80.6% of 991.28GB
Time: 2023-08-02-22-54-06; Memory: 1%; Disk: 80.6% of 991.28GB
Time: 2023-08-02-22-55-07; Memory: 1%; Disk: 80.6% of 991.28GB
Time: 2023-08-02-22-56-08; Memory: 1%; Disk: 80.6% of 991.28GB
Time: 2023-08-02-22-57-09; Memory: 1%; Disk: 80.6% of 991.28GB
Time: 2023-08-02-22-58-10; Memory: 1%; Disk: 80.7% of 991.28GB
Time: 2023-08-02-22-59-11; Memory: 1%; Disk: 80.7% of 991.28GB
Time: 2023-08-02-23-00-12; Memory: 1%; Disk: 80.7% of 991.28GB
Time: 2023-08-02-23-01-12; Memory: 1%; Disk: 80.7% of 991.28GB
Time: 2023-08-02-23-02-13; Memory: 1%; Disk: 80.8% of 991.28GB
Time: 2023-08-02-23-03-14; Memory: 1%; Disk: 80.8% of 991.28GB
Time: 2023-08-02-23-04-15; Memory: 1%; Disk: 80.8% of 991.28GB
Time: 2023-08-02-23-05-16; Memory: 1%; Disk: 80.8% of 991.28GB
Time: 2023-08-02-23-06-17; Memory: 1%; Disk: 80.9% of 991.28GB
Time: 2023-08-02-23-07-18; Memory: 1%; Disk: 80.9% of 991.28GB
Time: 2023-08-02-23-08-19; Memory: 1%; Disk: 80.9% of 991.28GB
Time: 2023-08-02-23-09-20; Memory: 1%; Disk: 81.0% of 991.28GB
Time: 2023-08-02-23-10-21; Memory: 1%; Disk: 81.0% of 991.28GB
Time: 2023-08-02-23-11-22; Memory: 1%; Disk: 81.0% of 991.28GB
Time: 2023-08-02-23-12-23; Memory: 1%; Disk: 81.1% of 991.28GB
Time: 2023-08-02-23-13-24; Memory: 1%; Disk: 81.1% of 991.28GB
Time: 2023-08-02-23-14-24; Memory: 1%; Disk: 81.1% of 991.28GB
Time: 2023-08-02-23-15-25; Memory: 1%; Disk: 81.1% of 991.28GB
Time: 2023-08-02-23-16-26; Memory: 1%; Disk: 81.2% of 991.28GB
Time: 2023-08-02-23-17-27; Memory: 1%; Disk: 81.2% of 991.28GB
Time: 2023-08-02-23-18-28; Memory: 1%; Disk: 81.2% of 991.28GB
Time: 2023-08-02-23-19-29; Memory: 1%; Disk: 81.3% of 991.28GB
Time: 2023-08-02-23-20-30; Memory: 1%; Disk: 81.3% of 991.28GB
Time: 2023-08-02-23-21-31; Memory: 1%; Disk: 81.3% of 991.28GB
Time: 2023-08-02-23-22-32; Memory: 1%; Disk: 81.4% of 991.28GB
Time: 2023-08-02-23-23-33; Memory: 1%; Disk: 81.4% of 991.28GB
Time: 2023-08-02-23-24-34; Memory: 1%; Disk: 81.4% of 991.28GB
Time: 2023-08-02-23-25-35; Memory: 1%; Disk: 81.4% of 991.28GB
Time: 2023-08-02-23-26-36; Memory: 1%; Disk: 81.4% of 991.28GB
Time: 2023-08-02-23-27-36; Memory: 1%; Disk: 81.5% of 991.28GB
Time: 2023-08-02-23-28-37; Memory: 1%; Disk: 81.5% of 991.28GB
Time: 2023-08-02-23-29-38; Memory: 1%; Disk: 81.5% of 991.28GB
Time: 2023-08-02-23-30-39; Memory: 1%; Disk: 81.5% of 991.28GB
Time: 2023-08-02-23-31-40; Memory: 1%; Disk: 81.6% of 991.28GB
Time: 2023-08-02-23-32-41; Memory: 1%; Disk: 81.6% of 991.28GB
Time: 2023-08-02-23-33-42; Memory: 1%; Disk: 81.6% of 991.28GB
Time: 2023-08-02-23-34-43; Memory: 1%; Disk: 81.7% of 991.28GB
Time: 2023-08-02-23-35-44; Memory: 1%; Disk: 81.7% of 991.28GB
Time: 2023-08-02-23-36-45; Memory: 1%; Disk: 81.7% of 991.28GB
Time: 2023-08-02-23-37-46; Memory: 1%; Disk: 81.7% of 991.28GB
Time: 2023-08-02-23-38-47; Memory: 1%; Disk: 81.8% of 991.28GB
Time: 2023-08-02-23-39-48; Memory: 1%; Disk: 81.8% of 991.28GB
Time: 2023-08-02-23-40-49; Memory: 1%; Disk: 81.8% of 991.28GB
Time: 2023-08-02-23-41-49; Memory: 1%; Disk: 81.9% of 991.28GB
Time: 2023-08-02-23-42-50; Memory: 1%; Disk: 81.9% of 991.28GB
Time: 2023-08-02-23-43-51; Memory: 1%; Disk: 81.9% of 991.28GB
Time: 2023-08-02-23-44-52; Memory: 1%; Disk: 81.9% of 991.28GB
Time: 2023-08-02-23-45-53; Memory: 1%; Disk: 82.0% of 991.28GB
Time: 2023-08-02-23-46-54; Memory: 1%; Disk: 82.0% of 991.28GB
Time: 2023-08-02-23-47-55; Memory: 1%; Disk: 82.0% of 991.28GB
Time: 2023-08-02-23-48-56; Memory: 1%; Disk: 82.1% of 991.28GB
Time: 2023-08-02-23-49-57; Memory: 1%; Disk: 82.1% of 991.28GB
Time: 2023-08-02-23-50-58; Memory: 1%; Disk: 82.1% of 991.28GB
Time: 2023-08-02-23-51-59; Memory: 1%; Disk: 82.2% of 991.28GB
Time: 2023-08-02-23-53-00; Memory: 1%; Disk: 82.2% of 991.28GB
Time: 2023-08-02-23-54-01; Memory: 1%; Disk: 82.2% of 991.28GB
Time: 2023-08-02-23-55-01; Memory: 1%; Disk: 82.3% of 991.28GB
Time: 2023-08-02-23-56-02; Memory: 1%; Disk: 82.3% of 991.28GB
Time: 2023-08-02-23-57-03; Memory: 1%; Disk: 82.3% of 991.28GB
Time: 2023-08-02-23-58-04; Memory: 1%; Disk: 82.3% of 991.28GB
Time: 2023-08-02-23-59-05; Memory: 1%; Disk: 82.4% of 991.28GB
Time: 2023-08-03-00-00-06; Memory: 1%; Disk: 82.4% of 991.28GB
Time: 2023-08-03-00-01-07; Memory: 1%; Disk: 82.4% of 991.28GB
Time: 2023-08-03-00-02-08; Memory: 1%; Disk: 82.4% of 991.28GB
Time: 2023-08-03-00-03-09; Memory: 1%; Disk: 82.4% of 991.28GB
Time: 2023-08-03-00-04-10; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-05-11; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-06-12; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-07-12; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-08-13; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-09-14; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-10-15; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-11-16; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-12-17; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-13-18; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-14-19; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-15-20; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-16-21; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-17-22; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-18-23; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-19-23; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-20-24; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-21-25; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-22-26; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-23-27; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-24-28; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-25-29; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-26-30; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-27-31; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-28-32; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-29-33; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-30-33; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-31-34; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-32-35; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-33-36; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-34-37; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-35-38; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-36-39; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-37-40; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-38-41; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-39-42; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-40-43; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-41-43; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-42-44; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-43-45; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-44-46; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-45-47; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-46-48; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-47-49; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-48-50; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-49-51; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-50-52; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-51-53; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-52-53; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-53-54; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-54-55; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-55-56; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-56-57; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-57-58; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-00-58-59; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-00-00; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-01-01; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-02-02; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-03-03; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-04-03; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-05-04; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-06-05; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-07-06; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-08-07; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-09-08; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-10-09; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-11-10; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-12-11; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-13-12; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-14-13; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-15-13; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-16-14; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-17-15; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-18-16; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-19-17; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-20-18; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-21-19; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-22-20; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-23-21; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-24-22; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-25-23; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-26-24; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-27-24; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-28-25; Memory: 1%; Disk: 82.5% of 991.28GB
Time: 2023-08-03-01-29-26; Memory: 1%; Disk: 82.5% of 991.28GB
```
</details>

## Diff Log For Report Files
<details>

	diff kg2-simplified-report-kg284-pretty.json kg2-simplified-report-jsonlines-pretty.json

```diff
2,6c2,6
<     "_build_time": "2023-08-02 08:41",
<     "_build_version": "RTX KG2.8.4",
<     "_number_of_edges": 54363116,
<     "_number_of_nodes": 8437100,
<     "_report_datetime": "2023-08-02 18:47:04",
---
>     "_build_time": "",
>     "_build_version": "",
>     "_number_of_edges": 54274670,
>     "_number_of_nodes": 8437101,
>     "_report_datetime": "2023-07-31 22:46:59",
36c36
<         "biolink:affects": 4918525,
---
>         "biolink:affects": 4947868,
41c41
<         "biolink:causes": 1050955,
---
>         "biolink:causes": 1059714,
43,44c43,44
<         "biolink:close_match": 2253339,
<         "biolink:coexists_with": 1927115,
---
>         "biolink:close_match": 2253060,
>         "biolink:coexists_with": 1943198,
50c50
<         "biolink:derives_from": 75766,
---
>         "biolink:derives_from": 75899,
52c52
<         "biolink:diagnoses": 302812,
---
>         "biolink:diagnoses": 306043,
56c56
<         "biolink:disrupts": 614544,
---
>         "biolink:disrupts": 619787,
58c58
<         "biolink:exacerbates": 51043,
---
>         "biolink:exacerbates": 51152,
65c65
<         "biolink:has_input": 1282003,
---
>         "biolink:has_input": 1275070,
71c71
<         "biolink:has_part": 1842678,
---
>         "biolink:has_part": 1808255,
80,81c80,81
<         "biolink:located_in": 3214635,
<         "biolink:manifestation_of": 177691,
---
>         "biolink:located_in": 3238028,
>         "biolink:manifestation_of": 177928,
84c84
<         "biolink:occurs_in": 5986716,
---
>         "biolink:occurs_in": 5915194,
86,90c86,90
<         "biolink:physically_interacts_with": 5171817,
<         "biolink:precedes": 164184,
<         "biolink:predisposes": 371603,
<         "biolink:prevents": 246580,
<         "biolink:produces": 417825,
---
>         "biolink:physically_interacts_with": 5197065,
>         "biolink:precedes": 160389,
>         "biolink:predisposes": 359716,
>         "biolink:prevents": 238664,
>         "biolink:produces": 406246,
92c92
<         "biolink:related_to": 4653653,
---
>         "biolink:related_to": 4666580,
94c94
<         "biolink:subclass_of": 3976498,
---
>         "biolink:subclass_of": 3978948,
99c99
<         "biolink:treats": 1511908
---
>         "biolink:treats": 1444640
102c102
<         "biolink": 54363116
---
>         "biolink": 54274670
105,938c105,169
<         "PA": 14160,
<         "aboral_to": 1,
<         "acetylation_reaction": 24,
<         "achieves_planned_objective": 1,
<         "activator": 597,
<         "acts_on_population_of": 286,
<         "acts_upstream_of": 354,
<         "acts_upstream_of_negative_effect": 24,
<         "acts_upstream_of_or_within": 2218,
<         "acts_upstream_of_or_within_negative_effect": 8,
<         "acts_upstream_of_or_within_positive_effect": 23,
<         "acts_upstream_of_positive_effect": 75,
<         "adheres_to": 7,
<         "adjacent_to": 1085,
<         "administered_to": 252445,
<         "adp_ribosylation_reaction": 57,
<         "affects": 2153961,
<         "afferent_to": 823,
<         "after": 20,
<         "agonist": 5147,
<         "aligned_with": 4,
<         "allele_absent_from_wild-type_chromosomal_location": 1,
<         "allele_has_abnormality": 180,
<         "allele_has_activity": 74,
<         "allele_in_chromosomal_location": 104,
<         "allele_plays_altered_role_in_process": 128,
<         "allele_plays_role_in_metabolism_of_chemical_or_drug": 3,
<         "allelic_variant_of": 33305,
<         "allosteric modulator": 11,
<         "allosteric_antagonist": 9,
<         "allosteric_modulator": 203,
<         "anastomoses_with": 4,
<         "anatomic__structure__has__location": 1,
<         "anatomic__structure__is__physical__part__of": 1,
<         "anatomic_structure_is_physical_part_of": 10101,
<         "antagonist": 5985,
<         "anterior_to": 590,
<         "anteriorly_connected_to": 39,
<         "anteroinferior_to": 41,
<         "anterolateral_to": 39,
<         "anteromedial_to": 53,
<         "anterosuperior_to": 35,
<         "antibody": 236,
<         "antibody_binding": 112,
<         "antisense oligonucleotide": 4,
<         "antisense_inhibitor": 48,
<         "antisense_oligonucleotide": 3,
<         "approximately_perpendicular_to": 1,
<         "arterial_supply_of": 632,
<         "articulates_with": 692,
<         "associated_disease": 243,
<         "associated_with": 2030259,
<         "association": 124175,
<         "at_cellular_location": 70552,
<         "at_tissue": 8770,
<         "atc-code": 5383,
<         "atc-code-level": 17177,
<         "atpase_reaction": 1,
<         "attached_to": 399,
<         "attached_to_part_of": 12,
<         "attaches_to": 692,
<         "augments": 647915,
<         "axon_synapses_in": 15,
<         "bearer_of": 3748,
<         "before": 13,
<         "binder": 481,
<         "binding": 10,
<         "binding_agent": 316,
<         "biological_process_has_associated_location": 565,
<         "biological_process_has_result_anatomy": 63,
<         "biological_process_has_result_biological_process": 90,
<         "biological_process_has_result_chemical_or_drug": 32,
<         "biological_process_involves_chemical_or_drug": 18,
<         "blocker": 1953,
<         "bounding_layer_of": 401,
<         "bounds": 1739,
<         "branch_of": 14199,
<         "branching_part_of": 542,
<         "by_means": 15,
<         "capable_of": 1796,
<         "capable_of_part_of": 724,
<         "capable_of_regulating": 1,
<         "carrier": 1,
<         "category": 63988,
<         "causal_agent_in_process": 1,
<         "causally_upstream_of": 1,
<         "causes": 1015821,
<         "channel_for": 165,
<         "channels_from": 109,
<         "channels_into": 95,
<         "chaperone": 17,
<         "characteristic_of": 131,
<         "characteristic_of_part_of": 15,
<         "chelating_agent": 23,
<         "chelator": 2,
<         "chemical_or_drug_affects_abnormal_cell": 28,
<         "chemical_or_drug_affects_cell_type_or_tissue": 789,
<         "chemical_or_drug_affects_gene_product": 435,
<         "chemical_or_drug_has_mechanism_of_action": 2776,
<         "chemical_or_drug_has_physiologic_effect": 2606,
<         "chemical_or_drug_initiates_biological_process": 115,
<         "chromosome_mapped_to_disease": 320,
<         "class_code_classified_by": 61,
<         "cleavage": 10,
<         "cleavage_reaction": 103,
<         "clinically_tested_approved_unknown_phase": 5863,
<         "clinically_tested_suspended_phase_0": 1,
<         "clinically_tested_suspended_phase_1": 13,
<         "clinically_tested_suspended_phase_1_or_phase_2": 35,
<         "clinically_tested_suspended_phase_2": 324,
<         "clinically_tested_suspended_phase_2_or_phase_3": 24,
<         "clinically_tested_suspended_phase_3": 56,
<         "clinically_tested_terminated_phase_0": 29,
<         "clinically_tested_terminated_phase_1": 519,
<         "clinically_tested_terminated_phase_1_or_phase_2": 236,
<         "clinically_tested_terminated_phase_2": 1111,
<         "clinically_tested_terminated_phase_2_or_phase_3": 39,
<         "clinically_tested_terminated_phase_3": 467,
<         "clinically_tested_withdrawn_phase_0": 8,
<         "clinically_tested_withdrawn_phase_1": 156,
<         "clinically_tested_withdrawn_phase_1_or_phase_2": 29,
<         "clinically_tested_withdrawn_phase_2": 276,
<         "clinically_tested_withdrawn_phase_2_or_phase_3": 18,
<         "clinically_tested_withdrawn_phase_3": 89,
<         "coexists_with": 1841184,
<         "cofactor": 180,
<         "coincident_with": 4,
<         "colocalization": 2795,
<         "colocalizes_with": 1070,
<         "compared_with": 477689,
<         "complex_has_physical_part": 714,
<         "complicates": 51043,
<         "component of": 4,
<         "component_of": 10828,
<         "composed_primarily_of": 1380,
<         "compound_to_enzyme": 32474,
<         "compound_to_pathway": 10035,
<         "compound_to_reaction": 50075,
<         "conceptual_part_of": 3585,
<         "concretizes": 1,
<         "conduit_for": 136,
<         "confers_advantage_in": 15,
<         "confers_resistance_to": 25,
<         "connected_to": 740,
<         "connection_type_of": 4,
<         "connects": 1119,
<         "constitutional_part_of": 21454,
<         "contains": 921,
<         "contains_process": 76,
<         "continuation_branch_of": 43,
<         "continuous_distally_with": 1948,
<         "continuous_proximally_with": 1948,
<         "continuous_with": 2941,
<         "contraindication": 25069,
<         "contributes_to": 900,
<         "contributes_to_condition": 191,
<         "contributes_to_morphology_of": 2628,
<         "converts_to": 49242,
<         "correlated_with": 1,
<         "corresponds_to": 46,
<         "covalent_binding": 16,
<         "cross-linking_agent": 43,
<         "ctcae_5_parent_of": 4048,
<         "cytogenetic_abnormality_involves_chromosome": 1088,
<         "de-ADP-ribosylation_reaction": 1,
<         "deacetylation_reaction": 22,
<         "decreased_in_magnitude_relative_to": 2,
<         "deep_to": 36,
<         "degradation": 1,
<         "degrader": 5,
<         "demethylation_reaction": 6,
<         "deneddylation_reaction": 1,
<         "denotes": 1,
<         "dephosphorylation_reaction": 287,
<         "derives": 274,
<         "derives_from": 3207,
<         "determined_by": 18,
<         "determined_by_part_of": 1,
<         "deubiquitination_reaction": 11,
<         "development_type_of": 13,
<         "developmental_stage_of": 193,
<         "developmentally_induced_by": 126,
<         "developmentally_replaces": 35,
<         "develops_from": 8935,
<         "develops_from_part_of": 12,
<         "develops_in": 61,
<         "develops_into": 50,
<         "diagnoses": 302812,
<         "direct_cell_shape_of": 2,
<         "direct_interaction": 6880,
<         "direct_left_of": 487,
<         "direct_right_of": 487,
<         "directly_develops_from": 7,
<         "directly_negatively_regulates": 69,
<         "directly_positively_regulates": 55,
<         "directly_regulates": 48,
<         "disease": 24733,
<         "disease_arises_from_alteration_in_structure": 115,
<         "disease_caused_by_reactivation_of_latent_infectious_agent": 4,
<         "disease_causes_disruption_of": 97,
<         "disease_causes_dysfunction_of": 7,
<         "disease_causes_feature": 19,
<         "disease_has_associated_anatomic_site": 43871,
<         "disease_has_associated_disease": 1201,
<         "disease_has_basis_in": 466,
<         "disease_has_basis_in_accumulation_of": 1,
<         "disease_has_basis_in_development_of": 2,
<         "disease_has_basis_in_disruption_of": 266,
<         "disease_has_basis_in_dysfunction_of": 76,
<         "disease_has_basis_in_feature": 176,
<         "disease_has_feature": 1416,
<         "disease_has_finding": 46423,
<         "disease_has_infectious_agent": 391,
<         "disease_has_inflammation_site": 163,
<         "disease_has_location": 1533,
<         "disease_has_major_feature": 200,
<         "disease_has_metastatic_anatomic_site": 329,
<         "disease_has_molecular_abnormality": 2356,
<         "disease_has_normal_tissue_origin": 23237,
<         "disease_has_primary_anatomic_site": 30082,
<         "disease_has_primary_infectious_agent": 129,
<         "disease_is_grade": 1761,
<         "disease_is_marked_by_gene": 26,
<         "disease_is_stage": 6358,
<         "disease_may_have_abnormal_cell": 1492,
<         "disease_may_have_associated_disease": 2256,
<         "disease_may_have_finding": 18006,
<         "disease_may_have_molecular_abnormality": 11409,
<         "disease_may_have_normal_cell_origin": 199,
<         "disease_may_have_normal_tissue_origin": 3,
<         "disease_responds_to": 12,
<         "disease_shares_features_of": 68,
<         "disease_triggers": 2,
<         "disrupting_agent": 50,
<         "disrupts": 614390,
<         "distal_to": 193,
<         "distally_connected_to": 110,
<         "distalmost_part_of": 19,
<         "disulfide_bond": 26,
<         "dna_cleavage": 2,
<         "dorsal_to": 39,
<         "downregulator": 26,
<         "drains": 297,
<         "drains_into": 252,
<         "drug-interaction": 2866397,
<         "efferent_to": 823,
<         "enables": 69685,
<         "ends_during": 2,
<         "ends_with": 53,
<         "enzymatic_reaction": 26,
<         "enzyme_metabolizes_chemical_or_drug": 650,
<         "enzyme_to_pathway": 6102,
<         "enzyme_to_reaction": 6940,
<         "eo_disease_has_associated_cell_type": 13,
<         "eo_disease_has_associated_eo_anatomy": 3129,
<         "eo_disease_has_property_or_attribute": 273,
<         "equivalent_to": 82,
<         "existence_ends_during": 2636,
<         "existence_ends_during_or_before": 7,
<         "existence_ends_with": 25,
<         "existence_starts_and_ends_during": 47,
<         "existence_starts_during": 2773,
<         "existence_starts_during_or_after": 10,
<         "existence_starts_with": 30,
<         "expresses": 59,
<         "extends_fibers_into": 416,
<         "external-identifier": 18149,
<         "external-identifier-protein": 71,
<         "external_to": 1,
<         "fasciculates_with": 1,
<         "filtered_through": 16,
<         "finishes": 9,
<         "finishes_axis": 7,
<         "follows_axis": 4,
<         "formed_as_result_of": 6,
<         "forms": 15,
<         "full_grown_phenotype_of": 3,
<         "functionally_related_to": 25,
<         "fuses_with": 26,
<         "fusion_of": 7,
<         "gating_inhibitor": 12,
<         "gene replacement": 1,
<         "gene_associated_with_condition": 342525,
<         "gene_associated_with_disease": 2162,
<         "gene_encodes_gene_product": 20800,
<         "gene_found_in_organism": 3684,
<         "gene_has_physical_location": 988,
<         "gene_in_chromosomal_location": 4221,
<         "gene_involved_in_molecular_abnormality": 4214,
<         "gene_involved_in_pathogenesis_of_disease": 1221,
<         "gene_is_biomarker_of": 26,
<         "gene_is_biomarker_type": 39,
<         "gene_is_element_in_pathway": 14102,
<         "gene_mapped_to_disease": 6706,
<         "gene_mutant_encodes_gene_product_sequence_variation": 2250,
<         "gene_plays_role_in_process": 43680,
<         "gene_product_expressed_in_tissue": 1715,
<         "gene_product_has_abnormality": 27,
<         "gene_product_has_associated_anatomy": 5912,
<         "gene_product_has_biochemical_function": 5306,
<         "gene_product_has_chemical_classification": 1916,
<         "gene_product_has_organism_source": 1433,
<         "gene_product_has_structural_domain_or_motif": 7073,
<         "gene_product_is_biomarker_of": 32,
<         "gene_product_is_biomarker_type": 357,
<         "gene_product_is_element_in_pathway": 14225,
<         "gene_product_is_physical_part_of": 714,
<         "gene_product_malfunction_associated_with_disease": 510,
<         "gene_product_of": 43649,
<         "gene_product_plays_role_in_biological_process": 24735,
<         "gene_product_sequence_variation_encoded_by_gene_mutant": 2250,
<         "gene_product_variant_of_gene_product": 855,
<         "genetic_biomarker_related_to": 3991,
<         "germ_origin_of": 1,
<         "glycan_to_enzyme": 977,
<         "glycan_to_pathway": 511,
<         "glycan_to_reaction": 1465,
<         "glycosylation_reaction": 3,
<         "group": 17769,
<         "gtpase_reaction": 3,
<         "guanine_nucleotide_exchange_factor_reaction": 4,
<         "happens_during": 30,
<         "has_2_d_boundary": 7,
<         "has_about_it": 2,
<         "has_adherent": 7,
<         "has_allergic_trigger": 123,
<         "has_ancestry_status": 2,
<         "has_arterial_supply": 632,
<         "has_axis": 6,
<         "has_bound": 946,
<         "has_branch": 7032,
<         "has_completed": 7,
<         "has_component": 11285,
<         "has_compound": 5765838,
<         "has_connection_type": 4,
<         "has_constitutional_part": 21454,
<         "has_consumer": 10,
<         "has_context_binding": 67,
<         "has_continuation_branch": 43,
<         "has_country_of_origin": 10,
<         "has_cross_section": 2,
<         "has_data_element": 10,
<         "has_defining_ingredient": 228,
<         "has_development_type": 13,
<         "has_developmental_contribution_from": 594,
<         "has_developmental_stage": 193,
<         "has_direct_cell_shape": 2,
<         "has_disease_driver": 18,
<         "has_disease_location": 477,
<         "has_dose_form": 18596,
<         "has_element": 32610,
<         "has_element_collection": 10976,
<         "has_element_in_bound": 1577,
<         "has_end_location": 30,
<         "has_enzyme": 165371,
<         "has_event": 17803,
<         "has_exposure_stimulus": 121,
<         "has_food_substance_analog": 38,
<         "has_form": 1,
<         "has_full_grown_phenotype": 3,
<         "has_functional_parent": 18826,
<         "has_fused_element": 78,
<         "has_fusion": 7,
<         "has_gene_template": 94856,
<         "has_germ_origin": 1,
<         "has_habitat": 1,
<         "has_high_plasma_membrane_amount": 116,
<         "has_inc_parent": 201,
<         "has_increased_levels_of": 5,
<         "has_ingredient": 161,
<         "has_inherent_3d_shape": 4,
<         "has_inheritance_type": 7078,
<         "has_input": 29132,
<         "has_insertion": 213,
<         "has_interaction_type": 1,
<         "has_intermediate": 83,
<         "has_left_element": 763572,
<         "has_location": 3066988,
<         "has_low_plasma_membrane_amount": 106,
<         "has_lymphatic_drainage": 764,
<         "has_manifestation": 129299,
<         "has_mapping_qualifier": 33861,
<         "has_material_basis_in": 3243,
<         "has_material_basis_in_gain_of_function_germline_mutation_in": 11,
<         "has_material_basis_in_germline_mutation_in": 4478,
<         "has_material_basis_in_somatic_mutation_in": 4,
<         "has_measurement_unit_label": 5,
<         "has_member": 29977,
<         "has_metabolite": 1680,
<         "has_modifier": 47,
<         "has_muscle_antagonist": 100,
<         "has_muscle_insertion": 387,
<         "has_muscle_origin": 383,
<         "has_nerve_supply": 2133,
<         "has_not_completed": 30,
<         "has_nucleic_acid": 2579,
<         "has_observed_anatomical_entity": 3,
<         "has_occurrence": 252,
<         "has_occurrent_part": 2,
<         "has_onset": 1,
<         "has_onset_before": 2,
<         "has_onset_during_or_after": 2,
<         "has_origin": 280,
<         "has_output": 21530,
<         "has_owning_affiliate": 1,
<         "has_parent_hydride": 1823,
<         "has_part": 42390,
<         "has_participant": 1366573,
<         "has_participant_at_all_times": 3,
<         "has_pharmaceutical_administration_method": 563,
<         "has_pharmaceutical_basic_dose_form": 613,
<         "has_pharmaceutical_intended_site": 549,
<         "has_pharmaceutical_release_characteristics": 521,
<         "has_pharmaceutical_state_of_matter": 637,
<         "has_pharmaceutical_transformation": 538,
<         "has_phenotype": 32808,
<         "has_physiologic_effect": 1,
<         "has_plasma_membrane_part": 813,
<         "has_potential_to_develop_into": 755,
<         "has_potential_to_developmentally_contribute_to": 61,
<         "has_primary_input": 3005,
<         "has_primary_input_or_output": 1604,
<         "has_primary_output": 1499,
<         "has_primary_segmental_supply": 81,
<         "has_projection": 112,
<         "has_protein": 303810,
<         "has_protein_association": 844946,
<         "has_protein_in_complex": 1906,
<         "has_quality": 1475,
<         "has_reaction": 747189,
<         "has_regional_part": 27654,
<         "has_related_developmental_entity": 15,
<         "has_right_element": 786958,
<         "has_role": 63145,
<         "has_salt_form": 1853,
<         "has_secondary_segmental_supply": 80,
<         "has_segmental_composition": 2,
<         "has_segmental_supply": 705,
<         "has_sensory_dendrite_in": 1,
<         "has_skeleton": 281,
<         "has_soma_location": 202,
<         "has_specified_input": 36,
<         "has_specified_output": 32,
<         "has_start_location": 39,
<         "has_structural_class": 2,
<         "has_subsequence": 1,
<         "has_substance_added": 5,
<         "has_supported_concept_property": 369,
<         "has_supported_concept_relationship": 324,
<         "has_symptom": 2245,
<         "has_synaptic_io_in_region": 118,
<         "has_synaptic_terminal_in": 3,
<         "has_target": 4488,
<         "has_target_end_location": 474,
<         "has_target_start_location": 152,
<         "has_tributary": 1138,
<         "has_venous_drainage": 132,
<         "higher_than": 124005,
<         "homonym_of": 73,
<         "human_disease_maps_to_eo_disease": 1820,
<         "hydrolytic_enzyme": 75,
<         "hydroxylation_reaction": 23,
<         "immediate_transformation_of": 377,
<         "immediately_anterior_to": 1,
<         "immediately_causally_upstream_of": 2,
<         "immediately_deep_to": 78,
<         "immediately_posterior_to": 1,
<         "immediately_preceded_by": 89,
<         "immediately_precedes": 4,
<         "immediately_superficial_to": 21,
<         "immersed_in": 1,
<         "in_anterior_side_of": 41,
<         "in_biospecimen": 54150,
<         "in_central_side_of": 8,
<         "in_deep_part_of": 10,
<         "in_distal_side_of": 4,
<         "in_dorsal_side_of": 21,
<         "in_innermost_side_of": 4,
<         "in_lateral_side_of": 422,
<         "in_left_side_of": 187,
<         "in_outermost_side_of": 4,
<         "in_pathway": 813123,
<         "in_posterior_side_of": 39,
<         "in_proximal_side_of": 6,
<         "in_response_to": 22,
<         "in_right_side_of": 179,
<         "in_species": 1841529,
<         "in_superficial_part_of": 11,
<         "in_taxon": 560241,
<         "in_ventral_side_of": 10,
<         "inactivator": 6,
<         "incorporation into and destabilization": 1,
<         "increased_in_magnitude_relative_to": 4,
<         "indication": 8083,
<         "indirectly_supplies": 24,
<         "inducer": 179,
<         "inferior_to": 469,
<         "inferolateral_to": 20,
<         "inferomedial_to": 20,
<         "ingredient_of": 32,
<         "inherent_3d_shape_of": 4,
<         "inhibition of synthesis": 1,
<         "inhibitor": 13441,
<         "inhibitory allosteric modulator": 3,
<         "inhibitory_allosteric_modulator": 1,
<         "inhibits": 928478,
<         "innervated_by": 321,
<         "innervates": 276,
<         "input_of": 1,
<         "insertion_of": 213,
<         "interacts_with": 1954730,
<         "interacts_with_an_exposure_receptor_via": 2,
<         "interacts_with_an_exposure_stressor_via": 1,
<         "intercalation": 2,
<         "internal_to": 1,
<         "intersects_midsagittal_plane_of": 55,
<         "inverse agonist": 28,
<         "inverse_agonist": 52,
<         "inverse_ends_during": 1,
<         "inverse_of": 691,
<         "inverse_of_bounds": 1079,
<         "inverse_of_contains": 888,
<         "inverse_of_derives": 274,
<         "inverse_of_exhibits": 1166,
<         "inverse_of_forms": 15,
<         "inverse_of_isa": 26730,
<         "inverse_of_rn": 123158,
<         "inverse_of_ro": 392118,
<         "inverse_of_rq": 1612,
<         "inverse_of_sy": 466,
<         "inverse_of_use": 2459,
<         "involved_in": 130659,
<         "is_abnormal_cell_of_disease": 58762,
<         "is_about": 1694,
<         "is_active_in": 17280,
<         "is_associated_disease_of": 1201,
<         "is_component_of_chemotherapy_regimen": 12603,
<         "is_conjugate_acid_of": 8911,
<         "is_conjugate_base_of": 8911,
<         "is_cytogenetic_abnormality_of_disease": 421,
<         "is_demonym_of": 9,
<         "is_enantiomer_of": 2838,
<         "is_executed_in": 4,
<         "is_input_of": 95,
<         "is_location_of_anatomic_structure": 359,
<         "is_molecular_abnormality_of_disease": 2356,
<         "is_normal_cell_origin_of_disease": 22256,
<         "is_organism_source_of_gene_product": 1433,
<         "is_qualified_by": 1,
<         "is_related_to_endogenous_product": 28,
<         "is_requirement_for": 142,
<         "is_substituent_group_from": 1326,
<         "is_tautomer_of": 2042,
<         "is_unit_of": 4,
<         "isa": 336573,
<         "lacks_part": 6542,
<         "lacks_plasma_membrane_part": 949,
<         "larger_than": 1,
<         "lateral_to": 207,
<         "left_lateral_to": 5,
<         "left_medial_to": 5,
<         "left_of": 1,
<         "ligand": 594,
<         "linked_to_disease": 17192,
<         "lipid_addition": 2,
<         "lipoprotein_cleavage_reaction": 2,
<         "located_in": 65850,
<         "location_of": 3006106,
<         "lower_than": 21609,
<         "lumen_of": 6,
<         "luminal_space_of": 320,
<         "lymphatic_drainage_of": 764,
<         "manifestation_of": 177690,
<         "mapped_to": 433357,
<         "matures_from": 76,
<         "matures_into": 76,
<         "may_be_normal_cell_origin_of_disease": 199,
<         "may_be_normal_tissue_origin_of_disease": 3,
<         "may_be_qualified_by": 20,
<         "measures": 228816,
<         "medial_to": 207,
<         "member_of": 7066,
<         "mentions": 14,
<         "merges_with": 6,
<         "methylation_reaction": 36,
<         "mf#manifestation_of": 1,
<         "modulator": 454,
<         "multitarget": 7,
<         "myristoylation_reaction": 2,
<         "neddylation_reaction": 14,
<         "negative modulator": 32,
<         "negative_allosteric_modulator": 33,
<         "negative_modulator": 16,
<         "negatively_regulated_by": 3106,
<         "negatively_regulates": 9965,
<         "negatively_regulates_characteristic": 20,
<         "negatively_regulates_gene_expression": 135,
<         "neoplasm_has_special_category": 105,
<         "nerve_supply_of": 2133,
<         "neutralizer": 2,
<         "non-covalently_bound_to": 42,
<         "nucleotide exchange blocker": 1,
<         "occurs_in": 61603,
<         "off-label_use": 1790,
<         "only_in_taxon": 287016,
<         "opener": 80,
<         "opposite_to": 4,
<         "organism_has_gene": 3684,
<         "origin_of": 277,
<         "orphanet:317343": 4586,
<         "orphanet:317344": 178,
<         "orphanet:317345": 496,
<         "orphanet:317346": 38,
<         "orphanet:317348": 227,
<         "orphanet:317349": 229,
<         "orphanet:327767": 309,
<         "orphanet:410295": 1093,
<         "orphanet:410296": 206,
<         "orphanet:465410": 44,
<         "orphanet:c016": 6366,
<         "orphanet:c017": 9706,
<         "orthogonal_to": 4,
<         "output_of": 1046,
<         "overlaps": 937,
<         "overlaps_with": 35078,
<         "owning_section_of": 9,
<         "owning_subsection_of": 42,
<         "oxidative_enzyme": 3,
<         "oxidizer": 3,
<         "oxidoreductase_activity_electron_transfer_reaction": 10,
<         "palmitoylation_reaction": 4,
<         "part_of": 1325788,
<         "part_of_progression_of_disease": 4,
<         "partial agonist": 83,
<         "partial antagonist": 1,
<         "partial_agonist": 163,
<         "partially_surrounded_by": 1,
<         "participates_in": 128,
<         "passes_through": 1,
<         "pathway": 3762,
<         "pathway_has_gene_element": 14102,
<         "pathway_to_compound": 5864,
<         "pathway_to_drug": 10442,
<         "pathway_to_glycan": 291,
<         "pharmacological_chaperone": 3,
<         "phenotype_of": 32614,
<         "phosphorylation_reaction": 1206,
<         "physical_association": 138043,
<         "physically_interacts_with": 42187,
<         "positive allosteric modulator": 983,
<         "positive_allosteric_modulator": 390,
<         "positive_modulator": 721,
<         "positively_regulated_by": 3101,
<         "positively_regulates": 10012,
<         "positively_regulates_characteristic": 20,
<         "positively_regulates_gene_expression": 549,
<         "postaxialmost_part_of": 15,
<         "posterior_to": 570,
<         "posteriorly_connected_to": 7,
<         "posteroinferior_to": 35,
<         "posterolateral_to": 53,
<         "posteromedial_to": 39,
<         "posterosuperior_to": 41,
<         "potentiator": 156,
<         "preaxialmost_part_of": 24,
<         "preceded_by": 73,
<         "precedes": 163860,
<         "predisposes": 371603,
<         "predisposes_towards": 409,
<         "prevents": 246580,
<         "primary_segmental_supply_of": 81,
<         "procedure__has__target__anatomy": 3,
<         "procedure_has_completely_excised_anatomy": 111,
<         "procedure_has_excised_anatomy": 539,
<         "procedure_has_imaged_anatomy": 1,
<         "procedure_has_partially_excised_anatomy": 237,
<         "procedure_has_target_anatomy": 1041,
<         "procedure_may_have_completely_excised_anatomy": 6,
<         "procedure_may_have_excised_anatomy": 14,
<         "procedure_may_have_partially_excised_anatomy": 11,
<         "process_has_causal_agent": 160,
<         "process_includes_biological_process": 693,
<         "process_initiates_biological_process": 139,
<         "process_involves_gene": 43680,
<         "process_of": 1016403,
<         "produced_by": 185,
<         "produces": 417608,
<         "product of": 38,
<         "projects_from": 112,
<         "projects_to": 117,
<         "proline_isomerization__reaction": 1,
<         "protects": 39,
<         "protein_cleavage": 77,
<         "proteolytic_enzyme": 7,
<         "proximal_to": 198,
<         "proximally_connected_to": 226,
<         "proximalmost_part_of": 20,
<         "proximity": 32809,
<         "qualifier_applies_to": 1,
<         "reaction_to_enzyme": 10321,
<         "reaction_to_pathway": 10594,
<         "realized_in": 19,
<         "realized_in_response_to": 52,
<         "realized_in_response_to_stimulus": 55,
<         "realizes": 5,
<         "receives_attachment_from": 500,
<         "receives_drainage_from": 252,
<         "receives_input_from": 811,
<         "receives_projection": 117,
<         "reciprocal_of": 22,
<         "reducing_agent": 2,
<         "regimen_has_accepted_use_for_disease": 402,
<         "regional_part_of": 27654,
<         "regulated_by": 3599,
<         "regulates": 10978,
<         "regulates_characteristic": 84,
<         "regulates_levels_of": 124,
<         "regulator": 42,
<         "related_developmental_entity_of": 15,
<         "related_object": 252,
<         "related_part": 3574,
<         "related_to": 429462,
<         "releasing_agent": 33,
<         "results_in": 9,
<         "results_in_acquisition_of_features_of": 957,
<         "results_in_assembly_of": 453,
<         "results_in_commitment_to": 62,
<         "results_in_determination_of": 25,
<         "results_in_development_of": 2262,
<         "results_in_developmental_progression_of": 6,
<         "results_in_disassembly_of": 138,
<         "results_in_distribution_of": 12,
<         "results_in_fission_of": 18,
<         "results_in_formation_of": 615,
<         "results_in_fusion_of": 82,
<         "results_in_growth_of": 90,
<         "results_in_maintenance_of": 14,
<         "results_in_maturation_of": 246,
<         "results_in_morphogenesis_of": 1194,
<         "results_in_movement_of": 286,
<         "results_in_organization_of": 379,
<         "results_in_remodeling_of": 10,
<         "results_in_specification_of": 37,
<         "results_in_structural_organization_of": 37,
<         "results_in_transport_across": 141,
<         "results_in_transport_along": 40,
<         "results_in_transport_to_from_or_in": 72,
<         "right_lateral_to": 5,
<         "right_medial_to": 5,
<         "rna_cleavage": 3,
<         "rnai_inhibitor": 21,
<         "role_has_domain": 97,
<         "role_has_parent": 11,
<         "role_has_range": 97,
<         "rxcui:consists_of": 46791,
<         "rxcui:constitutes": 46791,
<         "rxcui:contained_in": 1966,
<         "rxcui:contains": 1966,
<         "rxcui:has_dose_form": 41665,
<         "rxcui:has_doseformgroup": 16874,
<         "rxcui:has_form": 3340,
<         "rxcui:has_ingredient": 71556,
<         "rxcui:has_part": 10382,
<         "rxcui:has_quantified_form": 6,
<         "rxcui:has_tradename": 43981,
<         "rxcui:ingredient_of": 71556,
<         "rxcui:ingredients_of": 4038,
<         "rxcui:inverse_isa": 89548,
<         "rxcui:isa": 89548,
<         "rxcui:part_of": 10382,
<         "rxcui:precise_ingredient_of": 5875,
<         "rxcui:reformulated_to": 7,
<         "same_as": 606513,
<         "secondary_segmental_supply_of": 80,
<         "segmental_composition_of": 2,
<         "segmental_supply_of": 705,
<         "sends_output_to": 811,
<         "sequestering_agent": 45,
<         "serially_homologous_to": 5,
<         "sexually_homologous_to": 29,
<         "simultaneous_with": 51,
<         "site_of": 50,
<         "skeleton_of": 169,
<         "specifies_value_of": 32,
<         "stabiliser": 22,
<         "stabilization": 10,
<         "starts": 9,
<         "starts_axis": 7,
<         "starts_with": 119,
<         "stimulates": 1061629,
<         "stimulator": 18,
<         "struct2atc": 5030,
<         "sub_property_of": 3314,
<         "subclass_of": 2608836,
<         "subdivision_of": 59,
<         "subset_includes_concept": 334678,
<         "subset_of": 3894,
<         "substrate": 108,
<         "sumoylation_reaction": 16,
<         "superficial_to": 41,
<         "superior_to": 469,
<         "superolateral_to": 20,
<         "superomedial_to": 20,
<         "superset_of": 3887,
<         "supplies": 395,
<         "suppressor": 4,
<         "surface_of": 12,
<         "surrounded_by": 307,
<         "surrounds": 380,
<         "symptomatic_treatment": 2,
<         "synapsed_by": 15,
<         "synapsed_to": 25,
<         "target": 7535,
<         "towards": 7,
<         "transcribed_from": 269941,
<         "transformation_of": 221,
<         "transforms_from": 50,
<         "transforms_into": 50,
<         "transglutamination_reaction": 2,
<         "translates_to": 48374,
<         "translocation inhibitor": 2,
<         "transmitted_by": 248,
<         "treats": 1492326,
<         "tributary_of": 1373,
<         "type": 294,
<         "ubiquitination_reaction": 333,
<         "use": 2459,
<         "uses": 483696,
<         "vaccine": 8,
<         "vaccine_antigen": 19,
<         "venous_drainage_of": 132,
<         "ventral_to": 25,
<         "weak inhibitor": 1,
<         "xref": 2267347
---
>         "biolink:actively_involved_in": 22302,
>         "biolink:affects": 4947868,
>         "biolink:associated_with": 2617,
>         "biolink:biomarker_for": 55254,
>         "biolink:capable_of": 7355,
>         "biolink:catalyzes": 17261,
>         "biolink:causes": 1059714,
>         "biolink:chemically_similar_to": 20679,
>         "biolink:close_match": 2253060,
>         "biolink:coexists_with": 1943198,
>         "biolink:colocalizes_with": 36674,
>         "biolink:composed_primarily_of": 1380,
>         "biolink:contraindicated_for": 25069,
>         "biolink:contributes_to": 4743,
>         "biolink:correlated_with": 2362,
>         "biolink:derives_from": 75899,
>         "biolink:develops_from": 9065,
>         "biolink:diagnoses": 306043,
>         "biolink:directly_physically_interacts_with": 10711,
>         "biolink:disease_has_basis_in": 3,
>         "biolink:disease_has_location": 1533,
>         "biolink:disrupts": 619787,
>         "biolink:enables": 69685,
>         "biolink:exacerbates": 51152,
>         "biolink:expressed_in": 7686,
>         "biolink:gene_associated_with_condition": 1345429,
>         "biolink:gene_product_of": 161555,
>         "biolink:has_completed": 7,
>         "biolink:has_decreased_amount": 106,
>         "biolink:has_increased_amount": 116,
>         "biolink:has_input": 1275070,
>         "biolink:has_member": 2634,
>         "biolink:has_metabolite": 1680,
>         "biolink:has_molecular_consequence": 74,
>         "biolink:has_not_completed": 30,
>         "biolink:has_output": 815905,
>         "biolink:has_part": 1808255,
>         "biolink:has_participant": 9583161,
>         "biolink:has_phenotype": 97258,
>         "biolink:has_plasma_membrane_part": 813,
>         "biolink:homologous_to": 29,
>         "biolink:in_taxon": 298029,
>         "biolink:indirectly_physically_interacts_with": 8,
>         "biolink:is_sequence_variant_of": 36410,
>         "biolink:lacks_part": 7491,
>         "biolink:located_in": 3238028,
>         "biolink:manifestation_of": 177928,
>         "biolink:mentions": 14,
>         "biolink:model_of": 38,
>         "biolink:occurs_in": 5915194,
>         "biolink:overlaps": 38917,
>         "biolink:physically_interacts_with": 5197065,
>         "biolink:precedes": 160389,
>         "biolink:predisposes": 359716,
>         "biolink:prevents": 238664,
>         "biolink:produces": 406246,
>         "biolink:regulates": 42144,
>         "biolink:related_to": 4666580,
>         "biolink:same_as": 607196,
>         "biolink:subclass_of": 3978948,
>         "biolink:superclass_of": 498642,
>         "biolink:temporally_related_to": 846,
>         "biolink:transcribed_from": 269941,
>         "biolink:translates_to": 48374,
>         "biolink:treats": 1444640
974c205
<         "infores:kegg": 168526,
---
>         "infores:kegg": 168171,
997c228
<         "infores:semmeddb": 21538765,
---
>         "infores:semmeddb": 21450674,
1004c235
<         "infores:semmeddb": 3974365
---
>         "infores:semmeddb": 3807691
1061c292
<         "retrieval_source": 68,
---
>         "retrieval_source": 69,
1190a422
>         "RTX": 1,
1239,1243c471,476
<         "infores:atc-codes-umls": 6569,
<         "infores:bfo": 52,
<         "infores:biolink-ontology": 915,
<         "infores:bspo": 380,
<         "infores:chebi": 183273,
---
>         "RTX:": 1,
>         "infores:atc-codes-umls": 6567,
>         "infores:bfo": 37,
>         "infores:biolink-ontology": 914,
>         "infores:bspo": 306,
>         "infores:chebi": 181590,
1245,1247c478,480
<         "infores:chv-umls": 2,
<         "infores:cl": 16407,
<         "infores:dda": 146,
---
>         "infores:chv-umls": 1,
>         "infores:cl": 14449,
>         "infores:dda": 137,
1249c482
<         "infores:disease-ontology": 18395,
---
>         "infores:disease-ontology": 16707,
1252c485
<         "infores:drugbank": 24323,
---
>         "infores:drugbank": 15356,
1255c488
<         "infores:ehdaa2": 2752,
---
>         "infores:ehdaa2": 2651,
1257,1262c490,495
<         "infores:fma-obo": 78989,
<         "infores:fma-umls": 104530,
<         "infores:foodon": 34282,
<         "infores:genepio": 7989,
<         "infores:go": 43676,
<         "infores:go-plus": 84363,
---
>         "infores:fma-obo": 78976,
>         "infores:fma-umls": 26203,
>         "infores:foodon": 31776,
>         "infores:genepio": 4071,
>         "infores:go": 26,
>         "infores:go-plus": 45430,
1264,1266c497,499
<         "infores:hcp-codes-umls": 7349,
<         "infores:hgnc": 43174,
<         "infores:hl7-umls": 8666,
---
>         "infores:hcp-codes-umls": 7347,
>         "infores:hgnc": 23292,
>         "infores:hl7-umls": 6120,
1268,1271c501,504
<         "infores:hpo": 46816,
<         "infores:icd10pcs-umls": 191282,
<         "infores:icd9cm-umls": 22415,
<         "infores:ino": 444,
---
>         "infores:hpo": 17880,
>         "infores:icd10pcs-umls": 191280,
>         "infores:icd9cm-umls": 22413,
>         "infores:ino": 318,
1274,1277c507,510
<         "infores:medlineplus": 2403,
<         "infores:medrt-umls": 45,
<         "infores:mesh": 352338,
<         "infores:mi": 1653,
---
>         "infores:medlineplus": 362,
>         "infores:medrt-umls": 39,
>         "infores:mesh": 352331,
>         "infores:mi": 1531,
1279,1287c512,520
<         "infores:mondo": 45730,
<         "infores:nbo": 4756,
<         "infores:ncbi-gene": 191171,
<         "infores:ncbi-taxon": 703976,
<         "infores:ncit": 171246,
<         "infores:nddf-umls": 31398,
<         "infores:ndfrt": 2,
<         "infores:omim": 104763,
<         "infores:ordo": 14285,
---
>         "infores:mondo": 22157,
>         "infores:nbo": 815,
>         "infores:ncbi-gene": 191153,
>         "infores:ncbi-taxon": 695986,
>         "infores:ncit": 170725,
>         "infores:nddf-umls": 31397,
>         "infores:ndfrt": 1,
>         "infores:omim": 104560,
>         "infores:ordo": 8109,
1289,1292c522,525
<         "infores:pato": 10910,
<         "infores:pdq-umls": 13344,
<         "infores:pr": 328950,
<         "infores:psy-umls": 7971,
---
>         "infores:pato": 2108,
>         "infores:pdq-umls": 13342,
>         "infores:pr": 318541,
>         "infores:psy-umls": 7969,
1295,1296c528,529
<         "infores:ro": 866,
<         "infores:rxnorm": 107615,
---
>         "infores:ro": 377,
>         "infores:rxnorm": 107614,
1300,1302c533,535
<         "infores:uberon": 26652,
<         "infores:umls": 1859991,
<         "infores:umls-metathesaurus": 358870,
---
>         "infores:uberon": 8666,
>         "infores:umls": 1859990,
>         "infores:umls-metathesaurus": 158763,
1305c538
<         "infores:vandf-umls": 2
---
>         "infores:vandf-umls": 1
1307a541,543
>         "RTX:": {
>             "retrieval_source": 1
>         },
2088c1324
<     "number_of_nodes_without_category__by_curie_prefix": {},
---
>     "number_of_nodes_without_category_by_curie_prefix": {},
2089a1326
>         "RTX:": 1,
2124c1361
<         "infores:kegg": 17388,
---
>         "infores:kegg": 17402,
2161c1398
<         "Biolink meta-model version downloaded:2023-07-30 23:15:25 GMT",
---
>         "Biolink meta-model version downloaded:2023-07-31 00:46:56 GMT",
2205c1442
<         "Interaction Network Ontology version downloaded:2023-07-31 09:05:17 GMT",
---
>         "Interaction Network Ontology version downloaded:2023-07-29 03:59:01 GMT",
2207c1444
<         "Molecular Interactions Controlled Vocabulary version downloaded:2023-07-31 09:05:43 GMT",
---
>         "Molecular Interactions Controlled Vocabulary version downloaded:2023-07-29 03:59:27 GMT",
2209c1446
<         "Semantic Medline Database (SemMedDB) v43",
---
>         "Semantic Medline Database (SemMedDB) v43\n",
2223c1460
<         "miRBase v22.1<br>",
---
>         "miRBase v22.1",
2228c1465,1466
<         "Kyoto Encyclopedia of Genes and Genomes v107.0"
---
>         "Kyoto Encyclopedia of Genes and Genomes v107.0",
>         "RTX-KG2.8.4"
2263,2264c1501,1502
<         "NCBIGene---NCBIGene": 142,
<         "NCBIGene---UMLS": 632,
---
>         "NCBIGene---NCBIGene": 140,
>         "NCBIGene---UMLS": 630,
2280,2281c1518,1519
<         "UMLS---NCBIGene": 717,
<         "UMLS---UMLS": 16057
---
>         "UMLS---NCBIGene": 714,
>         "UMLS---UMLS": 15785
2436c1674
<         "UMLS---NCBIGene": 47322,
---
>         "UMLS---NCBIGene": 47332,
```
</details>