"""
Detect UMLS concept

Usage:
    negbio dner [options] --metamap=BINARY --out=DIRECTORY SOURCE ...

Options:
    --suffix=<str>      [default: .mm.xml]
    --out=<dest>        output file
    --verbose
    --metamap=BINARY    The MetaMap binary
    --cuis=FILE         CUI list
"""
from __future__ import print_function

import logging

import docopt

import pymetamap
from pipeline import scan
from pipeline.dner_mm import run_metamap_col
from util import get_args


def read_cuis(pathname):
    cuis = set()
    with open(pathname) as fp:
        for line in fp:
            line = line.strip()
            if line:
                cuis.add(line)
    return cuis


if __name__ == '__main__':
    argv = docopt.docopt(__doc__)
    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug('global arguments:\n%s', get_args(argv))

    mm = pymetamap.MetaMap.get_instance(argv['--metamap'])

    if argv['--cuis'] is None:
        cuis = None
    else:
        cuis = read_cuis(argv['--cuis'])

    scan.scan_collection(source=argv['SOURCE'], directory=argv['--out'], suffix=argv['--suffix'],
                         fn=run_metamap_col, non_sequences=[mm, cuis])
