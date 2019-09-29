from negbio.neg.utils import contains, intersect


def test_contains():
    assert contains(lambda a: a == 1, [0, 1, 2])
    assert not contains(lambda a: a == 3, [0, 1, 2])
    assert not contains(lambda a: a == 3, [])
    assert not contains(None, [False, False, False])


def test_intersect():
    assert intersect((0, 1), (.5, .9))
    assert not intersect((0, 1), (-1, 0))
    assert intersect((0, 1), (-1, .1))
    assert not intersect((0, 1), (1, 2))
    assert intersect((0, 1), (.9, 2))
    assert intersect((.5, .9), (0, 1))
