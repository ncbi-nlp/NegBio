"""
Detect negative and uncertain findings from SOURCE and output to DEST
Example: python negbio/main_mm.py --metamap=/opt/public_mm/bin/metamap16 --output=examples/test.neg.xml examples/1.txt examples/2.txt

Usage:
    main_text text [options] --metamap=BINARY --output=DEST SOURCES ...
    main_text bioc [options] --metamap=BINARY --output=DEST SOURCE ...

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
    --verbose                       Print more information about progress.
"""
from __future__ import print_function
import logging
import sys
import os
import bioc
import docopt

import pymetamap
from negbio.pipeline import negdetect, text2bioc, dner_mm
from negbio.negbio_dner_matamap import read_cuis
from negbio.pipeline.parse import NegBioParser
from negbio.pipeline.ssplit import NegBioSSplitter
from negbio.pipeline.ptb2ud import NegBioPtb2DepConverter, Lemmatizer


def pipeline(collection, metamap, splitter, parser, ptb2dep, neg_detector, cuis):
    """

    Args:
        splitter (NegBioSSplitter):
        parser (NegBioParser)
        ptb2dep (NegBioPtb2DepConverter)
        neg_detector (Detector):

    Returns:

    """
    for document in collection.documents:
        splitter.split_doc(document)

    dner_mm.run_metamap_col(collection, metamap, cuis)

    for document in collection.documents:
        document = parser.parse_doc(document)
        document = ptb2dep.convert_doc(document)
        document = negdetect.detect(document, neg_detector)
        # remove sentence
        for passage in document.passages:
            del passage.sentences[:]

    return collection


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)

    ptb2dep = NegBioPtb2DepConverter(Lemmatizer(), universal=True)
    splitter = NegBioSSplitter(newline=argv['--newline_is_sentence_break'])
    parser = NegBioParser(model_dir=argv['--bllip-model'])

    mm = pymetamap.MetaMap.get_instance(argv['--metamap'])
    neg_detector = negdetect.Detector(argv['--neg-patterns'], argv['--uncertainty-patterns'])

    if argv['--cuis'] == 'None':
        cuis = None
    else:
        cuis = read_cuis(argv['--cuis'])

    if argv['text']:
        collection = text2bioc.text2collection(argv['SOURCES'])
    elif argv['bioc']:
        with open(argv['SOURCE']) as fp:
            collection = bioc.load(fp)
    else:
        raise KeyError

    pipeline(collection, mm, splitter, parser, ptb2dep, neg_detector, cuis)

    with open(os.path.expanduser(argv['--output']), 'w') as fp:
        bioc.dump(collection, fp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
