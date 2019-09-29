"""
Detect negation and uncertainty

Usage:
    neg_chexpert [options] --output=<directory> <file> ...

Options:
    --neg-patterns=FILE                         Negation rules [default: patterns/chexpert_negation.yml]
    --pre-negation-uncertainty-patterns=FILE    Pre negation uncertainty rules
                                                [default: patterns/chexpert_pre_negation_uncertainty.yml]
    --post-negation-uncertainty-patterns=FILE   Post negation uncertainty rules
                                                [default: patterns/chexpert_post_negation_uncertainty.yml]
    --suffix=<suffix>                           Append an additional SUFFIX to file names. [default: .chexpert-neg.xml]
    --verbose                                   Print more information about progress.
    --output=<directory>                        Specify the output directory.
    --workers=<n>                               Number of threads [default: 1]
    --files_per_worker=<n>                      Number of input files per worker [default: 8]
    --overwrite                                 Overwrite the output file.
"""

from negbio.ext.chexpert_classify import CheXpertDetector
from negbio.cli_utils import parse_args, get_absolute_path, calls_asynchronously
from negbio.pipeline2.negdetect import NegBioNegDetector
from negbio.pipeline2.pipeline import NegBioPipeline

if __name__ == '__main__':
    argv = parse_args(__doc__)
    workers = int(argv['--workers'])
    if workers == 1:
        argv = get_absolute_path(argv,
                                 '--pre-negation-uncertainty-patterns',
                                 'negbio/chexpert/patterns/pre_negation_uncertainty.txt')
        argv = get_absolute_path(argv,
                                 '--post-negation-uncertainty-patterns',
                                 'negbio/chexpert/patterns/post_negation_uncertainty.txt')
        argv = get_absolute_path(argv,
                                 '--neg-patterns',
                                 'negbio/chexpert/patterns/negation.txt')

        neg_detector = NegBioNegDetector(CheXpertDetector(
            argv['--pre-negation-uncertainty-patterns'],
            argv['--neg-patterns'],
            argv['--post-negation-uncertainty-patterns']))
        pipeline = NegBioPipeline(pipeline=[('ModifiedDetector', neg_detector)])
        pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                      overwrite=argv['--overwrite'])
    else:
        calls_asynchronously(argv, 'python -m negbio.negbio_neg_chexpert')
