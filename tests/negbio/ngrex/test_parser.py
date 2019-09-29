import re

import pytest

from negbio import ngrex
from negbio.ngrex import parser


def test_lex():
    _test_lex_helper('{lemma:/xxx/} <{dependency:/nmod:without|x/} {lemma:/yyy/}')
    _test_lex_helper('{} <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}')
    _test_lex_helper('{}=t <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}=key')
    with pytest.raises(TypeError):
        parser.lexer.input(None)


def _test_lex_helper(s):
    parser.lexer.input(s)
    actual = ''.join([tok.value for tok in parser.lexer])
    expected = s.replace(' ', '')
    assert actual == expected


def test_yacc():
    # and
    _test_yacc("{} <{} {} <{} {}", "({}) <{} ({}) & ({}) <{} ({})")
    _test_yacc("{} <{} {} & <{} {}", "({}) <{} ({}) & ({}) <{} ({})")

    # or
    _test_yacc("{} <{} {} | <{} {}", "({}) <{} ({}) | ({}) <{} ({})")

    # ()
    _test_yacc("({lemma:/xxx/})", "{lemma:/xxx/}")
    _test_yacc("({lemma:/xxx/}) <{dependency:/nmod:without|x/} ({lemma:/yyy/})",
               "({lemma:/xxx/}) <{dependency:/nmod:without|x/} ({lemma:/yyy/})")

    _test_yacc("{lemma:/xxx/} <{dependency:/nmod:without|x/} {lemma:/yyy/}",
               "({lemma:/xxx/}) <{dependency:/nmod:without|x/} ({lemma:/yyy/})")
    _test_yacc("{lemma:/xxx/} >{dependency:/nmod:without/} {lemma:/yyy/}",
               "({lemma:/xxx/}) >{dependency:/nmod:without/} ({lemma:/yyy/})")
    _test_yacc("{lemma:/xxx/} >{dependency:/nmod:without/} ({lemma:/yyy/} >{} {lemma:/zzz/})",
               "({lemma:/xxx/}) >{dependency:/nmod:without/} (({lemma:/yyy/}) >{} ({lemma:/zzz/}))")
    _test_yacc("{} >{} {lemma:/left/} <{} {lemma:/question/}",
               "({}) >{} ({lemma:/left/}) & ({}) <{} ({lemma:/question/})")
    _test_yacc("{} <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}",
               "({}) <{dependency:/nsubj/} ({lemma:/suspect/,tag:/VBN/})")
    _test_yacc("{}=t <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}=key",
               "({}=t) <{dependency:/nsubj/} ({lemma:/suspect/,tag:/VBN/}=key)")

    with pytest.raises(KeyError):
        ngrex.compile("{}=t <{dependency:/nsubj/} {lemma:/suspect/,tag:/VBN/}=t")

    with pytest.raises(TypeError):
        ngrex.compile("xxx ? xxx")


def _test_yacc(s, expected):
    pattern = ngrex.compile(s)
    actual = re.sub('[$^]', '', str(pattern))
    assert actual == expected, '{} vs {}'.format(actual, expected)

