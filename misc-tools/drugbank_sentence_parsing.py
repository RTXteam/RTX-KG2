#!/usr/bin/env python3
''' drugbank_sentence_parsing.py: identify the common substrings in DrugBank sentences

    Usage: drugbank_sentence_parsing.py <inputFile.txt> 
        <outputFile.json>
'''

import json
import argparse

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

KEY_PREFIX = "KEY_"
MAIN_DRUG_KEY = KEY_PREFIX + "maindrug"
INTERACTION_DRUG_KEY = KEY_PREFIX + "interactiondrug"
ACTIVITY_KEY = KEY_PREFIX + "activity"
DISEASE_KEY = KEY_PREFIX + "disease"

SENTENCE_MAP = {"risk_or_severity_increase": ["The risk or severity of ", DISEASE_KEY, " can be increased when ", MAIN_DRUG_KEY, " is combined with ", INTERACTION_DRUG_KEY],
                "risk_or_severity_decrease": ["The risk or severity of ", DISEASE_KEY, " can be decreased when ", MAIN_DRUG_KEY, " is combined with ", INTERACTION_DRUG_KEY],
                "may_impact_activity_increase": [MAIN_DRUG_KEY, " may increase the ", ACTIVITY_KEY, " activities of ", INTERACTION_DRUG_KEY],
                "may_impact_activity_decrease": [MAIN_DRUG_KEY, " may decrease the ", ACTIVITY_KEY, " activities of ", INTERACTION_DRUG_KEY],
                "therapeutic_efficacy_increase": ["The therapeutic efficacy of ", INTERACTION_DRUG_KEY, " can be increased when used in combination with ", MAIN_DRUG_KEY],
                "therapeutic_efficacy_decrease": ["The therapeutic efficacy of ", INTERACTION_DRUG_KEY, " can be decreased when used in combination with ", MAIN_DRUG_KEY],
                "higher_serum_level": [MAIN_DRUG_KEY, " may decrease the excretion rate of ", INTERACTION_DRUG_KEY, " which could result in a higher serum level"],
                "metabolism_increase": ["The metabolism of ", MAIN_DRUG_KEY, " can be increased when combined with ", INTERACTION_DRUG_KEY],
                "metabolism_decrease": ["The metabolism of ", MAIN_DRUG_KEY, " can be decreased when combined with ", INTERACTION_DRUG_KEY],
                "serum_concentration_increase": ["The serum concentration of ", MAIN_DRUG_KEY, " can be increased when it is combined with ", INTERACTION_DRUG_KEY],
                "serum_concentration_decrease": ["The serum concentration of ", MAIN_DRUG_KEY, " can be decreased when it is combined with ", INTERACTION_DRUG_KEY],
                "excretion_rate_increase": [INTERACTION_DRUG_KEY, " may increase the excretion rate of ", MAIN_DRUG_KEY, " which could result in a lower serum level and potentially a reduction in efficacy"],
                "absorption_decrease": [INTERACTION_DRUG_KEY, " can cause a decrease in the absorption of ", MAIN_DRUG_KEY, " resulting in a reduced serum concentration and potentially a decrease in efficacy"],
                "excretion_increase": ["The excretion of ", MAIN_DRUG_KEY, " can be increased when combined with ", INTERACTION_DRUG_KEY],
                "excretion_decrease": ["The excretion of ", MAIN_DRUG_KEY, " can be decreased when combined with ", INTERACTION_DRUG_KEY],
                "active_metabolites_increase": ["The serum concentration of the active metabolites of ", INTERACTION_DRUG_KEY, " can be increased when ", INTERACTION_DRUG_KEY, " is used in combination with ", MAIN_DRUG_KEY],
                "active_metabolites_decrease": ["The serum concentration of the active metabolites of ", INTERACTION_DRUG_KEY, " can be decreased when ", INTERACTION_DRUG_KEY, " is used in combination with ", MAIN_DRUG_KEY],
                "bioavailibility_decrease": ["The bioavailability of ", MAIN_DRUG_KEY, " can be decreased when combined with ", INTERACTION_DRUG_KEY],
                "bioavailibility_increase": ["The bioavailability of ", MAIN_DRUG_KEY, " can be increased when combined with ", INTERACTION_DRUG_KEY],
                "diagnostic_agent_effectiveness_decrease": [INTERACTION_DRUG_KEY, " may decrease effectiveness of ", MAIN_DRUG_KEY, " as a diagnostic agent"],
                "absorption_increase": [MAIN_DRUG_KEY, " can cause an increase in the absorption of ", INTERACTION_DRUG_KEY, " resulting in an increased serum concentration and potentially a worsening of adverse effects"],
                "diagnostic_agent_effectiveness_increase": [INTERACTION_DRUG_KEY, " may increase effectiveness of ", MAIN_DRUG_KEY, " as a diagnostic agent"],
                "absorption_of_decreased": ["The absorption of ", INTERACTION_DRUG_KEY, " can be decreased when combined with ", MAIN_DRUG_KEY],
                "protein_binding_decrease": ["The protein binding of ", INTERACTION_DRUG_KEY, " can be decreased when combined with ", MAIN_DRUG_KEY],
                "hypersensitivity_reaction_increase": ["The risk of a hypersensitivity reaction to ", INTERACTION_DRUG_KEY, " is increased when it is combined with ", MAIN_DRUG_KEY],
                "serum_concentration_of_active_metabolites": ["The serum concentration of the active metabolites of ", MAIN_DRUG_KEY, " can be reduced when ", MAIN_DRUG_KEY, " is used in combination with ", INTERACTION_DRUG_KEY, " resulting in a loss in efficacy"],
                "serum_concentration_increased_in_combination": ["The serum concentration of ", INTERACTION_DRUG_KEY, ", an active metabolite of ", MAIN_DRUG_KEY, ", can be increased when used in combination with ", MAIN_DRUG_KEY],
                "serum_concentration_decreased_in_combination": ["The serum concentration of ", INTERACTION_DRUG_KEY, ", an active metabolite of ", MAIN_DRUG_KEY, ", can be decreased when used in combination with ", MAIN_DRUG_KEY]
                }

def get_args():
    description = 'drugbank_sentence_parsing.py: \
                    parse the DrugBank drug interaction information'
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('--test',
                            dest='test',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('inputFile', type=str)

    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()

def map_sentence(sentence):
    sentence = sentence.strip().strip('.')
    for sentence_type in SENTENCE_MAP:
        working_sentence = sentence
        sentence_form = SENTENCE_MAP[sentence_type]
        form_length = len(sentence_form)

        sentence_parsed = dict()
        current_key = ""
        current_val = ""

        broken = False

        for index in range(form_length):
            element = sentence_form[index]
            if element.startswith(KEY_PREFIX):
                current_key = element.replace(KEY_PREFIX, "")

                if index == form_length - 1:
                    sentence_parsed[current_key] = working_sentence
                else:
                    split_sentence = working_sentence.split(sentence_form[index + 1])
                    sentence_parsed[current_key] = split_sentence[0]
                working_sentence = working_sentence.replace(sentence_parsed[current_key], '')
            else:
                if not working_sentence.startswith(element):
                    broken = True
                    break
                working_sentence = working_sentence.replace(element, '')

        if not broken:
            return sentence_type, sentence_parsed

    return None, None

if __name__ == '__main__':
    args = get_args()

    sentence_count = 0

    sentence_type_counts = dict()

    output_str = ""

    test_lines = ["The risk or severity of methemoglobinemia can be increased when Enmetazobactam is combined with Articaine."]

    with open(args.inputFile) as input_file:
        for line in input_file:
            sentence_count += 1
            sentence_type, sentence_parsed = map_sentence(line)

            if sentence_type is None:
                print(line.strip())
            else:
                if sentence_type not in sentence_type_counts:
                    sentence_type_counts[sentence_type] = 0
                sentence_type_counts[sentence_type] += 1
                output_str += sentence_type + str(sentence_parsed) + "\n"
            

    with open(args.outputFile, 'w+') as output_file:
        output_file.write(output_str)

        print(json.dumps(sentence_type_counts, sort_keys=True, indent=4))