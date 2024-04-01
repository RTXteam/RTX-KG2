#!/usr/bin/env python3
'''umls_util.py: handles source-specific conversion of UMLS MySQL JSON Lines dump into KG2 JSON format

   Usage: import umls_util.py
'''

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import kg2_util

class UMLS_Processor(object):
    def __init__(self, nodes_output, edges_output, tui_mappings, iri_mappings, full_name_heirarchy):
        self.nodes_output = nodes_output
        self.edges_output = edges_output
        self.TUI_MAPPINGS = tui_mappings
        self.IRI_MAPPINGS = iri_mappings
        self.full_name_heirarchy = full_name_heirarchy
        self.SOURCES = {'UMLS_SOURCE': [self.process_umls_source_item, None, None],
                        'ATC': [self.process_atc_item, kg2_util.CURIE_PREFIX_ATC, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'ATC')],
                        'CHV': [self.process_chv_item, kg2_util.CURIE_PREFIX_CHV, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'CHV')],
                        'DRUGBANK': [self.process_drugbank_item, kg2_util.CURIE_PREFIX_DRUGBANK, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'DRUGBANK')],
                        'FMA': [self.process_fma_item, kg2_util.CURIE_PREFIX_FMA, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'FMA')],
                        'GO': [self.process_go_item, kg2_util.CURIE_PREFIX_GO, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'GO')],
                        'HCPCS': [self.process_hcpcs_item, kg2_util.CURIE_PREFIX_HCPCS, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'HCPCS')],
                        'HGNC': [self.process_hgnc_item, kg2_util.CURIE_PREFIX_HGNC, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'HGNC')],
                        'HL7V3.0': [self.process_hl7_item, kg2_util.CURIE_PREFIX_UMLS, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'HL7')],
                        'HPO': [self.process_hpo_item, kg2_util.CURIE_PREFIX_HP, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'HPO')],
                        'ICD10PCS': [self.process_icd10pcs_item, kg2_util.CURIE_PREFIX_ICD10PCS, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'ICD10PCS')],
                        'ICD9CM': [self.process_icd9cm_item, kg2_util.CURIE_PREFIX_ICD9, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'ICD9CM')],
                        'MED-RT': [self.process_medrt_item, kg2_util.CURIE_PREFIX_UMLS, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'MED-RT')],
                        'MEDLINEPLUS': [self.process_medlineplus_item, kg2_util.CURIE_PREFIX_UMLS, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'MEDLINEPLUS')],
                        'MSH': [self.process_msh_item, kg2_util.CURIE_PREFIX_MESH, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'MSH')],
                        'MTH': [self.process_mth_item, kg2_util.CURIE_PREFIX_UMLS, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'MTH')],
                        'NCBI': [self.process_ncbi_item, kg2_util.CURIE_PREFIX_NCBI_TAXON, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'NCBITAXON')],
                        'NCI': [self.process_nci_item, kg2_util.CURIE_PREFIX_NCIT, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'NCI')],
                        'NDDF': [self.process_nddf_item, kg2_util.CURIE_PREFIX_NDDF, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'NDDF')],
                        'OMIM': [self.process_omim_item, kg2_util.CURIE_PREFIX_OMIM, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'OMIM')],
                        'PDQ': [self.process_pdq_item, kg2_util.CURIE_PREFIX_PDQ, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'PDQ')],
                        'PSY': [self.process_psy_item, kg2_util.CURIE_PREFIX_PSY, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'PSY')],
                        'RXNORM': [self.process_rxnorm_item, kg2_util.CURIE_PREFIX_RXNORM, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'RXNORM')],
                        'VANDF': [self.process_vandf_item, kg2_util.CURIE_PREFIX_VANDF, self.make_node_id(kg2_util.CURIE_PREFIX_UMLS_SOURCE, 'VANDF')],
                        'UMLS': [self.process_umls_item, kg2_util.CURIE_PREFIX_UMLS, self.make_node_id(kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY, 'umls')]}
        self.create_umls_accession_heirarchy()
        self.create_accession_sources_heirarchy()

        self.CUIS_KEY = 'cuis'
        self.INFO_KEY = 'attributes'
        self.NAMES_KEY = 'names'
        self.TUIS_KEY = 'tuis'
        self.DEFINITIONS_KEY = 'definitions'
        self.RELATIONS_KEY = 'relations'
        self.last_source = ''
        self.hgnc_to_omim = dict()


    def process_node(self, source, node_id, data):
        if source != self.last_source:
            if self.last_source != '' and self.last_source in self.SOURCES:
                print("Finished processing", self.last_source, "at", kg2_util.date())
            if source in self.SOURCES:
                print("Started processing", source, "at", kg2_util.date())
        self.last_source = source
        if source in self.SOURCES:
            self.SOURCES[source][0](node_id, data, source)


    def create_umls_accession_heirarchy(self):
        self.UMLS_ACCESSION_HEIRARCHY = list()
        for [source, key] in self.full_name_heirarchy:
            if source in self.SOURCES:
                self.UMLS_ACCESSION_HEIRARCHY.append((source, key))

    def create_accession_sources_heirarchy(self):
        self.ACCESSION_SOURCES_HEIRARCHY = dict()
        for (source, key) in self.UMLS_ACCESSION_HEIRARCHY:
            if source not in self.ACCESSION_SOURCES_HEIRARCHY:
                self.ACCESSION_SOURCES_HEIRARCHY[source] = list()
            self.ACCESSION_SOURCES_HEIRARCHY[source].append(key)

    def make_umls_node(self, node_curie, iri, name, category, update_date, provided_by, synonyms, description, full_name=None):
        node = kg2_util.make_node(node_curie, iri, name, category, "2023", provided_by)
        node['synonym'] = synonyms
        node['description'] = description

        if full_name is not None:
            node['full_name'] = full_name

        self.nodes_output.write(node)

    def make_node_id(self, curie_prefix, node_id):
        return curie_prefix + ':' + node_id

    def get_name_synonyms(self, names_dict, source):
        names = list()
        if source == 'UMLS':
            for (key_source, key) in self.UMLS_ACCESSION_HEIRARCHY:
                names += [name for name in names_dict.get(key_source, dict()).get(key, dict()).get('Y', list())]
                names += [name for name in names_dict.get(key_source, dict()).get(key, dict()).get('N', list())]
        else:
            for key in self.ACCESSION_SOURCES_HEIRARCHY[source]:
                names += [name for name in names_dict.get(key, dict()).get('Y', list())]
                names += [name for name in names_dict.get(key, dict()).get('N', list())]

        if len(names) == 0:
            return None, None
        if len(names) == 1:
            return names[0], list()
        return names[0], names[1:]

    def create_xref_edges(self, subject_id, cuis, provided_by):
        relation_curie = 'UMLS:xref'
        relation_label = 'xref'

        for cui in cuis:
            object_id = self.make_node_id(kg2_util.CURIE_PREFIX_UMLS, cui)
            # TODO: resolve update_date
            self.edges_output.write(kg2_util.make_edge(subject_id, object_id, relation_curie, relation_label, provided_by, "2023"))

## TODO: make TUI nodes

    def create_umls_edges(self, object_id, relations):
        for relation_source in relations:
            if relation_source in self.SOURCES:
                provided_by = self.SOURCES[relation_source][2]
                relation_prefix = self.SOURCES[relation_source][1]
                for relation in relations[relation_source]:
                    relation_abbr, relation_label, relation_direction = relation.split(',')
                    if relation_label == 'None':
                        relation_label = relation_abbr
                    relation_curie = self.make_node_id(relation_prefix, relation_label)
                    for cui in relations[relation_source][relation]:
                        subject_id = self.make_node_id(kg2_util.CURIE_PREFIX_UMLS, cui)
                        # TODO: resolve update_date
                        if relation_direction == 'N':
                            self.edges_output.write(kg2_util.make_edge(object_id, subject_id, relation_curie, relation_label, provided_by, "2023"))
                        else:
                            self.edges_output.write(kg2_util.make_edge(subject_id, object_id, relation_curie, relation_label, provided_by, "2023"))

    def get_basic_info(self, source, node_id, info):
        curie_prefix = self.SOURCES[source][1]
        provided_by = self.SOURCES[source][2]
        cuis = info.get(self.CUIS_KEY, list())
        tuis = sorted(info.get(self.TUIS_KEY, list()))
        description = str()
        if source == 'UMLS':
            description = list()
            description_dict = info.get(self.DEFINITIONS_KEY, dict())
            for description_key in description_dict:
                if description_key in self.SOURCES:
                    description.append(description_dict[description_key])
            description = '; '.join(description)
        else:
            description = info.get(self.DEFINITIONS_KEY, str())
        if curie_prefix == kg2_util.CURIE_PREFIX_UMLS and source != 'UMLS':
            if len(cuis) != 1:
                return None, None, None, None, None, None, None, None, None
            node_id = cuis[0]
        node_curie = self.make_node_id(curie_prefix, node_id)
        iri = self.IRI_MAPPINGS[curie_prefix] + node_id
        category = self.TUI_MAPPINGS[str(tuple(tuis))]

        names = info.get(self.NAMES_KEY, dict())
        name, synonyms = self.get_name_synonyms(names, source)
        if name == None:
            return None, None, None, None, None, None, None, None, None

        return node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis

    def create_description(self, tuis, comment=""):
        description = comment.replace('<p>', '').replace('</p>', '').replace('<li>', '').replace('</li>', '').replace('<ul>', '').replace('</ul>', '')
        for tui in tuis:
            description += "; UMLS Semantic Type: STY:" + tui
        description = description.strip("; ")
        return description


    def process_umls_source_item(self, node_id, info, umls_code):
        if node_id not in self.SOURCES:
            return
        source_id = self.SOURCES[node_id][2]
        curie_prefix = source_id.split(':')[0]
        node_specific_id = source_id.split(':')[1]
        iri = self.IRI_MAPPINGS[curie_prefix] + node_specific_id
        name = info.get('source_name', '') + ' v' + info.get('version', '')
        update_date = info.get('update_date', '')
        self.make_umls_node(source_id, iri, name, kg2_util.SOURCE_NODE_CATEGORY, update_date, source_id, list(), "")


    def process_atc_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        atc_level = info.get(self.INFO_KEY, dict()).get('ATC_LEVEL', list())[0]
        is_drug_class = info.get(self.INFO_KEY, dict()).get('IS_DRUG_CLASS', list()) == ["Y"]

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_chv_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        combo_score = info.get(self.INFO_KEY, dict()).get('COMBO_SCORE', list())
        combo_score_no_top_words = info.get(self.INFO_KEY, dict()).get('COMBO_SCORE_NO_TOP_WORDS', list())
        context_score = info.get(self.INFO_KEY, dict()).get('CONTEXT_SCORE', list())
        cui_score = info.get(self.INFO_KEY, dict()).get('CUI_SCORE', list())
        disparaged = info.get(self.INFO_KEY, dict()).get('DISPARAGED', list())
        frequency = info.get(self.INFO_KEY, dict()).get('FREQUENCY', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_drugbank_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        fda_codes = info.get(self.INFO_KEY, dict()).get('FDA_UNII_CODE', list())
        secondary_accession_keys = info.get(self.INFO_KEY, dict()).get('SID', list())

        # TODO: figure out update date

        category = kg2_util.BIOLINK_CATEGORY_DRUG

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_fma_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        authority = info.get(self.INFO_KEY, dict()).get('AUTHORITY', list())
        date_last_modified = info.get(self.INFO_KEY, dict()).get('DATE_LAST_MODIFIED', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_go_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id.replace('GO:', ''), info)

        # GO-specific information
        attributes = info.get(self.INFO_KEY, dict())
        go_namespace = attributes.get('GO_NAMESPACE', list())
        assert len(go_namespace) == 1
        go_namespace = go_namespace[0]
        namespace_category_map = {'molecular_function': kg2_util.BIOLINK_CATEGORY_MOLECULAR_ACTIVITY,
                                  'cellular_component': kg2_util.BIOLINK_CATEGORY_CELLULAR_COMPONENT,
                                  'biological_process': kg2_util.BIOLINK_CATEGORY_BIOLOGICAL_PROCESS}
        category = namespace_category_map.get(go_namespace, category)
        go_comment = attributes.get('GO_COMMENT', str())
        if len(go_comment) > 0:
            go_comment = go_comment[0]
            go_comment = "// COMMENTS: " + go_comment

        # Currently not used, but extracting them in case we want them in the future
        date_created = attributes.get('DATE_CREATED', list())
        go_subset = attributes.get('GO_SUBSET', list())
        gxr = attributes.get('GXR', list())
        ref = attributes.get('REF', list())
        sid = attributes.get('SID', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, go_comment))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_hcpcs_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future - descriptions from https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/attribute_names.html
        attributes = info.get(self.INFO_KEY, dict())
        had = attributes.get('HAD', list()) # HCPCS Action Effective Date - effective date of action to a procedure or modifier code.
        hcc = attributes.get('HCC', list()) # HCPCS Coverage Code - code denoting Medicare coverage status. There are two subelements separated by "=".
        hts = attributes.get('HTS', list()) # HCPCS Type of Service Code - carrier assigned HCFA Type of Service which describes the particular kind(s) of service represented by the procedure code.
        hcd = attributes.get('HCD', list()) # HCPCS Code Added Date - year the HCPCS code was added to the HCFA Common Procedure Coding System.
        hpn = attributes.get('HPN', list()) # HCPCS processing note number identifying the processing note contained in Appendix A of the HCPCS Manual.
        haq = attributes.get('HAQ', list()) # HCPCS Anesthesia Base Unit Quantity - base unit represents the level of intensity for anesthesia procedure services that reflects all activities except time.
        hlc = attributes.get('HLC', list()) # HCPCS Lab Certification Code - code used to classify laboratory procedures according to the specialty certification categories listed by CMS(formerly HCFA).
        hsn = attributes.get('HSN', list()) # HCPCS Statute Number identifying statute reference for coverage or noncoverage of procedure or service.
        hpd = attributes.get('HPD', list()) # HCPCS ASC payment group effective date - date the procedure is assigned to the ASC payment group.
        hpg = attributes.get('HPG', list()) # HCPCS ASC payment group code which represents the dollar amount of the facility charge payable by Medicare for the procedure.
        hmg = attributes.get('HMR', list()) # HCPCS Medicare Carriers Manual reference section number - number identifying a section of the Medicare Carriers Manual.
        hir = attributes.get('HIR', list()) # HCPCS Coverage Issues Manual Reference Section Number - number identifying the Reference Section of the Coverage Issues Manual.
        hxr = attributes.get('HXR', list()) # HCPCS Cross reference code - an explicit reference crosswalking a deleted code or a code that is not valid for Medicare to a valid current code (or range of codes).
        hmp = attributes.get('HMP', list()) # HCPCS Multiple Pricing Indicator Code - code used to identify instances where a procedure could be priced.
        hpi = attributes.get('HPI', list()) # HCPCS Pricing Indicator Code - used to identify the appropriate methodology for developing unique pricing amounts under Part B.
        hac = attributes.get('HAC', list()) # HCPCS action code - code denoting the change made to a procedure or modifier code within the HCPCS system.
        hbt = attributes.get('HBT', list()) # HCPCS Berenson-Eggers Type of Service Code - BETOS for the procedure code based on generally agreed upon clinically meaningful groupings of procedures and services.

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_hgnc_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id.replace('HGNC:', ''), info)

        full_name = name

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        mgd_id = attributes.get('MGD_ID', list())
        vega_id = attributes.get('VEGA_ID', list())
        genecc = attributes.get('GENCC', list())
        swp = attributes.get('SWP', list())
        mane_select = attributes.get('MANE_SELECT', list())
        local_specific_db_xr = attributes.get('LOCUS_SPECIFIC_DB_XR', list())
        locus_type = attributes.get('LOCUS_TYPE', list())
        agr = attributes.get('AGR', list())
        cytogenetic_location = attributes.get('CYTOGENETIC_LOCATION', list())
        date_created = attributes.get('DATE_CREATED', list())
        ensemblgene_id = attributes.get('ENSEMBLGENE_ID', list())
        db_xr_id = attributes.get('DB_XR_ID', list())
        locus_group = attributes.get('LOCUS_GROUP', list())
        entrezgene_id = attributes.get('ENTREZGENE_ID', list())
        date_name_changed = attributes.get('DATE_NAME_CHANGED', list())
        pmid = attributes.get('PMID', list())
        date_last_modified = attributes.get('DATE_LAST_MODIFIED', list())
        mapped_ucsc_id = attributes.get('MAPPED_UCSC_ID', list())
        refseq_id = attributes.get('REFSEQ_ID', list())
        ena = attributes.get('ENA', list())
        rgd_id = attributes.get('RGD_ID', list())
        date_symbol_changed = attributes.get('DATE_SYMBOL_CHANGED', list())
        omim_id_list = attributes.get('OMIM_ID', list())
        gene_fam_id = attributes.get('GENE_FAM_ID', list())
        gene_symbol = attributes.get('GENESYMBOL', list())
        ez = attributes.get('EZ', list())
        ccds_id = attributes.get('CCDS_ID', list())
        lncipedia = attributes.get('LNCIPEDIA', list())
        gene_fam_desc = attributes.get('GENE_FAM_DESC', list())

        if len(gene_symbol) > 0:
            for omim_id in omim_id_list:
                self.hgnc_to_omim[self.make_node_id(kg2_util.CURIE_PREFIX_OMIM, omim_id)] = gene_symbol[0]
            name = gene_symbol[0]

        category = kg2_util.BIOLINK_CATEGORY_GENE

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description), full_name=full_name)
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_hl7_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)
        if node_curie == None:
            return

        # Currently not used, but extracting them in case we want them in the future - descriptions from https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/attribute_names.html
        attributes = info.get(self.INFO_KEY, dict())
        hl7at = attributes.get('HL7AT', list())
        hl7ii = attributes.get('HL7II', list())
        hl7im = attributes.get('HL7IM', list())
        hl7lt = attributes.get('HL7LT', list())
        hl7un = attributes.get('HL7UN', list())
        hl7oa = attributes.get('HL7OA', list())
        hl7scs = attributes.get('HL7SCS', list())
        hl7cc = attributes.get('HL7CC', list())
        hl7na = attributes.get('HL7NA', list())
        hl7in = attributes.get('HL7IN', list())
        hl7ap = attributes.get('HL7AP', list())
        hl7mi = attributes.get('HL7MI', list())
        hl7hi = attributes.get('HL7HI', list())
        hl7ir = attributes.get('HL7IR', list())
        hl7ai = attributes.get('HL7AI', list())
        hl7ha = attributes.get('HL7HA', list())
        hl7rf = attributes.get('HL7RF', list())
        hl7rd = attributes.get('HL7RD', list())
        hl7vd = attributes.get('HL7VD', list())
        hl7dc = attributes.get('HL7DC', list())
        hl7rk = attributes.get('HL7RK', list())
        hl7is = attributes.get('HL7IS', list())
        hl7sy = attributes.get('HL7SY', list())
        hl7cd = attributes.get('HL7CD', list())
        hl7sl = attributes.get('HL7SL', list())
        hl7pl = attributes.get('HL7PL', list())
        hl7vc = attributes.get('HL7VC', list())
        hl7ty = attributes.get('HL7TY', list())
        hl7rg = attributes.get('HL7RG', list())
        hl7csc = attributes.get('HL7CSC', list())
        hl7od = attributes.get('HL7OD', list())
        hl7id = attributes.get('HL7ID', list())
        hl7tr = attributes.get('HL7TR', list())
        hl7di = attributes.get('HL7DI', list())
        hl7cs = attributes.get('HL7CS', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))


    def process_hpo_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id.replace('HP:', ''), info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        sid = attributes.get('SID', list())
        hpo_comment = attributes.get('HPO_COMMENT', str())
        if len(hpo_comment) > 0:
            hpo_comment = hpo_comment[0]
        date_created = attributes.get('DATE_CREATED', list())
        syn_qualifier = attributes.get('SYN_QUALIFIER', list())
        ref = attributes.get('REF', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_icd10pcs_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        added_meaning = attributes.get('ADDED_MEANING', list())
        order_no = attributes.get('ORDER_NO', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_icd9cm_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        icc = attributes.get('ICC', list())
        ice = attributes.get('ICE', list())
        icf = attributes.get('ICF', list())
        sos = attributes.get('SOS', list())
        icn = attributes.get('ICN', list())
        ica = attributes.get('ICA', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)

    def process_medrt_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)
        if node_curie == None:
            return

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        term_status = attributes.get('TERM_STATUS', list())
        concept_type = attributes.get('CONCEPT_TYPE', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))


    def process_medlineplus_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)
        if node_curie == None:
            return

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        sos = attributes.get('SOS', list())
        date_created = attributes.get('DATE_CREATED', list())
        mp_group_url = attributes.get('MP_GROUP_URL', list())
        mp_primary_institute_url = attributes.get('MP_PRIMARY_INSTITUTE_URL', list())
        mp_other_language_url = attributes.get('MP_OTHER_LANGUAGE_URL', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))


    def process_msh_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        mmr = attributes.get('MMR', list())
        fx = attributes.get('FX', list())
        lt = attributes.get('LT', list())
        dc = attributes.get('DC', list())
        pa = attributes.get('PA', list())
        rr = attributes.get('RR', list())
        hm = attributes.get('HM', list())
        pi = attributes.get('PI', list())
        ec = attributes.get('EC', list())
        hn = attributes.get('HN', list())
        termui = attributes.get('TERMUI', list())
        th = attributes.get('TH', list())
        sos = attributes.get('SOS', list())
        ii = attributes.get('II', list())
        rn = attributes.get('RN', list())
        an = attributes.get('AN', list())
        cx = attributes.get('CX', list())
        dq = attributes.get('DQ', list())
        dx = attributes.get('DX', list())
        pm = attributes.get('PM', list())
        aql = attributes.get('AQL', list())
        sc = attributes.get('SC', list())
        fr = attributes.get('FR', list())
        mda = attributes.get('MDA', list())
        src = attributes.get('SRC', list())
        ol = attributes.get('OL', list())
        mn = attributes.get('MN', list())

        if category == kg2_util.BIOLINK_CATEGORY_DRUG and "T109" in tuis:
            category = kg2_util.BIOLINK_CATEGORY_CHEMICAL_ENTITY

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_mth_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)
        if node_curie == None:
            return

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        mth_mapsetcomplexity = attributes.get('MTH_MAPSETCOMPLEXITY', list())
        fromvsab = attributes.get('FROMVSAB', list())
        mapsetrsab = attributes.get('MAPSETRSAB', list())
        mapsetversion = attributes.get('MAPSETVERSION', list())
        mapsetvsab = attributes.get('MAPSETVSAB', list())
        tovsab = attributes.get('TOVSAB', list())
        mth_mapfromexhaustive = attributes.get('MTH_MAPFROMEXHAUSTIVE', list())
        torsab = attributes.get('TORSAB', list())
        mapsetsid = attributes.get('MAPSETSID', list())
        mapsetgrammar = attributes.get('MAPSETGRAMMAR', list())
        mapsettype = attributes.get('MAPSETTYPE', list())
        mth_maptoexhaustive = attributes.get('MTH_MAPTOEXHAUSTIVE', list())
        fromrsab = attributes.get('FROMRSAB', list())
        mth_mapfromcomplexity = attributes.get('MTH_MAPFROMCOMPLEXITY', list())
        lt = attributes.get('LT', list())
        mth_maptocomplexity = attributes.get('MTH_MAPTOCOMPLEXITY', list())
        sos = attributes.get('SOS', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))


    def process_ncbi_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        div = attributes.get('DIV', list())
        authority_name = attributes.get('AUTHORITY_NAME', list())
        rank = attributes.get('RANK', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_nci_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        clinvar_variation_id = attributes.get('CLINVAR_VARIATION_ID', list())
        micronutrient = attributes.get('MICRONUTRIENT', list())
        genbank_accession_number = attributes.get('GENBANK_ACCESSION_NUMBER', list())
        fda_table = attributes.get('FDA_TABLE', list())
        usda_id = attributes.get('USDA_ID', list())
        icd_o_3_code = attributes.get('ICD-O-3_CODE', list())
        tolerable_level = attributes.get('TOLERABLE_LEVEL', list())
        ncbi_taxon_id = attributes.get('NCBI_TAXON_ID', list())
        mgi_accession_id = attributes.get('MGI_ACCESSION_ID', list())
        homologous_gene = attributes.get('HOMOLOGOUS_GENE', list())
        pid_id = attributes.get('PID_ID', list())
        swiss_prot = attributes.get('SWISS_PROT', list())
        essential_amino_acid = attributes.get('ESSENTIAL_AMINO_ACID', list())
        publish_value_set = attributes.get('PUBLISH_VALUE_SET', list())
        cas_registry = attributes.get('CAS_REGISTRY', list())
        value_set_pair = attributes.get('VALUE_SET_PAIR', list())
        accepted_therapeutic_use_for = attributes.get('ACCEPTED_THERAPEUTIC_USE_FOR', list())
        hgnc_id = attributes.get('HGNC_ID', list())
        nci_drug_dictionary_id = attributes.get('NCI_DRUG_DICTIONARY_ID', list())
        chebi_id = attributes.get('CHEBI_ID', list())
        cnu = attributes.get('CNU', list())
        mirbase_id = attributes.get('MIRBASE_ID', list())
        macronutrient = attributes.get('MACRONUTRIENT', list())
        essential_fatty_acid = attributes.get('ESSENTIAL_FATTY_ACID', list())
        unit = attributes.get('UNIT', list())
        pdq_open_trial_search_id = attributes.get('PDQ_OPEN_TRIAL_SEARCH_ID', list())
        term_browser_value_set_description = attributes.get('TERM_BROWSER_VALUE_SET_DESCRIPTION', list())
        entrezgene_id = attributes.get('ENTREZGENE_ID', list())
        infoods = attributes.get('INFOODS', list())
        pubmedid_primary_reference = attributes.get('PUBMEDID_PRIMARY_REFERENCE', list())
        biocarta_id = attributes.get('BIOCARTA_ID', list())
        extensible_list = attributes.get('EXTENSIBLE_LIST', list())
        use_for = attributes.get('USE_FOR', list())
        neoplastic_status = attributes.get('NEOPLASTIC_STATUS', list())
        nsc_number = attributes.get('NSC_NUMBER', list())
        omim_number = attributes.get('OMIM_NUMBER', list())
        lt = attributes.get('LT', list())
        kegg_id = attributes.get('KEGG_ID', list())
        gene_encodes_product = attributes.get('GENE_ENCODES_PRODUCT', list())
        pdq_closed_trial_search_id = attributes.get('PDQ_CLOSED_TRIAL_SEARCH_ID', list())
        design_note = attributes.get('DESIGN_NOTE', list())
        nutrient = attributes.get('NUTRIENT', list())
        fda_unii_code = attributes.get('FDA_UNII_CODE', list())
        us_recommended_intake = attributes.get('US_RECOMMENDED_INTAKE', list())
        chemical_formula = attributes.get('CHEMICAL_FORMULA', list())

        if tuis == ['T028'] and (len(entrezgene_id) > 0 or len(hgnc_id) > 0 or len(gene_encodes_product) > 0 or "gene" in name.lower() or "allele" in name.lower()):
            category = kg2_util.BIOLINK_CATEGORY_GENE

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)

    def process_nddf_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        ndc = attributes.get('NDC', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)

    def process_omim_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        gene_symbol = attributes.get('GENESYMBOL', list())
        mimtypevalue = attributes.get('MIMTYPEVALUE', list())
        moved_from = attributes.get('MOVED_FROM', list())
        sos = attributes.get('SOS', list())
        genelocus = attributes.get('GENELOCUS', list())
        mimtypemeaning = attributes.get('MIMTYPEMEANING', list())
        mimtype = attributes.get('MIMTYPE', list())

        name = name.capitalize()
        if len(mimtype) > 0:
            mimtype = int(mimtype[0])
            if mimtype in [0, 3, 5]:
                category = kg2_util.BIOLINK_CATEGORY_PHENOTYPIC_FEATURE
                name += " related phenotypic feature"
            if mimtype in [1, 4]:
                category = kg2_util.BIOLINK_CATEGORY_GENE
                if len(gene_symbol) > 0:
                    name = gene_symbol[0]
                name = self.hgnc_to_omim.get(node_curie, name)

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_pdq_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        lt = attributes.get('LT', list())
        cas_registry = attributes.get('CAS_REGISTRY', list())
        date_first_published = attributes.get('DATE_FIRST_PUBLISHED', list())
        date_last_modified = attributes.get('DATE_LAST_MODIFIED', list())
        ind_code = attributes.get('IND_CODE', list())
        pid = attributes.get('PID', list())
        nsc_code = attributes.get('NSC_CODE', list())
        pxc = attributes.get('PXC', list())
        menu_parent = attributes.get('MENU_PARENT', list())
        nci_id = attributes.get('NCI_ID', list())
        orig_sty = attributes.get('ORIG_STY', list())
        menu_type = attributes.get('MENU_TYPE', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_psy_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        hn = attributes.get('HN', list())
        pyr = attributes.get('PYR', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_rxnorm_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        ndc = attributes.get('NDC', list())
        rxn_obsoleted = attributes.get('RXN_OBSOLETED', list())
        rxn_available_strength = attributes.get('RXN_AVAILABLE_STRENGTH', list())
        rxn_human_drug = attributes.get('RXN_HUMAN_DRUG', list())
        rxn_quantity = attributes.get('RXN_QUANTITY', list())
        rxterm_form = attributes.get('RXTERM_FORM', list())
        rxn_in_expressed_flag = attributes.get('RXN_IN_EXPRESSED_FLAG', list())
        rxaui = attributes.get('RXAUI', list())
        rxn_bn_cardinality = attributes.get('RXN_BN_CARDINALITY', list())
        rxn_activated = attributes.get('RXN_ACTIVATED', list())
        rxn_boss_strength_denom_unit = attributes.get('RXN_BOSS_STRENGTH_DENOM_UNIT', list())
        ambiguity_flag = attributes.get('AMBIGUITY_FLAG', list())
        rxn_strength = attributes.get('RXN_STRENGTH', list())
        rxcui = attributes.get('RXCUI', list())
        rxn_ai = attributes.get('RXN_AI', list())
        rxn_boss_from = attributes.get('RXN_BOSS_FROM', list())
        rxn_boss_strength_num_unit = attributes.get('RXN_BOSS_STRENGTH_NUM_UNIT', list())
        rxn_vet_drug = attributes.get('RXN_VET_DRUG', list())
        orig_code = attributes.get('ORIG_CODE', list())
        rxn_am = attributes.get('RXN_AM', list())
        rxn_boss_strength_denom_value = attributes.get('RXN_BOSS_STRENGTH_DENOM_VALUE', list())
        rxn_boss_strength_num_value = attributes.get('RXN_BOSS_STRENGTH_NUM_VALUE', list())
        rxn_qualitative_distinction = attributes.get('RXN_QUALITATIVE_DISTINCTION', list())
        orig_source = attributes.get('ORIG_SOURCE', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)


    def process_vandf_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)

        # Currently not used, but extracting them in case we want them in the future
        attributes = info.get(self.INFO_KEY, dict())
        ndf_transmit_to_cmop = attributes.get('NDF_TRANSMIT_TO_CMOP', list())
        sngl_or_mult_src_prd = attributes.get('SNGL_OR_MULT_SRC_PRD', list())
        dcsa = attributes.get('DCSA', list())
        exclude_di_check = attributes.get('EXCLUDE_DI_CHECK', list())
        nfi = attributes.get('NFI', list())
        va_class_name = attributes.get('VA_CLASS_NAME', list())
        vmo = attributes.get('VMO', list())
        drug_class_type = attributes.get('DRUG_CLASS_TYPE', list())
        nf_name = attributes.get('NF_NAME', list())
        ndc = attributes.get('NDC', list())
        vac = attributes.get('VAC', list())
        va_generic_name = attributes.get('VA_GENERIC_NAME', list())
        parent_class = attributes.get('PARENT_CLASS', list())
        va_dispense_unit = attributes.get('VA_DISPENSE_UNIT', list())
        ddf = attributes.get('DDF', list())

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_xref_edges(node_curie, cuis, provided_by)

    def process_umls_item(self, node_id, info, umls_code):
        node_curie, iri, name, category, provided_by, synonyms, description, cuis, tuis = self.get_basic_info(umls_code, node_id, info)
        if node_curie == None:
            return

        if category == kg2_util.BIOLINK_CATEGORY_DRUG and "T109" in tuis:
            category = kg2_util.BIOLINK_CATEGORY_CHEMICAL_ENTITY

        if category == kg2_util.BIOLINK_CATEGORY_NAMED_THING and tuis == ["T028"] and ("gene" in name.lower() or "allele" in name.lower()):
            category = kg2_util.BIOLINK_CATEGORY_GENE

        self.make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, self.create_description(tuis, description))
        self.create_umls_edges(node_curie, info.get(self.RELATIONS_KEY, dict()))
