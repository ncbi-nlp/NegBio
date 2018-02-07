"""
Detect negative and uncertain findings from SOURCE and output to DIRECTORY
Example: python negbio/main.py --out=examples examples/1.xml examples/2.xml

Usage:
    negbio [options] --out=DIRECTORY SOURCE ...

Options:
    --neg-patterns=FILE             negation rules [default: patterns/neg_patterns.txt]
    --uncertainty-patterns=FILE     uncertainty rules [default: patterns/uncertainty_patterns.txt]
    --model=MODEL_DIR               Bllip parser model directory
"""

import logging
import sys
import os
import docopt

from negbio.pipeline import scan
from negbio.pipeline import parse, ssplit, ptb2ud, negdetect


def pipeline(document, splitter, parser, ptb2dep, lemmatizer, neg_detector):
    document = ssplit.ssplit(document, splitter)
    document = parse.parse(document, parser)
    document = ptb2ud.convert(document, ptb2dep, lemmatizer)
    document = negdetect.detect(document, neg_detector)

    # remove sentence
    for passage in document.passages:
        del passage.sentences[:]

    return document


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)
    splitter = ssplit.NltkSSplitter(newline=True)
    parser = parse.Bllip(model_dir=argv['--model'])
    ptb2dep = ptb2ud.Ptb2DepConverter(universal=True)
    lemmatizer = ptb2ud.Lemmatizer()
    neg_detector = negdetect.Detector(argv['--neg-patterns'], argv['--uncertainty-patterns'])

    scan.scan_document(source=argv['SOURCE'], directory=argv['--out'], suffix='.neg.xml',
                       fn=pipeline, non_sequences=[splitter, parser, ptb2dep, lemmatizer, neg_detector])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
