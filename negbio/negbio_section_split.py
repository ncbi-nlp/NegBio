"""
Convert text to the BioC format

Usage:
    negbio section_split [options] --out=<dest> <source> ...

Actions:
    --suffix=<str>  [default: .split.xml]
    --out=<dest>    output file
    --verbose
"""
from __future__ import print_function

import logging

import docopt

from pipeline.scan import scan_collection
from pipeline.section_split import split_collection

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)

    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    scan_collection(source=argv['<source>'], verbose=argv['--verbose'], suffix=argv['--suffix'],
                    directory=argv['--out'], fn=split_collection)
