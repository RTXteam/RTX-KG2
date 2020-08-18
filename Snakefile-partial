rule Finish:
    input:
        stats_original = config['REPORT_FILE_FULL'],
        nodes_original = config['OUTPUT_NODES_FILE_FULL'],
        stats_simplify = config['SIMPLIFIED_REPORT_FILE_FULL'],
        nodes_simplify = config['SIMPLIFIED_OUTPUT_NODES_FILE_FULL'],
        kg_original = config['FINAL_OUTPUT_FILE_FULL'],
        kg_simplify = config['SIMPLIFIED_OUTPUT_FILE_FULL'],
        orphan = config['OUTPUT_FILE_ORPHAN_EDGES'],
        slim = config['SLIM_OUTPUT_FILE_FULL'],
        placeholder = config['BUILD_DIR'] + "/tsv_placeholder.empty"
    run:
        shell("gzip -f {input.nodes_original}")
        shell("gzip -f {input.nodes_simplify}")
        shell("gzip -f {input.kg_original}")
        shell("gzip -f {input.kg_simplify}")
        shell("gzip -f {input.slim}")
        shell("gzip -f {input.orphan}")
        shell("tar -czvf " + config['KG2_TSV_TARBALL'] + " " + config['KG2_TSV_DIR'])

#        shell(config['S3_CP_CMD'] + " {input.nodes_original}.gz s3://rtx-kg2-public")
#        shell(config['S3_CP_CMD'] + " {input.nodes_simplify}.gz s3://rtx-kg2-public")
#        shell(config['S3_CP_CMD'] + " {input.stats_original} s3://rtx-kg2-public")
#        shell(config['S3_CP_CMD'] + " {input.kg_original}.gz s3://rtx-kg2")
#        shell(config['S3_CP_CMD'] + " {input.kg_simplify}.gz s3://rtx-kg2")
#        shell(config['S3_CP_CMD'] + " {input.slim}.gz s3://rtx-kg2-public")
#        shell(config['S3_CP_CMD'] + " {input.stats_simplify} s3://rtx-kg2-public")
#        shell(config['S3_CP_CMD'] + " {input.orphan}.gz s3://rtx-kg2-public")
#        shell(config['S3_CP_CMD'] + " " + config['KG2_TSV_TARBALL'] + " s3://rtx-kg2-public")


rule ValidationTests:
    output:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    log:
        config['BUILD_DIR'] + "/run-validation-tests.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/run-validation-tests.sh > {log} 2>&1 && touch {output}"


rule UMLS:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['BUILD_DIR'] + "/umls-placeholder.empty"
    log:
        config['BUILD_DIR'] + "/extract-umls.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-umls.sh " + config['BUILD_DIR'] + " > {log} 2>&1 && touch {output}" 

rule SemMedDB:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['SEMMED_TUPLELIST_FILE']
    log:
        config['BUILD_DIR'] + "/extract-semmeddb.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-semmeddb.sh {output} " + config['TEST_FLAG'] + " > {log} 2>&1"

rule UniprotKB:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['UNIPROTKB_DAT_FILE']
    log:
        config['BUILD_DIR'] + "/extract-uniprotkb.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-uniprotkb.sh {output} > {log} 2>&1"

rule Ensembl:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['ENSEMBL_SOURCE_JSON_FILE']
    log:
        config['BUILD_DIR'] + "/extract-ensembl.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-ensembl.sh > {log} 2>&1"

rule UniChem:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['UNICHEM_OUTPUT_TSV_FILE']
    log:
        config['BUILD_DIR'] + "/extract-unichem.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-unichem.sh {output} > {log} 2>&1"

rule ChemBL:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        placeholder = config['BUILD_DIR'] + "/chembl-placeholder.empty"
    log:
        config['BUILD_DIR'] + "/extract-chembl.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-chembl.sh " + config['CHEMBL_MYSQL_DBNAME'] +" > {log} 2>&1 && touch {output.placeholder}"

rule NCBIGene:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['NCBI_GENE_TSV_FILE']
    log:
        config['BUILD_DIR'] + "/extract-ncbigene.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-ncbigene.sh {output} > {log} 2>&1"

rule DGIDB:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['DGIDB_DIR'] + "/interactions.tsv"
    log:
        config['BUILD_DIR'] + "/extract-dgidb.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-dgidb.sh " + config['DGIDB_DIR'] + " > {log} 2>&1"

rule RepoDB:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['REPODB_INPUT_FILE']
    log:
        config['BUILD_DIR'] + "/download-repodb-csv.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/download-repodb-csv.sh " + config['REPODB_DIR'] + " > {log} 2>&1"

rule SMPDB:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['SMPDB_INPUT_FILE']
    log:
        config['BUILD_DIR'] + "/extract-smpdb.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-smpdb.sh " + config['SMPDB_DIR'] + " > {log} 2>&1"

rule DrugBank:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['DRUGBANK_INPUT_FILE']
    log:
        config['BUILD_DIR'] + "/extract-drugbank.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-drugbank.sh {output} > {log} 2>&1"

rule HMDB:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['HMDB_INPUT_FILE']
    log:
        config['BUILD_DIR'] + "/extract-hmdb.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-hmdb.sh > {log} 2>&1"

rule GO_Annotations:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['GO_ANNOTATION_INPUT_FILE']
    log:
        config['BUILD_DIR'] + "/extract-go-annotations.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/extract-go-annotations.sh {output} > {log} 2>&1"

rule KG_One:
    input:
        config['BUILD_DIR'] + "/validation-placeholder.empty"
    output:
        config['KG1_OUTPUT_FILE']
    run:
        shell(config['S3_CP_CMD'] + " s3://rtx-kg2/" + config['RTX_CONFIG_FILE'] + " " + config['BUILD_DIR'] + "/" + config['RTX_CONFIG_FILE'])
        shell(config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/rtx_kg1_neo4j_to_kg_json.py " + config['TEST_ARG'] + " --configFile " + config['BUILD_DIR'] + "/" + config['RTX_CONFIG_FILE'] + " " + config['CURIES_TO_URLS_FILE'] + " {output}")

rule Ontologies_and_TTL:
    input:
        config['BUILD_DIR'] + "/umls-placeholder.empty"
    output:
        config['OUTPUT_FILE_FULL']
    log:
        config['BUILD_DIR'] + "/build-multi-owl-kg.log"
    shell:
        "bash -x " + config['CODE_DIR'] + "/build-multi-ont-kg.sh {output} " + config['TEST_FLAG'] + " > {log} 2>&1" 

rule NCBIGene_Conversion:
    input:
        config['NCBI_GENE_TSV_FILE']
    output:
        config['NCBI_GENE_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/ncbigene_tsv_to_kg_json.py " + config['TEST_ARG'] + " {input} {output}"

rule DGIDB_Conversion:
    input:
        config['DGIDB_DIR'] + "/interactions.tsv"
    output:
        config['DGIDB_OUTPUT_FILE']
    log:
        config['DGIDB_DIR'] + "/dgidb-tsv-to-kg-json-stderr.log"
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/dgidb_tsv_to_kg_json.py " + config['TEST_ARG'] + " {input} {output}" + " > {log} 2>&1"

rule ChemBL_Conversion:
    input:
        placeholder = config['BUILD_DIR'] + "/chembl-placeholder.empty"
    output:
        config['CHEMBL_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/chembl_mysql_to_kg_json.py " + config['TEST_ARG'] + " " + config['MYSQL_CONF'] + " " + config['CHEMBL_MYSQL_DBNAME'] + " {output}"

rule UniChem_Conversion:
    input:
        config['UNICHEM_OUTPUT_TSV_FILE']
    output:
        config['UNICHEM_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/unichem_tsv_to_edges_json.py " + config['TEST_ARG'] + " {input} {output}"

rule Ensembl_Conversion:
    input:
        config['ENSEMBL_SOURCE_JSON_FILE']
    output:
        config['ENSEMBL_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/ensembl_json_to_kg_json.py " + config['TEST_ARG'] + " {input} {output}"

rule SemMed_Conversion:
    input:
        config['SEMMED_TUPLELIST_FILE']
    output:
        config['SEMMED_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/semmeddb_tuple_list_json_to_kg_json.py " + config['TEST_ARG'] + " {input} {output}"

rule Uniprot_Conversion:
    input:
        config['UNIPROTKB_DAT_FILE']
    output:
        config['UNIPROTKB_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/uniprotkb_dat_to_json.py " + config['TEST_ARG'] + " {input} {output}"

rule RepodDB_Conversion:
    input:
        config['REPODB_INPUT_FILE']
    output:
        config['REPODB_OUTPUT_FILE']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/repodb_csv_to_kg_json.py " + config['TEST_ARG'] + " {input} {output}"

rule SMPDB_Conversion:
    input:
        config['SMPDB_INPUT_FILE']
    output:
        config['SMPDB_OUTPUT_FILE']
    log:
        config['SMPDB_DIR'] + "/smpdb-csv-to-kg-json.log"
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/smpdb_csv_to_kg_json.py " + config['TEST_ARG'] + " " + config['SMPDB_DIR'] + " {output} > {log} 2>&1"

rule DrugBank_Conversion:
    input:
        config['DRUGBANK_INPUT_FILE']
    output:
        config['DRUGBANK_OUTPUT_FILE']
    log:
        config['BUILD_DIR'] + "/drugbank-xml-to-kg-json.log"
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/drugbank_xml_to_kg_json.py " + config['TEST_ARG'] + " {input} {output} > {log} 2>&1"

rule HMDB_Conversion:
    input:
        config['HMDB_INPUT_FILE']
    output:
        config['HMDB_OUTPUT_FILE']
    log:
        config['BUILD_DIR'] + "/hmdb-xml-to-kg-json.log"
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/hmdb_xml_to_kg_json.py " + config['TEST_ARG'] + " {input} {output} > {log} 2>&1"

rule GO_Annotations_Conversion:
    input:
        config['GO_ANNOTATION_INPUT_FILE']
    output:
        config['GO_ANNOTATION_OUTPUT_FILE']
    log:
        config['BUILD_DIR'] + "/go-gpa-to-kg-json.log"
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/go_gpa_to_kg_json.py " + config['TEST_ARG'] + " {input} {output} > {log} 2>&1"
        
rule Merge:
    input:
        owl = config['OUTPUT_FILE_FULL'],
        uniprot = config['UNIPROTKB_OUTPUT_FILE'],
        semmeddb = config['SEMMED_OUTPUT_FILE'],
        chembl = config['CHEMBL_OUTPUT_FILE'],
        ensembl = config['ENSEMBL_OUTPUT_FILE'],
        unichem = config['UNICHEM_OUTPUT_FILE'],
        ncbigene = config['NCBI_GENE_OUTPUT_FILE'],
        dgidb = config['DGIDB_OUTPUT_FILE'],
        kg_one = config['KG1_OUTPUT_FILE'],
        repoddb = config['REPODB_OUTPUT_FILE'],
        drugbank = config['DRUGBANK_OUTPUT_FILE'],
        smpdb = config['SMPDB_OUTPUT_FILE'],
        hmdb = config['HMDB_OUTPUT_FILE'],
        go_annotations = config['GO_ANNOTATION_OUTPUT_FILE']
    output:
        full = config['FINAL_OUTPUT_FILE_FULL'],
        orph = config['OUTPUT_FILE_ORPHAN_EDGES']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/merge_graphs.py " + config['TEST_ARG'] + " --kgFiles {input.owl} {input.uniprot} {input.semmeddb} {input.chembl} {input.ensembl} {input.unichem} {input.ncbigene} {input.dgidb} {input.kg_one} {input.repoddb} {input.drugbank} {input.smpdb} {input.hmdb} {input.go_annotations} --kgFileOrphanEdges {output.orph} {output.full}"

rule Nodes:
    input:
        real = config['FINAL_OUTPUT_FILE_FULL'],
        placeholder = config['REPORT_FILE_FULL']
    output:
        config['OUTPUT_NODES_FILE_FULL']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/get_nodes_json_from_kg_json.py " + config['TEST_ARG'] + " {input.real} {output}"

rule Stats:
    input:
        config['FINAL_OUTPUT_FILE_FULL']
    output:
        config['REPORT_FILE_FULL']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/report_stats_on_json_kg.py {input} {output}"

rule Simplify:
    input:
        real = config['FINAL_OUTPUT_FILE_FULL'],
        placeholder = config['OUTPUT_NODES_FILE_FULL']
    output:
        config['SIMPLIFIED_OUTPUT_FILE_FULL']
    log:
        config['BUILD_DIR'] + "/filter_kg_and_remap_predicates.log"
    run:
        shell("bash -x " + config['CODE_DIR'] + "/version.sh " + config['VERSION_FILE'] + " " + code['TEST_FLAG'] + " > {log} 2>&1")
        shell(config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/filter_kg_and_remap_predicates.py " + config['TEST_ARG'] + " --dropNegated --dropSelfEdgesExcept interacts_with,positively_regulates,inhibits,increase " + config['PREDICATE_MAPPING_FILE'] + " " + config['CURIES_TO_URLS_FILE'] + " {input.real} {output} " + config['VERSION_FILE'] + " >> {log} 2>&1")

rule Simplify_Nodes:
    input:
        config['SIMPLIFIED_OUTPUT_FILE_FULL']
    output:
        config['SIMPLIFIED_OUTPUT_NODES_FILE_FULL']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/get_nodes_json_from_kg_json.py " + config['TEST_ARG'] + " {input} {output}"

rule Slim:
    input:
        real = config['SIMPLIFIED_OUTPUT_FILE_FULL'],
        placeholder = config['SIMPLIFIED_OUTPUT_NODES_FILE_FULL']
    output:
        config['SLIM_OUTPUT_FILE_FULL']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/slim_kg2.py " + config['TEST_ARG'] + " {input.real} {output}"

rule Simplify_Stats:
    input:
        real = config['SIMPLIFIED_OUTPUT_FILE_FULL'],
        placeholder = config['SLIM_OUTPUT_FILE_FULL']
    output:
        config['SIMPLIFIED_REPORT_FILE_FULL']
    shell:
        config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/report_stats_on_json_kg.py --useSimplifiedPredicates {input.real} {output}"

rule TSV:
    input:
        real = config['SIMPLIFIED_OUTPUT_FILE_FULL'],
        placeholder = config['SIMPLIFIED_REPORT_FILE_FULL']
    output:
        placeholder = config['BUILD_DIR'] + "/tsv_placeholder.empty"
    run:
        shell("rm -rf " + config['KG2_TSV_DIR'])
        shell("mkdir -p " + config['KG2_TSV_DIR'])
        shell(config['VENV_DIR'] + "/bin/python3 -u " + config['CODE_DIR'] + "/kg_json_to_tsv.py {input.real} " + config['KG2_TSV_DIR'])
        shell("touch {output.placeholder}")

