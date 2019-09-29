from negbio.pipeline2.lemmatize import Lemmatizer
from negbio.pipeline2.ptb2ud import NegBioPtb2DepConverter
from tests.negbio.utils import text_to_bioc


def test_lemmatize_doc():
    converter = NegBioPtb2DepConverter(representation='CCprocessed', universal=True)
    lemmatizer = Lemmatizer()

    text = 'no evidence of focal infiltrate, effusion or pneumothorax.'
    tree = '(S1 (S (S (NP (NP (DT no) (NN evidence)) (PP (IN of) (NP (NP (JJ focal)' \
           ' (NN infiltrate)) (, ,) (NP (NN effusion)) (CC or) (NP (NN pneumothorax)))))) (. .)))'
    d = text_to_bioc([text], type='d/p/s')
    s = d.passages[0].sentences[0]
    s.infons['parse tree'] = tree
    converter.__call__(d)

    expected = []
    for ann in s.annotations:
        expected.append(ann.infons['lemma'])
        del ann.infons['lemma']

    lemmatizer(d)
    for i, ann in enumerate(s.annotations):
        assert expected[i] == ann.infons['lemma']
