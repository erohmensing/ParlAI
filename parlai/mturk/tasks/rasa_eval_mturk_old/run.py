#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from parlai.core.params import ParlaiParser
from parlai.mturk.tasks.rasa_eval_mturk.worlds import \
    RasaEvaluatorWorld, ModelEvaluatorOnboardWorld
from parlai.mturk.core.mturk_manager import MTurkManager
from task_config import task_config
import os


def main():
    argparser = ParlaiParser(False, False)
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()

    # The dialog model we want to evaluate
    # ella - we don't want to actually eval a model here
    from parlai.agents.repeat_label.repeat_label import RepeatLabelAgent
    RepeatLabelAgent.add_cmdline_args(argparser)
    opt = argparser.parse_args()
    opt['task'] = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    opt.update(task_config)

    # The task that we will evaluate the dialog model on
    task_opt = {}
    task_opt['datatype'] = 'train'
    task_opt['datapath'] = opt['datapath']
    task_opt['task'] = 'rasa_eval'

    mturk_agent_id = 'Worker'
    mturk_manager = MTurkManager(
        opt=opt,
        mturk_agent_ids=[mturk_agent_id]
    )
    mturk_manager.setup_server()

    try:
        mturk_manager.start_new_run()

        def run_onboard(worker):
            world = ModelEvaluatorOnboardWorld(opt=opt, mturk_agent=worker)
            while not world.episode_done():
                world.parley()
            world.shutdown()

        mturk_manager.set_onboard_function(onboard_function=None)
        mturk_manager.ready_to_accept_workers()  # move this
        mturk_manager.create_hits()

        def check_worker_eligibility(worker):
            return True

        def assign_worker_roles(worker):
            worker[0].id = mturk_agent_id

        global run_conversation

        def run_conversation(mturk_manager, opt, workers):
            mturk_agent = workers[0]

            model_agent = RepeatLabelAgent(opt=opt)

            world = RasaEvaluatorWorld(
                opt=opt,
                model_agent=model_agent,
                task_opt=task_opt,
                mturk_agent=mturk_agent
            )

            while not world.episode_done():
                world.parley()
            world.shutdown()
            world.review_work()

        mturk_manager.start_task(
            eligibility_function=check_worker_eligibility,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation
        )
    except BaseException:
        raise
    finally:
        mturk_manager.expire_all_unassigned_hits()
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()
