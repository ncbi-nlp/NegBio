import pytest

from negbio import ngrex
from negbio.ngrex import parser
from ply.lex import LexToken


def test_lex():
    _test_lex('{lemma:/xxx/} <{dependency:/nmod:without|x/} {lemma:/yyy/}')
    _test_lex('{} <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}')
    _test_lex('{}=t <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}=key')
    with pytest.raises(TypeError):
        _test_yacc("xxx")


def _test_lex(s):
    parser.lexer.input(s)
    for tok in parser.lexer:
        print(tok)


def test_yacc():
    # _test_yacc("{lemma:/xxx/} <{dependency:/nmod:without|x/} {lemma:/yyy/}")
    # _test_yacc("{lemma:/xxx/} >{dependency:/nmod:without/} {lemma:/yyy/}")
    # _test_yacc("{lemma:/xxx/} >{dependency:/nmod:without/} ({lemma:/yyy/} >{} {lemma:/zzz/})")
    # _test_yacc("{} >{} {lemma:/left/} <{} {lemma:/question/}")
    # _test_yacc("{} <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}")
    _test_yacc("{}=t <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}=key")
    with pytest.raises(KeyError):
        _test_yacc("{}=t <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}=t")


def _test_yacc(s):
    pattern = ngrex.compile(s)
    print(pattern)


if __name__ == '__main__':
    test_lex()
    test_yacc()
