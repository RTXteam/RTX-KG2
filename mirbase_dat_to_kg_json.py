#!/usr/bin/env python3
''' mirbase_dat_to_kg_json.py: Extracts a KG2 JSON file from the
    miRBase dataset in DAT format

    Usage: mirbase_dat_to_kg_json.py [--test] <inputFile.json>
    <outputFile.json>
'''

import json
import kg2_util
import argparse

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
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def format_data(mirbase):
    entry_list = []
    entry = dict()
    for line in mirbase:
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
    return entry_list


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



def make_nodes(entries, test_mode):
    nodes = []
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
        description += entry.get('SQ', '').replace('\t', ' ')
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
        nodes.append(node)
        nodes_to_species[node_id] = species_id
    return [nodes, all_xrefs, nodes_to_species]


def make_edges(xrefs, nodes_to_species, test_mode):
    edges = []
    edge_count = 0  
    for node_id in xrefs:
        edge_count += 1
        if test_mode and edge_count > 1000:
            break
        for xref_id in xrefs[node_id]:
            if xref_id.startswith(CURIE_PREFIX_HGNC) or xref_id.startswith(CURIE_PREFIX_NCBI_GENE):
                edge = kg2_util.make_edge_biolink(node_id,
                                                  xref_id,
                                                  kg2_util.EDGE_LABEL_BIOLINK_SAME_AS,
                                                  MIRBASE_KB_CURIE_ID,
                                                  None)
                edges.append(edge)
            else:
                edge = kg2_util.make_edge_biolink(node_id,
                                                  xref_id,
                                                  kg2_util.EDGE_LABEL_BIOLINK_RELATED_TO,
                                                  MIRBASE_KB_CURIE_ID,
                                                  None)
                edges.append(edge)
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
        edges.append(taxon_edge)
    return edges


if __name__ == '__main__':
    args = get_args()
    with open(args.inputFile, 'r') as mirbase:
        entries = format_data(mirbase)
    kp_node = kg2_util.make_node(MIRBASE_KB_CURIE_ID,
                                 MIRBASE_KB_URL,
                                 'miRBase',
                                 kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                 None,
                                 MIRBASE_KB_CURIE_ID)
    [nodes, xrefs, nodes_to_species] = make_nodes(entries, args.test)
    nodes.append(kp_node)
    edges = make_edges(xrefs, nodes_to_species, args.test)
    graph = {'nodes': nodes,
             'edges': edges}
    kg2_util.save_json(graph, args.outputFile, args.test)