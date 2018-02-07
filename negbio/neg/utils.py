def contains(func, iterable):
    """
    Return true if one element of iterable for which function returns true.
    """
    if func is None:
        func = bool
    for x in iterable:
        if func(x):
            return True
    return False


def intersect(range1, range2):
    """
    Args:
        range1(int, int): [begin, end)
        range2(int, int): [begin, end)
    """
    if range1[0] <= range2[0] < range1[1]:
        return True
    elif range1[0] < range2[1] <= range1[1]:
        return True
    elif range2[0] <= range1[0] < range2[1]:
        return True
    elif range2[0] < range1[1] <= range2[1]:
        return True
    return False
