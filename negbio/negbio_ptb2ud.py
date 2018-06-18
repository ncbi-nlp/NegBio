"""
Convert from parse tree to universal dependencies

Usage:
    negbio ptb2ud [options] --out=DIRECTORY SOURCE ...

Options:
    --suffix=<str>      [default: .ud.xml]
    --verbose
"""

from __future__ import print_function

import logging

import docopt

from pipeline import scan
from pipeline.ptb2ud import Ptb2DepConverter, Lemmatizer, convert
from util import get_args

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)
    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug('Arguments:\n%s', get_args(argv))

    ptb2dep = Ptb2DepConverter(universal=True)
    lemmatizer = Lemmatizer()
    scan.scan_document(source=argv['SOURCE'], directory=argv['--out'], suffix=argv['--suffix'],
                       fn=convert, non_sequences=[ptb2dep, lemmatizer])
