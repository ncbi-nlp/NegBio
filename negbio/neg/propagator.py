from __future__ import print_function

import logging
from negbio import semgraph


def propagate(G):

    logger = logging.getLogger(__name__)

    for i in range(0, 2):
        edges = []
        for node in G.nodes_iter():
            # hypoinflated but clear of
            if G.node[node]['lemma'] == 'hypoinflated':
                for child in G.successors_iter(node):
                    edge_dep = G.edge[node][child]['dependency']
                    if G.node[child]['lemma'] == 'clear' and edge_dep == 'conj:but':
                        for of in G.successors_iter(node):
                            of_dep = G.edge[node][of]['dependency']
                            if of_dep == 'nmod:of':
                                edges.append((child, of, {'dependency': of_dep}))
                        break

        for p, c, d in G.edges_iter(data=True):
            # propagate appos
            if d['dependency'] == 'appos':
                # x > y >appos > z
                for grandpa in G.predecessors_iter(p):
                    edge_dep = G[grandpa][p]['dependency']
                    edges.append((grandpa, c, {'dependency': edge_dep}))
                # x <neg < y >appos > z
                for child in G.successors_iter(p):
                    edge_dep = G.edge[p][child]['dependency']
                    if edge_dep == 'neg':
                        edges.append((c, child, {'dependency': edge_dep}))
            # propagate dep
            if d['dependency'] == 'dep' \
                    and G.node[p]['tag'].startswith('N') \
                    and G.node[c]['tag'].startswith('N'):
                for grandchild in G.successors_iter(c):
                    edge_dep = G.edge[c][grandchild]['dependency']
                    if edge_dep == 'neg':
                        edges.append((p, grandchild, {'dependency': edge_dep}))
            # propagate cop conjunction
            if d['dependency'].startswith('conj') \
                    and G.node[p]['tag'].startswith('N') \
                    and G.node[c]['tag'].startswith('N'):
                for child in G.successors_iter(p):
                    edge_dep = G.edge[p][child]['dependency']
                    if edge_dep in ('aux', 'cop', 'neg', 'amod'):
                        edges.append((c, child, {'dependency': edge_dep}))
                    if edge_dep in ('dep', 'compound') and G.node[child]['lemma'] == 'no':
                        edges.append((c, child, {'dependency': edge_dep}))
                    if edge_dep == 'case' and G.node[child]['lemma'] == 'without':
                        edges.append((c, child, {'dependency': edge_dep}))
            # propagate area/amount >of XXX
            if d['dependency'] == 'nmod:of' and G.node[p]['lemma'] in ('area', 'amount'):
                for grandpa in G.predecessors_iter(p):
                    edge_dep = G[grandpa][p]['dependency']
                    edges.append((grandpa, c, {'dependency': edge_dep}))
            # propagate combination of XXX
            if d['dependency'] == 'nmod:of' and G.node[p]['lemma'] == 'combination':
                for grandpa in G.predecessors_iter(p):
                    edge_dep = G[grandpa][p]['dependency']
                    edges.append((grandpa, c, {'dependency': edge_dep}))
            if d['dependency'] == 'nmod:of':
                for child in G.successors_iter(p):
                    edge_dep = G.edge[p][child]['dependency']
                    # propagate no <neg x >of XXX
                    if edge_dep == 'neg':
                        edges.append((c, child, {'dependency': edge_dep}))
                    # propagate without <case x >of XXX
                    if edge_dep == 'case' and G.node[child] == 'without':
                        edges.append((c, child, {'dependency': edge_dep}))
            # parse error
            # no xx and xxx
            if d['dependency'] == 'neg' and semgraph.has_out_node(G, p, ['or', 'and']):
                for child in G.successors_iter(p):
                    edge_dep = G.edge[p][child]['dependency']
                    if edge_dep == 'compound' and G.node[child]['tag'].startswith('N'):
                        edges.append((child, c, {'dependency': 'neg'}))

        has_more_edges = False
        for p, c, d in edges:
            if not G.has_edge(p, c):
                G.add_edge(p, c, attr_dict=d)
                has_more_edges = True

        if not has_more_edges:
            break

