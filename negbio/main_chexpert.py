"""
Detect negative and uncertain findings from SOURCE and output to DEST
Example: python negbio/main_chexpert.py --output=examples/test.neg.xml examples/1.txt examples/2.txt
         python negbio/main_chexpert.py --skip-to-bioc --output=examples/test.neg.xml examples/1.xml

Usage:
    main_chexpert text [options] --output=DEST SOURCES ...
    main_chexpert bioc [options] --output=DEST SOURCE

Options:
    --mention_phrases_dir=<directory>           Directory containing mention phrases for each observation.
                                                [default: negbio/chexpert/phrases/mention]
    --unmention_phrases_dir=<directory>         Directory containing unmention phrases  for each observation.
                                                [default: negbio/chexpert/phrases/unmention]
    --neg-patterns=FILE                         Negation rules [default: negbio/chexpert/patterns/negation.txt]
    --pre-negation-uncertainty-patterns=FILE    Pre negation uncertainty rules
                                                [default: negbio/chexpert/patterns/pre_negation_uncertainty.txt]
    --post-negation-uncertainty-patterns=FILE   Post negation uncertainty rules
                                                [default: negbio/chexpert/patterns/post_negation_uncertainty.txt]
    --bllip-model=MODEL_DIR                     Bllip parser model directory
                                                [default: ~/.local/share/bllipparser/GENIA+PubMed]
    --split-document                            Split document into passages based on section titles such as "Finding",
                                                "Impression"
    --newline_is_sentence_break                 Whether to treat newlines as sentence breaks. True means that a newline
                                                is always a sentence break. False means to ignore newlines for the
                                                purpose of sentence splitting. This is appropriate for continuous text,
                                                when just the non-whitespace characters should be used to determine
                                                sentence breaks.
    --verbose                                   Print more information about progress.
"""
import logging
import os
import sys

import bioc
import docopt
import tqdm
from pathlib2 import Path

from negbio.cli_utils import parse_args
from negbio.pipeline import parse, ssplit, ptb2ud, text2bioc, negdetect
from negbio.chexpert.stages.classify import ModifiedDetector, CATEGORIES
from negbio.chexpert.stages.extract import Extractor
from negbio.chexpert.stages.aggregate import Aggregator


def pipeline(collection, extractor, splitter, parser, ptb2dep, lemmatizer, neg_detector, aggregator, verbose=False):
    """
    Args:
        extractor (Extractor):
        neg_detector (ModifiedDetector):
        aggregator (Aggregator):
    """
    for document in collection.documents:
        ssplit.ssplit(document, splitter)

    extractor.extract(collection)

    for document in tqdm.tqdm(collection.documents, disable=not verbose):
        document = parse.parse(document, parser)
        document = ptb2ud.convert(document, ptb2dep, lemmatizer)
        document = negdetect.detect(document, neg_detector)

        # remove sentence
        for passage in document.passages:
            del passage.sentences[:]

    aggregator.aggregate(collection)

    return collection


if __name__ == '__main__':
    argv = parse_args(__doc__, version='negbio version 2')
    splitter = ssplit.NltkSSplitter(newline=argv['--newline_is_sentence_break'])
    parser = parse.Bllip(model_dir=argv['--bllip-model'])
    ptb2dep = ptb2ud.Ptb2DepConverter(universal=True)
    lemmatizer = ptb2ud.Lemmatizer()

    # chexpert
    extractor = Extractor(Path(argv['--mention_phrases_dir']),
                          Path(argv['--unmention_phrases_dir']),
                          verbose=argv['--verbose'])
    neg_detector = ModifiedDetector(argv['--pre-negation-uncertainty-patterns'],
                                    argv['--neg-patterns'],
                                    argv['--post-negation-uncertainty-patterns'])
    aggregator = Aggregator(CATEGORIES,
                            verbose=argv['--verbose'])

    if argv['text']:
        collection = text2bioc.text2collection(argv['SOURCES'])
    elif argv['bioc']:
        with open(argv['SOURCE']) as fp:
            collection = bioc.load(fp)
    else:
        raise KeyError

    pipeline(collection, extractor, splitter, parser, ptb2dep, lemmatizer, neg_detector, aggregator,
             verbose=argv['--verbose'])

    with open(os.path.expanduser(argv['--out']), 'w') as fp:
        bioc.dump(collection, fp)
