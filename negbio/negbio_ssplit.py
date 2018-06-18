"""
Split text into sentences

Usage:
    negbio ssplit [options] --out=<dest> <source> ...

Options:
    --newline_is_sentence_break     Whether to treat newlines as sentence breaks. True means that a newline is always a
                                    sentence break. False means to ignore newlines for the purpose of sentence
                                    splitting. This is appropriate for continuous text, when just the non-whitespace
                                    characters should be used to determine sentence breaks. [default=False]
    --suffix=<str>                  [default: .ssplit.xml]
    --out=<dest>                    output file
    --verbose
"""

from __future__ import print_function

import logging

import docopt

from pipeline import scan
from pipeline.ssplit import NltkSSplitter, ssplit

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)

    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    splitter = NltkSSplitter(newline=argv['--newline_is_sentence_break'])
    scan.scan_document(source=argv['<source>'], directory=argv['--out'], suffix='.ss.xml',
                       fn=ssplit, non_sequences=[splitter])
