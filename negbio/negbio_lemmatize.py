"""
Determines the lemma

Usage:
    negbio_lemmatize [options] --output=<directory> <file> ...

Options:
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .ud.xml]
    --verbose               Print more information about progress.
    --overwrite             Overwrite the output file.
"""
from negbio.cli_utils import parse_args
from negbio.pipeline2.lemmatize import Lemmatizer
from negbio.pipeline2.pipeline import NegBioPipeline

if __name__ == '__main__':
    argv = parse_args(__doc__)
    lemmatizer = Lemmatizer()
    pipeline = NegBioPipeline(pipeline=[('Lemmatizer', lemmatizer)])
    pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  overwrite=argv['--overwrite'])
