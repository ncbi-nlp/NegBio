"""
Parse sentences

Usage:
    negbio_parse [options] --output=<directory> <file> ...

Options:
    --model=<directory>     Bllip parser model directory.
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .bllip.xml]
    --verbose               Print more information about progress.
    --workers=<n>           Number of threads [default: 1]
    --files_per_worker=<n>  Number of input files per worker [default: 8]
    --overwrite             Overwrite the output file.
"""
from negbio.cli_utils import parse_args, calls_asynchronously
from negbio.pipeline2.parse import NegBioParser
from negbio.pipeline2.pipeline import NegBioPipeline


if __name__ == '__main__':
    argv = parse_args(__doc__)
    workers = int(argv['--workers'])
    if workers == 1:
        parser = NegBioParser(model_dir=argv['--model'])
        pipeline = NegBioPipeline(pipeline=[('NegBioParser', parser)])
        pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                      overwrite=argv['--overwrite'])
    else:
        calls_asynchronously(argv, 'python -m negbio.negbio_parse')
