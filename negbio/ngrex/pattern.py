import itertools
import re
import collections

L = '<'
R = '>'
LEFT = '<'
RIGHT = '>'


class NgrexPattern(object):
    """
    A NgrexPattern is a tgrep-type pattern for matching node configurations in Networkx structures.
    """

    def __init__(self):
        self._pattern = None

    def finditer(self, graph):
        """
        Returns an iterator yielding MatcherObj instances over all matches for the ngrex pattern 
        in graph.
        
        Args:
            graph(DiGraph): graph
            
        Yields:
            MatcherObj: an iterator yielding MatcherObj instances over all matches for the 
                ngrex pattern in graph.
        """
        raise NotImplementedError('Should have implemented this')

    @property
    def pattern(self):
        """
        str: The pattern string from which the ngrex object was compiled.
        """
        return self._pattern

    def __str__(self):
        return self.pattern


class NodePattern(NgrexPattern):
    def __init__(self, attributes, name=None):
        super(NodePattern, self).__init__()
        self._name = name
        self._attributes = _get_attributes_regex(attributes)
        self._pattern = '{' + _attributes_to_str(self._attributes) + '}'
        if name:
            self._pattern += '=' + name

    def finditer(self, graph):
        for node in graph.nodes():
            if self._attributes:
                if _match(self._attributes, graph.node[node]):
                    yield MatcherObj(self, graph, [(self._name, node)])
            else:
                yield MatcherObj(self, graph, [(self._name, node)])


class EdgePattern(NgrexPattern):
    def __init__(self, governor, dependant, edge_attributes, direction=LEFT):
        """
        Args:
            direction(str): right if 'governor >edge dependant', left if 'dependant <edge governor'
        """
        super(EdgePattern, self).__init__()
        self._governor = governor
        self._dependant = dependant
        self._direction = direction
        self._edge_attributes = _get_attributes_regex(edge_attributes)

        if self._direction == LEFT:
            args = (dependant, '<', governor)
        else:
            args = (governor, '>', dependant)
        self._pattern = '({args[0].pattern}) {args[1]}{{{edge}}} ({args[2].pattern})'.format(
            args=args, edge=_attributes_to_str(self._edge_attributes))

    def finditer(self, graph):
        governors = self._governor.finditer(graph)
        dependants = self._dependant.finditer(graph)
        for g, d in itertools.product(governors, dependants):
            for p, c, e in graph.edges(data=True):
                if p == g.group(0) and c == d.group(0):
                    if _match(self._edge_attributes, e):
                        if self._direction == LEFT:
                            yield MatcherObj(self, graph, d._nodes + g._nodes)
                        else:
                            yield MatcherObj(self, graph, g._nodes + d._nodes)


class CoordinationPattern(NgrexPattern):
    def __init__(self, pattern1, pattern2, is_conj=True):
        """
        Args:
            is_conj(bool): if is_conj is true, then it is an "AND"; otherwise, it is an "OR".
        """
        super(CoordinationPattern, self).__init__()
        self._pattern1 = pattern1
        self._pattern2 = pattern2
        self._is_conj = is_conj
        self._pattern = '{} {} {}'.format(pattern2.pattern,
                                          '&' if is_conj else '|',
                                          pattern1.pattern)

    def finditer(self, graph):
        if self._is_conj:
            matchers1 = self._pattern1.finditer(graph)
            matchers2 = self._pattern2.finditer(graph)
            for m1, m2 in itertools.product(matchers1, matchers2):
                if m1.group(0) == m2.group(0):
                    nodes = list(m1._nodes)
                    if len(m2._nodes) > 2:
                        nodes.extend(m2._nodes[1:])
                    yield MatcherObj(self, graph, nodes)
        else:
            for m in self._pattern1.finditer(graph):
                yield m
            for m in self._pattern2.finditer(graph):
                yield m


class MatcherObj:
    """
    Match objects always have a boolean value of True.
    """

    def __init__(self, pattern, graph, nodes):
        """
        Args:
            nodes(list): [(name, node)]
        """
        self._pattern = pattern
        self._graph = graph
        self._nodes = nodes

    def __bool__(self):
        return True

    def group(self, index):
        """
        Returns the input node captured by the given group during the previous match operation.
        """
        return self._nodes[index][1]

    def groups(self):
        """
        Returns a list containing all the subgroups of the match, from 0 up to however many nodes 
        are in the pattern.
        """
        return (node[1] for node in self._nodes)

    def get(self, name):
        for node in self._nodes:
            if node[0] == name:
                return node[1]
        raise KeyError(name)

    @property
    def pattern(self):
        """
        The expression object whose `finditer()` produced this instance
        """
        return self._pattern

    @property
    def graph(self):
        """
        The graph passed to `finditer()`
        """
        return self._graph


def validate_names(pattern):
    def _helper(p, names):
        if isinstance(p, NodePattern):
            if p._name in names:
                raise KeyError(p._name)
            if p._name:
                names.add(p._name)
        elif isinstance(p, EdgePattern):
            _helper(p._governor, names)
            _helper(p._dependant, names)
        elif isinstance(p, CoordinationPattern):
            _helper(p._pattern1, names)
            _helper(p._pattern2, names)
    _helper(pattern, set())


def _get_attributes_regex(attributes):
    def _get_regex(v):
        v = v[1:-1]
        if v:
            if v[0] != '^':
                v = '^' + v
            if v[-1] != '$':
                v += '$'
        return re.compile(v)
    return {k: _get_regex(v) for k, v in attributes.items()}


def _match(attributes, element):
    for k, v in attributes.items():
        if k not in element or not v.match(element[k]):
            return False
    return True


def _attributes_to_str(attributes):
    return ','.join(['{}:/{}/'.format(k, v.pattern) for k, v in attributes.items()])
