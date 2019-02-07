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
from __future__ import print_function

import os

import bioc
import tqdm
from pathlib2 import Path

from negbio.chexpert.stages.aggregate import NegBioAggregator
from negbio.chexpert.stages.classify import ModifiedDetector, CATEGORIES
from negbio.chexpert.stages.extract import NegBioExtractor
from negbio.chexpert.stages.load import NegBioLoader
from negbio.cli_utils import parse_args, get_absolute_path
from negbio.pipeline import text2bioc, negdetect
from negbio.pipeline.parse import NegBioParser
from negbio.pipeline.ptb2ud import NegBioPtb2DepConverter, Lemmatizer
from negbio.pipeline.ssplit import NegBioSSplitter


def pipeline(collection, loader, ssplitter, extractor, parser, ptb2dep, neg_detector, aggregator, verbose=False):
    """
    Args:
        loader (NegBioLoader)
        ssplitter (NegBioSSplitter)
        parser (NegBioParser)
        extractor (NegBioExtractor)
        ptb2dep (NegBioPtb2DepConverter)
        neg_detector (ModifiedDetector)
        aggregator (NegBioAggregator)
    """
    # for document in collection.documents:
    #
    #     for passage in document.passages:
    #         passage.text = clean(passage.text)
    #     ssplitter.split_doc(document)
    for document in tqdm.tqdm(collection.documents, disable=not verbose):
        document = loader.clean_doc(document)
        document = ssplitter.split_doc(document)
        document = extractor.extract_doc(document)
        document = parser.parse_doc(document)
        document = ptb2dep.convert_doc(document)
        document = negdetect.detect(document, neg_detector)
        document = aggregator.aggregate_doc(document)
        # remove sentence
        for passage in document.passages:
            del passage.sentences[:]

    return collection


def main():
    argv = parse_args(__doc__, version='version 2')
    print(argv)

    lemmatizer = Lemmatizer()
    ptb2dep = NegBioPtb2DepConverter(lemmatizer, universal=True)
    ssplitter = NegBioSSplitter(newline=argv['--newline_is_sentence_break'])
    parser = NegBioParser(model_dir=argv['--bllip-model'])

    argv = get_absolute_path(argv,
                             '--mention_phrases_dir',
                             'negbio/chexpert/phrases/mention')
    argv = get_absolute_path(argv,
                             '--unmention_phrases_dir',
                             'negbio/chexpert/phrases/unmention')
    argv = get_absolute_path(argv,
                             '--pre-negation-uncertainty-patterns',
                             'negbio/chexpert/patterns/pre_negation_uncertainty.txt')
    argv = get_absolute_path(argv,
                             '--post-negation-uncertainty-patterns',
                             'negbio/chexpert/patterns/post_negation_uncertainty.txt')
    argv = get_absolute_path(argv,
                             '--neg-patterns',
                             'negbio/chexpert/patterns/negation.txt')

    # chexpert
    loader = NegBioLoader()
    extractor = NegBioExtractor(Path(argv['--mention_phrases_dir']),
                                Path(argv['--unmention_phrases_dir']),
                                verbose=argv['--verbose'])
    neg_detector = ModifiedDetector(argv['--pre-negation-uncertainty-patterns'],
                                    argv['--neg-patterns'],
                                    argv['--post-negation-uncertainty-patterns'])
    aggregator = NegBioAggregator(CATEGORIES, verbose=argv['--verbose'])

    if argv['text']:
        collection = text2bioc.text2collection(argv['SOURCES'])
    elif argv['bioc']:
        with open(argv['SOURCE']) as fp:
            collection = bioc.load(fp)
    else:
        raise KeyError

    pipeline(collection, loader, ssplitter, extractor, parser, ptb2dep, neg_detector, aggregator,
             verbose=argv['--verbose'])

    with open(os.path.expanduser(argv['--output']), 'w') as fp:
        bioc.dump(collection, fp)


if __name__ == '__main__':
    main()
