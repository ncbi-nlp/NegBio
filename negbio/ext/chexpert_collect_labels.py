"""
Aggregate document-level labels

Usage:
    negbio_parse [options] --output=<file> <file> ...

Options:
    --output=<file>         Specify the output file.
    --phrases_file=<file>   File containing phrases for each observation. [default: patterns/cxr14_phrases_v2.yml]
    --verbose               Print more information about progress.
    --overwrite             Overwrite the output file.

Author: stanfordmlgroup
Modified by: Yifan Peng
"""

import collections
import logging
from pathlib import Path
from typing import List

import bioc
import numpy as np
import pandas as pd
import tqdm
import yaml


# Numeric constants
from negbio.cli_utils import parse_args

POSITIVE = 1
NEGATIVE = 0
UNCERTAIN = -1

# Misc. constants
UNCERTAINTY = "uncertainty"
NEGATION = "negation"


def dict_to_vec(d, total_findings: List[str]):
    """
    Convert a dictionary of the form
    {cardiomegaly: [1],
     opacity: [u, 1],
     fracture: [0]}
    into a vector of the form
    [np.nan, np.nan, 1, u, np.nan, ..., 0, np.nan]
    """
    vec = []
    for category in total_findings:
        # There was a mention of the category.
        if category in d:
            label_list = d[category]
            # Only one label, no conflicts.
            if len(label_list) == 1:
                vec.append(label_list[0])
            # Multiple labels.
            else:
                # Case 1. There is negated and uncertain.
                if NEGATIVE in label_list and UNCERTAIN in label_list:
                    vec.append(NEGATIVE)
                # Case 2. There is negated and positive.
                elif NEGATIVE in label_list and POSITIVE in label_list:
                    vec.append(POSITIVE)
                # Case 3. There is uncertain and positive.
                elif UNCERTAIN in label_list and POSITIVE in label_list:
                    vec.append(POSITIVE)
                # Case 4. All labels are the same.
                else:
                    vec.append(label_list[0])

        # No mention of the category
        else:
            vec.append(np.nan)

    return vec


def aggregate(doc):
    label_dict = {}
    no_finding = True
    for p in doc.passages:
        for annotation in p.annotations:
            category = annotation.infons['observation']

            if NEGATION in annotation.infons:
                label = NEGATIVE
            elif UNCERTAINTY in annotation.infons:
                label = UNCERTAIN
            else:
                label = POSITIVE

            # Don't add any labels for No Finding
            if category == "No Finding":
                continue
                
            # If at least one non-support category has a uncertain or
            # positive label, there was a finding
            if category != 'Support Devices' and label in [UNCERTAIN, POSITIVE]:
                no_finding = False

            # add exception for 'chf' and 'heart failure'
            if ((label in [UNCERTAIN, POSITIVE]) and
                    (annotation.text.lower() == 'chf' or
                     annotation.text.lower() == 'heart failure')):
                if "Cardiomegaly" not in label_dict:
                    label_dict["Cardiomegaly"] = [UNCERTAIN]
                else:
                    label_dict["Cardiomegaly"].append(UNCERTAIN)

            if category not in label_dict:
                label_dict[category] = [label]
            else:
                label_dict[category].append(label)

    if no_finding:
        label_dict["No Finding"] = [POSITIVE]

    return label_dict


def create_prediction(source, dest, phrases_file, verbose=True):
    """

    Args:
        source: a list of source pathnames
        dest: output file name
        phrases_file: phrase pathname
    """
    with open(phrases_file) as fp:
        phrases = yaml.load(fp, yaml.FullLoader)
    total_findings = list(phrases.keys())

    rows = []
    cnt = collections.Counter()
    for pathname in tqdm.tqdm(source, total=len(source), disable=not verbose, unit='col'):
            with open(pathname, encoding='utf8') as fp:
                collection = bioc.load(fp)

            for doc in collection.documents:
                label_dict = aggregate(doc)
                label_vec = dict_to_vec(label_dict, total_findings)
                findings = collections.OrderedDict()
                findings['id'] = str(doc.id)
                for i, f in enumerate(total_findings):
                    findings[f] = label_vec[i]
                rows.append(findings)

    rows = sorted(rows, key=lambda x: x['id'])
    row_df = pd.DataFrame(rows)
    row_df.to_csv(dest, index=None, float_format='%1.0f')
    logging.debug(cnt)


if __name__ == '__main__':
    argv = parse_args(__doc__)
    phrases_file = Path(argv['--phrases_file'])
    findings = phrases_file
    create_prediction(source=argv['<file>'], dest=argv['--output'], phrases_file=phrases_file,
                      verbose=argv['--verbose'])
