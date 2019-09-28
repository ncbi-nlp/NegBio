"""
A NgrexPattern is a tgrep-type pattern for matching node configurations in one of the Networkx 
structures. Unlike tgrep but like Unix grep, there is no pre-indexing of the data to be searched. 
Rather there is a linear scan through the graph where matches are sought.

A node/edge is represented by a set of attributes and their values contained by curly braces: 
`{attr1:value1;attr2:value2;...}`. Therefore, {} represents any node/edge in the graph. 
Attributes must be plain strings; values can be regular expressions blocked off by "/". 
(I think regular expressions must match the whole attribute value; so that /NN/ matches "NN" only, 
while /NN.* / matches "NN", "NNS", "NNP", etc.)
"""
from typing import List, Dict

import yaml

from . import parser
from . import pattern


def compile(ngrex):
    """
    Compiles the given expression into a pattern
    
    Args:
        ngrex(str): expression
        
    Returns:
        NgrexPattern: a pattern
    """
    p = parser.yacc.parse(ngrex)
    pattern.validate_names(p)
    return p


def load(filename):
    """
    Read a pattern file
    
    Args:
        filename(str): file name
    
    Returns:
        list: a list of NgexPattern
    """
    patterns = []
    with open(filename) as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue
            patterns.append(compile(line))
    return patterns


def load_yml(filename) -> List[Dict]:
    """
    Read a pattern file in the yaml format

    Args:
        filename(str): file name

    Returns:
        list: a list of dict NgexPattern
    """
    with open(filename) as fp:
        patterns = yaml.load(fp, yaml.FullLoader)

    for p in patterns:
        p['patternobj'] = compile(p['pattern'])
    return patterns
