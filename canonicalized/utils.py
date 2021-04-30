import textstat
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('dmis-lab/biobert-v1.1')
import numpy as np
import re

class select_best_description:
    '''
    This class is used to select the best description for the preferred curie in KG2c based on three rules (the length of description, 
    the number of detected human-readable words from biobert model and the estimated school grade level returned from textstat.text_standard[
    https://github.com/shivam5992/textstat]). For each rule, each candicate description is assigned a score based on its rank in this rule. 
    For example, based on the length of description, the longest description is assigned 0, the second longest one is assigned 1 and so on. 
    Then the final ranking score for each description is the summation of all scores from three rules. The 'best' description is the one with 
    the lowest score. 
    '''
    #### Constructor
    def __init__(self, desc_list):
        self.desc_list = list(set([x if x is not None else '' for x in desc_list]))

    @staticmethod
    def _call_biobert_tokenizer(desc, len_limit=3):
        '''
        Convert a description text to token via biotokenizer
        parameter desc[string]: description text
        paramter len_limit[int]: at least token length to be considered as an effective token
        '''
        if type(desc) is str:
            desc = desc.replace('UMLS Semantic Type:','').replace('UMLS_STY:','')
            return [token for token in tokenizer.tokenize(desc) if not '#' in token and token.isalpha() and len(token)>=len_limit]
        else:
            raise TypeError(f"'desc' should be str but {type(desc)} detected")

    @staticmethod
    def _call_textstat(desc):
        '''
        Get an estimated school grade level required to understand the text from textstat package (reference: https://github.com/shivam5992/textstat)
        parameter desc[string]: description text
        '''
        if type(desc) is str:
            desc = desc.replace('UMLS Semantic Type:','').replace('UMLS_STY:','')
            res = textstat.text_standard(desc)
            grade = int(re.sub('[a-z]','',res.split(' ')[0]))
            return grade
        else:
            raise TypeError(f"'desc' should be str but {type(desc)} detected")

    #### Get the socres based on the length of description
    @property
    def get_length_score(self):
        if 'length_score' in self.__dict__:
            return self.length_score
        else:
            self._desc_length = {x:len(x.replace('UMLS Semantic Type:','').replace('UMLS_STY:','')) for x in self.desc_list}
            self.length_score = {desc: index for index, (desc, _) in enumerate(sorted(self._desc_length.items(), key=lambda item: item[1], reverse=True))}
            return self.length_score

    #### Get the socres based on the number of detected human-readable words from biobert model
    @property
    def get_word_num_score(self):
        if 'word_num_score' in self.__dict__:
            return self.word_num_score
        else:
            self._desc_detected_word_num = {x:len(self._call_biobert_tokenizer(x)) for x in self.desc_list}
            self.word_num_score = {desc: index for index, (desc, _) in enumerate(sorted(self._desc_detected_word_num.items(), key=lambda item: item[1], reverse=True))}
            return self.word_num_score

    #### Get the socres based on the estimated school grade level returned from textstat.text_standard
    @property
    def get_readability_level_score(self):
        if 'readability_level_score' in self.__dict__:
            return self.readability_level_score
        else:
            self._desc_school_grade_level = {x:self._call_textstat(x) for x in self.desc_list}
            self.readability_level_score = {desc: index for index, (desc, _) in enumerate(sorted(self._desc_school_grade_level.items(), key=lambda item: item[1], reverse=False))}
            return self.readability_level_score

    #### Get the final socres based on three rules
    @property
    def get_final_score(self):
        if 'final_score' in self.__dict__:
            return self.final_score 
        else:
            length_score = self.get_length_score
            word_num_score = self.get_word_num_score
            readability_level_score = self.get_readability_level_score
            self._sum_score = {key:length_score[key]+word_num_score[key]+readability_level_score[key] for key in length_score}
            self.final_score = {desc: index for index, (desc, _) in enumerate(sorted(self._sum_score.items(), key=lambda item: item[1], reverse=False))}
            return self.final_score

    #### Get the best description with the lowest score
    @property
    def get_best_description(self):
        if len(self.desc_list) == 0:
            return None
        elif len(self.desc_list) == 1:
            return self.desc_list[0]
        else:
            final_score = self.get_final_score
            for desc in final_score:
                if desc != '':
                    return desc
                else:
                    next
            return self.desc_list[0]