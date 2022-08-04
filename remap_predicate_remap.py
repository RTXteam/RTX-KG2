#! /usr/bin/venv python3

"""
    Purpose: Remap entries in predicate_remap.yaml according to biolink_model 3.0
"""
from collections import OrderedDict

import yaml


OUTPUT_FILE_PATH = "predicate_remap_biolink_3.0.yaml"
BIOLINK_MODEL_FILE_PATH = "biolink-model.yaml"
PREDICATE_REMAP_OLD_FILE_PATH = "predicate_remap.yaml"
QUALIFIER_MAPPING_DICT = {"biolink:negatively_regulates": """  
  core_predicate: biolink:regulates
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: activity_or_abundance
    - object_direction: decreased
""",
                          "biolink:positively_regulates": """  
  core_predicate: biolink:regulates
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: activity_or_abundance
    - object_direction: increased
""",
                          "biolink:affects_abundance_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: abundance
""",
                          "biolink:decreases_abundance_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers: 
    - object_aspect: abundance
    - object_direction: decreased
""",
                          "biolink:decreases_synthesis_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers: 
    - object_aspect: synthesis
    - object_direction: decreased
""",
                          "biolink:decreases_expression_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers: 
    - object_aspect: expression
    - object_direction: decreased
""",
                          "biolink:increases_degradation_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers: 
    - object_aspect: degradation
    - object_direction: increased
""",
                          "biolink:increases_abundance_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: abundance
    - object_direction: increased
""",
                          "biolink:increases_synthesis_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: synthesis
    - object_direction: increased
""",
                          "biolink:increases_expression_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: expression
    - object_direction: increased
""",
                          "biolink:decreases_degradation_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: degradation
    - object_direction: decreased
""",
                          "biolink:affects_synthesis_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: synthesis
""",
                          "biolink:affects_expression_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: expression
""",
                          "biolink:affects_degradation_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: degradation
""",
                          "biolink:affects_activity_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: activity
""",
                          "biolink:decreases_activity_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: activity
    - object_direction: decreased
""",
                          "biolink:increases_activity_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: activity
    - object_direction: increased
""",
                          "biolink:affects_expression_in": """
  core_predicate: biolink:affects
""",
                          "biolink:affects_folding_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: folding
""",
                          "biolink:decreases_folding_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: folding
    - object_direction: decreased
""",
                          "biolink:increases_folding_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: folding
    - object_direction: increased
""",
                          "biolink:affects_localization_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: localization
""",
                          "biolink:decreases_localization_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: localization
    - object_direction: decreased
""",
                          "biolink:increases_localization_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: localization
    - object_direction: increased
""",
                          "biolink:affects_metabolic_processing_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: processing
""",
                          "biolink:decreases_metabolic_processing_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: localization
    - object_direction: decreased
""",
                          "biolink:increases_metabolic_processing_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: localization
    - object_direction: increased
""",
                          "biolink:affects_molecular_modification_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: molecular_modification
""",
                          "biolink:decreases_molecular_modification_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: molecular_modification
    - object_direction: decreased
""",
                          "biolink:increases_molecular_modification_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: molecular_modification
    - object_direction: increased
""",
                          "biolink:affects_mutation_rate_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: mutation_rate
""",
                          "biolink:decreases_mutation_rate_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: mutation_rate
    - object_direction: decreased
""",
                          "biolink:increases_mutation_rate_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: mutation_rate
    - object_direction: increased
""",
                          "biolink:affects_splicing_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: splicing
""",
                          "biolink:decreases_splicing_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: splicing
    - object_direction: decreased
""",
                          "biolink:increases_splicing_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: splicing
    - object_direction: increased
""",
                          "biolink:affects_stability_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: stability
""",
                          "biolink:decreases_stability_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: stability
    - object_direction: decreased
""",
                          "biolink:increases_stability_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: stability
    - object_direction: increased
""",
                          "biolink:affects_transport_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: transport
""",
                          "biolink:decreases_transport_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: transport
    - object_direction: decreased
""",
                          "biolink:increases_transport_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: transport
    - object_direction: increased
""",
                          "biolink:affects_uptake_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: uptake
""",
                          "biolink:decreases_uptake_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: uptake
    - object_direction: decreased
""",
                          "biolink:increases_uptake_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: uptake
    - object_direction: increased
""",
                          "biolink:affects_secretion_of": """
  core_predicate: biolink:affects
  qualifiers:
    - object_aspect: secretion
""",
                          "biolink:decreases_secretion_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: secretion
    - object_direction: decreased
""",
                          "biolink:increases_secretion_of": """
  core_predicate: biolink:affects
  qualified_predicate: biolink:causes
  qualifiers:
    - object_aspect: secretion
    - object_direction: increased
"""
                          }


def get_mapped_predicates():
    # Get info from the existing predicate-remap.yaml
    # Note yaml.full_load does not retain comments
    with open(PREDICATE_REMAP_OLD_FILE_PATH, "r") as fp:
        predicate_remap_dict = yaml.full_load(fp)

    for key, value_dict in predicate_remap_dict.items():
        for operation, values in value_dict.items():
            # disregards current "keep" operation, changes "rename" to "keep
            if operation == "rename":
                new_value = ["keep"]
            elif operation in ("invert", "delete"):
                new_value = [operation]

            # add biolink predicate to list
            if values is not None:
                new_value.append(values[1])
        predicate_remap_dict[key] = new_value

    return predicate_remap_dict


def get_biolink_predicates():
    with open(BIOLINK_MODEL_FILE_PATH, "r") as fp:
        # convert biolink-model.yaml into a dictionary
        biolink_dict = yaml.full_load(fp)

        # create a dict for valid predicates
        valid_dict = {}

        # create a dictionary for the remapped predicates
        predicates_dict = {}

        # iterate over the biolink dictionary to remap predicates
        # while also generating a list of predicates
        for biolink_key, biolink_value in biolink_dict["slots"].items():

            deprecated = False

            # build a dictionary of biolink predicates
            if biolink_key == "related to":
                valid_dict[biolink_key] = "keep"
            elif type(biolink_value) == dict and "is_a" in biolink_value.keys() \
                    and biolink_value["is_a"] in valid_dict.keys():
                if "inverse" in biolink_value.keys():
                    valid_dict[biolink_key] = "invert"
                else:
                    valid_dict[biolink_key] = "keep"

                # Add flag for deprecated
                if "deprecated" in biolink_value.keys():
                    deprecated = True

            # If key is in valid_dict, add it to `predicates_dict`
            if biolink_key in valid_dict.keys():
                for key, value_list in biolink_value.items():
                    # Map predicates to `related to`
                    if key in ("exact_mappings", "broad_mappings", "narrow_mappings") and value_list is not None:
                        # value_list is a list of predicates
                        for predicate in value_list:
                            if predicate not in predicates_dict:
                                operation = valid_dict[biolink_key]
                                biolink_predicate = "biolink:" + "_".join(biolink_key.split())
                                # Filter out undesired KPs
                                if predicate.split(":", 1)[0] not in ("SNOMED", "SNOMEDCT", "GAMMA"):
                                    if operation != "invert":
                                        predicates_dict[predicate] = [operation, biolink_predicate]
                                    else:
                                        invert_predicate = "biolink:" + "_".join(biolink_value["inverse"].split())
                                        predicates_dict[predicate] = [operation, invert_predicate]

                                    if deprecated:
                                        predicates_dict[predicate].append("deprecated")

        return predicates_dict


def remap_predicates(predicates_dict, predicate_map_dict):
    # print(predicate_map_dict)
    print(predicates_dict)

    # Add data from the old predicate_remap.yaml to the predicates dict
    for predicate, value_list in predicate_map_dict.items():
        if predicate not in predicates_dict:
            predicates_dict[predicate] = value_list

    ordered_dict = OrderedDict(sorted(predicates_dict.items()))

    with open(OUTPUT_FILE_PATH, "w") as ofp, open("remap.log", "w") as log:
        text = ""
        for key, value in ordered_dict.items():
            # print(f"{key} {value}")
            operation = value[0]
            if len(value) > 1:
                biolink_predicate = value[1]
            ofp.write(f"{key}: \n  operation: {operation}")  # (key + ":\n  operation: keep")
            # Check if the predicate is in the qualifiers dict and has a "keep" operation
            if operation == "keep" and biolink_predicate in QUALIFIER_MAPPING_DICT.keys():
                text = QUALIFIER_MAPPING_DICT[biolink_predicate]
            elif operation == "delete":
                text = "\n"
            else:
                text = "\n  core_predicate: " + biolink_predicate + "\n"

            # Write to log predicates that are deprecated but not covered in qualifier map
            if len(value) == 3 and value[1] not in QUALIFIER_MAPPING_DICT.keys():
                log.write(f"{key} {value[1]} {operation}\n")

            ofp.write(text)

    print("Completed")

    return


if __name__ == "__main__":
    predicates = get_biolink_predicates()
    mapped_predicates = get_mapped_predicates()
    remap_predicates(predicates, mapped_predicates)
