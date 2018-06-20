"""
Detect negative and uncertain findings from SOURCE and output to DEST
Example: python negbio/main_text.py --metamap=/opt/public_mm/bin/metamap16 --out=examples/test.neg.xml examples/1.txt examples/2.txt

Usage:
    main_text [options] --metamap=BINARY --out=DEST SOURCE ...

Options:
    --neg-patterns=FILE             negation rules [default: patterns/neg_patterns.txt]
    --uncertainty-patterns=FILE     uncertainty rules [default: patterns/uncertainty_patterns.txt]
    --bllip-model=MODEL_DIR         Bllip parser model directory
    --split-document                Split document into passages based on section titles such as "Finding", "Impression"
    --cuis=FILE                     CUI list. To keep all CUIs, set it to None [default: examples/cuis-cvpr2017.txt]
    --newline_is_sentence_break     Whether to treat newlines as sentence breaks. True means that a newline is always a
                                    sentence break. False means to ignore newlines for the purpose of sentence
                                    splitting. This is appropriate for continuous text, when just the non-whitespace
                                    characters should be used to determine sentence breaks.
"""

import logging
import sys
import os
import bioc
import docopt

import pymetamap
from negbio.pipeline import parse, ssplit, ptb2ud, negdetect, text2bioc, dner_mm


def pipeline(collection, metamap, splitter, parser, ptb2dep, lemmatizer, neg_detector, cuis):
    for document in collection.documents:
        ssplit.ssplit(document, splitter)

    dner_mm.run_metamap_col(collection, metamap, cuis)

    for document in collection.documents:
        document = parse.parse(document, parser)
        document = ptb2ud.convert(document, ptb2dep, lemmatizer)
        document = negdetect.detect(document, neg_detector)
        # remove sentence
        for passage in document.passages:
            del passage.sentences[:]

    return collection


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)

    splitter = ssplit.NltkSSplitter(newline=argv['--newline_is_sentence_break'])
    parser = parse.Bllip(model_dir=argv['--bllip-model'])
    ptb2dep = ptb2ud.Ptb2DepConverter(universal=True)
    lemmatizer = ptb2ud.Lemmatizer()
    mm = pymetamap.MetaMap.get_instance(argv['--metamap'])
    neg_detector = negdetect.Detector(argv['--neg-patterns'], argv['--uncertainty-patterns'])

    if argv['--cuis'] == 'None':
        cuis = None
    else:
        cuis = dner_mm.read_cuis(argv['--cuis'])

    collection = text2bioc.text2collection(argv['SOURCE'])
    pipeline(collection, mm, splitter, parser, ptb2dep, lemmatizer, neg_detector, cuis)

    with open(os.path.expanduser(argv['--out']), 'w') as fp:
        bioc.dump(collection, fp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
