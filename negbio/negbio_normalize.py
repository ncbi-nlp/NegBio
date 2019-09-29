"""
Usage:
    negbio_normalize [options] --output=<directory> <file> ...

Options:
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .normalized.xml]
    --verbose               Print more information about progress.
    --overwrite             Overwrite the output file.
"""

from negbio.cli_utils import parse_args
from negbio.pipeline2.pipeline import NegBioPipeline
from negbio.pipeline2.normalize_mimiccxr import MIMICCXRNormalizer

if __name__ == '__main__':
    argv = parse_args(__doc__)
    normalizer = MIMICCXRNormalizer()
    pipeline = NegBioPipeline(pipeline=[('MIMICCXRNormalizer', normalizer)])
    pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  overwrite=argv['--overwrite'])
