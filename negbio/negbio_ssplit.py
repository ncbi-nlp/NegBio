"""
Split text into sentences

Usage:
    negbio_pipeline ssplit [options] --output=<directory> <file> ...

Options:
    --newline_is_sentence_break     Whether to treat newlines as sentence breaks. True means that a newline is always a
                                    sentence break. False means to ignore newlines for the purpose of sentence
                                    splitting. This is appropriate for continuous text, when just the non-whitespace
                                    characters should be used to determine sentence breaks. [default=False]
    --suffix=<suffix>               Append an additional SUFFIX to file names. [default: .ssplit.xml]
    --output=<directory>            Specify the output directory.
    --verbose                       Print more information about progress.
"""
from negbio.pipeline.scan import scan_document
from negbio.pipeline.ssplit import NegBioSSplitter
from negbio.cli_utils import parse_args

if __name__ == '__main__':
    argv = parse_args(__doc__)
    splitter = NegBioSSplitter(newline=argv['--newline_is_sentence_break'])
    scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  fn=splitter.split_doc, non_sequences=[])
