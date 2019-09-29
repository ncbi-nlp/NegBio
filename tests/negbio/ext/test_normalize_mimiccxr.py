from negbio.ext.normalize_mimiccxr import trim, normalize
from tests.negbio.utils import text_to_bioc


def test_trim():
    text = '[**Hospital 9**] MEDICAL CONDITION'
    expe = '                 MEDICAL CONDITION'
    actu = trim(text)
    assert expe == actu

    text = 'consult service. M[0KM[0KM[0KM[0KM[0KM'
    expe = 'consult service.                      '
    actu = trim(text)
    assert expe == actu


def test_normalize():
    text = '[**Hospital 9**] MEDICAL CONDITION'
    expe = '                 MEDICAL CONDITION'
    d = text_to_bioc([text], 'd/p')
    d = normalize(d)
    assert d.passages[0].text == expe

    d.passages[0].text = None
    normalize(d)

    # skip if there is more than one passages
    d = text_to_bioc([text, text], 'd/p')
    d = normalize(d)
    assert d.passages[0].text == text

    del d.passages[:]
    normalize(d)
