"""
Detect negation and uncertainty

Usage:
    negbio_pipeline neg [options] --output=<directory> <file> ...

Options:
    --neg-patterns=<file>           Specify negation rules [default: negbio/patterns/neg_patterns.txt]
    --uncertainty-patterns=<file>   Specify uncertainty rules [default: negbio/patterns/uncertainty_patterns.txt]
    --suffix=<suffix>               Append an additional SUFFIX to file names. [default: .neg.xml]
    --verbose                       Print more information about progress.
    --output=<directory>            Specify the output directory.
"""
import os

from negbio.cli_utils import parse_args, get_absolute_path
from negbio.neg.neg_detector import Detector
from negbio.pipeline.negdetect import detect
from negbio.pipeline.scan import scan_document

if __name__ == '__main__':
    argv = parse_args(__doc__)

    argv = get_absolute_path(argv,
                             '--neg-patterns',
                             'negbio/patterns/neg_patterns.txt')
    argv = get_absolute_path(argv,
                             '--uncertainty-patterns',
                             'negbio/patterns/uncertainty_patterns.txt')

    neg_detector = Detector(os.path.realpath(argv['--neg-patterns']),
                            os.path.realpath(argv['--uncertainty-patterns']))
    scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  fn=detect, non_sequences=[neg_detector])
