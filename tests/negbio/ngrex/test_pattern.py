import networkx as nx
from negbio import ngrex


def get_graph():
    G = nx.DiGraph()
    G.add_node('xxx', attr_dict={'lemma': 'xxx'})
    G.add_node('yyy', attr_dict={'lemma': 'yyy'})
    G.add_node('zzz', attr_dict={'lemma': 'zzz'})
    G.add_edge('xxx', 'yyy', attr_dict={'dependency': 'aaa'})
    G.add_edge('yyy', 'zzz', attr_dict={'dependency': 'bbb'})
    G.add_edge('xxx', 'zzz', attr_dict={'dependency': 'ccc'})
    return G


def helper(G, p, expected):
    pattern = ngrex.compile(p)
    print(pattern.pattern)
    # actual = {m.group(0) for m in pattern.finditer(G)}
    actual = set()
    for m in pattern.finditer(G):
        actual.add(m.group(0))
    assert actual == expected, '{} vs {}'.format(actual, expected)


def test_regex():
    G = get_graph()
    helper(G, '{} >{dependency:/aaa|bbb/} {}', {'xxx', 'yyy'})


def test_attribute():
    G = get_graph()
    helper(G, '{} >{dependency:/aaa|bbb/} {}', {'xxx', 'yyy'})
    helper(G, '{} >{tag:/aaa|bbb/} {}', set())


def test_relation():
    G = get_graph()
    helper(G, '{lemma:/xxx/} >{dependency:/aaa/} {lemma:/yyy/}', {'xxx'})
    helper(G, '{lemma:/yyy/} <{dependency:/aaa/} {lemma:/xxx/}', {'yyy'})
    helper(G, '{} >{} {}', {'xxx', 'yyy'})


def test_relation_next():
    G = get_graph()
    helper(G, '{lemma:/xxx/} >{dependency:/aaa/} ({lemma:/yyy/} >{dependency:/bbb/} {lemma:/zzz/})',
           {'xxx'})


def test_relation_conj():
    G = get_graph()
    helper(G, '{} >{} {lemma:/yyy/} >{} {lemma:/zzz/}', {'xxx'})
    helper(G, '{} >{} {lemma:/yyy/} <{} {lemma:/zzz/}', set())


def test_relation_disj():
    G = get_graph()
    helper(G, '{} >{dependency:/aaa/} {} | >{dependency:/bbb/} {}', {'xxx', 'yyy'})


def test_variables():
    G = get_graph()
    pattern = ngrex.compile('{}=t >{dependency:/aaa|bbb/} {}')
    print(pattern.pattern)
    actual = {m.get('t') for m in pattern.finditer(G)}
    assert actual == {'xxx', 'yyy'}


if __name__ == '__main__':
    # test_relation()
    # test_relation_next()
    test_relation_conj()
    # test_relation_disj()
    # test_regex()
    # test_attribute()
    # test_variables()
