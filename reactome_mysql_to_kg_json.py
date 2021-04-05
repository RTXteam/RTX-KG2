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
    arg_parser.add_argument('mysqlConfigFile', type=str)
    arg_parser.add_argument('mysqlDBName', type=str)
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
                        'miRBase': kg2_util.CURIE_PREFIX_MIRBASE,
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


def get_nodes(connection, test):
    nodes = []

    # This MySQL query uses the StableIdentifier table,
    # which holds all of the node IDs for Reactome, as
    # its left most table. Then, it inner joins the
    # DatabaseObject table, which contains identifiers (called
    # the DB_ID) that can be linked to all of the other tables,
    # which the StableIdentifier can not be. Then, the
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
                 GROUP_CONCAT(DISTINCT ins_ed.dateTime) as created_date \
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
        nodes_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for result in run_sql(nodes_sql, connection):
        node_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + result[0])
        if node_id is None:
            continue
        name = result[1]
        update_date = str(result[2])
        try:
            category_label = match_reactome_category_to_biolink(result[3])
            if category_label is None:
                continue
        except KeyError:
            print("Category for", result[3], "not in match_reactome_category_to_biolink")
            continue
        publications_event = result[4]
        publications_phy_ent = result[5]
        description_event = result[6]
        description_phy_ent = result[7]
        descrption_reg = result[8]
        iri = REACTOME_BASE_IRI + result[0]
        created_date = result[9]

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
        nodes.append(node)

    return nodes


def get_reaction_inputs_and_outputs(connection, test):
    edges = []

    # This MySQL statement uses the ReactionlikeEvent_2_input
    # table to gather the DB_ID's for each reaction and its inputs.
    # Then, it retreives the Reactome ID for both the reaction and
    # the input using the StableIdentifier table.
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

    # This MySQL statement uses the ReactionlikeEvent_2_output
    # table to gather the DB_ID's for each reaction and its outputs.
    # Then, it retreives the Reactome ID for both the reaction and
    # the output using the StableIdentifier table.
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

    # This MySQL query uses the Pathway_2_hasEvent
    # table to connect pathways to their events (reactions,
    # black box events, polymerisation, etc). It takes the DB_ID's
    # of both the pathway and the event and connects each to its
    # Reactome identifier using the StableIdentifier table.
    event_sql = "SELECT DISTINCT si_sub.identifier, si_obj.identifier \
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
        event_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for has_event in run_sql(event_sql, connection):
        subject_id = only_include_certain_species(has_event[0])
        object_id = only_include_certain_species(has_event[1])
        if subject_id is None or object_id is None:
            continue
        predicate = "has_event"
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    return edges


def get_author_of_PMID(pmid: str, connection):
    # This MySQL query gathers the necessary information about
    # a PubMed ID to construct its citation (to match with a
    # claim). This includes the last name of the first author,
    # the year published, the number of authors (to determine
    # structure), and the last name of the second author, if relevant.
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

    # This MySQL query uses the Event_2_disease table to
    # connect events to diseases they are related to. It takes
    # the DB_ID of both the disease and the event from that table,
    # then connects the event's DB_ID to its Reactome ID within
    # StableIdentifier. The disease's DB_ID is connected to
    # ExternalOntology to return its DOID ID.
    event_to_disease_sql = "SELECT si.identifier, eo.identifier \
                            FROM Event_2_disease ev_dis \
                            INNER JOIN DatabaseObject dbobj_sub \
                            ON dbobj_sub.DB_ID=ev_dis.DB_ID \
                            INNER JOIN StableIdentifier si \
                            ON si.DB_ID=dbobj_sub.stableIdentifier \
                            INNER JOIN ExternalOntology eo \
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
        edges.append(edge)

    # This MySQL query uses the Event_2_compartment table to
    # connect events to the parts of the cell they occur in.
    # The event's Reactome ID is retreived from the StableIdentifier
    # table and the compartment's GO ID is retrieved from the
    # GO_CellularComponent table.
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
        predicate = 'in_compartment'
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    # This MySQL query uses the ReactionlikeEvent_2_regulatedBy
    # table to link Reactionlike Events (Reaction, BlackBoxEvent, etc)
    # to things that regulate them. This uses the Regulation nodes
    # (Requirement, PositiveRegulation, Negative Regulation,
    # PositiveGeneExpressionRegulation, and NegativeGeneExpressionRegulation)
    # to form these edges, because the nodes are better represented as edges.
    # It applies those node's description and the PMIDs linked to that
    # description to its edge counterpart's publications info field. Since on
    # edge can have multiple PMIDs, the query uses GROUP_CONCAT and DISTINCT
    # to ensure that each edge is not represented more than once.
    # To retreive the PMIDs, this query uses Regulation_2_summation
    # to connect the Regulation to its description. Then, it uses
    # Summation_2_literatureReference to connect that description
    # to its PMIDs. Finally, the query uses the LiteratureReference table
    # to get the PubMed identifiers for the edge.
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

        edges.append(edge)

    return edges


def get_physical_entity_characteristics(connection, test):
    edges = []

    # This MySQL query uses the PhysicalEntity_2_disease table to
    # connect physical entities to diseases they are related to. It takes
    # the DB_ID of both the disease and the entity from that table,
    # then connects the entity's DB_ID to its Reactome ID within
    # StableIdentifier. The disease's DB_ID is connected to
    # ExternalOntology to return its DOID ID.
    entity_to_disease_sql = "SELECT si.identifier, eo.identifier \
                             FROM PhysicalEntity_2_disease pe_dis \
                             INNER JOIN DatabaseObject dbobj \
                             ON dbobj.DB_ID=pe_dis.DB_ID \
                             INNER JOIN StableIdentifier si \
                             ON si.DB_ID=dbobj.stableIdentifier \
                             INNER JOIN ExternalOntology eo \
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
        edges.append(edge)

    # This MySQL query uses the PhysicalEntity_2_compartment table to
    # connect physical entities to the parts of the cell they occur in.
    # The entity's Reactome ID is retreived from the StableIdentifier
    # table and the compartment's GO ID is retrieved from the
    # GO_CellularComponent table.
    compartment_sql = "SELECT si.identifier, go.accession \
                       FROM PhysicalEntity_2_compartment pe_c \
                       INNER JOIN Compartment c \
                       ON c.DB_ID=pe_c.compartment \
                       INNER JOIN GO_CellularComponent_2_instanceOf g \
                       ON g.instanceOf=c.DB_ID \
                       INNER JOIN GO_CellularComponent go \
                       ON go.DB_ID=g.instanceOf \
                       INNER JOIN DatabaseObject dbobj \
                       ON pe_c.DB_ID=dbobj.DB_ID \
                       INNER JOIN StableIdentifier si \
                       ON si.DB_ID=dbobj.stableIdentifier"
    if test:
        compartment_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for compartment_pe_c in run_sql(compartment_sql, connection):
        subject_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + compartment_pe_c[0])
        if subject_id is None:
            continue
        object_id = kg2_util.CURIE_PREFIX_GO + ':' + compartment_pe_c[1]
        predicate = 'in_compartment'
        edge = format_edge(subject_id, object_id, predicate)
        edges.append(edge)

    return edges


def get_equivalencies(connection, test):
    edges = []

    # This MySQL query uses the Event table to match
    # Reactome IDs (from the StableIdentifier table)
    # with their equivalent GO Biological Processes
    # using the GO_Biological_Process table.
    go_eq_sql = "SELECT go.accession, si.identifier \
                 FROM Event event \
                 INNER JOIN DatabaseObject dbobj \
                 ON event.DB_ID=dbobj.DB_ID \
                 INNER JOIN StableIdentifier si \
                 ON dbobj.stableIdentifier=si.DB_ID \
                 INNER JOIN GO_BiologicalProcess go \
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
        edges.append(edge)

    # This MySQL query uses the PhysicalEntity_2_crossReference
    # table to generate related_to edges from Reactome IDs
    # (which are discovered using the StableIdentifier table)
    # to IDs from various other sources. Some are very close
    # matches and others are very loose, so we use the related_to
    # predicate to accommodate this.
    ex_ont_sql = "SELECT rd_n.name, di.identifier, si.identifier, rd.accessUrl \
                  FROM PhysicalEntity_2_crossReference pe \
                  INNER JOIN DatabaseObject dbobj \
                  ON dbobj.DB_ID=pe.DB_ID \
                  INNER JOIN StableIdentifier si \
                  ON dbobj.stableIdentifier=si.DB_ID \
                  INNER JOIN DatabaseIdentifier di \
                  ON di.DB_ID=pe.crossReference \
                  INNER JOIN ReferenceDatabase rd \
                  ON rd.DB_ID=di.referenceDatabase \
                  INNER JOIN ReferenceDatabase_2_name rd_n \
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
            print("The source " + ex_ont[0] + " is not in the name_prefix_dict.")
            continue
        ex_ont_id = ex_ont_prefix + ":" + str(ex_ont[1])
        react_id = only_include_certain_species(kg2_util.CURIE_PREFIX_REACTOME + ':' + ex_ont[2])
        if react_id is None:
            continue
        predicate = 'related_to'
        edge = format_edge(react_id, ex_ont_id, predicate)
        edges.append(edge)

    # This group of MySQL queries iterates over a series of tables
    # (the 'reference_entity_tables') that have a 'referenceEntity'
    # column. This connects the entity's Reactome ID (retreived
    # from the StableIdentifier table) with another source's ID.
    # There is only one mapping per entity (as far as I know)
    # and they are precise, so we use the 'same_as' predicate.
    reference_entity_tables = ['EntityWithAccessionedSequence',
                               'SimpleEntity',
                               'Drug']
    for reference_entity_table in reference_entity_tables:
        reference_entity_sql = f"SELECT si_sub.identifier, re.identifier, \
                                 dbobj_obj._displayName \
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
                print("The source " + result[2] + " is not in the name_prefix_dict")
                continue
            object_id = obj_prefix + ':' + result[1]
            predicate = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
            edge = format_edge(subject_id, object_id, predicate)
            edges.append(edge)

    return edges


def get_elements_of_complex(connection, test):
    edges = []

    # This MySQL query uses the Complex_2_hasComponent
    # table to get edges between Reactome complexes and
    # their elements. It uses the StableIdentifier table
    # to retreive the Reactome IDs for each, based on
    # their DB_IDs from Complex_2_hasComponent.
    complex_elements_sql = "SELECT si.identifier, si2.identifier \
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
        complex_elements_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for com_elm in run_sql(complex_elements_sql, connection):
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

    # This MySQL query uses the EntitySet_2_hasMember
    # table to get edges between Reactome sets and
    # their members. It uses the StableIdentifier table
    # to retreive the Reactome IDs for each, based on
    # their DB_IDs from EntitySet_2_hasMember.
    complex_members_sql = "SELECT si_sub.identifier, si_obj.identifier \
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
        complex_members_sql += " LIMIT " + str(ROW_LIMIT_TEST_MODE)
    for result in run_sql(complex_members_sql, connection):
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

    # This MySQL query iterates through a list
    # of tables ('to_species_tables') that contain
    # links between Reactome nodes and the species
    # they are in. It retreives the Reactome ID
    # for the Reactome node and the species name
    # for the species (which is linked to NCBITaxon
    # using match_species_to_id).
    to_species_tables = ['Event_2_species',
                         'Polymer_2_species',
                         'Complex_2_species',
                         'EntitySet_2_species']
    for to_species_table in to_species_tables:
        species_sql = f"SELECT si_sub.identifier, dbobj_obj._displayName \
                        FROM {to_species_table} sp \
                        INNER JOIN DatabaseObject dbobj_obj \
                        ON dbobj_obj.DB_ID=sp.species \
                        INNER JOIN DatabaseObject dbobj_sub \
                        ON dbobj_sub.DB_ID=sp.DB_ID \
                        INNER JOIN StableIdentifier si_sub \
                        ON si_sub.DB_ID=dbobj_sub.stableIdentifier"
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

    connection = pymysql.connect(read_default_file=args.mysqlConfigFile, db=args.mysqlDBName)

    run_sql("SET SESSION group_concat_max_len=35000", connection)
    run_sql("SET SESSION sort_buffer_size=256000000", connection)

    nodes = get_nodes(connection, args.test)
    edges = get_edges(connection, args.test)

    kp_node = kg2_util.make_node(REACTOME_KB_CURIE_ID,
                                 REACTOME_KB_IRI,
                                 'Reactome',
                                 kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                 None,
                                 REACTOME_KB_CURIE_ID)
    nodes.append(kp_node)

    graph = {'nodes': nodes,
             'edges': edges}

    kg2_util.save_json(graph, args.outputFile, args.test)
