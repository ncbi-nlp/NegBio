"""
Detect negation and uncertainty

Usage:
    negbio_neg [options] --output=<directory> <file> ...

Options:
    --neg-patterns=<file>           Specify negation rules [default: patterns/neg_patterns2.yml]
    --uncertainty-patterns=<file>   Specify uncertainty rules [default: patterns/uncertainty_patterns.yml]
    --suffix=<suffix>               Append an additional SUFFIX to file names. [default: .neg.xml]
    --verbose                       Print more information about progress.
    --output=<directory>            Specify the output directory.
    --workers=<n>                   Number of threads [default: 1]
    --files_per_worker=<n>          Number of input files per worker [default: 32]
    --overwrite                     Overwrite the output file.
"""
from negbio.cli_utils import parse_args, get_absolute_path, calls_asynchronously
from negbio.neg.neg_detector import Detector
from negbio.pipeline2.negdetect import NegBioNegDetector
from negbio.pipeline2.pipeline import NegBioPipeline

if __name__ == '__main__':
    argv = parse_args(__doc__)
    workers = int(argv['--workers'])
    if workers == 1:
        argv = get_absolute_path(argv,
                                 '--neg-patterns',
                                 'negbio/patterns/neg_patterns.txt')
        argv = get_absolute_path(argv,
                                 '--uncertainty-patterns',
                                 'negbio/patterns/uncertainty_patterns.txt')

        neg_detector = NegBioNegDetector(Detector(argv['--neg-patterns'],
                                                  argv['--uncertainty-patterns']))
        pipeline = NegBioPipeline(pipeline=[('NegBioNegDetector', neg_detector)])
        pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                      overwrite=argv['--overwrite'])
    else:
        calls_asynchronously(argv, 'python -m negbio.negbio_neg')
