"""
Convert from parse tree to universal dependencies

Usage:
    negbio ptb2ud [options] --out=<directory> <file> ...

Options:
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .ud.xml]
    --verbose               Print more information about progress.
"""
from negbio.cli_utils import parse_args
from negbio.pipeline.ptb2ud import Ptb2DepConverter, Lemmatizer, convert
from negbio.pipeline.scan import scan_document

if __name__ == '__main__':
    argv = parse_args(__doc__)
    ptb2dep = Ptb2DepConverter(universal=True)
    lemmatizer = Lemmatizer()
    scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  fn=convert, non_sequences=[ptb2dep, lemmatizer])
