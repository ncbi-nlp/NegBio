"""
Clean up sentences

Usage:
    clean_sentences --out=DIRECTORY SOURCE ...
"""

from __future__ import print_function

import logging
import sys

import docopt

from negbio.pipeline import scan


def clean_sentences(document):
    """
    Args:
        document(BioCDocument):
    """
    logger = logging.getLogger(__name__)

    try:
        for passage in document.passages:
            del passage.sentences[:]
            id = 0
            for ann in sorted(passage.annotations, key=lambda ann: ann.get_total_location().offset):
                ann.id = str(id)
                id += 1
    except:
        logger.exception("Cannot process %s", document.id)
    return document


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)
    scan.scan_document(source=argv['SOURCE'], directory=argv['--out'], suffix='.negbio.xml',
                       fn=clean_sentences, non_sequences=[])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    main(sys.argv[1:])
