"""
Detect negation and uncertainty

Usage:
    negbio neg [options] --out=DIRECTORY SOURCE ...

Options:
    --neg-patterns=FILE             negation rules [default: patterns/neg_patterns.txt]
    --uncertainty-patterns=FILE     uncertainty rules [default: patterns/uncertainty_patterns.txt]
    --suffix=<str>                  [default: .neg.xml]
    --verbose
"""

from __future__ import print_function

import logging

import docopt

from neg.neg_detector import Detector
from pipeline import scan
from pipeline.negdetect import detect
from util import get_args
import os

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)
    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug('Arguments:\n%s', get_args(argv))

    neg_detector = Detector(os.path.realpath(argv['--neg-patterns']),
                            os.path.realpath(argv['--uncertainty-patterns']))
    scan.scan_document(source=argv['SOURCE'], directory=argv['--out'], suffix=argv['--suffix'],
                       fn=detect, non_sequences=[neg_detector])
