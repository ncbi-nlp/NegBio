"""
Detect negative and uncertain findings from SOURCE and output to DEST
Example: python negbio/main_mm.py --metamap=/opt/public_mm/bin/metamap16 --output=examples/test.neg.xml examples/1.txt examples/2.txt

Usage:
    main_mm text [options] --metamap=BINARY --output=DEST SOURCES ...
    main_mm bioc [options] --metamap=BINARY --output=DEST SOURCE ...

Options:
    --neg-patterns=FILE             negation rules [default: negbio/patterns/neg_patterns.txt]
    --uncertainty-patterns=FILE     uncertainty rules [default: negbio/patterns/uncertainty_patterns.txt]
    --bllip-model=MODEL_DIR         Bllip parser model directory
    --split-document                Split document into passages based on section titles such as "Finding", "Impression"
    --cuis=FILE                     CUI list. To keep all CUIs, set it to None [default: examples/cuis-cvpr2017.txt]
    --newline_is_sentence_break     Whether to treat newlines as sentence breaks. True means that a newline is always a
                                    sentence break. False means to ignore newlines for the purpose of sentence
                                    splitting. This is appropriate for continuous text, when just the non-whitespace
                                    characters should be used to determine sentence breaks.
    --word_sense_disambiguation     Whether to use word sense disambiguation.
    --verbose                       Print more information about progress.
"""
from __future__ import print_function
import logging
import sys
import os
import bioc
import docopt

import pymetamap

from negbio.cli_utils import parse_args, get_absolute_path
from negbio.pipeline import negdetect, text2bioc, dner_mm
from negbio.negbio_dner_matamap import read_cuis
from negbio.pipeline.parse import NegBioParser
from negbio.pipeline.ssplit import NegBioSSplitter
from negbio.pipeline.ptb2ud import NegBioPtb2DepConverter, Lemmatizer


def pipeline(collection, metamap, splitter, parser, ptb2dep, neg_detector, cuis, extra_args):
    """

    Args:
        collection(BioCCollection):
        metamap(MetaMap): MetaMap instance
        splitter (NegBioSSplitter):
        parser (NegBioParser)
        ptb2dep (NegBioPtb2DepConverter)
        neg_detector (Detector):

    Returns:
        BioCCollection
    """
    for document in collection.documents:
        splitter.split_doc(document)

    dner_mm.run_metamap_col(collection, metamap, cuis, extra_args)

    for document in collection.documents:
        document = parser.parse_doc(document)
        document = ptb2dep.convert_doc(document)
        document = negdetect.detect(document, neg_detector)
        # remove sentence
        for passage in document.passages:
            del passage.sentences[:]

    return collection


def main():
    argv = parse_args(__doc__, version='version 2')
    print(argv)

    lemmatizer = Lemmatizer()
    ptb2dep = NegBioPtb2DepConverter(lemmatizer, universal=True)
    splitter = NegBioSSplitter(newline=argv['--newline_is_sentence_break'])
    parser = NegBioParser(model_dir=argv['--bllip-model'])

    argv = get_absolute_path(argv,
                             '--neg-patterns',
                             'negbio/patterns/neg_patterns.txt')
    argv = get_absolute_path(argv,
                             '--uncertainty-patterns',
                             'negbio/patterns/uncertainty_patterns.txt')

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

    extra_args = dict()
    if argv['--word_sense_disambiguation']:
        extra_args['word_sense_disambiguation'] = True

    # Converting empty dict to None
    if len(extra_args) == 0:
        extra_args = None

    pipeline(collection, mm, splitter, parser, ptb2dep, neg_detector, cuis, extra_args)

    with open(os.path.expanduser(argv['--output']), 'w') as fp:
        bioc.dump(collection, fp)


if __name__ == '__main__':
    main()
