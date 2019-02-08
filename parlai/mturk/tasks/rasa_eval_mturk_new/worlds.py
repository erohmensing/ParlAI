#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.core.worlds import validate
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld


class QADataCollectionOnboardWorld(MTurkOnboardWorld):
    '''Example onboarding world. Sends a message from the world to the
    worker and then exits as complete
    '''
    def parley(self):
        ad = {}
        ad['id'] = 'System'
        ad['text'] = 'Welcome onboard!'
        self.mturk_agent.observe(ad)
        self.mturk_agent.act()
        self.episodeDone = True


class QADataCollectionWorld(MTurkTaskWorld):
    """
    World for recording a turker's question and answer given a context.
    Assumes the context is a random context from a given task, e.g.
    from SQuAD, CBT, etc.
    """

    collector_agent_id = 'Rating Collector'

    def __init__(self, opt, task, mturk_agent):
        self.task = task
        self.mturk_agent = mturk_agent
        self.episodeDone = False
        self.turn_index = -1
        self.context = None
        self.rating_1 = None
        self.rating_2 = None

    def parley(self):
        # Each turn starts from the QA Collector agent
        self.turn_index = (self.turn_index + 1) % 2
        ad = {'episode_done': False}
        ad['id'] = self.__class__.collector_agent_id

        if self.turn_index == 0:
            # At the first turn, the Rating Collector agent provides the context
            # and prompts the turker to ask a question regarding the context

            # Get context from rasa teacher agent
            qa = self.task.act()
            self.pairs = (qa['text'].split('~'))
            self.pair_1 = '\n'.join(self.pairs[0].split('_'))
            self.pair_2 = '\n'.join(self.pairs[1].split('_'))
            # self.context = '\n'.join(qa['text'].split('_'))
            self.pc_labels = qa['labels']

            # Wrap the context with a prompt telling the turker what to do next
            ad['text'] = ('\n' + self.pair_1 +
                          '\n\nPlease provide a rating ' +
                          'for Conversation Pair 1.')

            self.mturk_agent.observe(validate(ad))
            self.rating_1 = self.mturk_agent.act()
            # Can log the turker's first rating here

        if self.turn_index == 1:
            # At the second turn, the Rating Collector collects the turker's
            # rating of the first pair, and then prompts the turker to
            # provide a rating for the second pair

            # A prompt telling the turker what to do next
            ad['text'] = ('Thanks!\n\n' + self.pair_2 +
                          '\n\nNow, please provide a rating '
                          'for Conversation Pair 2.')
            ad['episode_done'] = True  # end of episode

            self.mturk_agent.observe(validate(ad))
            self.rating_2 = self.mturk_agent.act()

            self.episodeDone = True

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.task.shutdown()
        self.mturk_agent.shutdown()

    def review_work(self):
        # Can review the work here to accept or reject it
        pass

    def get_custom_task_data(self):
        # brings important data together for the task, to later be used for
        # creating the dataset. If data requires pickling, put it in a field
        # called 'needs-pickle'.
        return {
            'context': [self.context],
            'pc_labels': [self.pc_labels],
            'ratings': [self.rating_1, self.rating_2],
        }