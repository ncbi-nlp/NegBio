import logging

from negbio.pipeline.parse import Bllip


def test_Bllip():
    b = Bllip()
    t = b.parse('hello world!')
    assert str(t) == '(S1 (S (NP (NN hello) (NN world) (NN !))))'


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    test_Bllip()
