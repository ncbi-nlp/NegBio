"""
Clean up sentences

Usage:
    negbio_cleanup [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .negbio.xml]
    --verbose               Print more information about progress.
    --output=<directory>    Specify the output directory.
    --overwrite             Overwrite the output file.
    --workers=<n>           Number of threads [default: 1]
    --files_per_worker=<n>  Number of input files per worker [default: 8]
"""

from negbio.cli_utils import parse_args, calls_asynchronously
from negbio.pipeline2.cleanup import CleanUp
from negbio.pipeline2.pipeline import NegBioPipeline

if __name__ == '__main__':
    argv = parse_args(__doc__)
    workers = int(argv['--workers'])
    if workers == 1:
        cleanup = CleanUp()
        pipeline = NegBioPipeline(pipeline=[('CleanUp', cleanup)])
        pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                      overwrite=argv['--overwrite'])
    else:
        calls_asynchronously(argv, 'python -m negbio.negbio_clean')
