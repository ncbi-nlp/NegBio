"""
Detect negative and uncertain findings from FILEs.

Usage:
    negbio simp [options] --metamap=<binary> --output=<file> <file> ...

Options:
    --metamap=<binary>              The MetaMap binary
    --bllip-model=<directory>       Bllip parser model directory.
    --cuis=<file>                   Specify CUI list. [default: examples/cuis-cvpr2017.txt]
    --newline_is_sentence_break     Whether to treat newlines as sentence breaks. True means that a newline is always a
                                    sentence break. False means to ignore newlines for the purpose of sentence
                                    splitting. This is appropriate for continuous text, when just the non-whitespace
                                    characters should be used to determine sentence breaks.
    --section_patterns=<file>       Specify section title list for matching.
    --neg-patterns=<file>           Specify negation rules [default: patterns/neg_patterns.txt]
    --uncertainty-patterns=<file>   Specify uncertainty rules [default: patterns/uncertainty_patterns.txt]
    --suffix=<suffix>               Append an additional SUFFIX to file names. [default: .neg.xml]
    --verbose                       Print more information about progress.
    --output=<file>                 Specify the output file name.
"""

import os

import bioc

import pymetamap
from negbio.cli_utils import parse_args
from negbio.negbio_dner import read_cuis
from negbio.negbio_section_split import read_section_titles
from negbio.pipeline import parse, ssplit, ptb2ud, negdetect, pipeline

if __name__ == '__main__':
    argv = parse_args(__doc__)

    splitter = ssplit.NltkSSplitter(newline=argv['--newline_is_sentence_break'])
    parser = parse.Bllip(model_dir=argv['--bllip-model'])
    ptb2dep = ptb2ud.Ptb2DepConverter(universal=True)
    lemmatizer = ptb2ud.Lemmatizer()
    mm = pymetamap.MetaMap.get_instance(argv['--metamap'])
    neg_detector = negdetect.Detector(argv['--neg-patterns'], argv['--uncertainty-patterns'])

    if argv['--cuis'] is None:
        cuis = None
    else:
        cuis = read_cuis(argv['--cuis'])

    if argv['--section_patterns'] is None:
        section_patterns = None
    else:
        section_patterns = read_section_titles(argv['--section_patterns'])

    collection = pipeline.process_text(
        sources=argv['<file>'], metamap=mm, splitter=splitter, parser=parser, ptb2dep=ptb2dep,
        lemmatizer=lemmatizer, neg_detector=neg_detector, cuis=cuis, sec_title_patterns=section_patterns)
    with open(os.path.expanduser(argv['--output']), 'w') as fp:
        bioc.dump(collection, fp)
