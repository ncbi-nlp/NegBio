"""
Detect negation and uncertainty

Usage:
    negbio_cli neg_chexpert [options] --output=<directory> <file> ...

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
from negbio.cli_utils import parse_args
from negbio.pipeline.negdetect import detect
from negbio.pipeline.scan import scan_document

if __name__ == '__main__':
    argv = parse_args(__doc__)
    neg_detector = ModifiedDetector(argv['--pre-negation-uncertainty-patterns'],
                                    argv['--neg-patterns'],
                                    argv['--post-negation-uncertainty-patterns'])
    scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  fn=detect, non_sequences=[neg_detector])
