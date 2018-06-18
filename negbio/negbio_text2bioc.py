"""
Convert text to the BioC format

Usage:
    git text2bioc --out=<dest> <source> ...

Actions:
    --out=<dest>    output file
"""
from __future__ import print_function

import logging
import os

import bioc
import docopt

from pipeline.text2bioc import text2collection


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    argv = docopt.docopt(__doc__)
    print(argv)

    collection = text2collection(argv['<source>'])
    with open(os.path.expanduser(argv['--out']), 'w') as fp:
        bioc.dump(collection, fp)
