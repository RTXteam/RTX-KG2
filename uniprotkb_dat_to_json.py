#!/usr/bin/env python3
'''uniprotkb_dat_to_json.py: Extracts a KG2 JSON file from the UniProtKB distribution in "dat" format

   Usage: uniprotkb_dat_to_json.py [--test] --inputFile <inputFile.dat> --outputFile <outputFile.json>
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
import functools
import kg2_util
import re

UNIPROTKB_BASE_IRI = 'https://www.uniprot.org'
RE_ORGANISM_TAXID = re.compile('NCBI_TaxID=(\d+)')
FIELD_CODES_USE_STRING = ['ID', 'SQ', 'RA', 'RX', 'RT', 'KW', 'CC', 'GN']
FIELD_CODES_DO_NOT_STRIP_NEWLINE = ['SQ']
REGEX_PUBLICATIONS = re.compile('((?:(?:PMID)|(?:PubMed)):\d+)')
REGEX_GENE_NAME = re.compile('^Name=([^ \;]+)(\;| )')
REGEX_GENE_SYNONYMS = re.compile('Synonyms=([^\;]+)')
REGEX_HGNC = re.compile('^HGNC; (HGNC:\d+)')
REGEX_NCBIGeneID = re.compile('^GeneID; (\d+)')
DESIRED_SPECIES_INTS = set([9606])


def init_record():
    return {'organism': None,
            'organism_host': []}


def parse_records_from_uniprot_dat(uniprot_dat_file_name: str,
                                   desired_species_ints: set,
                                   test_mode: bool = False):
    record_list = []
    record = dict()
    line_ctr = 0
    with open(uniprot_dat_file_name, 'r') as uniprot_file:
        record = init_record()
        for line_str in uniprot_file:
            fields = line_str.split("   ", maxsplit=1)
            field_code = fields[0]
            if field_code == "//\n":
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
                    field_value = field_value.lstrip(' ')
                if field_code not in FIELD_CODES_DO_NOT_STRIP_NEWLINE:
                    field_value = field_value.rstrip('\n')
                if record.get(field_code, None) is None:
                    if field_code not in FIELD_CODES_USE_STRING:
                        if field_code != 'AC':
                            record[field_code] = [field_value]
                        else:
                            record[field_code] = [ac.strip() for ac in field_value.split(';')]
                    else:
                        record[field_code] = field_value
                else:
                    if type(record[field_code]) == list:
                        if field_code != 'AC':
                            record[field_code].append(field_value)
                        else:
                            record[field_code] += [ac.strip() for ac in field_value.split(';')]
                    else:
                        record[field_code] += field_value
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
    return record_list


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='uniprotkb_dat_to_json.py: builds a JSON representation of the UniProtKB')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('--inputFile', type=str, nargs=1)
    arg_parser.add_argument('--outputFile', type=str, nargs=1)
    return arg_parser




def make_edges(records: list, nodes_dict: dict):
    ret_list = []
    for record_dict in records:
        accession = record_dict['AC'][0]
        curie_id = 'UniProtKB:' + accession
        organism_int = record_dict['organism']
        update_date = nodes_dict[curie_id]['update date']
        ret_list.append(kg2_util.make_edge(curie_id, 'NCBITaxon:' + str(organism_int),
                                           'gene_product_has_organism_source',
                                           UNIPROTKB_BASE_IRI,
                                           update_date))
        record_xrefs = record_dict.get('DR', None)
        if record_xrefs is not None:
            for xref_str in record_xrefs:
                hgnc_match = REGEX_HGNC.match(xref_str)
                if hgnc_match is not None:
                    hgnc_curie = hgnc_match[1]
                    ret_list.append(kg2_util.make_edge(hgnc_curie,
                                                       curie_id,
                                                       'encodes',
                                                       UNIPROTKB_BASE_IRI,
                                                       update_date))
                gene_id_match = REGEX_NCBIGeneID.match(xref_str)
                if gene_id_match is not None:
                    ncbi_curie = 'NCBIGene:' + gene_id_match[1]
                    ret_list.append(kg2_util.make_edge(ncbi_curie,
                                                       curie_id,
                                                       'encodes',
                                                       UNIPROTKB_BASE_IRI,
                                                       update_date))
    return ret_list


def make_nodes(records: list, map_category_label_to_iri: callable):
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
                if not description_str.startswith('Flags:'):
                    synonyms.append(description_str)
                else:
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
        if publications_raw is not None:
            publications = [pub.strip().replace('=', ':').replace('PubMed:', 'PMID:') for pub in publications_raw.split(';')]
        else:
            publications = []
        assert type(publications) == list
        assert type(description) == str
        publications += [pub.replace('PubMed:', 'PMID:') for pub in REGEX_PUBLICATIONS.findall(description)]
        publications = list(set(publications))
        gene_names_str = record_dict.get('GN', None)
        if gene_names_str is not None:
            gene_names_match = REGEX_GENE_NAME.match(gene_names_str)
            if gene_names_match is not None:
                gene_symbol = gene_names_match[1]
                synonyms.append(gene_symbol)
            else:
                gene_symbol = None
            gene_synonyms_match = REGEX_GENE_SYNONYMS.match(gene_names_str)
            if gene_synonyms_match is not None:
                synonyms += [syn.strip() for syn in gene_synonyms_match[1].split(',')]
        if name is None:
            if gene_symbol is not None:
                name = gene_symbol
            else:
                name = full_name
        node_curie = 'UniProtKB:' + accession
        node_dict = {
            'id': node_curie,
            'iri': UNIPROTKB_BASE_IRI + '/' + accession,
            'full name': full_name,
            'name': name,
            'category': map_category_label_to_iri('protein'),
            'category label': 'protein',
            'description': description,
            'synonym': synonyms,
            'publications': publications,
            'creation date': creation_date,
            'update date': update_date,
            'deprecated': False,
            'replaced by': None,
            'provided by': UNIPROTKB_BASE_IRI,
            'ontology node type': 'INDIVIDUAL'
            }
        ret_dict[node_curie] = node_dict
    return ret_dict


# --------------- main starts here -------------------

if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    test_mode = args.test
    input_file_name = args.inputFile[0]
    output_file_name = args.outputFile[0]
    uniprot_records = parse_records_from_uniprot_dat(input_file_name,
                                                     DESIRED_SPECIES_INTS,
                                                     test_mode)
    map_category_label_to_iri = functools.partial(kg2_util.convert_biolink_category_to_iri,
                                                  biolink_category_base_iri=kg2_util.BIOLINK_CATEGORY_BASE_IRI)
    nodes_dict = make_nodes(uniprot_records, map_category_label_to_iri)
    nodes_list = [node_dict for node_dict in nodes_dict.values()]
    edges_list = make_edges(uniprot_records, nodes_dict)
    output_graph = {'nodes': nodes_list, 'edges': edges_list}
    kg2_util.save_json(output_graph, output_file_name, test_mode)
