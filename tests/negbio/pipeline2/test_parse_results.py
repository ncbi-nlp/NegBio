import pytest

from negbio.pipeline2.ptb2ud import NegBioPtb2DepConverter
from tests.negbio.utils import text_to_bioc
from tests.negbio.pipeline2.test_parse import parser


def test_parse():
    converter = NegBioPtb2DepConverter(representation='CCprocessed', universal=True)
    # neg(evidence-2, no-1)
    # !root(ROOT-0, evidence-2)
    # !case(infiltrate-5, of-3)
    # amod(infiltrate-5, focal-4)
    # nmod:of(evidence-2, infiltrate-5)
    # nmod:of(evidence-2, effusion-7)
    # conj:or(infiltrate-5, effusion-7)
    # cc(infiltrate-5, or-8)
    # nmod:of(evidence-2, pneumothorax-9)
    # conj:or(infiltrate-5, pneumothorax-9)
    text = 'no evidence of focal infiltrate, effusion or pneumothorax.'
    tree = '(S1 (S (S (NP (NP (DT no) (NN evidence)) (PP (IN of) (NP (NP (JJ focal)' \
           ' (NN infiltrate)) (, ,) (NP (NN effusion)) (CC or) (NP (NN pneumothorax)))))) (. .)))'
    t = parser.parse(text)
    assert str(t) == tree

    d = text_to_bioc([text], type='d/p/s')
    s = d.passages[0].sentences[0]
    s.infons['parse tree'] = tree
    converter.__call__(d)

    # print(repr(d))

    for i, word in enumerate('no evidence of focal infiltrate , effusion or pneumothorax .'.split()):
        assert s.annotations[i].text == word

    for i, dep in enumerate('neg case amod nmod:of punct nmod:of conj:or cc nmod:of conj:or punct'.split()):
        assert s.relations[i].infons['dependency'] == dep
