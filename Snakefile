rule UMLS:
    output:
        "kg2-build/umls-placeholder.empty"
    shell:
        "kg2-code/extract-umls.sh && touch {output}" 

rule SemMedDB:
    output:
        "kg2-build/semmeddb/kg2-semmeddb-tuplelist.json"
    shell:
        "kg2-code/extract-semmeddb.sh {output} " + config['test'] + ""

rule UniprotKB:
    output:
        "kg2-build/uniprotkb/uniprot_sprot.dat"
    shell:
        "kg2-code/extract-uniprotkb.sh {output}"

rule Ensembl:
    output:
        "kg2-build/ensembl/ensembl_genes_homo_sapiens.json"
    shell:
        "kg2-code/extract-ensembl.sh"

rule UniChem:
    output:
        "kg2-build/unichem/chembl-to-curies.tsv"
    shell:
        "kg2-code/extract-unichem.sh"

rule ChemBL:
    output:
        placeholder = "kg2-build/chembl-placeholder.empty"
    shell:
        "kg2-code/extract-chembl.sh chembl && touch {output.placeholder}"

rule NCBIGene:
    output:
        "kg2-build/ncbigene/Homo_sapiens_gene_info.tsv"
    shell:
        "kg2-code/extract-ncbigene.sh"

rule DGIDB:
    output:
        "kg2-build/dgidb/interactions.tsv"
    shell:
        "kg2-code/extract-dgidb.sh"

rule KG_One:
    output:
        "kg2-build/kg2-rtx-kg1.json"
    run:
        shell("aws s3 cp --no-progress --region us-west-2 s3://rtx-kg2/RTXConfiguration-config.json kg2-build/RTXConfiguration-config.json")
        shell("kg2-venv/bin/python3 -u kg2-code/rtx_kg1_neo4j_to_kg_json.py " + config['testdd'] + " --configFile kg2-build/RTXConfiguration-config.json {output}")

rule Ontologies_and_TTL:
    input:
        "kg2-build/umls-placeholder.empty"
    output:
        "kg2-build/kg2-owl" + config['testd'] + ".json"
    shell:
        "kg2-code/build-multi-owl-kg.sh ~/{output} " + config['test'] + "" 

rule NCBIGene_Conversion:
    input:
        "kg2-build/ncbigene/Homo_sapiens_gene_info.tsv"
    output:
        "kg2-build/kg2-ncbi.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/ncbigene_tsv_to_kg_json.py " + config['testdd'] + " --inputFile {input} --outputFile {output}"

rule DGIDB_Conversion:
    input:
        "kg2-build/dgidb/interactions.tsv"
    output:
        "kg2-build/kg2-dgidb.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/dgidb_tsv_to_kg_json.py " + config['testdd'] + " --inputFile {input} --outputFile {output}"

rule ChemBL_Conversion:
    input:
        placeholder = "kg2-build/chembl-placeholder.empty"
    output:
        "kg2-build/kg2-chembl.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/chembl_mysql_to_kg_json.py " + config['testdd'] + " --mysqlConfigFile ~/kg2-build/mysql-config.conf --mysqlDBName chembl --outputFile {output}"

rule UniChem_Conversion:
    input:
        "kg2-build/unichem/chembl-to-curies.tsv"
    output:
        "kg2-build/kg2-unichem.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/unichem_tsv_to_edges_json.py " + config['testdd'] + " --inputFile {input} --outputFile {output}"

rule Ensembl_Conversion:
    input:
        "kg2-build/ensembl/ensembl_genes_homo_sapiens.json"
    output:
        "kg2-build/kg-ensembl.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/ensembl_json_to_kg_json.py --inputFile {input} --outputFile {output} " + config['testdd'] + ""

rule SemMed_Conversion:
    input:
        "kg2-build/semmeddb/kg2-semmeddb-tuplelist.json"
    output:
        "kg2-build/kg2-semmeddb-edges.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/semmeddb_tuple_list_json_to_kg_json.py " + config['testdd'] + " --inputFile {input} --outputFile {output}"

rule Uniprot_Conversion:
    input:
        "kg2-build/uniprotkb/uniprot_sprot.dat"
    output:
        "kg2-build/kg2-uniprotkb.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/uniprotkb_dat_to_json.py " + config['testdd'] + " --inputFile {input} --outputFile {output}"
        
rule Merge:
    input:
        owl = "kg2-build/kg2-owl" + config['testd'] + ".json",
        uniprot = "kg2-build/kg2-uniprotkb.json",
        semmeddb = "kg2-build/kg2-semmeddb-edges.json",
        chembl = "kg2-build/kg2-chembl.json",
        ensembl = "kg2-build/kg2-ensembl.json",
        unichem = "kg2-build/kg2-unichem.json",
        ncbigene = "kg2-build/kg2-ncbi.json",
        dgidb = "kg2-build/kg2-dgidb.json",
        kg_one = "kg2-build/kg2-rtx-kg1.json"

    output:
        full = "kg2-build/kg2" + config['testd'] + ".json",
        orph = "kg2-build/kg2-orphans-edges" + config['testd'] + ".json"
    shell:
        "kg2-venv/bin/python3 kg2-code/merge_graphs.py --kgFiles {input.owl} {input.uniprot} {input.semmeddb} {input.chembl} {input.ensembl} {input.unichem} {input.ncbigene} {input.dgidb} {input.kg_one} --outputFile {output.full} --kgFileOrphanEdges {output.orph}"

rule Nodes:
    input:
        real = "kg2-build/kg2" + config['testd'] + ".json",
        placeholder = "kg2-build/kg2-report" + config['testd'] + ".json"
    output:
        "kg2-build/kg2-nodes" + config['testd'] + ".json"
    shell:
        "kg2-venv/bin/python3 kg2-code/get_nodes_json_from_kg_json.py --inputFile {input.real} --outputFile {output}"

rule Stats:
    input:
        "kg2-build/kg2" + config['testd'] + ".json"
    output:
        "kg2-build/kg2-report" + config['testd'] + ".json"
    shell:
        "kg2-venv/bin/python3 kg2-code/report_stats_on_json_kg.py --inputFile {input} --outputFile {output}"

rule TSV:
    input:
        real = "kg2-build/kg2" + config['testd'] + ".json",
        placeholder = "kg2-build/kg2-nodes" + config['testd'] + ".json"
    output:
        placeholder = "kg2-build/tsv_placeholder.empty"
    shell:
        "mkdir -p kg2-build/TSV/ && kg2-venv/bin/python3 kg_json_to_tsv.py --inputFile {input.real} --outputFileLocation kg2-build/TSV/ && touch {output.placeholder}"

rule Finish:
    input:
        stats = "kg2-build/kg2-report" + config['testd'] + ".json",
        nodes ="kg2-build/kg2-nodes" + config['testd'] + ".json",
        full = "kg2-build/kg2" + config['testd'] + ".json",
        orphan = "kg2-build/kg2-orphans-edges" + config['testd'] + ".json",
        placeholder = "kg2-build/tsv_placeholder.empty"
    run:
        shell("gzip -f {input.nodes}")
        shell("gzip -f {input.full}")
        shell("gzip -f {input.orphan}")
        shell("tar -czvf kg2-build/kg2_tsv" + config['testd'] + ".tar.gz kg2-build/TSV")

        shell("aws s3 cp --no-progress --region us-west-2 {input.nodes}.gz s3://rtx-kg2-public")
        shell("aws s3 cp --no-progress --region us-west-2 {input.full}.gz s3://rtx-kg2-public")
        shell("aws s3 cp --no-progress --region us-west-2 {input.stats} s3://rtx-kg2-public")
        shell("aws s3 cp --no-progress --region us-west-2 {input.orphan}.gz s3://rtx-kg2-public")
        shell("aws s3 cp --no-progress --region us-west-2 kg2-build/kg2_tsv" + config['testd'] + ".tar.gz s3://rtx-kg2-public")
