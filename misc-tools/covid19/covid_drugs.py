import sys
import os
import re
import pandas as pd
from neo4j import GraphDatabase
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../")  # code directory
from RTXConfiguration import RTXConfiguration


def _run_cypher_query(cypher_query: str, kg="KG2") -> List[Dict[str, any]]:
    # This function sends a cypher query to neo4j (either KG1 or KG2) and returns results
    rtxc = RTXConfiguration()
    if kg == "KG2":
        rtxc.live = "KG2"
    try:
        driver = GraphDatabase.driver(rtxc.neo4j_bolt, auth=(rtxc.neo4j_username, rtxc.neo4j_password))
        with driver.session() as session:
            print(f"Sending cypher query to {kg} neo4j")
            query_results = session.run(cypher_query).data()
            print(f"Got {len(query_results)} results back from neo4j")
        driver.close()
    except Exception:
        tb = traceback.format_exc()
        error_type, error, _ = sys.exc_info()
        print(f"Encountered an error interacting with {kg} neo4j. {tb}")
        return []
    else:
        return query_results

def get_result_ids(full_results: dict):
    results = [n["d"]["id"] for n in full_results]
    return results

def filter_by_fda_approval(result_ids: list, approved_drug_df: pd.DataFrame):
    ids_not_available = set()
    skipped = 0
    for full_id in result_ids:
        src, id = full_id.split(":")
        if src in approved_drug_df.columns:
            if id in approved_drug_df[src].values:
                yield approved_drug_df["DRUGBANK"][approved_drug_df[src]==id].values[0]
        else:
            if src not in ids_not_available:
                print("Do not have equivalent ids for drugs from", src)
                ids_not_available.add(src)
            skipped += 1

    print("Skipped", skipped,"drugs because of lack of equivalent ids")

def ask(cypher_query:str, outputFilename:str):
    full_results = _run_cypher_query(cypher_query)
    ids = get_result_ids(full_results)
    result_ids = list(filter_by_fda_approval(ids, approved_drug_df))
    if len(result_ids) != 0:
        result_df = pd.DataFrame(result_ids, columns=["DRUGBANK"])
        result_df = result_df.merge(approved_drug_df, how="left", on=["DRUGBANK"])
        result_df = result_df[["DRUGBANK", "name", "groups"]]
        result_df.to_csv("./results/"+outputFilename, index=False)
    else:
        print("No FDA approved results for query.")


approved_drug_df = pd.read_csv("./approved_ids.csv", sep=',')

#add queries and result filenames here. make sure cypher querie returns d
cypher_queries = {
    'match p=(n{name:"Viral pneumonia"})<-[causes_condition*1]-(l:disease)<-[is_substance_that_treats*1]-(d:drug) return distinct d': "pneumonia.csv",
    'match p=(n)-[*1]-(t:protein)-[*1]-(d:drug) where toLower(n.name) contains "remdesivir" return d' : "remdesivir_proteins.csv",
    'match p=(d:drug)-[*1]-(h {name: "Chronic hepatitis C"}) return d': "hepC_remdesivir.csv",
    'match (n)-[*1]-(d:drug) where toLower(n.name) contains "antimalarial" return d': "antimalarials.csv",
    'match p=(d:drug)-[*1]-(n {name: "ACE2"}) return d': "ace2_direct_connections.csv",
    'match p=(d:drug)-[*1]-(n {name: "Ace inhibitors"}) return d' : "ace_inhibitors_category.csv",
    'match (n)-[*1]-(d:drug) where toLower(n.name) contains "antiviral agent" return d': "antiviral_agents.csv",
    }

for query, filename in cypher_queries.items():
    print("\n******generating", filename,"******")
    ask(query, filename)


