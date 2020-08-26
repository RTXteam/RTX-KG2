# FDA approval filtering and Covid19 Drug Exploration
______

### drugbank_get_approved_drugs_and_ids.py

This script is intended to be run on a build server, and could probably be integrated into [drugbank_xml_to_kg_json.py](https://github.com/RTXteam/RTX/blob/lindsey_covid_proj/code/kg2/drugbank_xml_to_kg_json.py) to save on load time if it's going to be used consistently. It generates a csv file of drugbank drugs that are in the approved group, parsed from drugbank.xml. 

Usage:
``` bash
python3 drugbank_get_approved_drugs_and_ids.py <path_to_drugbank.xml> <outputFile.csv>
```

* Drugs that are in both approved and withdrawn groups are omitted. 
* Each drug row includes any external identifiers mentioned by drugbank 
  *  includes ids from *drugs product database (dpd), pubchem substance, kegg drug, pharmgkb, uniprotkb, therapeutic targets database, wikipedia, chembl, rxcui, genbank, kegg compound, chebi, pubchem compound, chemspider, bindingdb, iuphar, guide to pharmacology, pdb, and zinc.* (8.26.2020)
  *  Any given drug without a specific external id has nan for it's value in that column.

### covid_drugs.py

This script contains fuctionality to filter drugs based on FDA approval status using the file generated above based on node ids. It runs a set of hardcoded cypher queries about covid-19, and stores the resulting approved drugs as .csv files in the specified results directory.

Usage:
```bash
python3 covid_drugs.py <path_to_approved_ids.csv> <path_to_results_directory>
```

* works with KG2 version 2.0 and above
  * needs to be tweaked to work with KG2 Canonicalized
