# General script for renaming
#
# Inputs: finder, new label, list of subjects
#
#

import flywheel
import json
import argparse
import re

# Create client, define project
fw = flywheel.Client()
project = fw.lookup('davis/presurgicalEpilepsy')

# Argument parsing
parser = argparse.ArgumentParser(
        description="Conduct a batch analysis with a gear on Flywheel")

parser.add_argument(
        "--finder",
        help="string to discriminate analyses",
        required=True
        )
parser.add_argument(
        "--newlabel",
        help="new label for analyses",
        required=True
        )
parser.add_argument(
        "--subs",
        help="path to text file containing list of subjects",
        required=False
        )

args = parser.parse_args()
finder = args.finder
newlabel = args.newlabel
subject_list = args.subs

if subject_list is not None:
    slabel_list = [line.rstrip('\n').split()[0] for line in open(subject_list)]
else:
    print("No subject list provided. Using all subjects.")
    slabel_list = []
    for subject_container in project.subjects():
        slabel_list.append(subject_container.label)

for sub in slabel_list:
    subject_container = fw.lookup('davis/presurgicalEpilepsy/%s' % (sub))
    for ses_container in subject_container.sessions():
        ses = fw.get(ses_container.id)
        if ses.analyses is not None: # and len(ses_container.analyses) > 0:
            for a in ses.analyses:
                if finder in a.label:
                    if "<date>" in newlabel:
                        date_str = str(a.created).split()[0]
                        newlabel = re.sub('<date>',date_str, newlabel)
                    print('Renaming {} for {} to {}'.format(a.label, subject_container.label, newlabel))
                    a.update(label=newlabel)
        else:
            print("Session does not have analyses.")
