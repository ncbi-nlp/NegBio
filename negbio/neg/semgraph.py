import logging

import networkx as nx


def load(sentence):
    """
    Args:
        sentence(BioCSentence): a sentence with tag, text, lemma, start and end
    
    Returns:
        DiGraph: dependency graph
    
    Examples:
        ```xml
        <annotation id="T0">
          <infon key="lemma">small</infon>
          <infon key="tag">JJ</infon>
          <location length="5" offset="128"/>
          <text>Small</text>
        </annotation>
        ```
    """
    graph = nx.DiGraph()
    for ann in sentence.annotations:
        loc = ann.get_total_location()
        graph.add_node(ann.id, tag=ann.infons['tag'], text=ann.text, lemma=ann.infons['lemma'].lower(),
                       start=loc.offset, end=loc.offset + loc.length)
    for rel in sentence.relations:
        dependant = None
        governor = None
        for node in rel.nodes:
            if node.role == 'dependant':
                dependant = node.refid
            elif node.role == 'governor':
                governor = node.refid
        if not dependant or not governor:
            logging.debug('Cannot find dependant or governor at {}'.format(sentence))
        graph.add_edge(governor, dependant, dependency=rel.infons['dependency'], id=rel.id)
    return graph


def has_out_edge(graph, node, dependencies):
    for _, _, d in graph.out_edges(node, data=True):
        if d['dependency'] in dependencies:
            return True
    return False


def has_in_edge(graph, node, dependencies):
    for _, _, d in graph.in_edges(node, data=True):
        if d['dependency'] in dependencies:
            return True
    return False


def has_out(graph, node, lemmas, dependencies):
    return get_out(graph, node, lemmas, dependencies) is not None


def get_out(graph, node, lemmas, dependencies):
    for _, c, d in graph.out_edges(node, data=True):
        if d['dependency'] in dependencies and graph.node[c]['lemma'] in lemmas:
            return c
    return None


def get_in(graph, node, lemmas, dependencies):
    for p, _, d in graph.in_edges(node, data=True):
        if d['dependency'] in dependencies and graph.node[p]['lemma'] in lemmas:
            return p
    return None


def has_in(graph, node, lemmas, dependencies):
    return get_in(graph, node, lemmas, dependencies) is not None


def has_out_node(graph, node, lemmas):
    for child in graph.successors(node):
        if graph.node[child]['lemma'] in lemmas:
            return True
    return False


def has_in_node(graph, node, lemmas):
    for child in graph.predecessors(node):
        if graph.node[child]['lemma'] in lemmas:
            return True
    return False
