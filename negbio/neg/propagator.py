from __future__ import print_function

import logging

from negbio.neg import semgraph
import collections


Edge = collections.namedtuple('Edge', ['gov', 'dep', 'data'])


def propagate(G):

    for i in range(0, 2):
        edges = []
        for node in G.nodes():
            # hypoinflated but clear of
            if G.node[node]['lemma'] == 'hypoinflated':
                for child in G.successors(node):
                    edge_dep = G[node][child]['dependency']
                    if G.node[child]['lemma'] == 'clear' and edge_dep == 'conj:but':
                        for of in G.successors(node):
                            of_dep = G[node][of]['dependency']
                            if of_dep == 'nmod:of':
                                edges.append(Edge(child, of, of_dep))
                        break

        for p, c, d in G.edges(data=True):
            # propagate appos
            if d['dependency'] == 'appos':
                # x > y >appos > z
                for grandpa in G.predecessors(p):
                    edge_dep = G[grandpa][p]['dependency']
                    edges.append(Edge(grandpa, c, edge_dep))
                # x <neg < y >appos > z
                for child in G.successors(p):
                    edge_dep = G[p][child]['dependency']
                    if edge_dep == 'neg':
                        edges.append(Edge(c, child, edge_dep))
            # propagate dep
            if d['dependency'] == 'dep' \
                    and G.node[p]['tag'].startswith('N') \
                    and G.node[c]['tag'].startswith('N'):
                for grandchild in G.successors(c):
                    edge_dep = G[c][grandchild]['dependency']
                    if edge_dep == 'neg':
                        edges.append(Edge(p, grandchild, edge_dep))
            # propagate cop conjunction
            if d['dependency'].startswith('conj') \
                    and G.node[p]['tag'].startswith('N') \
                    and G.node[c]['tag'].startswith('N'):
                for child in G.successors(p):
                    edge_dep = G[p][child]['dependency']
                    if edge_dep in ('aux', 'cop', 'neg', 'amod'):
                        edges.append(Edge(c, child, edge_dep))
                    if edge_dep in ('dep', 'compound') and G.node[child]['lemma'] == 'no':
                        edges.append(Edge(c, child, edge_dep))
                    if edge_dep == 'case' and G.node[child]['lemma'] == 'without':
                        edges.append(Edge(c, child, edge_dep))

            # propagate area/amount >of XXX
            if d['dependency'] == 'nmod:of' and G.node[p]['lemma'] in ('area', 'amount'):
                for grandpa in G.predecessors(p):
                    edge_dep = G[grandpa][p]['dependency']
                    edges.append(Edge(grandpa, c, edge_dep))
            # propagate combination of XXX
            if d['dependency'] == 'nmod:of' and G.node[p]['lemma'] == 'combination':
                for grandpa in G.predecessors(p):
                    edge_dep = G[grandpa][p]['dependency']
                    edges.append(Edge(grandpa, c, edge_dep))
            if d['dependency'] == 'nmod:of':
                for child in G.successors(p):
                    edge_dep = G[p][child]['dependency']
                    # propagate no <neg x >of XXX
                    if edge_dep == 'neg':
                        edges.append(Edge(c, child, edge_dep))
                    # propagate without <case x >of XXX
                    if edge_dep == 'case' and G.node[child] == 'without':
                        edges.append(Edge(c, child, edge_dep))
            # parse error
            # no xx and xxx
            if d['dependency'] == 'neg' and semgraph.has_out_node(G, p, ['or', 'and']):
                for child in G.successors(p):
                    edge_dep = G[p][child]['dependency']
                    if edge_dep == 'compound' and G.node[child]['tag'].startswith('N'):
                        edges.append(Edge(child, c, 'neg'))

        has_more_edges = False
        for e in edges:
            if not G.has_edge(e.gov, e.dep):
                assert isinstance(e.data, str) or isinstance(e.data, unicode), type(e.data)
                G.add_edge(e.gov, e.dep, dependency=e.data)
                has_more_edges = True

        if not has_more_edges:
            break

