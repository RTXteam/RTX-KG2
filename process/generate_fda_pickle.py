#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import stitch_proj.local_babel as lb
import pickle
import argparse

__author__ = 'Frankie Hodges'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Frankie Hodges']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate fda_approved_drugs_v1.0_KG2.10.3c.pickle "
                    "from DrugBank XML and local Babel DB"
    )

    parser.add_argument(
        "--drugbank_xml",
        type=str,
        default="/home/ubuntu/kg2-build/drugbank.xml",
        help="Path to drugbank.xml"
    )

    parser.add_argument(
        "--babel_db",
        type=str,
        default="/data/babel-20250901-p1.sqlite",
        help="Path to local Babel sqlite DB"
    )

    parser.add_argument(
        "--output_pickle",
        type=str,
        default="/home/ubuntu/kg2-build/fda_approved_drugs_v1.0_KG2.10.3c.pickle",
        help="Output pickle filename"
    )

    return parser.parse_args()




def extract_approved_drugbank_ids(xml_path):
    ns = {"db": "http://www.drugbank.ca"}

    tree = ET.parse(xml_path)
    root = tree.getroot()

    approved_curie_ids = []

    for drug in root.findall("db:drug", ns):
        groups = drug.find("db:groups", ns)
        if groups is None:
            continue

        is_approved = any(
            g.text == "approved"
            for g in groups.findall("db:group", ns)
        )

        if not is_approved:
            continue

        primary_id = drug.find("db:drugbank-id[@primary='true']", ns)
        if primary_id is not None and primary_id.text:
            approved_curie_ids.append("DRUGBANK:" + primary_id.text.strip())

    return approved_curie_ids


def canonicalize_ids(curie_ids, babel_db_path):
    canonical_ids = set()

    with lb.connect_to_db_read_only(babel_db_path) as conn:
        for curie in curie_ids:
            cliques = lb.map_any_curie_to_cliques(conn, curie)
            if not cliques:
                continue

            for clique in cliques:
                canonical_ids.add(clique["id"]["identifier"])

    return canonical_ids


def main():
    args = parse_args()

    print("Extracting approved DrugBank IDs...")
    approved_curie_ids = extract_approved_drugbank_ids(args.drugbank_xml)
    print(f"Found {len(approved_curie_ids)} approved DrugBank IDs.")

    print("Canonicalizing via local Babel...")
    canonical_ids = canonicalize_ids(approved_curie_ids, args.babel_db)
    print(f"Canonicalized to {len(canonical_ids)} unique canonical IDs.")

    print("Writing pickle...")
    with open(args.output_pickle, "wb") as out:
        pickle.dump(canonical_ids, out)

    print("Done.")


if __name__ == "__main__":
    main()