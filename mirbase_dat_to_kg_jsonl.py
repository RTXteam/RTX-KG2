#!/usr/bin/env python3
''' mirbase_dat_to_kg_json.py: Extracts a KG2 JSON file from the
    miRBase dataset in DAT format

    Usage: mirbase_dat_to_kg_json.py [--test] <inputFile.json>
    <outputNodesFile.json> <outputEdgesFile.json>
'''

import json
import kg2_util
import argparse
import datetime

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


CURIE_PREFIX_MIRBASE = kg2_util.CURIE_PREFIX_MIRBASE
CURIE_PREFIX_NCBI_GENE = kg2_util.CURIE_PREFIX_NCBI_GENE
CURIE_PREFIX_HGNC = kg2_util.CURIE_PREFIX_HGNC

MIRBASE_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY + ':' + 'mirbase'
MIRBASE_KB_URL = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + 'mirbase'


def get_args():
    arg_parser = argparse.ArgumentParser(description='mirbase_dat_to_kg_json.py: \
                                         builds a KG2 JSON representation of \
                                         miRBase microRNAs')
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_data(mirbase):
    entry_list = []
    entry = dict()
    for line in mirbase:
        if line.startswith('# '):
            version = line.split('Version: ')[1].strip()
            continue
        if line.startswith('//\n'):
            entry_list.append(entry)
            entry = dict()
            continue
        if line.startswith('  '):
            line = line.replace('  ', 'SQ', 1)
        field_name = line.split('   ', maxsplit=1)[0].strip()
        try:
            field_data = line.split('   ', maxsplit=1)[1].replace('\n', ' ')
        except IndexError:
            field_data = ''
        if field_name in entry:
            entry[field_name] += "\t" + field_data
        else:
            entry[field_name] = field_data
    return entry_list, version


def get_node_id(entry):
    return CURIE_PREFIX_MIRBASE + ':' + entry['AC'].replace(';', '').strip()


def only_include_certain_species(species):
    # Options are: "PTC", "GMO", "IPU", "AOF", "FVE", "TNI", "TTU", "PMA",
    # "SEU", "OAR", "PPE", "PIN", "ESI", "TUR", "CCA", "PXY", "DMA", "CRT",
    # "DNO", "PNY", "HAR", "CLI", "DMO", "GPY", "PRA", "MCO", "GMA", "BMO",
    # "CCL", "EMU", "OHA", "SOF", "ALY", "CSA", "CFA", "SLA", "SSY", "DWI",
    # "SMO", "SSL", "PTR", "AAE", "CBR", "DRE", "PEU", "AGE", "VVI", "OAN",
    # "ASU", "GHR", "DSI", "API", "CBN", "BFL", "BOL", "AQU", "EEL", "BRA",
    # "LJA", "MES", "SMR", "APL", "DME", "RGL", "MDM", "NGI", "BMA", "MJA",
    # "BBE", "HHI", "CAS", "DER", "SKO", "AJA", "PRD", "SJA", "PPC", "MNE",
    # "AAU", "TCF", "PGI", "PTI", "PAL", "CTE", "RMI", "NVI", "HME", "LVA",
    # "MTR", "TAE", "PBI", "CCR", "VCA", "CJA", "SMC", "CQU", "HBR", "CIN",
    # "VRL", "OLA", "STR", "PAB", "ODI", "DDI", "CSI", "OSA", "TRE", "CME",
    # "BDI", "PPA", "TCC", "PMI", "CHI", "SBO", "MEU", "EUN", "BNA", "LGI",
    # "SFR", "CPI", "CLA", "AGA", "DYA", "XLA", "VUN", "HTU", "ATH", "MZE",
    # "PTE", "ZMA", "XTR", "BCY", "PLA", "MMR", "AME", "TGU", "PTA", "CEL",
    # "DGR", "SLY", "GSO", "PPT", "MLE", "PSJ", "BIB", "SMI", "NLE", "LLA",
    # "HPA", "DPE", "GHB", "AMI", "SMA", "SCI", "HRU", "GGA", "CPO", "TCA",
    # "DSE", "PBV", "RNO", "OCU", "CLN", "SHA", "LMI", "PCA", "SPU", "BGY",
    # "RCO", "BDO", "LCO", "ATA", "MDO", "SSA", "CRE", "HAN", "NTA", "HPE",
    # "NBR", "ACA", "OGA", "EGU", "DPR", "NVE", "PPY", "CTR", "MML", "XBO",
    # "STU", "MMU", "CGR", "FAR", "POL", "DQU", "PHA", "BTA", "SSC", "CPA",
    # "FRU", "SME", "ISC", "EFU", "ABU", "DPU", "DVI", "HVU", "AHY", "AMG",
    # "ATR", "TCH", "LCA", "GAR", "SBI", "AQC", "GRA", "ONI", "HMA", "GSA",
    # "CRM", "CST", "PDE", "GGO", "HEX", "MSE", "AMA", "EGR", "HCO", "DAN",
    # "NLO", "LUS", "HPO", "FHE", "SSP", "DPS", "HCI", "PVU", "ECA"
    human_id = kg2_util.CURIE_PREFIX_NCBI_TAXON + ':' + str(kg2_util.NCBI_TAXON_ID_HUMAN)
    include_dict = {'HSA': human_id}
    if species in include_dict:
        return include_dict[species]
    return False


def format_publication(publication):
    return 'PMID:' + publication.split(';')[1].replace('.', '').strip()


def format_xref(xref: str):
    source_to_kg2_source = {'ENTREZGENE': CURIE_PREFIX_NCBI_GENE,
                            'HGNC': CURIE_PREFIX_HGNC,
                            'MIR': None,
                            'RFAM': None,
                            'TARGETS:PICTAR-VERT': None}
    source = source_to_kg2_source[xref.split(';')[0].strip()]
    id = xref.split(';')[1].strip()
    if source is not None:
        return source + ':' + id
    return None


def make_nodes(entries, nodes_output, test_mode):
    all_xrefs = dict()
    nodes_to_species = dict()
    entry_count = 0
    for entry in entries:
        species = entry['ID'].split(';')[2].strip()
        species_id = only_include_certain_species(species)
        if not species_id:
            continue
        entry_count += 1
        if test_mode and entry_count > 1000:
            break
        node_id = get_node_id(entry)
        node_iri = kg2_util.BASE_URL_MIRBASE + node_id.split(':')[1]
        node_category = kg2_util.BIOLINK_CATEGORY_MICRORNA
        node_name = entry['DE'].strip()
        description = entry.get('CC', '').replace('\t', ' ').replace('  ', ' ')
        sequence = entry.get('SQ', '').replace('\t', ' ')
        publications = entry.get('RX', None)
        xrefs = entry.get('DR', None)
        if xrefs is not None:
            xrefs = [format_xref(xref) for xref in xrefs.split('\t') if format_xref(xref) is not None]
            all_xrefs[node_id] = xrefs
        if publications is not None:
            publications = [format_publication(publication) for publication in publications.split('\t')]
        node = kg2_util.make_node(node_id,
                                  node_iri,
                                  node_name,
                                  node_category,
                                  None,
                                  MIRBASE_KB_CURIE_ID)
        node['description'] = description
        node['publications'] = publications
        node['has_biological_sequence'] = sequence.strip('Sequence ')
        nodes_output.write(node)
        nodes_to_species[node_id] = species_id
    return [all_xrefs, nodes_to_species]


def make_edges(xrefs, nodes_to_species, edges_output, test_mode):
    edge_count = 0
    for node_id in xrefs:
        edge_count += 1
        if test_mode and edge_count > 1000:
            break
        for xref_id in xrefs[node_id]:
            if xref_id.startswith(CURIE_PREFIX_HGNC) or \
               xref_id.startswith(CURIE_PREFIX_NCBI_GENE):
                edge = kg2_util.make_edge_biolink(node_id,
                                                  xref_id,
                                                  kg2_util.EDGE_LABEL_BIOLINK_GENE_PRODUCT_OF,
                                                  MIRBASE_KB_CURIE_ID,
                                                  None)
                edges_output.write(edge)
            else:
                edge = kg2_util.make_edge_biolink(node_id,
                                                  xref_id,
                                                  kg2_util.EDGE_LABEL_BIOLINK_RELATED_TO,
                                                  MIRBASE_KB_CURIE_ID,
                                                  None)
                edges_output.write(edge)
    taxon_edge_count = 0
    for node_id in nodes_to_species:
        taxon_edge_count += 1
        if test_mode and taxon_edge_count > 1000:
            break
        taxon_edge = kg2_util.make_edge_biolink(node_id,
                                                nodes_to_species[node_id],
                                                kg2_util.EDGE_LABEL_BIOLINK_IN_TAXON,
                                                MIRBASE_KB_CURIE_ID,
                                                None)
        edges_output.write(taxon_edge)


if __name__ == '__main__':
    print("Start time: ", date())
    args = get_args()
    input_file_name = args.inputFile
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    with open(input_file_name, 'r') as mirbase:
        entries, version = format_data(mirbase)
    kp_node = kg2_util.make_node(MIRBASE_KB_CURIE_ID,
                                 MIRBASE_KB_URL,
                                 'miRBase v' + version,
                                 kg2_util.SOURCE_NODE_CATEGORY,
                                 None,
                                 MIRBASE_KB_CURIE_ID)
    [xrefs, nodes_to_species] = make_nodes(entries, nodes_output, test_mode)
    nodes_output.write(kp_node)

    make_edges(xrefs, nodes_to_species, edges_output, test_mode)

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)

    print("Finish time: ", date())
