#!/usr/bin/env python3
'''chembl_mysql_to_kg_json.py: Extracts a KG in JSON format from the ChEMBL mysql database

   Usage: chembl_mysql_to_kg_json.py [--test] <mysql_conf> <chembl_mysql_dbname> <outputFile.json>
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
import pymysql

CHEMBL_CURIE_BASE_COMPOUND = kg2_util.CURIE_PREFIX_CHEMBL_COMPOUND
CHEMBL_CURIE_BASE_TARGET = kg2_util.CURIE_PREFIX_CHEMBL_TARGET
CHEMBL_CURIE_BASE_MECHANISM = kg2_util.CURIE_PREFIX_CHEMBL_MECHANISM
CHEMBL_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY + ':' + 'chembl'
CHEMBL_BASE_IRI_COMPOUND = kg2_util.BASE_URL_CHEMBL_COMPOUND
CHEMBL_BASE_IRI_TARGET = kg2_util.BASE_URL_CHEMBL_TARGET
CHEMBL_BASE_IRI_PREDICATE = kg2_util.BASE_URL_CHEMBL_MECHANISM

ROW_LIMIT_TEST_MODE = 10000

TARGET_TYPE_TO_CATEGORY = {
    'CELL-LINE': 'cell type',
    'CHIMERIC PROTEIN': 'protein',
    'LIPID': 'lipid',
    'MACROMOLECULE': 'biological molecular complex',
    'METAL': 'element',
    'NUCLEIC-ACID': 'nucleic acid',
    'OLIGOSACCHARIDE': 'metabolite',
    'ORGANISM': 'organism taxon',
    'PHENOTYPE': 'phenotypic feature',
    'PROTEIN COMPLEX': 'biological molecular complex',
    'PROTEIN COMPLEX GROUP': 'biological molecular complex',
    'PROTEIN FAMILY': 'protein family',
    'PROTEIN NUCLEIC-ACID COMPLEX': 'biological molecular complex',
    'PROTEIN-PROTEIN INTERACTION': 'protein',
    'SELECTIVITY GROUP': 'protein family',
    'SINGLE PROTEIN': 'protein',
    'SMALL MOLECULE': 'chemical substance',
    'SUBCELLULAR': 'cellular component',
    'TISSUE': 'anatomical entity',
    'UNKNOWN': 'biological molecule'
}


def get_args():
    arg_parser = argparse.ArgumentParser(description='ensembl_json_to_kg2_json.py: builds a KG2 JSON representation for Ensembl genes')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('mysqlConfigFile', type=str)
    arg_parser.add_argument('mysqlDBName', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def make_edge(subject_id: str,
              object_id: str,
              predicate_label: str,
              update_date: str = None,
              publications: list = None):
    relation = CHEMBL_BASE_IRI_PREDICATE + kg2_util.convert_snake_case_to_camel_case(predicate_label)
    if publications is None:
        publications = []
    return {'subject': subject_id,
            'object': object_id,
            'edge label': predicate_label,
            'relation': relation,
            'relation curie': 'CHEMBL:' + predicate_label,
            'negated': False,
            'publications': publications,
            'publications info': {},
            'update date': update_date,
            'provided by': CHEMBL_KB_CURIE_ID}


def make_node(id: str,
              iri: str,
              name: str,
              category_label: str,
              description: str,
              synonym: list,
              publications: list,
              update_date: str):
    node_dict = kg2_util.make_node(id,
                                   iri,
                                   name,
                                   category_label,
                                   update_date,
                                   CHEMBL_KB_CURIE_ID)
    node_dict['description'] = description
    node_dict['synonym'] = synonyms
    node_dict['publications'] = publications
    return node_dict


if __name__ == '__main__':
    args = get_args()
    mysql_config_file = args.mysqlConfigFile
    mysql_db_name = args.mysqlDBName
    output_file_name = args.outputFile
    test_mode = args.test
    connection = pymysql.connect(read_default_file=mysql_config_file, db=mysql_db_name)

    nodes = []
    edges = []

    str_sql_row_limit_test_mode = ' limit ' + str(ROW_LIMIT_TEST_MODE)

    sql = "select DATE_FORMAT(creation_date, '%Y-%m-%d') from version"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        update_date = cursor.fetchone()[0]

# create node objects for ChEMBL compounds

    sql = '''select distinct
       molecule_dictionary.chembl_id,
       molecule_dictionary.pref_name,
       molecule_dictionary.molecule_type,
       molecule_dictionary.max_phase,
       molecule_dictionary.availability_type,
       compound_structures.standard_inchi,
       compound_structures.standard_inchi_key,
       compound_structures.canonical_smiles,
       compound_properties.full_mwt,
       molecule_dictionary.molregno
       from (molecule_dictionary
       left join compound_structures on molecule_dictionary.molregno = compound_structures.molregno)
       left join compound_properties on molecule_dictionary.molregno = compound_properties.molregno'''
    if test_mode:
        sql += str_sql_row_limit_test_mode
    with connection.cursor() as cursor:
        cursor.execute(sql)
        molecule_sql_results = cursor.fetchall()
    row_ctr = 0
    for (chembl_id,
         pref_name,
         molecule_type,
         max_phase_int,
         availability_type,
         standard_inchi,
         standard_inchi_key,
         canonical_smiles,
         full_mwt,
         molregno) in molecule_sql_results:
        row_ctr += 1
        if row_ctr % 100000 == 0:
            print("have processed " + str(row_ctr) + " compounds")
        synonyms = []
        if standard_inchi is not None:
            synonyms.append(standard_inchi)
        if standard_inchi_key is not None:
            synonyms.append(standard_inchi_key)
        if canonical_smiles is not None:
            synonyms.append(canonical_smiles)

        curie_id = 'CHEMBL.COMPOUND:' + chembl_id
        category_label = kg2_util.BIOLINK_CATEGORY_CHEMICAL_SUBSTANCE

        # query to get all synonyms and publications associated with the ChEMBL molecule

        sql_synonyms = '''select distinct compound_name, src_short_name, src_compound_id, pubmed_id 
                          from (compound_records natural join source) 
                          left join docs on compound_records.doc_id = docs.doc_id 
                          where molregno ='''

        sql_synonyms += str(molregno)
        publications = []
        publications_set = set()
        with connection.cursor() as cursor:
            cursor.execute(sql_synonyms)
            synonym_results = cursor.fetchall()
            synonym_set = set()
            for (compound_name,
                 src_short_name,
                 src_compound_id,
                 pubmed_id) in synonym_results:
                if pref_name is None and compound_name is not None:
                    pref_name = compound_name
                synonym_set.add(compound_name)
                if pubmed_id is not None:
                    publications_set.add(kg2_util.CURIE_PREFIX_PMID + ':' + str(pubmed_id))
                if src_compound_id is not None and src_short_name is not None and src_short_name != "LITERATURE":
                    synonym_set.add(src_short_name + ':' + src_compound_id)
        compound_synonyms = list(synonym_set)
        publications += list(publications_set)
        synonyms += compound_synonyms
        if pref_name is not None:
            description = pref_name
        else:
            description = ''
        if full_mwt is not None:
            description += '; FULL_MW:' + str(full_mwt)
        if max_phase_int is not None:
            description += '; MAX_FDA_APPROVAL_PHASE: ' + str(max_phase_int)
        id = CHEMBL_CURIE_BASE_COMPOUND + ':' + chembl_id
        iri = CHEMBL_BASE_IRI_COMPOUND + '/' + chembl_id
        node_dict = make_node(id,
                              iri,
                              pref_name,
                              category_label,
                              description,
                              synonyms,
                              publications,
                              update_date)
        nodes.append(node_dict)

# create node objects for ChEMBL targets

    sql = '''select distinct
             target_dictionary.chembl_id,
             target_dictionary.tax_id,
             target_dictionary.pref_name,
             target_type.target_type from
             target_dictionary natural join target_type'''
    if test_mode:
        sql += str_sql_row_limit_test_mode
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    for (chembl_id,
         tax_id,
         pref_name,
         target_type) in results:
        curie_id = 'CHEMBL.TARGET:' + chembl_id
        category_label = 'drug_target'
        description = pref_name
        if target_type is not None:
            description += '; TARGET_TYPE: ' + target_type
        category_label = TARGET_TYPE_TO_CATEGORY.get(target_type, None)
        if category_label is None:
            continue
        category_label = category_label.replace(' ', '_')
        node_dict = make_node(curie_id,
                              CHEMBL_BASE_IRI_TARGET + chembl_id,
                              pref_name,
                              category_label,
                              description,
                              synonyms,
                              [],
                              update_date)
        nodes.append(node_dict)

# create node objects for "mechanism_of_action" types

    sql = 'select distinct mechanism_of_action from drug_mechanism'
    if test_mode:
        sql += str_sql_row_limit_test_mode
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    for (mechanism_of_action,) in results:
        if mechanism_of_action is not None:
            node_label = mechanism_of_action.lower().replace(' ', '_')
            node_curie_id = CHEMBL_CURIE_BASE_MECHANISM + ':' + node_label
            category_label = 'mechanism_of_action'
            node_dict = make_node(node_curie_id,
                                  CHEMBL_BASE_IRI_PREDICATE + node_label,
                                  mechanism_of_action,
                                  category_label,
                                  None,
                                  [],
                                  [],
                                  update_date)
            nodes.append(node_dict)

# get action_type nodes and their subclass_of relationships

    sql = 'select action_type, description, parent_type from action_type'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    for (action_type, description, parent_type) in results:
        name = action_type.lower()
        predicate_label = name.replace(' ', '_')
        curie_id = 'CHEMBL:' + predicate_label
        category_label = 'semantic_type'
        node_dict = make_node(curie_id,
                              CHEMBL_BASE_IRI_PREDICATE + chembl_id,
                              name,
                              category_label,
                              description,
                              [],
                              [],
                              update_date)
        nodes.append(node_dict)
        parent_label = parent_type.lower().replace(' ', '_')
        parent_curie_id = 'CHEMBL:' + parent_label
        edges.append(make_edge(curie_id,
                               parent_curie_id,
                               'subclass_of',
                               update_date))

# get target-to-target subset_of relationships

    sql = '''select distinct
             t1.chembl_id,
             target_relations.relationship,
             t2.chembl_id
             from
             (target_dictionary as t1 inner join
             target_relations on t1.tid = target_relations.tid) inner join
             target_dictionary as t2 on t2.tid = target_relations.related_tid'''
    if test_mode:
        sql += str_sql_row_limit_test_mode
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    for (t1_chembl_id,
         relationship,
         t2_chembl_id) in results:
        subject_curie_id = 'CHEMBL.TARGET:' + t1_chembl_id
        object_curie_id = 'CHEMBL.TARGET:' + t2_chembl_id
        predicate_label = relationship.lower().replace(' ', '_')
        edges.append(make_edge(subject_curie_id,
                               object_curie_id,
                               predicate_label,
                               update_date))

# get ChEMBL target-to-protein and target-to-RNA relationships

    sql = '''select distinct
             target_dictionary.chembl_id,
             target_components.homologue,
             component_sequences.component_type,
             component_sequences.accession,
             component_sequences.db_source,
             component_sequences.db_version
             from
             (target_dictionary right join
             target_components on target_dictionary.tid = target_components.tid)
             left join component_sequences on target_components.component_id = component_sequences.component_id
             where component_sequences.accession is not NULL'''
    if test_mode:
        sql += str_sql_row_limit_test_mode
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    for (chembl_id,
         homologue,
         component_type,
         accession,
         db_source,
         db_version) in results:
        subject_curie_id = 'CHEMBL.TARGET:' + chembl_id
        if component_type == 'PROTEIN':
            object_curie_id = 'UniProtKB:' + accession
        elif component_type == 'RNA':
            object_curie_id = kg2_util.CURIE_PREFIX_ENSEMBL + ':' + accession
        predicate_label = 'has_sequence'
        edges.append(make_edge(subject_curie_id,
                               object_curie_id,
                               predicate_label,
                               update_date))

# get drug-to-target edges and additional information about drugs (direct_interaction, has_role, etc.)

    sql = '''select distinct
             molecule_dictionary.chembl_id,
             drug_mechanism.mechanism_of_action,
             drug_mechanism.direct_interaction,
             mechanism_refs.ref_url,
             action_type.action_type,
             target_dictionary.chembl_id
             from (((molecule_dictionary
             natural join drug_mechanism)
             inner join target_dictionary on drug_mechanism.tid = target_dictionary.tid)
             natural join action_type
             left join mechanism_refs on drug_mechanism.mec_id = mechanism_refs.mec_id)'''
    if test_mode:
        sql += str_sql_row_limit_test_mode
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    for (molec_chembl_id,
         mechanism_of_action,
         direct_interaction,
         ref_url,
         action_type,
         target_chembl_id) in results:
        subject_curie_id = CHEMBL_CURIE_BASE_COMPOUND + ':' + molec_chembl_id
        object_curie_id = CHEMBL_CURIE_BASE_TARGET + ':' + target_chembl_id
        predicate_label = action_type.lower().replace(' ', '_')
        if ref_url is not None:
            publications = [ref_url]
        else:
            publications = None
        edges.append(make_edge(subject_curie_id,
                               object_curie_id,
                               predicate_label,
                               update_date,
                               publications))
        if direct_interaction is not None and direct_interaction == 1:
            edges.append(make_edge(subject_curie_id,
                                   object_curie_id,
                                   'directly_interacts_with',
                                   update_date))
        if mechanism_of_action is not None:
            mech_label = mechanism_of_action.lower().replace(' ', '_')
            mech_curie_id = CHEMBL_CURIE_BASE_MECHANISM + ':' + mech_label
            edges.append(make_edge(subject_curie_id,
                                   mech_curie_id,
                                   'has_role',
                                   update_date))

# get molecule-to-disease indications

    sql = '''select md.chembl_id, di.mesh_id 
             from molecule_dictionary as md 
             inner join drug_indication as di on md.molregno = di.molregno'''
    if test_mode:
        sql += str_sql_row_limit_test_mode
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    for (chembl_id, mesh_id) in results:
        subject_curie_id = CHEMBL_CURIE_BASE_COMPOUND + ':' + chembl_id
        object_curie_id = 'MESH:' + mesh_id
        predicate_label = 'has_indication'
        edges.append(make_edge(subject_curie_id,
                               object_curie_id,
                               predicate_label,
                               update_date,
                               []))
    kg2_util.save_json({'nodes': nodes, 'edges': edges},
                       output_file_name,
                       test_mode)
