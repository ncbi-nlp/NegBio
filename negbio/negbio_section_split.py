"""
Convert text to the BioC format

Usage:
    negbio section_split [options] --out=<dest> <source> ...

Options:
    --suffix=<str>      [default: .secsplit.xml]
    --out=<dest>        output file
    --verbose
    --patterns=FILE     section title list.
"""
from __future__ import print_function

import logging
import re
import docopt

from pipeline.scan import scan_document
from pipeline.section_split import split_document

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)

    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if '--patterns' in argv:
        with open(argv['--patterns']) as fp:
            lines = fp.readlines()
        patterns = re.compile('|'.join(lines), re.MULTILINE)
    else:
        patterns = None

    scan_document(source=argv['<source>'], verbose=argv['--verbose'], suffix=argv['--suffix'],
                  directory=argv['--out'], fn=split_document, non_sequences=[patterns])
