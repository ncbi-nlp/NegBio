"""
Split text into sentences

Usage:
    negbio_ssplit [options] --output=<directory> <file> ...

Options:
    --newline_is_sentence_break     Whether to treat newlines as sentence breaks. True means that
                                    a newline is always a sentence break. False means to ignore
                                    newlines for the purpose of sentence splitting. This is
                                    appropriate for continuous text, when just the non-whitespace
                                    characters should be used to determine sentence breaks.
                                    [default=False]
    --suffix=<suffix>               Append an additional SUFFIX to file names.
                                    [default: .ssplit.xml]
    --output=<directory>            Specify the output directory.
    --verbose                       Print more information about progress.
    --overwrite                     Overwrite the output file.
    --workers=<n>                               Number of threads [default: 1]
    --files_per_worker=<n>                      Number of input files per worker [default: 8]
"""
from negbio.pipeline2.pipeline import NegBioPipeline
from negbio.pipeline2.ssplit import NegBioSSplitter
from negbio.cli_utils import parse_args, calls_asynchronously

if __name__ == '__main__':
    argv = parse_args(__doc__)
    workers = int(argv['--workers'])
    if workers == 1:
        splitter = NegBioSSplitter(newline=argv['--newline_is_sentence_break'])
        pipeline = NegBioPipeline(pipeline=[('NegBioSSplitter', splitter)])
        pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                      overwrite=argv['--overwrite'])
    else:
        calls_asynchronously(argv, 'python -m negbio.negbio_ssplit')
