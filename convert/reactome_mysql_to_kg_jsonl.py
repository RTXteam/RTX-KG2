#!/usr/bin/env python3
''' reactome_mysql_to_kg_json.py: Extracts a KG2 JSON file from the
    Reactome MySQL Database

    Usage: reactome_mysql_to_kg_json.py [--test] <mysqlConfigFile> <mysqlDBName> 
                                                 <outputNodesFile.json> <outputEdgesFile.json>
'''

import pymysql
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


REACTOME_BASE_IRI = kg2_util.BASE_URL_REACTOME
REACTOME_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
                                + ":reactome"
REACTOME_RELATION_CURIE_PREFIX = kg2_util.CURIE_PREFIX_REACTOME
REACTOME_KB_IRI = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + 'reactome'

NCBI_TAXON_PREFIX = kg2_util.CURIE_PREFIX_NCBI_TAXON
ENSEMBL_PREFIX = kg2_util.CURIE_PREFIX_ENSEMBL
PMID_PREFIX = kg2_util.CURIE_PREFIX_PMID

BIOLOGICAL_PROCESS = kg2_util.BIOLINK_CATEGORY_BIOLOGICAL_PROCESS
SMALL_MOLECULE = kg2_util.BIOLINK_CATEGORY_SMALL_MOLECULE
MOLECULAR_ACTIVITY = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ACTIVITY
MOLECULAR_ENTITY = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ENTITY
BIOLOGICAL_ENTITY = kg2_util.BIOLINK_CATEGORY_BIOLOGICAL_ENTITY
PATHWAY = kg2_util.BIOLINK_CATEGORY_PATHWAY
PROTEIN = kg2_util.BIOLINK_CATEGORY_PROTEIN
PATHOLOGICAL_PROCESS = kg2_util.BIOLINK_CATEGORY_PATHOLOGICAL_PROCESS
CHEMICAL_ENTITY = kg2_util.BIOLINK_CATEGORY_CHEMICAL_ENTITY

ROW_LIMIT_TEST_MODE = 1000


def get_args():
    arg_parser = argparse.ArgumentParser(description='reactome_mysql_to_kg_json.py: \
                                         builds a KG2 JSON representation of \
                                         Reactome')
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('mysqlConfigFile', type=str)
    arg_parser.add_argument('mysqlDBName', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
    if predicate_label == kg2_util.EDGE_LABEL_BIOLINK_SAME_AS:
        return kg2_util.make_edge_biolink(subject_id,
                                          object_id,
                                          predicate_label,
                                          REACTOME_KB_CURIE_ID,
                                          None)
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
                        'COMPOUND': kg2_util.CURIE_PREFIX_KEGG_COMPOUND,
                        'PubChem Compound': None,
                        'GenBank': None,
                        'KEGG Glycan': kg2_util.CURIE_PREFIX_KEGG_GLYCAN,
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
                        'miRBase': kg2_util.CURIE_PREFIX_MIRBASE,
                        'PRF': None,
                        'IUPHAR': None,
                        'PubChem': None,
                        'PubChem SID': None,
                        'Guide to Pharmacology': kg2_util.CURIE_PREFIX_GTPI,
                        'NCIthesaurus': kg2_util.CURIE_PREFIX_NCIT}

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


def match_reactome_category_to_biolink(reactome_category: str,
                                       reference_class: str):
    category_dict = {'Reaction': BIOLOGICAL_PROCESS,
                     'OtherEntity': BIOLOGICAL_ENTITY,
                     'SimpleEntity': BIOLOGICAL_ENTITY,
                     'GenomeEncodedEntity': BIOLOGICAL_ENTITY,
                     'BlackBoxEvent': BIOLOGICAL_PROCESS,
                     'DefinedSet': BIOLOGICAL_ENTITY,
                     'ChemicalDrug': SMALL_MOLECULE,
                     'Complex': BIOLOGICAL_ENTITY,
                     'FailedReaction': PATHOLOGICAL_PROCESS,
                     'Pathway': kg2_util.BIOLINK_CATEGORY_PATHWAY,
                     'Depolymerisation': BIOLOGICAL_PROCESS,
                     'PositiveRegulation': BIOLOGICAL_PROCESS,
                     'NegativeGeneExpressionRegulation': BIOLOGICAL_PROCESS,
                     'NegativeRegulation': BIOLOGICAL_PROCESS,
                     'CandidateSet': BIOLOGICAL_ENTITY,
                     'Requirement': BIOLOGICAL_PROCESS,
                     'ProteinDrug': CHEMICAL_ENTITY,
                     'Polymer': BIOLOGICAL_ENTITY,
                     'EntityWithAccessionedSequence': BIOLOGICAL_ENTITY,
                     'Polymerisation': BIOLOGICAL_PROCESS,
                     'PositiveGeneExpressionRegulation': BIOLOGICAL_PROCESS}

    biolink_category = category_dict[reactome_category]
    if reactome_category == 'EntityWithAccessionedSequence' and reference_class is not None \
       and reference_class == 'ReferenceGeneProduct':
        biolink_category = PROTEIN
        
    return biolink_category


def only_include_certain_species(reactome_id: str):
    # This code checks if a Reactome ID's species is in
    # the list of species desired in KG2 (the 'include_species'
    # list) by splitting the ID into its species component and
    # comparing it to the list. If it is not in the list,
    # None is returned to signal that the ID is of a species
    # that should not be included.

    # HSA: homo sapiens
    # ALL: all species, including homo sapiens (many entities have this)
    include_species = ['HSA', 'ALL']
    if reactome_id.split('-')[1] in include_species:
        return reactome_id
    return None


def get_nodes(connection, nodes_output, test):
    # This MySQL query uses the stableidentifier table,
    # which holds all of the node IDs for Reactome, as
    # its left most table. Then, it inner joins the
    # databaseobject table, which contains identifiers (called
    # the DB_ID) that can be linked to all of the other tables,
    # which the stableidentifier can not be. Then, the
    # various node properties are added on using left joins.
    # In general, there are three types of nodes: events (which
    # includes pathways and reactions), physical entities (which
    # includes polymers, drugs, and complexes), and regulations.
    # The regulations are nodes that stand in for edges. As a result,
    # they are filtered out in category assignment. However, we retreive
    # them in this statement in case they are wanted later.
    # Each general node type has different table linkage to
    # retreive its publications and description. As a result,
    # this statement uses left joins, so that each node gets the
    # publications and description that fits it. However,
    # nodes can have more than one publication, so we have
    # to use group by and group concat to ensure that each node
    # is only included in the knowledge graph once and all of its
    # publications are on it. In addition, this statement includes
    # distinct when using group concat, because we don't need repeats
    # of the various fields, it is merely a way to collapse all iterations
    # of the node (because each publication creates a new row of the node)
    # into one.
    nodes_sql = "SELECT si.identifier as node_id, \
                 GROUP_CONCAT(DISTINCT dbobj._displayName) as node_name, \
                 GROUP_CONCAT(DISTINCT dbobj._timestamp) as update_date, \
                 GROUP_CONCAT(DISTINCT dbobj._class) as category, \
                 GROUP_CONCAT(DISTINCT lit_fr_e.pubMedIdentifier) as pmid_event, \
                 GROUP_CONCAT(DISTINCT lit_fr_p.pubMedIdentifier) as pmid_entity, \
                 GROUP_CONCAT(DISTINCT sum_fr_e.text) as description_event, \
                 GROUP_CONCAT(DISTINCT sum_fr_p.text) as description_entity, \
                 GROUP_CONCAT(DISTINCT sum_fr_r.text) as description_regulation, \
                 GROUP_CONCAT(DISTINCT ins_ed.dateTime) as created_date, \
                 GROUP_CONCAT(DISTINCT ewas.referenceEntity_class) as refclass  \
                 FROM stableidentifier si \
                 INNER JOIN databaseobject dbobj \
                 ON si.DB_ID=dbobj.stableidentifier \
                 LEFT JOIN instanceedit ins_ed \
                 ON dbobj.created=ins_ed.DB_ID \
                 LEFT JOIN event_2_literaturereference ev_lit \
                 ON dbobj.DB_ID=ev_lit.DB_ID \
                 LEFT JOIN literaturereference lit_fr_e \
                 ON lit_fr_e.DB_ID=ev_lit.literaturereference \
                 LEFT JOIN event_2_summation ev_sum \
                 ON ev_sum.DB_ID=dbobj.DB_ID \
                 LEFT JOIN summation sum_fr_e \
                 ON ev_sum.summation=sum_fr_e.DB_ID \
                 LEFT JOIN physicalentity_2_literaturereference pe_lit \
                 ON dbobj.DB_ID=pe_lit.DB_ID \
                 LEFT JOIN literaturereference lit_fr_p \
                 ON lit_fr_p.DB_ID=pe_lit.literaturereference \
                 LEFT JOIN physicalentity_2_summation pe_sum \
                 ON dbobj.DB_ID=pe_sum.DB_ID \
                 LEFT JOIN summation sum_fr_p \
                 ON pe_sum.summation = sum_fr_p.DB_ID \
                 LEFT JOIN event_2_summation reg_sum \
                 on reg_sum.DB_ID=dbobj.DB_ID \
                 LEFT JOIN summation sum_fr_r \
                 ON sum_fr_r.DB_ID=reg_sum.summation \
                 LEFT JOIN entitywithaccessionedsequence ewas \
                 ON dbobj.DB_ID = ewas.DB_ID \
                 GROUP BY si.identifier"
    if test:
        nodes_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for result in run_sql(nodes_sql, connection):
        (reactome_id,
         name,
         update_date,
         reactome_category,
         publications_event, 
         publications_phy_ent,
         description_event,
         description_phy_ent,
         descrption_reg,
         created_date,
         reference_class) = result
        node_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + reactome_id)
        if node_id is None:
            continue
        update_date = str(update_date)
        try:
            category_label = match_reactome_category_to_biolink(reactome_category, reference_class)
            if category_label is None:
                continue
        except KeyError:
            print("Category for \"", reactome_category, "\" not in match_reactome_category_to_biolink")
            continue
        iri = REACTOME_BASE_IRI + result[0]
        
        # Check to see which general type of node it is and generate the
        # publications list using that
        if publications_event is not None:
            publications = publications_event.split(',')
            publications = [PMID_PREFIX + ':' + publication for publication in publications]
        elif publications_phy_ent is not None:
            publications = publications_phy_ent.split(',')
            publications = [PMID_PREFIX + ':' + publication for publication in publications]
        else:
            publications = []

        # Check to see which general type of node it is and assign the node's
        # description based on that
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
        nodes_output.write(node)


def get_reaction_inputs_and_outputs(connection, edges_output, test):
    # This MySQL statement uses the reactionlikeevent_2_input
    # table to gather the DB_ID's for each reaction and its inputs.
    # Then, it retreives the Reactome ID for both the reaction and
    # the input using the stableidentifier table.
    in_sql = "SELECT DISTINCT si_sub.identifier, si_obj.identifier \
              FROM reactionlikeevent_2_input reaction \
              INNER JOIN databaseobject dbobj_sub \
              ON reaction.DB_ID=dbobj_sub.DB_ID \
              INNER JOIN stableidentifier si_sub \
              ON si_sub.DB_ID=dbobj_sub.stableidentifier \
              INNER JOIN databaseobject dbobj_obj \
              ON dbobj_obj.DB_ID=reaction.input \
              INNER JOIN stableidentifier si_obj \
              ON si_obj.DB_ID=dbobj_obj.stableidentifier"
    if test:
        in_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    in_results = run_sql(in_sql, connection)
    for input in in_results:
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + input[0])
        object_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + input[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_input"
        edge = format_edge(subject_id, object_id, predicate)
        edges_output.write(edge)

    # This MySQL statement uses the reactionlikeevent_2_output
    # table to gather the DB_ID's for each reaction and its outputs.
    # Then, it retreives the Reactome ID for both the reaction and
    # the output using the stableidentifier table.
    out_sql = "SELECT DISTINCT si_sub.identifier, si_obj.identifier \
               FROM reactionlikeevent_2_output reaction \
               INNER JOIN databaseobject dbobj_sub \
               ON reaction.DB_ID=dbobj_sub.DB_ID \
               INNER JOIN stableidentifier si_sub \
               ON si_sub.DB_ID=dbobj_sub.stableidentifier \
               INNER JOIN databaseobject dbobj_obj \
               ON dbobj_obj.DB_ID=reaction.output \
               INNER JOIN stableidentifier si_obj \
               ON si_obj.DB_ID=dbobj_obj.stableidentifier"
    if test:
        out_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    out_results = run_sql(out_sql, connection)
    for out in out_results:
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + out[0])
        object_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + out[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_output"
        edge = format_edge(subject_id, object_id, predicate)
        edges_output.write(edge)


def get_pathway_events(connection, edges_output, test):
    # This MySQL query uses the pathway_2_hasevent
    # table to connect pathways to their events (reactions,
    # black box events, polymerisation, etc). It takes the DB_ID's
    # of both the pathway and the event and connects each to its
    # Reactome identifier using the stableidentifier table.
    event_sql = "SELECT DISTINCT si_sub.identifier, si_obj.identifier \
                 FROM pathway_2_hasevent pathway \
                 INNER JOIN databaseobject dbobj_sub \
                 ON pathway.DB_ID=dbobj_sub.DB_ID \
                 INNER JOIN stableidentifier si_sub \
                 ON si_sub.DB_ID=dbobj_sub.stableidentifier \
                 INNER JOIN databaseobject dbobj_obj \
                 ON dbobj_obj.DB_ID=pathway.hasEvent \
                 INNER JOIN stableidentifier si_obj \
                 ON si_obj.DB_ID=dbobj_obj.stableidentifier"
    if test:
        event_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for has_event in run_sql(event_sql, connection):
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + has_event[0])
        object_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + has_event[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_event"
        edge = format_edge(subject_id, object_id, predicate)
        edges_output.write(edge)


def get_author_of_PMID(pmid: str, connection):
    # This MySQL query gathers the necessary information about
    # a PubMed ID to construct its citation (to match with a
    # claim). This includes the last name of the first author,
    # the year published, the number of authors (to determine
    # structure), and the last name of the second author, if relevant.
    sql = "SELECT per.surname, lr.year \
           FROM literaturereference lr \
           INNER JOIN publication_2_author pub_auth \
           ON pub_auth.DB_ID=lr.DB_ID \
           INNER JOIN person per \
           ON per.DB_ID=pub_auth.author \
           WHERE lr.pubMedIdentifier=" + str(pmid)
    results = run_sql(sql, connection)
    try:
        second_result = results[1][0].lower().title()
    except IndexError:
        second_result = None
    return [results[0][0].lower().title(), results[0][1], len(results), second_result]


def get_event_characteristics(connection, edges_output, test):
    # This MySQL query uses the event_2_disease table to
    # connect events to diseases they are related to. It takes
    # the DB_ID of both the disease and the event from that table,
    # then connects the event's DB_ID to its Reactome ID within
    # stableidentifier. The disease's DB_ID is connected to
    # externalontology to return its DOID ID.
    event_to_disease_sql = "SELECT si.identifier, eo.identifier \
                            FROM event_2_disease ev_dis \
                            INNER JOIN databaseobject dbobj_sub \
                            ON dbobj_sub.DB_ID=ev_dis.DB_ID \
                            INNER JOIN stableidentifier si \
                            ON si.DB_ID=dbobj_sub.stableidentifier \
                            INNER JOIN externalontology eo \
                            ON eo.DB_ID=ev_dis.disease"
    if test:
        event_to_disease_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for ev_dis in run_sql(event_to_disease_sql, connection):
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + ev_dis[0])
        if subject_id is None:
            continue
        object_id = kg2_util.CURIE_PREFIX_DOID + ':' + ev_dis[1]
        predicate = 'linked_to_disease'
        edge = format_edge(subject_id, object_id, predicate)
        edges_output.write(edge)

    # This MySQL query uses the event_2_compartment table to
    # connect events to the parts of the cell they occur in.
    # The event's Reactome ID is retreived from the stableidentifier
    # table and the compartment's GO ID is retrieved from the
    # go_cellularcomponent table.

    # This table doesn't exist in the latest version of Reactome.
    # compartment_sql = "SELECT si_sub.identifier, go.accession \
    #                    FROM event_2_compartment ev_comp \
    #                    INNER JOIN compartment compart \
    #                    ON compart.DB_ID=ev_comp.compartment \
    #                    INNER JOIN go_cellularcomponent_2_instanceof go_io \
    #                    ON go_io.instanceOf=compart.DB_ID \
    #                    INNER JOIN go_cellularcomponent go \
    #                    ON go.DB_ID=go_io.instanceOf \
    #                    INNER JOIN databaseobject dbobj_sub \
    #                    ON ec.DB_ID=dbobj_sub.DB_ID \
    #                    INNER JOIN stableidentifier si_sub \
    #                    ON si_sub.DB_ID=dbobj_sub.stableidentifier"
    # if test:
    #     compartment_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    # compartment_results = run_sql(compartment_sql, connection)
    # for compartment_ev in compartment_results:
    #     subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + compartment_ev[0])
    #     if subject_id is None:
    #         continue
    #     object_id = kg2_util.CURIE_PREFIX_GO + ':' + compartment_ev[1]
    #     predicate = 'in_compartment'
    #     edge = format_edge(subject_id, object_id, predicate)
    #     edges_output.write(edge)

    # This MySQL query uses the reactionlikeevent_2_regulatedby
    # table to link Reactionlike Events (Reaction, BlackBoxEvent, etc)
    # to things that regulate them. This uses the regulation nodes
    # (Requirement, PositiveRegulation, Negative regulation,
    # PositiveGeneExpressionRegulation, and NegativeGeneExpressionRegulation)
    # to form these edges, because the nodes are better represented as edges.
    # It applies those node's description and the PMIDs linked to that
    # description to its edge counterpart's publications info field. Since on
    # edge can have multiple PMIDs, the query uses GROUP_CONCAT and DISTINCT
    # to ensure that each edge is not represented more than once.
    # To retreive the PMIDs, this query uses event_2_summation
    # to connect the regulation to its description. Then, it uses
    # summation_2_literaturereference to connect that description
    # to its PMIDs. Finally, the query uses the literaturereference table
    # to get the PubMed identifiers for the edge.
    regulation_sql = "SELECT si_sub.identifier, \
                      si_reg.identifier, \
                      GROUP_CONCAT(DISTINCT rl_rb.regulatedBy_class), \
                      si_obj.identifier, \
                      GROUP_CONCAT(DISTINCT sum_fr_r.text), \
                      GROUP_CONCAT(DISTINCT lit.pubMedIdentifier)\
                      FROM reactionlikeevent_2_regulatedby rl_rb \
                      INNER JOIN databaseobject dbobj_obj \
                      ON dbobj_obj.DB_ID=rl_rb.DB_ID \
                      INNER JOIN stableidentifier si_obj \
                      ON dbobj_obj.stableidentifier=si_obj.DB_ID \
                      INNER JOIN databaseobject dbobj_reg \
                      ON dbobj_reg.DB_ID=rl_rb.regulatedBy \
                      INNER JOIN stableidentifier si_reg \
                      ON dbobj_reg.stableidentifier=si_reg.DB_ID \
                      INNER JOIN regulation reg \
                      ON reg.DB_ID=rl_rb.regulatedBy \
                      INNER JOIN databaseobject dbobj_sub \
                      ON dbobj_sub.DB_ID=reg.regulator \
                      INNER JOIN stableidentifier si_sub \
                      ON si_sub.DB_ID=dbobj_sub.stableidentifier \
                      LEFT JOIN event_2_summation reg_sum \
                      ON reg_sum.DB_ID=rl_rb.DB_ID \
                      LEFT JOIN summation sum_fr_r \
                      ON sum_fr_r.DB_ID=reg_sum.summation \
                      LEFT JOIN summation_2_literaturereference sum_lit \
                      ON sum_fr_r.DB_ID=sum_lit.DB_ID \
                      LEFT JOIN literaturereference lit \
                      ON lit.DB_ID=sum_lit.literaturereference \
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
                                    'Requirement': 'is_requirement_for'}
        predicate = regulation_to_edge_label[regulated_by_class]
        publications = result[5]
        edge = format_edge(subject_id, object_id, predicate)

        # This section adds a non null publications_info and publications
        # field to the edge if publications exist for the node. Then,
        # it uses get_author_of_PMID to get the relevant information about
        # the PMID to create a citation for it. In an attempt to divide the
        # description into sentences as best as possible, instances of
        # "et al." are replaced with "et al", to allow for the possibility
        # of splitting on '.' to get sentences. Then, the publications_info
        # dictionary is prepared with every PMID getting the entire
        # description (in case that PMID's citation is not in it). Next, the
        # different sentences are iterated over and if a PMID's citation
        # is found in that sentences, it's sentence field in the
        # publications_info dictionary becomes that sentence.
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
            description = result[4].replace('et al.', 'et al')
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

        edges_output.write(edge)


def get_physical_entity_characteristics(connection, edges_output, test):
    # This MySQL query uses the physicalentity_2_disease table to
    # connect physical entities to diseases they are related to. It takes
    # the DB_ID of both the disease and the entity from that table,
    # then connects the entity's DB_ID to its Reactome ID within
    # stableidentifier. The disease's DB_ID is connected to
    # externalontology to return its DOID ID.
    entity_to_disease_sql = "SELECT si.identifier, eo.identifier \
                             FROM physicalentity_2_disease pe_dis \
                             INNER JOIN databaseobject dbobj \
                             ON dbobj.DB_ID=pe_dis.DB_ID \
                             INNER JOIN stableidentifier si \
                             ON si.DB_ID=dbobj.stableidentifier \
                             INNER JOIN externalontology eo \
                             ON eo.DB_ID=pe_dis.disease"
    if test:
        entity_to_disease_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for pe_dis in run_sql(entity_to_disease_sql, connection):
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + pe_dis[0])
        if subject_id is None:
            continue
        object_id = kg2_util.CURIE_PREFIX_DOID + ':' + pe_dis[1]
        predicate = 'linked_to_disease'
        edge = format_edge(subject_id, object_id, predicate)
        edges_output.write(edge)

    # This MySQL query uses the physicalentity_2_compartment table to
    # connect physical entities to the parts of the cell they occur in.
    # The entity's Reactome ID is retreived from the stableidentifier
    # table and the compartment's GO ID is retrieved from the
    # go_cellularcomponent table.

    # This table doesn't exist in the latest version of Reactome.
    # compartment_sql = "SELECT si.identifier, go.accession \
    #                    FROM physicalentity_2_compartment pe_c \
    #                    INNER JOIN compartment c \
    #                    ON c.DB_ID=pe_c.compartment \
    #                    INNER JOIN go_cellularcomponent_2_instanceof g \
    #                    ON g.instanceOf=c.DB_ID \
    #                    INNER JOIN go_cellularcomponent go \
    #                    ON go.DB_ID=g.instanceOf \
    #                    INNER JOIN databaseobject dbobj \
    #                    ON pe_c.DB_ID=dbobj.DB_ID \
    #                    INNER JOIN stableidentifier si \
    #                    ON si.DB_ID=dbobj.stableidentifier"
    # if test:
    #     compartment_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    # for compartment_pe_c in run_sql(compartment_sql, connection):
    #     subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + compartment_pe_c[0])
    #     if subject_id is None:
    #         continue
    #     object_id = kg2_util.CURIE_PREFIX_GO + ':' + compartment_pe_c[1]
    #     predicate = 'in_compartment'
    #     edge = format_edge(subject_id, object_id, predicate)
    #     edges_output.write(edge)


def get_equivalencies(connection, edges_output, test):
    # This MySQL query uses the event table to match
    # Reactome IDs (from the stableidentifier table)
    # with their equivalent GO Biological Processes
    # using the GO_Biological_Process table.
    go_eq_sql = "SELECT go.accession, si.identifier \
                 FROM event event \
                 INNER JOIN databaseobject dbobj \
                 ON event.DB_ID=dbobj.DB_ID \
                 INNER JOIN stableidentifier si \
                 ON dbobj.stableidentifier=si.DB_ID \
                 INNER JOIN go_biologicalprocess go \
                 ON go.DB_ID=event.goBiologicalProcess"
    if test:
        go_eq_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for go_eq in run_sql(go_eq_sql, connection):
        go_id = "GO:" + go_eq[0]
        react_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + go_eq[1])
        if react_id is None:
            continue
        predicate = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
        edge = format_edge(react_id, go_id, predicate)
        edges_output.write(edge)

    # This MySQL query uses the physicalentity_2_crossreference
    # table to generate related_to edges from Reactome IDs
    # (which are discovered using the stableidentifier table)
    # to IDs from various other sources. Some are very close
    # matches and others are very loose, so we use the related_to
    # predicate to accommodate this.
    ex_ont_sql = "SELECT rd_n.name, di.identifier, si.identifier, rd.accessUrl \
                  FROM physicalentity_2_crossreference pe \
                  INNER JOIN databaseobject dbobj \
                  ON dbobj.DB_ID=pe.DB_ID \
                  INNER JOIN stableidentifier si \
                  ON dbobj.stableidentifier=si.DB_ID \
                  INNER JOIN databaseidentifier di \
                  ON di.DB_ID=pe.crossReference \
                  INNER JOIN referencedatabase rd \
                  ON rd.DB_ID=di.referenceDatabase \
                  INNER JOIN referencedatabase_2_name rd_n \
                  ON rd_n.DB_ID=rd.DB_ID"
    if test:
        ex_ont_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    ex_ont_results = run_sql(ex_ont_sql, connection)
    for ex_ont in ex_ont_results:
        try:
            ex_ont_prefix = match_name_to_prefix(ex_ont[0])
            if ex_ont_prefix is None:
                continue
        except KeyError:
            print("The source \"" + ex_ont[0] + "\" is not in the name_prefix_dict.")
            continue
        ex_ont_id = ex_ont_prefix + ":" + str(ex_ont[1])
        react_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + ex_ont[2])
        if react_id is None:
            continue
        predicate = 'related_to'
        edge = format_edge(react_id, ex_ont_id, predicate)
        edges_output.write(edge)

    # This group of MySQL queries iterates over a series of tables
    # (the 'reference_entity_tables') that have a 'referenceEntity'
    # column. This connects the entity's Reactome ID (retreived
    # from the stableidentifier table) with another source's ID.
    # There is only one mapping per entity (as far as I know)
    # and they are precise, so we use the 'same_as' predicate.
    reference_entity_tables = ['entitywithaccessionedsequence',
                               'simpleentity',
                               'drug']
    for reference_entity_table in reference_entity_tables:
        reference_entity_sql = f"SELECT si_sub.identifier, re.identifier, \
                                 dbobj_obj._displayName \
                                 FROM {reference_entity_table} ewas \
                                 INNER JOIN databaseobject dbobj_sub \
                                 ON dbobj_sub.DB_ID=ewas.DB_ID \
                                 INNER JOIN stableidentifier si_sub \
                                 ON si_sub.DB_ID=dbobj_sub.stableidentifier \
                                 INNER JOIN referenceentity re \
                                 ON re.DB_ID=ewas.referenceEntity \
                                 INNER JOIN databaseobject dbobj_obj \
                                 ON dbobj_obj.DB_ID=re.referenceDatabase"
        if test:
            reference_entity_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
        for result in run_sql(reference_entity_sql, connection):
            subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[0])
            if subject_id is None:
                continue
            try:
                obj_prefix = match_name_to_prefix(result[2])
                if obj_prefix is None:
                    continue
            except KeyError:
                print("The source \"" + result[2] + "\" is not in the name_prefix_dict")
                continue
            object_id = obj_prefix + ':' + result[1]
            predicate = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
            edge = format_edge(subject_id, object_id, predicate)
            edges_output.write(edge)


def get_elements_of_complex(connection, edges_output, test):
    # This MySQL query uses the complex_2_hascomponent
    # table to get edges between Reactome complexes and
    # their elements. It uses the stableidentifier table
    # to retreive the Reactome IDs for each, based on
    # their DB_IDs from complex_2_hascomponent.
    complex_elements_sql = "SELECT si.identifier, si2.identifier \
                            FROM complex_2_hascomponent complex \
                            INNER JOIN databaseobject dbobj \
                            ON dbobj.DB_ID=complex.DB_ID \
                            INNER JOIN stableidentifier si \
                            ON si.DB_ID=dbobj.stableidentifier \
                            INNER JOIN databaseobject dbobj2 \
                            ON dbobj2.DB_ID=complex.hasComponent \
                            INNER JOIN stableidentifier si2 \
                            ON si2.DB_ID=dbobj2.stableidentifier"
    if test:
        complex_elements_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for com_elm in run_sql(complex_elements_sql, connection):
        complex_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + com_elm[0])
        element_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + com_elm[1])
        if complex_id is None or element_id is None:
            continue
        predicate = 'has_element'
        edge = format_edge(complex_id, element_id, predicate)
        edges_output.write(edge)


def get_members_of_set(connection, edges_output, test):
    # This MySQL query uses the entityset_2_hasmember
    # table to get edges between Reactome sets and
    # their members. It uses the stableidentifier table
    # to retreive the Reactome IDs for each, based on
    # their DB_IDs from entityset_2_hasmember.
    complex_members_sql = "SELECT si_sub.identifier, si_obj.identifier \
                           FROM entityset_2_hasmember es_hm \
                           INNER JOIN databaseobject dbobj_sub \
                           ON dbobj_sub.DB_ID=es_hm.DB_ID \
                           INNER JOIN stableidentifier si_sub \
                           ON si_sub.DB_ID=dbobj_sub.stableidentifier \
                           INNER JOIN databaseobject dbobj_obj \
                           ON dbobj_obj.DB_ID=es_hm.hasMember \
                           INNER JOIN stableidentifier si_obj \
                           ON si_obj.DB_ID=dbobj_obj.stableidentifier"
    if test:
        complex_members_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for result in run_sql(complex_members_sql, connection):
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[0])
        object_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_member"
        edge = format_edge(subject_id, object_id, predicate)
        edges_output.write(edge)


def get_species(connection, edges_output, test):
    # This MySQL query iterates through a list
    # of tables ('to_species_tables') that contain
    # links between Reactome nodes and the species
    # they are in. It retreives the Reactome ID
    # for the Reactome node and the species name
    # for the species (which is linked to NCBITaxon
    # using match_species_to_id).
    to_species_tables = ['event_2_species',
                         'polymer_2_species',
                         'complex_2_species',
                         'entityset_2_species']
    for to_species_table in to_species_tables:
        species_sql = f"SELECT si_sub.identifier, dbobj_obj._displayName \
                        FROM {to_species_table} sp \
                        INNER JOIN databaseobject dbobj_obj \
                        ON dbobj_obj.DB_ID=sp.species \
                        INNER JOIN databaseobject dbobj_sub \
                        ON dbobj_sub.DB_ID=sp.DB_ID \
                        INNER JOIN stableidentifier si_sub \
                        ON si_sub.DB_ID=dbobj_sub.stableidentifier"
        if test:
            species_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
        for species in run_sql(species_sql, connection):
            subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + species[0])
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
            edges_output.write(edge)


def get_edges(connection, edges_output, test):
    get_reaction_inputs_and_outputs(connection, edges_output, test)

    get_pathway_events(connection, edges_output, test)

    get_equivalencies(connection, edges_output, test)

    get_elements_of_complex(connection, edges_output, test)

    get_event_characteristics(connection, edges_output, test)

    get_physical_entity_characteristics(connection, edges_output, test)

    get_members_of_set(connection, edges_output, test)

    get_species(connection, edges_output, test)


if __name__ == '__main__':
    print("Start time: ", date())
    args = get_args()
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    connection = pymysql.connect(read_default_file=args.mysqlConfigFile, db=args.mysqlDBName)

    run_sql("SET SESSION group_concat_max_len=35000", connection)
    run_sql("SET SESSION sort_buffer_size=256000000", connection)

    get_nodes(connection, nodes_output, test_mode)
    get_edges(connection, edges_output, test_mode)

    [update_date, version_number] = list(run_sql('SELECT releaseDate, releaseNumber FROM _release', connection)[0])

    kp_node = kg2_util.make_node(REACTOME_KB_CURIE_ID,
                                 REACTOME_KB_IRI,
                                 'Reactome v' + str(version_number),
                                 kg2_util.SOURCE_NODE_CATEGORY,
                                 update_date,
                                 REACTOME_KB_CURIE_ID)
    nodes_output.write(kp_node)

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)

    print("Finish time: ", date())
