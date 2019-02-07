#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from parlai.core.teachers import FixedDialogTeacher, DialogTeacher, ParlAIDialogTeacher
from .build import build

import copy
import json
import os


def get_sentence_tokenizer():
    """
    Loads the nltk sentence tokenizer
    """
    try:
        import nltk
    except ImportError:
        raise ImportError('Please install nltk (e.g. pip install nltk).')
    # nltk-specific setup
    st_path = 'tokenizers/punkt/{0}.pickle'.format('english')
    try:
        sent_tok = nltk.data.load(st_path)
    except LookupError:
        nltk.download('punkt')
        sent_tok = nltk.data.load(st_path)
    return sent_tok


class DefaultTeacher(DialogTeacher):
    """This version of SQuAD inherits from the core Dialog Teacher, which just
    requires it to define an iterator over its data `setup_data` in order to
    inherit basic metrics, a default `act` function.
    For SQuAD, this does not efficiently store the paragraphs in memory.
    """

    def __init__(self, opt, shared=None):
        self.datatype = opt['datatype']
        build(opt)
        opt['datafile'] = os.path.join(opt['datapath'], 'rasa_eval_new',
                                       'errors_10000_test.json')
        self.id = 'rasa'
        super().__init__(opt, shared)

    def setup_data(self, path):
        print('loading: ' + path)
        with open(path) as data_file:
            self.rasa = json.load(data_file)['data']

        for example in self.rasa:
            # pc_question = example['intent']
            pc_question = " ".join(example['intent'].split("_"))
            rasa_question = " ".join(example['intent_prediction']['name'].split("_"))
            answer = example['text']
            answers = ("one", "two")
            # secret = (0, 1)
            prompt = ('Conversation Pair 1: ' + '\n' +
                      'P1: ' + rasa_question + '\n' + 'P2: ' + answer + '\n\n' +
                      'Conversation Pair 2: ' + '\n' +
                      'P1: ' + pc_question + '\n' + 'P2: ' + answer)
            # context = example['intent']
            # yield(prompt, secret), True
            yield (prompt, answers), True


class FulldocTeacher(ParlAIDialogTeacher):
    def __init__(self, opt, shared=None):
        build(opt)
        opt = copy.deepcopy(opt)
        datafile = os.path.join(opt['datapath'], 'rasa_eval/data.txt')
        opt['parlaidialogteacher_datafile'] = datafile
        super().__init__(opt, shared)
        self.id = 'rasa-parlaiformat'
        self.reset()
