import sys

import pytest

from negbio.pipeline2.parse import NegBioParser
from tests.negbio.utils import text_to_bioc


parser = NegBioParser()


def test_parse():
    text = 'No pneumothorax.'
    tree = '(S1 (S (S (NP (DT No) (NN pneumothorax))) (. .)))'
    t = parser.parse(text)
    assert str(t) == tree, str(t)

    with pytest.raises(ValueError):
        parser.parse('')

    with pytest.raises(ValueError):
        parser.parse('\n')

    if sys.version_info[0] == 2:
        with pytest.raises(ValueError):
            parser.parse(u'\xe6')
    else:
        t = parser.parse(u'\xe6')
        assert str(t) == u'(S1 (S (NP (NN \xe6))))'


def test_parse_doc():
    text = 'No pneumothorax.'
    tree = '(S1 (S (S (NP (DT No) (NN pneumothorax))) (. .)))'
    document = text_to_bioc([text], type='d/p/s')
    d = parser.__call__(document)
    assert d.passages[0].sentences[0].infons['parse tree'] == tree

    # test empty sentence
    document = text_to_bioc([''], type='d/p/s')
    d = parser.__call__(document)
    assert d.passages[0].sentences[0].infons['parse tree'] is None
