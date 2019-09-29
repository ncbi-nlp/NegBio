"""
Convert from parse tree to universal dependencies

Usage:
    negbio_ptb2ud [options] --output=<directory> <file> ...

Options:
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .ud.xml]
    --verbose               Print more information about progress.
    --workers=<n>           Number of threads [default: 1]
    --files_per_worker=<n>  Number of input files per worker [default: 8]
    --overwrite             Overwrite the output file.
"""
from negbio.cli_utils import parse_args, calls_asynchronously
from negbio.pipeline2.ptb2ud import NegBioPtb2DepConverter
from negbio.pipeline2.pipeline import NegBioPipeline

if __name__ == '__main__':
    argv = parse_args(__doc__)
    workers = int(argv['--workers'])
    if workers == 1:
        converter = NegBioPtb2DepConverter(universal=True)
        pipeline = NegBioPipeline(pipeline=[('NegBioPtb2DepConverter', converter)])
        pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                      overwrite=argv['--overwrite'])
    else:
        calls_asynchronously(argv, 'python -m negbio.negbio_ptb2ud')
