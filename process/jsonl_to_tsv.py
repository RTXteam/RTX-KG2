#!/usr/bin/env python3
"""
A script to convert massive JSON-lines files to TSV files with a tqdm progress meter.
Usage examples:
    python convert_jsonl_to_tsv.py --type nodes nodes.jsonl nodes.tsv
    python convert_jsonl_to_tsv.py --type edges edges.jsonl edges.tsv
"""

import json, csv
from tqdm import tqdm
import argparse


NEO4J_CHAR_LIMIT = 3000000

def truncate_lists(field):
    """
    Truncate lists to obey Neo4j's character buffer NEO4j_CHAR_LIMIT,
    without cutting off a publication mid-way.
    Uses the last 'ǂ' delimiter before the NEO4j_CHAR_LIMIT as the cutoff point.
    Assumes input is already joined (string form).
    """
    if not field:
        return ""

    # If already under NEO4j_CHAR_LIMIT, return as-is
    if len(field) <= NEO4J_CHAR_LIMIT:
        return field

    # Slice at buffer NEO4j_CHAR_LIMIT
    truncated = field[:NEO4J_CHAR_LIMIT]

    # Find the last delimiter before the NEO4j_CHAR_LIMIT
    last_delim = truncated.rfind("ǂ")

    # If a delimiter exists, truncate to just before it
    if last_delim != -1:
        truncated = truncated[:last_delim]

    return truncated

def join_array(arr):
    """
    Convert a JSONL list to a string joined by a special delimiter.
    If the input is not a list, simply return str(arr).
    """
    if isinstance(arr, list):
        new_arr = "ǂ".join(str(x) for x in arr)
        return truncate_lists(new_arr)
    return str(arr)

def sanitize_entry(entry):
    if entry is None:
        return ""
    entry = join_array(entry)
    entry = (entry
             .replace("', '", "; ")
             .replace("'", "")
             .replace("[", "")
             .replace("]", "")
             .replace("\n", " ")
             .replace("\r", " "))
    return entry

def get_headers(input_file):
    headers = []
    # --- First pass: find the most complete header set ---
    with open(input_file, "r", encoding="utf-8") as fin:
        for line in tqdm(fin, desc="Finding Longest Header", unit="line"):
            line = line.strip()
            if not line:
                continue
            try:
                node = json.loads(line)
                if len(node.keys()) > len(headers):
                    headers = list(node.keys())  # convert to list to preserve order
            except json.JSONDecodeError:
                continue
    return headers

def extract_data(output_file, input_file, headers, types):
    out_file = f"{output_file}.tsv"
    with open(out_file, "w", newline="", encoding="utf-8") as fout:
        data_writer = csv.writer(fout, delimiter="\t")
        with open(input_file, "r", encoding="utf-8") as fin:
            for line in tqdm(fin, desc="Processing Nodes", unit="line"):
                line = line.strip()
                if not line:
                    continue
                try:
                    node = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if types == "nodes": 
                    vallist = [sanitize_entry(node.get(header, "")) for header in headers if header != ":LABEL"]
                    label_val = sanitize_entry(node.get("category", ""))
                    vallist.append(label_val)
                if types == "edges": 
                    vallist = [sanitize_entry(node.get(header, "")) for header in headers if header != ":TYPE" and header != ":START_ID" and header != ":END_ID"]
                    type_val = sanitize_entry(node.get("predicate", ""))
                    start_val = sanitize_entry(node.get("subject", ""))
                    end_val = sanitize_entry(node.get("object", ""))
                    vallist.append(type_val)
                    vallist.append(start_val)
                    vallist.append(end_val)
                data_writer.writerow(vallist) 

def process(input_file, output_file, types): 
    headers = get_headers(input_file)
    extract_data(output_file, input_file, headers, types)
    header_file = f"{output_file}_header.tsv"
        # --- Build Neo4j header row ---

    if types == "nodes": 
        if "id" in headers:
            headers[headers.index("id")] = "id:ID"
        if "publications" in headers: 
            headers[headers.index("publications")] = "publications:string[]"
        if "synonym" in headers: 
            headers[headers.index("synonym")] = "synonym:string[]"
        if "all_names" in headers: 
            headers[headers.index("all_names")] = "all_names:string[]"
        if "all_categories" in headers: 
            headers[headers.index("all_categories")] = "all_categories:string[]"
        headers.append(":LABEL")
    elif types == "edges": 
        if "publications" in headers: 
            headers[headers.index("publications")] = "publications:string[]"
        if "kg2_ids" in headers: 
            headers[headers.index("kg2_ids")] = "kg2_ids:string[]"
        headers.append(":TYPE")
        headers.append(":START_ID")
        headers.append(":END_ID")
    # --- Write header TSV ---
    with open(header_file, "w", newline="", encoding="utf-8") as hout:
        header_writer = csv.writer(hout, delimiter="\t")
        header_writer.writerow(headers)


def main():
    parser = argparse.ArgumentParser(
        description="Convert massive JSON-lines files (nodes or edges) to TSV files with a progress meter."
    )
    parser.add_argument("input", help="Input JSON-lines file")
    parser.add_argument("--type", choices=["nodes", "edges"], required=True,
                        help="The type of file to process: 'nodes' or 'edges'")
    args = parser.parse_args()

    if args.type == "nodes":
        output_file = "nodes_c"
        process(args.input, output_file, "nodes")
    elif args.type == "edges":
        output_file = "edges_c"
        process(args.input, output_file, "edges")


if __name__ == "__main__":
    main()