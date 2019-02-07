#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

task_config = {}


task_config['frontend_version'] = 1

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'Rank coherency of conversation pairs'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = 'Rank coherency of conversation pairs.'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'chat,question,answer'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config['task_description'] = """
In this task, you will be shown two conversation pairs, and will rank each on a scale of 1-5.<br><br>
Example:<br><br>
------------------- Task Begin ------------------- <br><br>
<b>QA Collector</b>:<br>
<b>Conversation Pair 1</b>:<br>
P1: Example.<br>
P2: Example.<br><br>
<b>Conversation Pair 2</b>:<br>
P1: Example.<br>
P2: Example.<br><br>
Please provide a ranking for <b>Conversation Pair 1</b>.<br><br>
<b>Worker</b>:<br>
2<br><br>
<b>QA Collector</b>:<br>
Thanks! Now please provide a ranking for <b>Conversation Pair 2</b>.
<br><br>
<b>Worker</b>:<br>
4<br><br>
<b>QA Collector</b>:<br>
Thanks!<br><br>
------------------- Task Done ------------------- <br><br>
If you are ready, please click "Accept HIT" to start this task.
"""
