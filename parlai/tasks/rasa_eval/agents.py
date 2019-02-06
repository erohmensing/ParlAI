#!/usr/bin/env python3

from parlai.core.teachers import ParlAIDialogTeacher
import copy
import os
from .build import build


def _path(opt, filtered):
    # build the data if it does not exist
    build(opt)

    # set up path to data (specific to each dataset)
    # helpful if you have specific train and test sets
    # dt = opt['datatype'].split(':')[0]

    return os.path.join(opt['datapath'], 'rasa_eval/data.txt')


class DefaultTeacher(ParlAIDialogTeacher):
    def __init__(self, opt, shared=None):
        opt['parlaidialogteacher_datafile'] = _path(opt, '')
        super().__init__(opt, shared)
        opt = copy.deepcopy(opt)

        # get datafile
        # opt['datafile'] = _path(opt, '')  # not necessary
