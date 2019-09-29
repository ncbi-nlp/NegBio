"""
Detect negation and uncertainty

Usage:
    negbio_neg2 [options] --output=<directory> <file> ...

Options:
    --neg-patterns=FILE                         Negation rules [default: patterns/neg_patterns2.yml]
    --pre-negation-uncertainty-patterns=FILE    Pre negation uncertainty rules
                                                [default: patterns/chexpert_pre_negation_uncertainty.yml]
    --post-negation-uncertainty-patterns=FILE   Post negation uncertainty rules
                                                [default: patterns/post_negation_uncertainty.yml]
    --neg-regex-patterns=FILE                   Regex Negation rules [default: patterns/neg_regex_patterns.yml]
    --uncertainty-regex-patterns=FILE           Regex uncertainty rules [default: patterns/uncertainty_regex_patterns.yml]
    --suffix=<suffix>               Append an additional SUFFIX to file names. [default: .neg2.xml]
    --verbose                       Print more information about progress.
    --output=<directory>            Specify the output directory.
    --workers=<n>                   Number of threads [default: 1]
    --files_per_worker=<n>          Number of input files per worker [default: 32]
    --overwrite                     Overwrite the output file.
"""
from negbio.cli_utils import parse_args, calls_asynchronously
from negbio.pipeline2.negdetect2 import NegBioNegDetector2, Detector2
from negbio.pipeline2.pipeline import NegBioPipeline

if __name__ == '__main__':
    argv = parse_args(__doc__)
    workers = int(argv['--workers'])
    if workers == 1:
        neg_detector = NegBioNegDetector2(
            Detector2(argv['--pre-negation-uncertainty-patterns'],
                      argv['--neg-patterns'],
                      argv['--post-negation-uncertainty-patterns'],
                      argv['--neg-regex-patterns'],
                      argv['--uncertainty-regex-patterns']))
        pipeline = NegBioPipeline(pipeline=[('NegBioNegDetector', neg_detector)])
        pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                      overwrite=argv['--overwrite'])
    else:
        calls_asynchronously(argv, 'python -m negbio.negbio_neg2')
