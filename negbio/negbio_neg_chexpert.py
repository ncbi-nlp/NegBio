"""
Detect negation and uncertainty

Usage:
    negbio_pipeline neg_chexpert [options] --output=<directory> <file> ...

Options:
    --neg-patterns=FILE                         Negation rules [default: negbio/chexpert/patterns/negation.txt]
    --pre-negation-uncertainty-patterns=FILE    Pre negation uncertainty rules
                                                [default: negbio/chexpert/patterns/pre_negation_uncertainty.txt]
    --post-negation-uncertainty-patterns=FILE   Post negation uncertainty rules
                                                [default: negbio/chexpert/patterns/post_negation_uncertainty.txt]
    --suffix=<suffix>                           Append an additional SUFFIX to file names. [default: .neg.xml]
    --verbose                                   Print more information about progress.
    --output=<directory>                        Specify the output directory.
"""
import os

from negbio.chexpert.stages.classify import ModifiedDetector
from negbio.cli_utils import parse_args, get_absolute_path
from negbio.pipeline.negdetect import detect
from negbio.pipeline.scan import scan_document


if __name__ == '__main__':
    argv = parse_args(__doc__)

    argv = get_absolute_path(argv,
                             '--pre-negation-uncertainty-patterns',
                             'negbio/chexpert/patterns/pre_negation_uncertainty.txt')
    argv = get_absolute_path(argv,
                             '--post-negation-uncertainty-patterns',
                             'negbio/chexpert/patterns/post_negation_uncertainty.txt')
    argv = get_absolute_path(argv,
                             '--neg-patterns',
                             'negbio/chexpert/patterns/negation.txt')

    neg_detector = ModifiedDetector(argv['--pre-negation-uncertainty-patterns'],
                                    argv['--neg-patterns'],
                                    argv['--post-negation-uncertainty-patterns'])
    scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  fn=detect, non_sequences=[neg_detector])
