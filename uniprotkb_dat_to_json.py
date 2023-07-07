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
import re
import sys


UNIPROTKB_PROVIDED_BY_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY + ':' + 'uniprot'
UNIPROTKB_IDENTIFIER_BASE_IRI = kg2_util.BASE_URL_UNIPROTKB
UNIPROT_KB_URL = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + 'uniprot'

RE_ORGANISM_TAXID = re.compile(r'NCBI_TaxID=(\d+)')
FIELD_CODES_USE_STRING = {'ID', 'SQ', 'RA', 'RX', 'RT', 'KW', 'CC', 'GN', 'OS'}
FIELD_CODES_DO_NOT_STRIP_NEWLINE = {}
FIELD_CODES_DO_NOT_STRIP_RIGHT_SEMICOLON = {'RX', 'CC', 'GN'}
FIELD_CODES_ADD_SPACE = {'CC'}
REGEX_PUBLICATIONS = re.compile(r'((?:(?:PMID)|(?:PubMed)):\d+)')
REGEX_GENE_NAME = re.compile(r'^Name=([^ \;]+)')
REGEX_GENE_SYNONYMS = re.compile(r'Synonyms=([^\;]+)')
REGEX_HGNC = re.compile(r'^HGNC; (HGNC:\d+)')
REGEX_NCBIGeneID = re.compile(r'^GeneID; (\d+)')
REGEX_XREF = re.compile(r'Xref=([^\;]+)\;')
REGEX_MIM = re.compile(r'\[MIM:([^\:\)]+)\]')
REGEX_EC_XREF = re.compile(r'EC=([\d\.]+)')
REGEX_SEPARATE_EVIDENCE_CODES = re.compile(r'(.*?)(\{(.*?)\})')
REGEX_HEADER = re.compile(r'([^\:]*)\: (.*)')
REGEX_BRACES = re.compile(r'\{[PE](?:[^\}]*)\}')
REGEX_PARENS = re.compile(r'\((?:PMID|PubMed|ECO)\:(?:[^\)]*)\)')
REGEX_SHORT = re.compile(r'Short=([^\;]*)')
REGEX_SHORT_DROP = re.compile(r'Short=(?:[^\;]*)')

LICENSE_TEXT = '---------------------------------------------------------------------------' \
               'Copyrighted by the UniProt Consortium, see https://www.uniprot.org/terms Di' \
               'stributed under the Creative Commons Attribution (CC BY 4.0) License ------' \
               '---------------------------------------------------------------------'

DESIRED_SPECIES_INTS = set([kg2_util.NCBI_TAXON_ID_HUMAN])


def scrub_braces_text(t: str) -> str:
    return ''.join(REGEX_PARENS.split(''.join(REGEX_BRACES.split(t))))


def init_record():
    return {'organism': None,
            'organism_host': []}


def re_match_to_tuple(m: re.Match) -> tuple:
    return tuple(m[i] for i in range(0, m.lastindex + 1))


def fix_publications(pub_curie: str) -> str:
    return pub_curie.replace('PubMed:', kg2_util.CURIE_PREFIX_PMID + ':')

def description_to_dict(untidy_description: str) -> dict:
    fields = untidy_description.split('-!- ')
    pairs = [re_match_to_tuple(REGEX_HEADER.match(field))[1:3] for field in fields if len(field.strip()) > 0]
    ret_dict = dict()
    for k, v in pairs:
        if k not in ret_dict:
            ret_dict[k] = [v]
        else:
            ret_dict[k].append(v)
    return ret_dict


def parse_records_from_uniprot_dat(uniprot_dat_file_name: str,
                                   desired_species_ints: set,
                                   test_mode: bool = False):
    record_list = []
    record = dict()
    line_ctr = 0
    with open(uniprot_dat_file_name, 'r') as uniprot_file:
        record = init_record()
        for line_str in uniprot_file:
            if line_str.startswith('# '):
                version = line_str.split('Version: ')[1].split(', ')[0].strip()
                update_date = line_str.split('Date: ')[1].strip()
                continue
            fields = line_str.split("   ", maxsplit=1)
            field_code = fields[0]
            if field_code == "//\n":
                # end of a record
                organism_host_list = record.get('organism_host', None)
                organism = record.get('organism', None)
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
                if field_code in FIELD_CODES_ADD_SPACE and not (field_value.endswith('-')):
                    field_value += ' '
                if record.get(field_code, None) is None:
                    if field_code not in FIELD_CODES_USE_STRING:
                        if field_code != 'AC':
                            record[field_code] = [field_value.rstrip(';')]
                        else:
                            record[field_code] = [ac.strip()
                                                  for ac in field_value.split(';')]
                    else:
                        record[field_code] = field_value
                else:
                    if type(record[field_code]) == list:
                        if field_code != 'AC':
                            record[field_code].append(field_value.rstrip(';'))
                        else:
                            record[field_code] += [ac.strip()
                                                   for ac in field_value.split(';')]
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
                print("Have processed " +
                      str(int(line_ctr / 1000000)) + " million lines")
                print("  Number of records: " + str(len(record_list)))
            if line_ctr > 1000000 and test_mode:
                break
    return [record_list, update_date, version]


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(
        description='uniprotkb_dat_to_json.py: builds a JSON representation of the UniProtKB')
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


def make_edges(records: list, nodes_dict: dict):
    ret_list = []
    for record_dict in records:
        accession = record_dict['AC'][0]
        curie_id = kg2_util.CURIE_PREFIX_UNIPROT + ':' + accession
        organism_int = record_dict['organism']
        update_date = nodes_dict[curie_id]['update_date']
        ret_list.append(kg2_util.make_edge_biolink(curie_id,
                                                   kg2_util.CURIE_PREFIX_NCBI_TAXON +
                                                   ':' + str(organism_int),
                                                   kg2_util.EDGE_LABEL_BIOLINK_IN_TAXON,
                                                   UNIPROTKB_PROVIDED_BY_CURIE_ID,
                                                   update_date))
        record_xrefs = record_dict.get('DR', None)
        if record_xrefs is not None:
            for xref_str in record_xrefs:
                hgnc_match = REGEX_HGNC.match(xref_str)
                if hgnc_match is not None:
                    hgnc_curie = hgnc_match[1]
                    ret_list.append(kg2_util.make_edge_biolink(curie_id,
                                                               hgnc_curie,
                                                               kg2_util.EDGE_LABEL_BIOLINK_GENE_PRODUCT_OF,
                                                               UNIPROTKB_PROVIDED_BY_CURIE_ID,
                                                               update_date))
                gene_id_match = REGEX_NCBIGeneID.match(xref_str)
                if gene_id_match is not None:
                    ncbi_curie = kg2_util.CURIE_PREFIX_NCBI_GENE + \
                        ':' + gene_id_match[1]
                    ret_list.append(kg2_util.make_edge_biolink(curie_id,
                                                               ncbi_curie,
                                                               kg2_util.EDGE_LABEL_BIOLINK_GENE_PRODUCT_OF,
                                                               UNIPROTKB_PROVIDED_BY_CURIE_ID,
                                                               update_date))
        if 'disease' in record_dict:
            for disease_rec in record_dict['disease']:
                mims = REGEX_MIM.findall(disease_rec)
                for m in mims:
                    mp = REGEX_PUBLICATIONS.findall(disease_rec)
                    pubs = [fix_publications(pub) for pub in mp]
                    e = kg2_util.make_edge_biolink(curie_id,
                                                   kg2_util.CURIE_PREFIX_OMIM + ':' + m,
                                                   kg2_util.EDGE_LABEL_BIOLINK_CAUSES, 
                                                   UNIPROTKB_PROVIDED_BY_CURIE_ID,
                                                   update_date)
                    e['publications'] = pubs
                    ret_list.append(e)
    for node_id, node_dict in nodes_dict.items():
        xrefs = node_dict['xrefs']
        if xrefs is not None and len(xrefs) > 0:
            for xref_curie in sorted(list(xrefs)):
                ret_list.append(kg2_util.make_edge_biolink(node_id,
                                                           xref_curie,
                                                           kg2_util.EDGE_LABEL_BIOLINK_PHYSICALLY_INTERACTS_WITH,
                                                           UNIPROTKB_PROVIDED_BY_CURIE_ID,
                                                           update_date))
        del node_dict['xrefs']
    return ret_list


def fix_xref(raw_xref: str):
    raw_xref = raw_xref.strip()
    if raw_xref.startswith('ChEBI:CHEBI:'):
        xref = kg2_util.CURIE_PREFIX_CHEBI + ':' + \
            raw_xref.replace('ChEBI:CHEBI:', '')
    elif raw_xref.startswith('Rhea:RHEA:'):
        xref = kg2_util.CURIE_PREFIX_RHEA + ':' + \
            raw_xref.replace('Rhea:RHEA:', '')
    elif raw_xref.startswith('Rhea:RHEA-COMP:'):
        xref = kg2_util.CURIE_PREFIX_RHEA_COMP + ':' + \
            raw_xref.replace('Rhea:RHEA-COMP:', '')
    elif raw_xref.startswith('EC='):
        xref = kg2_util.CURIE_PREFIX_KEGG_ENZYME + \
            ':EC:' + raw_xref.replace('EC=', '')
    else:
        print("Unknown xref: " + raw_xref, file=sys.stderr)
    return xref


def separate_evidence_codes(string: str):
    remaining_str = string
    ev_codes = ''
    match = REGEX_SEPARATE_EVIDENCE_CODES.match(string)
    if match is not None:
        remaining_str, ev_codes, _ = match.groups()
    return remaining_str, ev_codes


def make_nodes(records: list):
    ret_dict = {}
    for record_dict in records:
        xrefs = set()
        if 'CC' in record_dict:
            freetext_comments_str = record_dict['CC']
            freetext_comments_list = list(
                map(lambda thestr: thestr.strip(), freetext_comments_str.split('-!-')))
            for comment_str in freetext_comments_list:
                if comment_str.startswith('CATALYTIC ACTIVITY:') or comment_str.startswith('COFACTOR:'):
                    xref_match_res = REGEX_XREF.search(comment_str)
                    if xref_match_res is not None:
                        xrefs |= set(
                            filter(None, map(fix_xref, xref_match_res[1].split(','))))
        accession_list = record_dict['AC']
        accession = accession_list[0]
        synonyms = []
        if len(accession_list) > 1:
            synonyms += accession_list[1:(len(accession_list)+1)]
        description_list = record_dict['DE']
        full_name = None
        short_name = None
        desc_ctr = 0
        description = record_dict.get('CC', '')
        hit_contains = False
        for description_str in description_list:
            description_str = description_str.lstrip()
            if description_str.startswith('RecName: '):
                if not hit_contains:
                    full_name = description_str.replace('RecName: Full=', '')
                    if desc_ctr < len(description_list) - 1:
                        next_desc = description_list[desc_ctr + 1].lstrip()
                        if next_desc.startswith('Short='):
                            short_name = next_desc.replace('Short=', '')
                            synonyms += [short_name]
            elif description_str.startswith('AltName: Full='):
                synonyms.append(description_str.replace('AltName: Full=', ''))
            elif description_str.startswith('AltName: CD_antigen='):
                synonyms.append(description_str.replace(
                    'AltName: CD_antigen=', ''))
            elif description_str.startswith('Contains:'):
                hit_contains = True
            elif description_str.startswith('EC='):
                ec_match = REGEX_EC_XREF.search(description_str)
                if ec_match is not None:
                    xrefs.add(kg2_util.CURIE_PREFIX_KEGG +
                              ':' + 'EC:' + ec_match[1])
            else:
                pass
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
                    publications.append(pub.replace('=', ':').replace(
                        'PubMed:', kg2_util.CURIE_PREFIX_PMID + ':'))
        else:
            publications = []
        assert type(publications) == list
        assert type(description) == str
        publications += [fix_publications(pub) for pub in REGEX_PUBLICATIONS.findall(description)]
        publications = sorted(list(set(publications)))
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
                    gene_synonyms_match = REGEX_GENE_SYNONYMS.match(
                        gene_names_str_item)
                    if gene_synonyms_match is not None:
                        # evidence codes from gene synonyms are not preserved
                        synonyms += [separate_evidence_codes(syn)[0].strip()
                                     for syn in gene_synonyms_match[1].split(',')]
        if gene_symbol is not None:
            name = gene_symbol
        else:
            if short_name is not None:
                name = short_name
            else:
                name = full_name
        # remove evidence codes from name (issue #1171)
        name, _ = separate_evidence_codes(name)

        # append species name to name if not human (issue #1171)
        species = record_dict.get('OS', 'unknown species').rstrip(".")
        if "homo sapiens (human)" not in species.lower():
            name += f" ({species})"
        node_curie = kg2_util.CURIE_PREFIX_UNIPROT + ':' + accession
        iri = UNIPROTKB_IDENTIFIER_BASE_IRI + accession
        category_label = kg2_util.BIOLINK_CATEGORY_PROTEIN
        node_dict = kg2_util.make_node(node_curie,
                                       iri,
                                       name,
                                       category_label,
                                       update_date,
                                       UNIPROTKB_PROVIDED_BY_CURIE_ID)
        node_dict['full_name'] = scrub_braces_text(full_name)
        if not description.endswith(' '):
            description += ' '
        sequence = record_dict.get('SQ', '').strip('SEQUENCE   ')
        node_dict['has_biological_sequence'] = sequence
        description = description.replace(LICENSE_TEXT, '')
        description_dict = description_to_dict(description)
        if 'FUNCTION' in description_dict:
            function_text = ''.join(scrub_braces_text(t) for t in description_dict['FUNCTION'])
        else:
            function_text = ''
        if 'SIMILARITY' in description_dict:
            similarity_text = ''.join(scrub_braces_text(t) for t in description_dict['SIMILARITY'])
        else:
            similarity_text = ''
        description = ' '.join([function_text, similarity_text]).strip().replace(' . ', '')
        if ';' in description:
            got_short = False
            description_list = description.split(';')
            for s in description_list:
                m = REGEX_SHORT.match(s)
                if m is not None:
                    synonyms += m[1]
                    got_short = True
            if got_short:
                description = ''.join(REGEX_SHORT_DROP.split(description))
        node_dict['description'] = description.replace('. .', '.')
        record_dict['disease'] = description_dict.get('DISEASE', [])
        if len(synonyms) > 0:
            synonyms = [synonyms[0]] + list(set(synonyms) - {synonyms[0]})
        node_dict['synonym'] = synonyms
        node_dict['publications'] = publications
        node_dict['creation_date'] = creation_date
        if len(xrefs) == 0:
            xrefs = None
        node_dict['xrefs'] = xrefs
        ret_dict[node_curie] = node_dict
    return ret_dict


# --------------- main starts here -------------------

if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    test_mode = args.test
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    [uniprot_records,
     update_date,
     version] = parse_records_from_uniprot_dat(input_file_name,
                                               DESIRED_SPECIES_INTS,
                                               test_mode)

    nodes_dict = make_nodes(uniprot_records)
    ontology_curie_id = UNIPROTKB_PROVIDED_BY_CURIE_ID
    ont_node = kg2_util.make_node(ontology_curie_id,
                                  UNIPROT_KB_URL,
                                  'UniProtKB v' + version,
                                  kg2_util.BIOLINK_CATEGORY_RETRIEVAL_SOURCE,
                                  update_date,
                                  ontology_curie_id)
    nodes_list = [ont_node] + [node_dict for node_dict in nodes_dict.values()]
    edges_list = make_edges(uniprot_records, nodes_dict)
    output_graph = {'nodes': nodes_list, 'edges': edges_list}
    kg2_util.save_json(output_graph, output_file_name, test_mode)
