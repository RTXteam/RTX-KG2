rule UMLS:
    output:
        "kg2-build/umls-placeholder.empty"
    shell:
        "kg2-code/extract-umls.sh && touch {output}" 

rule SemMedDB:
    output:
        "kg2-build/kg2-semmeddb-tuplelist.json"
    shell:
        "kg2-code/extract-semmeddb.sh {output}"

rule UniprotKB:
    output:
        "kg2-build/uniprot_sprot.dat"
    shell:
        "kg2-code/extract-uniprotkb.sh"

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

rule Ontologies_and_TTL:
    input:
        "kg2-build/umls-placeholder.empty"
    output:
        "kg2-build/kg2-owl.json"
    shell:
        "kg2-code/build-multi-owl-kg.sh ~/{output}" 

rule NCBIGene_Conversion:
    input:
        "kg2-build/ncbigene/Homo_sapiens_gene_info.tsv"
    output:
        "kg2-build/ncbi.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/ncbigene_tsv_to_kg_json.py --inputFile {input} --outputFile {output}"

rule DGIDB_Conversion:
    input:
        "kg2-build/dgidb/interactions.tsv"
    output:
        "kg2-build/dgidb.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/dgidb_tsv_to_kg_json.py --inputFile {input} --outputFile {output}"

rule ChemBL_Conversion:
    input:
        placeholder = "kg2-build/chembl-placeholder.empty"
    output:
        "kg2-build/chembl.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/chembl_mysql_to_kg_json.py --mysqlConfigFile ~/kg2-build/mysql-config.conf --mysqlDBName chembl --outputFile {output}"

rule UniChem_Conversion:
    input:
        "kg2-build/unichem/chembl-to-curies.tsv"
    output:
        "kg2-build/unichem.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/unichem_tsv_to_edges_json.py  --inputFile {input} --outputFile {output}"

rule Ensembl_Conversion:
    input:
        "kg2-build/ensembl/ensembl_genes_homo_sapiens.json"
    output:
        "kg2-build/ensembl.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/ensembl_json_to_kg_json.py --inputFile {input} --outputFile {output}"

rule SemMed_Conversion:
    input:
        "kg2-build/kg2-semmeddb-tuplelist.json"
    output:
        "kg2-build/kg2-semmeddb-edges.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/semmeddb_tuple_list_json_to_edges_json.py --inputFile {input} --outputFile {output}"

rule Uniprot_Conversion:
    input:
        "kg2-build/uniprot_sprot.dat"
    output:
        "kg2-build/kg2-uniprotkb.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/uniprotkb_dat_to_json.py --inputFile {input} --outputFile {output}"
        
rule Merge:
    input:
        o = "kg2-build/kg2-owl.json",
        t = "kg2-build/kg2-uniprotkb.json",
        r = "kg2-build/kg2-semmeddb-edges.json",
        c = "kg2-build/chembl.json",
        e = "kg2-build/ensembl.json",
        u = "kg2-build/unichem.json",
        ncbigene = "kg2-build/ncbi.json",
        dgidb = "kg2-build/dgidb.json"

    output:
        f = "kg2-build/full_kg.json",
        orph = "kg2-build/orphan_edges.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/merge_graphs.py --kgFiles {input.o} {input.t} {input.r} {input.c} {input.e} {input.u} {input.ncbigene} {input.dgidb} --outputFile {output.f} --kgFileOrphanEdges {output.orph}"

rule Nodes:
    input:
        real = "kg2-build/full_kg.json",
        placeholder = "kg2-build/stats_kg.json"
    output:
        "kg2-build/nodes_kg.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/get_nodes_json_from_kg_json.py --inputFile {input.real} --outputFile {output}"

rule Stats:
    input:
        "kg2-build/full_kg.json"
    output:
        "kg2-build/stats_kg.json"
    shell:
        "kg2-venv/bin/python3 kg2-code/report_stats_on_kg.py --inputFile {input} --outputFile {output}"

rule Finish:
    input:
        o = "kg2-build/stats_kg.json",
        t ="kg2-build/nodes_kg.json",
        r = "kg2-build/full_kg.json",
        f = "kg2-build/orphan_edges.json"
    run:
        shell("gzip -f {input.t}")
        shell("gzip -f {input.r}")
        shell("gzip -f {input.f}")

        #shell("aws s3 cp --no-progress --region us-west-2 {input.t}.gz s3://rtx-kg2-public")
        #shell("aws s3 cp --no-progress --region us-west-2 {input.r}.gz s3://rtx-kg2-public")
        #shell("aws s3 cp --no-progress --region us-west-2 {input.o} s3://rtx-kg2-public")
        #shell("aws s3 cp --no-progress --region us-west-2 {input.f} s3://rtx-kg2-public")
onsuccess:
    shell("mail -s 'Snake file has completed!' -r example@gmail.com example@gmail.com < {log}")
onerror:
    shell("mail -s 'Snake file has failed!' -r example@gmail.com example@gmail.com < {log}")
