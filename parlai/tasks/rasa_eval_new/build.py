import parlai.core.build_data as build_data
import os
import shutil


def build(opt):
    # get path to data directory
    dpath = os.path.join(opt['datapath'], 'rasa_eval_new')
    # define version if any
    version = None

    # check if data had been previously built
    if not build_data.built(dpath, version_string=version):
        print('[building data: ' + dpath + ']')

        # make a clean directory if needed
        if build_data.built(dpath):
            # an older version exists, so remove these outdated files.
            build_data.remove_dir(dpath)
        build_data.make_dir(dpath)

        # download the data.
        source = os.path.join(opt['parlai_home'], 'parlai/tasks/' +
                              'rasa_eval_new/errors_10000_test.json')
        fname = 'errors_10000_test.json'

        outfile = os.path.join(dpath, fname)
        shutil.copy(source, outfile)

        # mark the data as built
        build_data.mark_done(dpath, version_string=version)
