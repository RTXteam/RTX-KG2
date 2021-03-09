#!/usr/bin/env python3
''' reactome_mysql_to_kg_json.py: Extracts a KG2 JSON file from the
    Reactome MySQL Database

    Usage: reactome_mysql_to_kg_json.py [--test] <outputFile.json>
'''

import pymysql
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


REACTOME_BASE_IRI = kg2_util.BASE_URL_REACTOME
REACTOME_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
                                + ":reactome"
REACTOME_RELATION_CURIE_PREFIX = kg2_util.CURIE_PREFIX_REACTOME
REACTOME_KB_IRI = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + 'reactome'

NCBI_TAXON_PREFIX = kg2_util.CURIE_PREFIX_NCBI_TAXON
ENSEMBL_PREFIX = kg2_util.CURIE_PREFIX_ENSEMBL
PMID_PREFIX = kg2_util.CURIE_PREFIX_PMID

BIOLOGICAL_PROCESS = kg2_util.BIOLINK_CATEGORY_BIOLOGICAL_PROCESS
DRUG = kg2_util.BIOLINK_CATEGORY_DRUG
MOLECULAR_ACTIVITY = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ACTIVITY
MOLECULAR_ENTITY = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ENTITY
PATHWAY = kg2_util.BIOLINK_CATEGORY_PATHWAY

ROW_LIMIT_TEST_MODE = 1000


def get_args():
    arg_parser = argparse.ArgumentParser(description='reactome_mysql_to_kg_json.py: \
                                         builds a KG2 JSON representation of \
                                         Reactome')
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def run_sql(sql: str, connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
    except pymysql.err.InternalError:
        results = ()
    return results


def format_edge(subject_id: str, object_id: str, predicate_label: str):
    relation_curie = kg2_util.predicate_label_to_curie(predicate_label,
                                                       REACTOME_RELATION_CURIE_PREFIX)
    return kg2_util.make_edge(subject_id,
                              object_id,
                              relation_curie,
                              predicate_label,
                              REACTOME_KB_CURIE_ID)


def match_name_to_prefix(name: str):
    # The prefix for 'COMPOUND' may seem weird, but it
    # has the IRI http://www.genome.ad.jp/kegg/ in the MySQL database.

    name_prefix_dict = {'ENSEMBL': kg2_util.CURIE_PREFIX_ENSEMBL,
                        'DDBJ': None,
                        'NCBI Entrez Gene': kg2_util.CURIE_PREFIX_NCBI_GENE,
                        'SwissProt': kg2_util.CURIE_PREFIX_UNIPROT,
                        'SPTREMBL': None,
                        'EMBL': None,
                        'UniProt': kg2_util.CURIE_PREFIX_UNIPROT,
                        'ChEBI': kg2_util.CURIE_PREFIX_CHEBI,
                        'NCBI_Protein': None,
                        'SPTR': None,
                        'COMPOUND': kg2_util.CURIE_PREFIX_KEGG,
                        'PubChem Compound': None,
                        'GenBank': None,
                        'KEGG Glycan': kg2_util.CURIE_PREFIX_KEGG,
                        'GLYCAN': None,
                        'GB': None,
                        'COSMIC': None,
                        'ENZYME': None,
                        'SWALL': None,
                        'ENSEMBL_homo_sapiens_GENE': ENSEMBL_PREFIX,
                        'ENSEMBL_Homo_sapiens_GENE': ENSEMBL_PREFIX,
                        'IntAct Complex Portal': None,
                        'OMIM': kg2_util.CURIE_PREFIX_OMIM,
                        'NCBI Nucleotide': None,
                        'PubChem Substance': None,
                        'ClinVar': None,
                        'ComplexPortal': None,
                        'EC': None,
                        'ClinGen': None,
                        'miRBase': 'miRBase',
                        'PRF': None,
                        'IUPHAR': None,
                        'PubChem': None,
                        'PubChem SID': None}

    return name_prefix_dict[name]


def match_species_to_id(species: str):
    human_id = NCBI_TAXON_PREFIX + ':' + str(kg2_util.NCBI_TAXON_ID_HUMAN)
    species_dict = {'Homo sapiens': human_id,
                    'Mus musculus': NCBI_TAXON_PREFIX + ':10090',
                    'Rattus norvegicus': NCBI_TAXON_PREFIX + ':10116',
                    'Bos taurus': NCBI_TAXON_PREFIX + ':9913',
                    'Ovis aries': NCBI_TAXON_PREFIX + ':9940',
                    'Oryctolagus cuniculus': NCBI_TAXON_PREFIX + ':9986',
                    'Gallus gallus': NCBI_TAXON_PREFIX + ':9031',
                    'Sus scrofa': NCBI_TAXON_PREFIX + ':9823',
                    'Canis familiaris': NCBI_TAXON_PREFIX + ':9615',
                    'Xenopus laevis': NCBI_TAXON_PREFIX + ':8355',
                    'Cercopithecus aethiops': NCBI_TAXON_PREFIX + ':9534',
                    'Macaca mulatta': NCBI_TAXON_PREFIX + ':9544',
                    'Drosophila melanogaster': NCBI_TAXON_PREFIX + ':7227',
                    'Cavia porcellus': NCBI_TAXON_PREFIX + ':10141',
                    'Cricetulus griseus': NCBI_TAXON_PREFIX + ':10029',
                    'Caenorhabditis elegans': NCBI_TAXON_PREFIX + ':6239',
                    'Danio rerio': NCBI_TAXON_PREFIX + ':7955',
                    'Saccharomyces cerevisiae': NCBI_TAXON_PREFIX + ':4932',
                    'Schizosaccharomyces pombe': NCBI_TAXON_PREFIX + ':4896',
                    'Penicillium chrysogenum': NCBI_TAXON_PREFIX + ':5076',
                    'Escherichia coli': NCBI_TAXON_PREFIX + ':562',
                    'Felis catus': NCBI_TAXON_PREFIX + ':9685',
                    'Chlorocebus sabaeus': NCBI_TAXON_PREFIX + ':60711',
                    'Plasmodium falciparum': NCBI_TAXON_PREFIX + ':5833',
                    'Dictyostelium discoideum': NCBI_TAXON_PREFIX + ':44689',
                    'Mycobacterium tuberculosis': NCBI_TAXON_PREFIX + ':1773',
                    'Crithidia fasciculata': NCBI_TAXON_PREFIX + ':5656',
                    'Xenopus tropicalis': NCBI_TAXON_PREFIX + ':8364',
                    'Triticum aestivum': NCBI_TAXON_PREFIX + ':4565',
                    'Vigna radiata var. radiata': NCBI_TAXON_PREFIX + ':3916',
                    'Meleagris gallopavo': NCBI_TAXON_PREFIX + ':9103',
                    'Homarus americanus': NCBI_TAXON_PREFIX + ':6706',
                    'Salmonella typhimurium': NCBI_TAXON_PREFIX + ':90371',
                    'Arenicola marina': NCBI_TAXON_PREFIX + ':6344',
                    'Human immunodeficiency virus 1': NCBI_TAXON_PREFIX + ':11676',
                    'Staphylococcus aureus': NCBI_TAXON_PREFIX + ':1280',
                    'Sendai virus': NCBI_TAXON_PREFIX + ':11191',
                    'Human herpesvirus 1': NCBI_TAXON_PREFIX + ':10298',
                    'West Nile virus': NCBI_TAXON_PREFIX + ':11082',
                    'Severe acute respiratory syndrome coronavirus 2': NCBI_TAXON_PREFIX + ':2697049',
                    'Candida albicans': NCBI_TAXON_PREFIX + ':5476',
                    'Rotavirus': NCBI_TAXON_PREFIX + ':10912',
                    'Human herpesvirus 8': NCBI_TAXON_PREFIX + ':37296',
                    'Sindbis virus': NCBI_TAXON_PREFIX + ':11034',
                    'Tick-borne encephalitis virus': NCBI_TAXON_PREFIX + ':11084',
                    'Human alphaherpesvirus 2': NCBI_TAXON_PREFIX + ':10310',
                    'Listeria monocytogenes': NCBI_TAXON_PREFIX + ':1639',
                    'Legionella pneumophila': NCBI_TAXON_PREFIX + ':446',
                    'Clostridium tetani': NCBI_TAXON_PREFIX + ':1513',
                    'Human cytomegalovirus': NCBI_TAXON_PREFIX + ':10359',
                    'Chlamydia trachomatis': NCBI_TAXON_PREFIX + ':813',
                    'Neisseria meningitidis serogroup B': NCBI_TAXON_PREFIX + ':491',
                    'Influenza A virus': NCBI_TAXON_PREFIX + ':11320',
                    'Corynephage beta': NCBI_TAXON_PREFIX + ':10703',
                    'Neisseria gonorrhoeae': NCBI_TAXON_PREFIX + ':485',
                    'Molluscum contagiosum virus subtype 1': NCBI_TAXON_PREFIX + ':10280',
                    'Hepatitis B virus': NCBI_TAXON_PREFIX + ':10407',
                    'Hepatitis C Virus': NCBI_TAXON_PREFIX + ':11103',
                    'Cowpox virus': NCBI_TAXON_PREFIX + ':10243',
                    'Human SARS coronavirus': None,
                    'Measles virus': NCBI_TAXON_PREFIX + ':11234',
                    'Clostridium botulinum': NCBI_TAXON_PREFIX + ':1491',
                    'Bacillus anthracis': NCBI_TAXON_PREFIX + ':1392',
                    'Hepatitis C virus genotype 2a': NCBI_TAXON_PREFIX + ':31649',
                    'Dengue virus': NCBI_TAXON_PREFIX + ':12637',
                    'Vaccinia virus': NCBI_TAXON_PREFIX + ':10245',
                    'Human gammaherpesvirus 4': NCBI_TAXON_PREFIX + ':10376'}
    return species_dict[species]


def match_reactome_category_to_biolink(category: str):
    category_dict = {'Reaction': MOLECULAR_ACTIVITY,
                     'OtherEntity': MOLECULAR_ENTITY,
                     'SimpleEntity': MOLECULAR_ENTITY,
                     'GenomeEncodedEntity': MOLECULAR_ENTITY,
                     'BlackBoxEvent': MOLECULAR_ACTIVITY,
                     'DefinedSet': MOLECULAR_ENTITY,
                     'ChemicalDrug': DRUG,
                     'Complex': MOLECULAR_ENTITY,
                     'FailedReaction': MOLECULAR_ACTIVITY,
                     'Pathway': kg2_util.BIOLINK_CATEGORY_PATHWAY,
                     'Depolymerisation': MOLECULAR_ACTIVITY,
                     'PositiveRegulation': None,
                     'NegativeGeneExpressionRegulation': None,
                     'NegativeRegulation': None,
                     'CandidateSet': MOLECULAR_ENTITY,
                     'Requirement': None,
                     'ProteinDrug': DRUG,
                     'Polymer': MOLECULAR_ENTITY,
                     'EntityWithAccessionedSequence': MOLECULAR_ENTITY,
                     'Polymerisation': MOLECULAR_ACTIVITY,
                     'PositiveGeneExpressionRegulation': None}

    return category_dict[category]


def only_include_certain_species(reactome_id: str):
    include_species = ['HSA', 'ALL']
    if reactome_id.split('-')[1] in include_species:
        return reactome_id
    return None


def get_nodes(connection, test):
    pathway_dict = dict()
    stable_id_sql = "SELECT si.identifier, \
                     GROUP_CONCAT(DISTINCT dbobj._displayName), \
                     GROUP_CONCAT(DISTINCT dbobj._timestamp), \
                     GROUP_CONCAT(DISTINCT dbobj._class), \
                     GROUP_CONCAT(DISTINCT lit_fr_e.pubMedIdentifier), \
                     GROUP_CONCAT(DISTINCT lit_fr_p.pubMedIdentifier), \
                     GROUP_CONCAT(DISTINCT sum_fr_e.text), \
                     GROUP_CONCAT(DISTINCT sum_fr_p.text), \
                     GROUP_CONCAT(DISTINCT sum_fr_r.text), \
                     GROUP_CONCAT(DISTINCT ins_ed.dateTime) \
                     FROM StableIdentifier si \
                     INNER JOIN DatabaseObject dbobj \
                     ON si.DB_ID=dbobj.stableIdentifier \
                     LEFT JOIN InstanceEdit ins_ed \
                     ON dbobj.created=ins_ed.DB_ID \
                     LEFT JOIN Event_2_literatureReference ev_lit \
                     ON dbobj.DB_ID=ev_lit.DB_ID \
                     LEFT JOIN LiteratureReference lit_fr_e \
                     ON lit_fr_e.DB_ID=ev_lit.literatureReference \
                     LEFT JOIN Event_2_summation ev_sum \
                     ON ev_sum.DB_ID=dbobj.DB_ID \
                     LEFT JOIN Summation sum_fr_e \
                     ON ev_sum.summation=sum_fr_e.DB_ID \
                     LEFT JOIN PhysicalEntity_2_literatureReference pe_lit \
                     ON dbobj.DB_ID=pe_lit.DB_ID \
                     LEFT JOIN LiteratureReference lit_fr_p \
                     ON lit_fr_p.DB_ID=pe_lit.literatureReference \
                     LEFT JOIN PhysicalEntity_2_summation pe_sum \
                     ON dbobj.DB_ID=pe_sum.DB_ID \
                     LEFT JOIN Summation sum_fr_p \
                     ON pe_sum.summation = sum_fr_p.DB_ID \
                     LEFT JOIN Regulation_2_summation reg_sum \
                     on reg_sum.DB_ID=dbobj.DB_ID \
                     LEFT JOIN Summation sum_fr_r \
                     ON sum_fr_r.DB_ID=reg_sum.summation \
                     GROUP BY si.identifier"
    if test:
        stable_id_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    stable_id_results = run_sql(stable_id_sql, connection)
    nodes = []
    for identifier in stable_id_results:
        node_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + identifier[0])
        if node_id is None:
            continue
        name = identifier[1]
        update_date = str(identifier[2])
        try:
            category_label = match_reactome_category_to_biolink(identifier[3])
            if category_label is None:
                continue
        except KeyError:
            print("Category for", identifier[3], "not in match_reactome_category_to_biolink")
            continue
        publications_event = identifier[4]
        publications_phy_ent = identifier[5]
        description_event = identifier[6]
        description_phy_ent = identifier[7]
        descrption_reg = identifier[8]
        iri = REACTOME_BASE_IRI + identifier[0]
        created_date = identifier[9]
        if publications_event is not None:
            publications = publications_event.split(',')
            publications = [PMID_PREFIX + ':' + publication for publication in publications]
        elif publications_phy_ent is not None:
            publications = publications_phy_ent.split(',')
            publications = [PMID_PREFIX + ':' + publication for publication in publications]
        else:
            publications = []
        if description_event is not None:
            description = description_event
        elif description_phy_ent is not None:
            description = description_phy_ent
        else:
            description = descrption_reg
        node = kg2_util.make_node(node_id,
                                  iri,
                                  name,
                                  category_label,
                                  update_date,
                                  REACTOME_KB_CURIE_ID)
        node['description'] = description
        node['publications'] = publications
        node['creation_date'] = str(created_date)
        nodes.append(node)

    return nodes


def get_reaction_inputs_and_outputs(connection, test):
    edges = []
    in_sql = "SELECT DISTINCT si_sub.identifier, si_obj.identifier \
              FROM ReactionlikeEvent_2_input reaction \
              INNER JOIN DatabaseObject dbobj_sub \
              ON reaction.DB_ID=dbobj_sub.DB_ID \
              INNER JOIN StableIdentifier si_sub \
              ON si_sub.DB_ID=dbobj_sub.stableIdentifier \
              INNER JOIN DatabaseObject dbobj_obj \
              ON dbobj_obj.DB_ID=reaction.input \
              INNER JOIN StableIdentifier si_obj \
              ON si_obj.DB_ID=dbobj_obj.stableIdentifier"
    if test:
        in_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    in_results = run_sql(in_sql, connection)
    for input in in_results:
        subject_id = only_include_certain_species(input[0])
        object_id = only_include_certain_species(input[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_input"
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    out_sql = "SELECT DISTINCT si_sub.identifier, si_obj.identifier \
               FROM ReactionlikeEvent_2_output reaction \
               INNER JOIN DatabaseObject dbobj_sub \
               ON reaction.DB_ID=dbobj_sub.DB_ID \
               INNER JOIN StableIdentifier si_sub \
               ON si_sub.DB_ID=dbobj_sub.stableIdentifier \
               INNER JOIN DatabaseObject dbobj_obj \
               ON dbobj_obj.DB_ID=reaction.output \
               INNER JOIN StableIdentifier si_obj \
               ON si_obj.DB_ID=dbobj_obj.stableIdentifier"
    if test:
        out_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    out_results = run_sql(out_sql, connection)
    for out in out_results:
        subject_id = only_include_certain_species(out[0])
        object_id = only_include_certain_species(out[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_output"
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)
    return edges


def get_pathway_events(connection, test):
    edges = []
    sql = "SELECT DISTINCT si_sub.identifier, si_obj.identifier \
           FROM Pathway_2_hasEvent pathway \
           INNER JOIN DatabaseObject dbobj_sub \
           ON pathway.DB_ID=dbobj_sub.DB_ID \
           INNER JOIN StableIdentifier si_sub \
           ON si_sub.DB_ID=dbobj_sub.stableIdentifier \
           INNER JOIN DatabaseObject dbobj_obj \
           ON dbobj_obj.DB_ID=pathway.hasEvent \
           INNER JOIN StableIdentifier si_obj \
           ON si_obj.DB_ID=dbobj_obj.stableIdentifier"
    if test:
        sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    has_event_results = run_sql(sql, connection)
    for has_event in has_event_results:
        subject_id = only_include_certain_species(has_event[0])
        object_id = only_include_certain_species(has_event[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_event"
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    return edges


def get_author_of_PMID(pmid: str, connection):
    sql = "SELECT per.surname, lr.year \
           FROM LiteratureReference lr \
           INNER JOIN Publication_2_author pub_auth \
           ON pub_auth.DB_ID=lr.DB_ID \
           INNER JOIN Person per \
           ON per.DB_ID=pub_auth.author \
           WHERE lr.pubMedIdentifier=" + str(pmid)
    results = run_sql(sql, connection)
    try:
        second_result = results[1][0].lower().title()
    except IndexError:
        second_result = None
    return [results[0][0].lower().title(), results[0][1], len(results), second_result]


def get_event_characteristics(connection, test):
    edges = []
    sql = "SELECT si.identifier, eo.identifier \
           FROM Event_2_disease ev_dis \
           INNER JOIN DatabaseObject dbobj_sub \
           ON dbobj_sub.DB_ID=ev_dis.DB_ID \
           INNER JOIN StableIdentifier si \
           ON si.DB_ID=dbobj_sub.stableIdentifier \
           INNER JOIN ExternalOntology eo \
           ON eo.DB_ID=ev_dis.disease"
    if test:
        sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    disease_results = run_sql(sql, connection)
    for ev_dis in disease_results:
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + ev_dis[0])
        if subject_id is None:
            continue
        object_id = kg2_util.CURIE_PREFIX_DOID + ':' + ev_dis[1]
        predicate = 'linked_to_disease'
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    compartment_sql = "SELECT si_sub.identifier, go.accession \
                       FROM Event_2_compartment ev_comp \
                       INNER JOIN Compartment compart \
                       ON compart.DB_ID=ev_comp.compartment \
                       INNER JOIN GO_CellularComponent_2_instanceOf go_io \
                       ON go_io.instanceOf=compart.DB_ID \
                       INNER JOIN GO_CellularComponent go \
                       ON go.DB_ID=go_io.instanceOf \
                       INNER JOIN DatabaseObject dbobj_sub \
                       ON ec.DB_ID=dbobj_sub.DB_ID \
                       INNER JOIN StableIdentifier si_sub \
                       ON si_sub.DB_ID=dbobj_sub.stableIdentifier"
    if test:
        compartment_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    compartment_results = run_sql(compartment_sql, connection)
    for compartment_ev in compartment_results:
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + compartment_ev[0])
        if subject_id is None:
            continue
        object_id = kg2_util.CURIE_PREFIX_GO + ':' + compartment_ev[1]
        predicate = 'in_location'
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    regulation_sql = "SELECT si_sub.identifier, \
                      si_reg.identifier, \
                      GROUP_CONCAT(DISTINCT rl_rb.regulatedBy_class), \
                      si_obj.identifier, \
                      GROUP_CONCAT(DISTINCT sum_fr_r.text), \
                      GROUP_CONCAT(DISTINCT lit.pubMedIdentifier)\
                      FROM ReactionlikeEvent_2_regulatedBy rl_rb \
                      INNER JOIN DatabaseObject dbobj_obj \
                      ON dbobj_obj.DB_ID=rl_rb.DB_ID \
                      INNER JOIN StableIdentifier si_obj \
                      ON dbobj_obj.stableIdentifier=si_obj.DB_ID \
                      INNER JOIN DatabaseObject dbobj_reg \
                      ON dbobj_reg.DB_ID=rl_rb.regulatedBy \
                      INNER JOIN StableIdentifier si_reg \
                      ON dbobj_reg.stableIdentifier=si_reg.DB_ID \
                      INNER JOIN Regulation reg \
                      ON reg.DB_ID=rl_rb.regulatedBy \
                      INNER JOIN DatabaseObject dbobj_sub \
                      ON dbobj_sub.DB_ID=reg.regulator \
                      INNER JOIN StableIdentifier si_sub \
                      ON si_sub.DB_ID=dbobj_sub.stableIdentifier \
                      LEFT JOIN Regulation_2_summation reg_sum \
                      ON reg_sum.DB_ID=dbobj_reg.DB_ID \
                      LEFT JOIN Summation sum_fr_r \
                      ON sum_fr_r.DB_ID=reg_sum.summation \
                      LEFT JOIN Summation_2_literatureReference sum_lit \
                      ON sum_fr_r.DB_ID=sum_lit.DB_ID \
                      LEFT JOIN LiteratureReference lit \
                      ON lit.DB_ID=sum_lit.literatureReference \
                      GROUP BY si_sub.identifier, si_obj.identifier, si_reg.identifier"
    if test:
        regulation_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for result in run_sql(regulation_sql, connection):
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[0])
        object_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[3])
        regulated_by_class = result[2]
        regulate_node = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[1])
        if subject_id is None or object_id is None or regulate_node is None:
            continue
        regulation_to_edge_label = {'PositiveRegulation': 'positively_regulates',
                                    'NegativeRegulation': 'negatively_regulates',
                                    'PositiveGeneExpressionRegulation': 'positively_regulates_gene_expression',
                                    'NegativeGeneExpressionRegulation': 'negatively_regulates_gene_expression',
                                    'Requirement': 'requires'}
        predicate = regulation_to_edge_label[regulated_by_class]
        publications = result[5]
        edge = format_edge(subject_id, object_id, predicate)
        if publications is not None:
            publications = str(publications)
            publication_author_dict = dict()
            for publication in publications.split(','):
                citation_list = get_author_of_PMID(publication, connection)
                et_al = ""
                if citation_list[2] > 2:
                    et_al += "et al "
                elif citation_list[2] == 2:
                    et_al += "& " + citation_list[3] + " "
                citation_string = citation_list[0] + ' ' + et_al + str(citation_list[1])
                publication_author_dict[PMID_PREFIX + ':' + publication] = citation_string
            description = result[4].replace('al.', 'al')
            publications_info = dict()
            for publication in publications.split(','):
                publications_info[PMID_PREFIX + ':' + publication] = {'sentence': description}
            if len(publication_author_dict) > 1:
                for publication in publication_author_dict:
                    publication_sentence = ""
                    citation_string = publication_author_dict[publication]
                    for sentence in description.split('. '):
                        if citation_string in sentence:
                            publication_sentence += sentence + "."
                    if len(publication_sentence) > 0:
                        publications_info[publication]['sentence'] = publication_sentence
            edge['publications'] = [PMID_PREFIX + ':' + publication for publication in publications.split(',')]
            edge['publications_info'] = publications_info
        edges.append(edge)

    return edges


def get_physical_entity_characteristics(connection, test):
    edges = []
    sql = "SELECT si.identifier, eo.identifier \
           FROM PhysicalEntity_2_disease pe_dis \
           INNER JOIN DatabaseObject dbobj \
           ON dbobj.DB_ID=pe_dis.DB_ID \
           INNER JOIN StableIdentifier si \
           ON si.DB_ID=dbobj.stableIdentifier \
           INNER JOIN ExternalOntology eo \
           ON eo.DB_ID=pe_dis.disease"
    if test:
        sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for ev_dis in run_sql(sql, connection):
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + ev_dis[0])
        if subject_id is None:
            continue
        object_id = kg2_util.CURIE_PREFIX_DOID + ':' + ev_dis[1]
        predicate = 'linked_to_disease'
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    compartment_sql = "SELECT si.identifier, go.accession \
                       FROM Event_2_compartment ec \
                       INNER JOIN Compartment c \
                       ON c.DB_ID=ec.compartment \
                       INNER JOIN GO_CellularComponent_2_instanceOf g \
                       ON g.instanceOf=c.DB_ID \
                       INNER JOIN GO_CellularComponent go \
                       ON go.DB_ID=g.instanceOf \
                       INNER JOIN DatabaseObject dbobj \
                       ON ec.DB_ID=dbobj.DB_ID \
                       INNER JOIN StableIdentifier si \
                       ON si.DB_ID=dbobj.stableIdentifier"
    if test:
        compartment_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    compartment_results = run_sql(compartment_sql, connection)
    for compartment_ev in compartment_results:
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + compartment_ev[0])
        if subject_id is None:
            continue
        object_id = kg2_util.CURIE_PREFIX_GO + ':' + compartment_ev[1]
        predicate = 'in_location'
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    return edges


def get_equivalencies(connection, test):
    edges = []
    sql = "SELECT go.accession, si.identifier \
           FROM Event event \
           INNER JOIN DatabaseObject dbobj \
           ON event.DB_ID=dbobj.DB_ID \
           INNER JOIN StableIdentifier si \
           ON dbobj.stableIdentifier=si.DB_ID \
           INNER JOIN GO_BiologicalProcess go \
           ON go.DB_ID=event.goBiologicalProcess"
    if test:
        sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    go_eq_results = run_sql(sql, connection)
    for go_eq in go_eq_results:
        go_id = "GO:" + go_eq[0]
        react_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + go_eq[1])
        if react_id is None:
            continue
        predicate = "same_as"
        edge = format_edge(react_id, go_id, predicate)
        edges.append(edge)

    ex_ont_sql = "SELECT rdn.name, di.identifier, si.identifier, rd.accessUrl \
                  FROM PhysicalEntity_2_crossReference pe \
                  INNER JOIN DatabaseObject dbobj \
                  ON dbobj.DB_ID=pe.DB_ID \
                  INNER JOIN StableIdentifier si \
                  ON dbobj.stableIdentifier=si.DB_ID \
                  INNER JOIN DatabaseIdentifier di \
                  ON di.DB_ID=pe.crossReference \
                  INNER JOIN ReferenceDatabase rd \
                  ON rd.DB_ID=di.referenceDatabase \
                  INNER JOIN ReferenceDatabase_2_name rdn \
                  ON rdn.DB_ID=rd.DB_ID"
    if test:
        ex_ont_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    ex_ont_results = run_sql(ex_ont_sql, connection)
    for ex_ont in ex_ont_results:
        try:
            ex_ont_prefix = match_name_to_prefix(ex_ont[0])
            if ex_ont_prefix is None:
                continue
        except KeyError:
            print("The source " + ex_ont[0] + " is not in the name_prefix_dict.")
            continue
        ex_ont_id = ex_ont_prefix + ":" + str(ex_ont[1])
        react_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + ex_ont[2])
        if react_id is None:
            continue
        predicate = 'related_to'
        edge = format_edge(react_id, ex_ont_id, predicate)
        edges.append(edge)

    reference_entity_tables = ['EntityWithAccessionedSequence', 'SimpleEntity', 'Drug']
    for reference_entity_table in reference_entity_tables:
        sql = f"SELECT si_sub.identifier, re.identifier, dbobj_obj._displayName \
                FROM {reference_entity_table} ewas \
                INNER JOIN DatabaseObject dbobj_sub \
                ON dbobj_sub.DB_ID=ewas.DB_ID \
                INNER JOIN StableIdentifier si_sub \
                ON si_sub.DB_ID=dbobj_sub.stableIdentifier \
                INNER JOIN ReferenceEntity re \
                ON re.DB_ID=ewas.referenceEntity \
                INNER JOIN DatabaseObject dbobj_obj \
                ON dbobj_obj.DB_ID=re.referenceDatabase"
        if test:
            sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
        for result in run_sql(sql, connection):
            subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[0])
            if subject_id is None:
                continue
            try:
                obj_prefix = match_name_to_prefix(result[2])
                if obj_prefix is None:
                    continue
            except KeyError:
                print("The source " + result[2] + " is not in the name_prefix_dict")
                continue
            object_id = obj_prefix + ':' + result[1]
            predicate = 'same_as'
            edge = format_edge(subject_id, object_id, predicate)
            edges.append(edge)

    return edges


def get_elements_of_complex(connection, test):
    edges = []
    sql = "SELECT si.identifier, si2.identifier \
           FROM Complex_2_hasComponent complex \
           INNER JOIN DatabaseObject dbobj \
           ON dbobj.DB_ID=complex.DB_ID \
           INNER JOIN StableIdentifier si \
           ON si.DB_ID=dbobj.stableIdentifier \
           INNER JOIN DatabaseObject dbobj2 \
           ON dbobj2.DB_ID=complex.hasComponent \
           INNER JOIN StableIdentifier si2 \
           ON si2.DB_ID=dbobj2.stableIdentifier"
    if test:
        sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    complex_results = run_sql(sql, connection)
    for com_elm in complex_results:
        complex_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + com_elm[0])
        element_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + com_elm[1])
        if complex_id is None or element_id is None:
            continue
        predicate = 'has_element'
        edge = format_edge(complex_id, element_id, predicate)
        edges.append(edge)
    return edges


def get_members_of_set(connection, test):
    edges = []
    sql = "SELECT si_sub.identifier, si_obj.identifier \
           FROM EntitySet_2_hasMember es_hm \
           INNER JOIN DatabaseObject dbobj_sub \
           ON dbobj_sub.DB_ID=es_hm.DB_ID \
           INNER JOIN StableIdentifier si_sub \
           ON si_sub.DB_ID=dbobj_sub.stableIdentifier \
           INNER JOIN DatabaseObject dbobj_obj \
           ON dbobj_obj.DB_ID=es_hm.hasMember \
           INNER JOIN StableIdentifier si_obj \
           ON si_obj.DB_ID=dbobj_obj.stableIdentifier"
    if test:
        sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for result in run_sql(sql, connection):
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[0])
        object_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_member"
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)
    return edges


def get_species(connection, test):
    edges = []
    to_species_tables = ['Event_2_species',
                         'Polymer_2_species',
                         'Complex_2_species',
                         'EntitySet_2_species']
    for to_species_table in to_species_tables:
        sql = f"SELECT si_sub.identifier, dbobj_obj._displayName \
                FROM {to_species_table} sp \
                INNER JOIN DatabaseObject dbobj_obj \
                ON dbobj_obj.DB_ID=sp.species \
                INNER JOIN DatabaseObject dbobj_sub \
                ON dbobj_sub.DB_ID=sp.DB_ID \
                INNER JOIN StableIdentifier si_sub \
                ON si_sub.DB_ID=dbobj_sub.stableIdentifier"
        if test:
            sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
        for species in run_sql(sql, connection):
            subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME +
                                                 ':' + species[0])
            if subject_id is None:
                continue
            try:
                object_id = match_species_to_id(species[1])
                if object_id is None:
                    continue
            except KeyError:
                print("The species " + species[1] + " is not in the species_dict.")
                continue
            predicate = 'in_species'
            edge = format_edge(subject_id, object_id, predicate)
            edges.append(edge)

    return edges


def get_edges(connection, test):
    edges = []
    for edge in get_reaction_inputs_and_outputs(connection, test):
        edges.append(edge)
    for edge in get_pathway_events(connection, test):
        edges.append(edge)
    for edge in get_equivalencies(connection, test):
        edges.append(edge)
    for edge in get_elements_of_complex(connection, test):
        edges.append(edge)
    for edge in get_event_characteristics(connection, test):
        edges.append(edge)
    for edge in get_physical_entity_characteristics(connection, test):
        edges.append(edge)
    for edge in get_members_of_set(connection, test):
        edges.append(edge)
    for edge in get_species(connection, test):
        edges.append(edge)
    return edges


if __name__ == '__main__':
    args = get_args()

    connection = pymysql.connect(user="root", password="1337", db="reactome")

    run_sql("SET SESSION group_concat_max_len=35000", connection)
    run_sql("SET SESSION sort_buffer_size=256000000", connection)
    
    nodes = get_nodes(connection, args.test)
    edges = get_edges(connection, args.test)

    graph = {'nodes': nodes,
             'edges': edges}

    kg2_util.save_json(graph, args.outputFile, args.test)
