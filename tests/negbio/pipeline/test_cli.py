import logging

from docopt import docopt

from negbio import negbio_pipeline, negbio_text2bioc, negbio_ssplit, negbio_section_split, negbio_parse


def test_negbio():
    doc = negbio_pipeline.__doc__
    args = docopt(doc, 'text2bioc a b c'.split())
    assert args['<command>'] == 'text2bioc'
    assert args['<args>'] == ['a', 'b', 'c']


def test_text2bioc():
    doc = negbio_text2bioc.__doc__
    args = docopt(doc, 'text2bioc --verbose --output=out a b c'.split())
    assert args['--verbose']
    assert args['--output'] == 'out'
    assert args['<file>'] == ['a', 'b', 'c']
    args = docopt(doc, 'text2bioc --output=out a b c'.split())
    assert not args['--verbose']


def test_ssplit():
    doc = negbio_ssplit.__doc__
    args = docopt(doc, 'ssplit --suffix suffix --newline_is_sentence_break --output out a b c'.split())
    assert args['--newline_is_sentence_break']
    assert args['--output'] == 'out'
    assert args['--suffix'] == 'suffix'
    assert args['<file>'] == ['a', 'b', 'c']


def test_section_split():
    doc = negbio_section_split.__doc__
    args = docopt(doc, 'section_split --pattern pattern --output out a b c'.split())
    assert args['--output'] == 'out'
    assert args['--pattern'] == 'pattern'
    assert args['<file>'] == ['a', 'b', 'c']


def test_parse():
    doc = negbio_parse.__doc__
    args = docopt(doc, 'parse --model model --output out a b c'.split())
    assert args['--output'] == 'out'
    assert args['--model'] == 'model'
    assert args['<file>'] == ['a', 'b', 'c']


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    test_ssplit()
