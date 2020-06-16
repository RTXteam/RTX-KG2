#!/usr/bin/env python3
'''uniprotkb_dat_to_json.py: Extracts a KG2 JSON file from the UniProtKB distribution in "dat" format

   Usage: uniprotkb_dat_to_json.py [--test] <inputFile.dat> <outputFile.json>
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import argparse
import kg2_util
import os
import re

UNIPROTKB_PROVIDED_BY_IRI = 'https://registry.identifiers.org/registry/uniprot'
UNIPROTKB_IDENTIFIER_BASE_IRI = 'https://identifiers.org/uniprot:'
RE_ORGANISM_TAXID = re.compile(r'NCBI_TaxID=(\d+)')
FIELD_CODES_USE_STRING = ['ID', 'SQ', 'RA', 'RX', 'RT', 'KW', 'CC', 'GN']
FIELD_CODES_DO_NOT_STRIP_NEWLINE = ['SQ']
FIELD_CODES_DO_NOT_STRIP_RIGHT_SEMICOLON = {'RX'}
REGEX_PUBLICATIONS = re.compile(r'((?:(?:PMID)|(?:PubMed)):\d+)')
REGEX_GENE_NAME = re.compile(r'^Name=([^ \;]+)')
REGEX_GENE_SYNONYMS = re.compile(r'Synonyms=([^\;]+)')
REGEX_HGNC = re.compile(r'^HGNC; (HGNC:\d+)')
REGEX_NCBIGeneID = re.compile(r'^GeneID; (\d+)')
DESIRED_SPECIES_INTS = set([kg2_util.NCBI_TAXON_ID_HUMAN])


def init_record():
    return {'organism': None,
            'organism_host': []}


def parse_records_from_uniprot_dat(uniprot_dat_file_name: str,
                                   desired_species_ints: set,
                                   test_mode: bool = False):
    record_list = []
    record = dict()
    line_ctr = 0
    update_date = os.path.getmtime(uniprot_dat_file_name)
    with open(uniprot_dat_file_name, 'r') as uniprot_file:
        record = init_record()
        for line_str in uniprot_file:
            fields = line_str.split("   ", maxsplit=1)
            field_code = fields[0]
            if field_code == "//\n":
                # end of a record
                organism_host_list = record.get('organism_host', None)
                organism = record.get('organism', None)
                assert organism is not None
                if (organism is not None and organism in desired_species_ints) or \
                   (organism_host_list is not None and len(set(organism_host_list) & desired_species_ints) > 0):
                    record_list.append(record)
                record = init_record()
            else:
                field_value = fields[1]
                if field_code == "":
                    field_code = 'SQ'
                    field_value = field_value.lstrip()
                if field_code not in FIELD_CODES_DO_NOT_STRIP_NEWLINE:
                    field_value = field_value.rstrip('\n')
                if field_code not in FIELD_CODES_DO_NOT_STRIP_RIGHT_SEMICOLON:
                    field_value = field_value.rstrip(';')
                if record.get(field_code, None) is None:
                    if field_code not in FIELD_CODES_USE_STRING:
                        if field_code != 'AC':
                            record[field_code] = [field_value.rstrip(';')]
                        else:
                            record[field_code] = [ac.strip() for ac in field_value.split(';')]
                    else:
                        record[field_code] = field_value
                else:
                    if type(record[field_code]) == list:
                        if field_code != 'AC':
                            record[field_code].append(field_value.rstrip(';'))
                        else:
                            record[field_code] += [ac.strip() for ac in field_value.split(';')]
                    else:
                        record[field_code] += field_value.lstrip()
                if field_code == 'OH':
                    re_match = RE_ORGANISM_TAXID.match(field_value)
                    if re_match is not None:
                        record['organism_host'].append(int(re_match[1]))
                if field_code == 'OX':
                    re_match = RE_ORGANISM_TAXID.match(field_value)
                    if re_match is not None:
                        organism = int(re_match[1])
                        record['organism'] = organism
            line_ctr += 1
            if line_ctr % 1000000 == 0:
                print("Have processed " + str(int(line_ctr / 1000000)) + " million lines")
                print("  Number of records: " + str(len(record_list)))
            if line_ctr > 1000000 and test_mode:
                break
    return [record_list, update_date]


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='uniprotkb_dat_to_json.py: builds a JSON representation of the UniProtKB')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


def make_edge(subject_curie_id: str,
              object_curie_id: str,
              predicate_label: str,
              update_date: str):
    relation = kg2_util.BIOLINK_CATEGORY_BASE_IRI + kg2_util.convert_snake_case_to_camel_case(predicate_label)
    relation_curie = kg2_util.CURIE_PREFIX_BIOLINK + ':' + predicate_label.replace(' ', '_')
    rel = kg2_util.make_edge(subject_curie_id,
                             object_curie_id,
                             relation,
                             relation_curie,
                             predicate_label,
                             UNIPROTKB_PROVIDED_BY_IRI,
                             update_date)
    return rel


def make_edges(records: list, nodes_dict: dict):
    ret_list = []
    for record_dict in records:
        accession = record_dict['AC'][0]
        curie_id = 'UniProtKB:' + accession
        organism_int = record_dict['organism']
        update_date = nodes_dict[curie_id]['update date']
        ret_list.append(make_edge(curie_id,
                                  'NCBITaxon:' + str(organism_int),
                                  'in_taxon',
                                  update_date))
        record_xrefs = record_dict.get('DR', None)
        if record_xrefs is not None:
            for xref_str in record_xrefs:
                hgnc_match = REGEX_HGNC.match(xref_str)
                if hgnc_match is not None:
                    hgnc_curie = hgnc_match[1]
                    ret_list.append(make_edge(hgnc_curie,
                                              curie_id,
                                              'encodes',
                                              update_date))
                gene_id_match = REGEX_NCBIGeneID.match(xref_str)
                if gene_id_match is not None:
                    ncbi_curie = 'NCBIGene:' + gene_id_match[1]
                    ret_list.append(make_edge(ncbi_curie,
                                              curie_id,
                                              'encodes',
                                              update_date))
    return ret_list


def make_nodes(records: list):
    ret_dict = {}
    for record_dict in records:
        synonyms = [record_dict['SQ']]
        accession_list = record_dict['AC']
        accession = accession_list[0]
        if len(accession_list) > 1:
            synonyms += accession_list[1:(len(accession_list)+1)]
        description_list = record_dict['DE']
        full_name = None
        name = None
        desc_ctr = 0
        description = record_dict.get('CC', '')
        for description_str in description_list:
            description_str = description_str.lstrip()
            if description_str.startswith('RecName: '):
                full_name = description_str.replace('RecName: Full=', '')
                if desc_ctr < len(description_list) - 1:
                    next_desc = description_list[desc_ctr + 1].lstrip()
                    if next_desc.startswith('Short='):
                        name = next_desc.replace('Short=', '')
                        continue
            else:
                if description_str.startswith('AltName: Full='):
                    synonyms.append(description_str.replace('AltName: Full=', ''))
                else:
                    if description_str.startswith('AltName: CD_antigen='):
                        synonyms.append(description_str.replace('AltName: CD_antigen=', ''))
                    if not description_str.startswith('Flags:') and not description_str.startswith('Contains:'):
                        description += '; ' + description_str
            desc_ctr += 1
        date_fields = record_dict['DT']
        date_ctr = 0
        creation_date = None
        update_date = None
        for date_str_raw in date_fields:
            date_str = date_str_raw.split(',')[0]
            if date_ctr == 0:
                creation_date = date_str
            if date_ctr == len(date_fields)-1:
                update_date = date_str
            date_ctr += 1
        publications_raw = record_dict.get('RX', None)
        publications = []
        if publications_raw is not None:
            for pub in publications_raw.split(';'):
                pub = pub.strip()
                if len(pub) > 0:
                    publications.append(pub.replace('=', ':').replace('PubMed:', 'PMID:'))
        else:
            publications = []
        assert type(publications) == list
        assert type(description) == str
        publications += [pub.replace('PubMed:', 'PMID:') for pub in REGEX_PUBLICATIONS.findall(description)]
        publications = list(set(publications))
        gene_names_str = record_dict.get('GN', None)
        gene_symbol = None
        if gene_names_str is not None:
            gene_names_str_list = gene_names_str.split(';')
            for gene_names_str_item in gene_names_str_list:
                gene_names_match = REGEX_GENE_NAME.match(gene_names_str_item)
                if gene_names_match is not None:
                    gene_symbol = gene_names_match[1]
                    synonyms.insert(0, gene_symbol)
                else:
                    gene_synonyms_match = REGEX_GENE_SYNONYMS.match(gene_names_str)
                    if gene_synonyms_match is not None:
                        synonyms += [syn.strip() for syn in gene_synonyms_match[1].split(',')]
        if name is None:
            if gene_symbol is not None:
                name = gene_symbol
            else:
                name = full_name
        node_curie = 'UniProtKB:' + accession
        iri = UNIPROTKB_IDENTIFIER_BASE_IRI + accession
        category_label = 'protein'
        node_dict = kg2_util.make_node(node_curie,
                                       iri,
                                       name,
                                       category_label,
                                       update_date,
                                       UNIPROTKB_PROVIDED_BY_IRI)
        node_dict['full name'] = full_name
        node_dict['description'] = description
        node_dict['synonym'] = synonyms
        node_dict['publications'] = publications
        node_dict['creation date'] = creation_date
        ret_dict[node_curie] = node_dict
    return ret_dict


# --------------- main starts here -------------------

if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    test_mode = args.test
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    [uniprot_records,
     update_date] = parse_records_from_uniprot_dat(input_file_name,
                                                   DESIRED_SPECIES_INTS,
                                                   test_mode)
    nodes_dict = make_nodes(uniprot_records)
    ontology_curie_id = kg2_util.IDENTIFIERS_ORG_REGISTRY_CURIE_PREFIX + ':uniprot'
    ont_node = kg2_util.make_node(ontology_curie_id,
                                  kg2_util.IDENTIFIERS_ORG_REGISTRY_IRI_BASE + 'uniprot',
                                  'UniProtKB',
                                  kg2_util.TYPE_DATA_SOURCE,
                                  update_date,
                                  ontology_curie_id)
    nodes_list = [ont_node] + [node_dict for node_dict in nodes_dict.values()]
    edges_list = make_edges(uniprot_records, nodes_dict)
    output_graph = {'nodes': nodes_list, 'edges': edges_list}
    kg2_util.save_json(output_graph, output_file_name, test_mode)
