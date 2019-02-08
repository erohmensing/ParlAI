#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

task_config = {}


# task_config['frontend_version'] = 1

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search
results, and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'Rate how well the prompt and response go together'


"""A description includes detailed information about the kind of task the HIT
contains. On the Amazon Mechanical Turk web site, the HIT description appears
in the expanded view of search results, and in the HIT and assignment screens.
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
<header>
<h2>Instructions:</h2>
</header>
In this task, you will be shown two conversation pairs,
and will rate each pair on how well the response fits the prompt,
on a scale from 1 to 10
(1 - makes no sense, 10 - logically follows).<br><br>
<header>
<h2>Example:</h2>
</header>
------------------- Task Begin ------------------- <br><br>
<b>Rating Collector</b>:<br>
Conversation Pair 1:<br>
P1:  hello , how are you this evening<br>
R1:  i'm good . hope you are having a great evening<br><br>
Please provide a rating for Conversation Pair 1.<br><br>
<b>Worker</b>:<br>
10<br><br>
<b>Rating Collector</b>:<br>
Thanks! <br><br>
Conversation Pair 2:<br>
P1:  getting ready for school tomorrow .<br>
R2:  i'm good . hope you are having a great evening .<br><br>
Now, please provide a rating for Conversation Pair 2.
<br><br>
<b>Worker</b>:<br>
2<br><br>
<b>Rating Collector</b>:<br>
Thanks!<br><br>
------------------- Task Done ------------------- <br><br>
If you are ready, please click "Accept HIT" to start this task.
"""
