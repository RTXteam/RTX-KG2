#!/usr/bin/env python3
''' drugbank_get_approved_drugs_and_ids.py: Extracts a comma delimited csv file of
    approved drugbank drugs and a comma delimited csv file of drugbank and eternal
    drug idsfrom DrugBank database in XML format

    Usage: drugbank_get_approved_drugs_and_ids.py <inputFile.xml>
    <approvedDrugOutputFile.csv>
'''

import argparse
import pandas as pd
import xmltodict
import os
__author__ = 'Lindsey Kvarfordt'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

os.sys.path.append("..")


def get_args():
    arg_parser = argparse.ArgumentParser(description='drugbank_get_approved_drugs_and_ids.py: \
                                         builds a csv file from Drugbank database,  \
                                         that contains approved drugs by name, drugbank id, \
                                         and all external ids noted by drugbank.')
    arg_parser.add_argument('inputFile', type=str,
                            help="path to the drugbank.xml file")
    arg_parser.add_argument('approvedDrugOutputFile', type=str)
    return arg_parser.parse_args()


def xml_to_drugbank_dict(input_file_name: str):
    drugbank = open(input_file_name)
    drugbank_dict = xmltodict.parse(drugbank.read())
    drugbank.close()
    return drugbank_dict


def get_drugbank_id(drug: dict):
    drugbank_id = ""
    if isinstance(drug["drugbank-id"], list):
        for id in drug["drugbank-id"]:
            if isinstance(id, dict):
                if id["@primary"] == "true":
                    drugbank_id = id["#text"]
    elif isinstance(drug["drugbank-id"], dict):
        id = drug["drugbank-id"]
        if id["@primary"] == "true":
            drugbank_id = id["#text"]
    return drugbank_id


def get_external_ids(x):
    ids_dict = {"DRUGBANK": get_drugbank_id(x)}
    if x["external-identifiers"]:
        ex_ids = x["external-identifiers"]["external-identifier"]
        if isinstance(ex_ids, dict):
            ids_dict[ex_ids["resource"].upper()] = ex_ids["identifier"]
        else:
            for d in ex_ids:
                ids_dict[d["resource"].upper()] = d["identifier"]
    return ids_dict


def get_groups(drug: dict):
    groups = ""
    if isinstance(drug["groups"]["group"], list):
        groups = ",".join(drug["groups"]["group"])
    elif isinstance(drug["groups"]["group"], str):
        groups = drug["groups"]["group"]
    return groups


def reformat_drug(x: dict):
    x["groups"] = get_groups(x)
    x["DRUGBANK"] = get_drugbank_id(x)
    return x


def create_approved_drug_df(drugbank_dict):
    drugs = [reformat_drug(dict(x)) for x in drugbank_dict["drugbank"]["drug"]]
    df = pd.DataFrame(drugs)
    df = df[["DRUGBANK", "name", "groups"]]
    approved_df = df[df["groups"].astype("str").str.contains(
        "[,]approved|^approved", regex=True)]
    approved_df = approved_df[~approved_df["groups"].astype(
        "str").str.contains("withdrawn", regex=True)]  # remove withdrawn drugs
    return approved_df


def create_external_drug_ids_df(drugbank_dict):
    all_drug_ids = [get_external_ids(dict(d))
                    for d in drugbank_dict["drugbank"]["drug"]]
    df = pd.DataFrame(all_drug_ids)
    external_id_name_map = { # change column name to match the first part of the colon separated node id
        "GUIDE TO PHARMACOLOGY": "GTPI",
    }
    df.rename(external_id_name_map, axis=1)
    return df


args = get_args()
print("Loading drugbank.xml...")
drugbank_dict = xml_to_drugbank_dict(args.inputFile)

print("Filtering by approval...")
approved_df = create_approved_drug_df(drugbank_dict)
print("Geting equivalent IDs...")
drug_ids_df = create_external_drug_ids_df(drugbank_dict)

# approved drugs with all external ids
approved_ids_df = approved_df.merge(drug_ids_df, how="left", on=["DRUGBANK"])
print("Exporting to csv...")
approved_ids_df.to_csv(args.approvedDrugOutputFile, index=False)
print("Done.")
