"""
Start : ALIGNRELN SubNode "\n"
      | SubNode ( ":" SubNode )* "\n"
      ;

SubNode : "(" SubNode ")" RelationDisj?
        | ModNode RelationDisj?
        ;

RelationDisj : RelationConj ( "|" RelationConj )*

RelationConj : ModRelation ( "&"? ModRelation )*

ModRelation : RelChild
            | "!" RelChild
            | "?" RelChild
            ;

RelChild : "[" RelationDisj "]"
         | Relation
         ;

Relation : ( ( ( (IDENTIFIER ("," IDENTIFIER)?)? RELATION ( IDENTIFIER | REGEX )? ) ( "=" IDENTIFIER )? ) | ALIGNRELN)
           ( ModNode | "(" SubNode ")" )
         ;

NodeDisj : "[" NodeConj ( "|" NodeConj )* "]"
         ;

NodeConj : ModNode ( "&"? ModNode )*
         ;

ModNode : Child
        | "!" Child
        ;

Child : NodeDisj
      | Description
      ;

Description :
  "{" ( 
          (  ( IDENTIFIER ":" (IDENTIFIER | REGEX) ) (";" ( IDENTIFIER ":" ( IDENTIFIER | REGEX ) ) )* "}")
        | ( ROOT "}" )
        | ( EMPTY "}" )
        | "}" )
      ("=" IDENTIFIER )?
"""
from ply import lex
from ply import yacc

from negbio.ngrex import pattern


t_ignore = ' \t\r'

tokens = (
    'RELATION',
    'IDENTIFIER',
    'REGEX',
)

literals = '{}()&[]:|,='

t_RELATION = r'[<>]'
t_IDENTIFIER = r'([^ \n\r!@#$%^&*()+={}\[\]\|\\;\':",./<>?`~-])+'
t_REGEX = r'/(/|[^\n\r/])*?/'


def t_error(t):
    raise TypeError('Unknown text "%s"' % (t.value,))

lexer = lex.lex()


def p_SubNode(p):
    """
    SubNode : ModNode
            | ModNode RelationDisj
            | '(' SubNode ')' 
            | '(' SubNode ')' RelationDisj
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        conj_patterns = []
        for relation_conj in p[2][1]:
            conj_patterns.append(_merge_conj(p[1], relation_conj[1]))
        p[0] = _merge_disj(conj_patterns)
    elif len(p) == 4:
        p[0] = p[2]
    elif len(p) == 5:
        conj_patterns = []
        for relation_conj in p[4][1]:
            conj_patterns.append(_merge_conj(p[2], relation_conj[1]))
        p[0] = _merge_disj(conj_patterns)


def _merge_disj(patterns):
    while len(patterns) > 1:
        p1 = patterns.pop()
        p2 = patterns.pop()
        patterns.append(pattern.CoordinationPattern(p1, p2, False))
    return patterns[0]


def _merge_conj(p1, relations):
    patterns = []
    for reln, attributes, node in relations:
        if reln == '<':
            p = pattern.EdgePattern(node, p1, attributes, direction=pattern.L)
        else:
            p = pattern.EdgePattern(p1, node, attributes, direction=pattern.R)
        patterns.append(p)
    if len(patterns) == 1:
        return patterns[0]
    else:
        while len(patterns) > 1:
            p1 = patterns.pop()
            p2 = patterns.pop()
            patterns.append(pattern.CoordinationPattern(p1, p2, True))
        return patterns[0]


def p_RelationDisj(p):
    """
    RelationDisj : RelationConj
                 | RelationConj '|' RelationDisj
    """
    """
    Returns:
        ("OR", relation_list)
    """
    if len(p) == 2:
        p[0] = ('OR', [p[1]])
    elif len(p) == 4:
        p[0] = ('OR', [p[1]] + p[3][1])


def p_RelationConj(p):
    """
    RelationConj : ModRelation
                 | ModRelation RelationConj
                 | ModRelation '&' RelationConj
    """
    # (AND, [ModRelations])
    if len(p) == 2:
        p[0] = ('AND', [p[1]])
    if len(p) == 3:
        p[0] = ('AND', [p[1]] + p[2][1])
    if len(p) == 4:
        p[0] = ('AND', [p[1]] + p[3][1])


def p_ModRelation(p):
    """
    ModRelation : RelChild
    """
    p[0] = p[1]


def p_RelChild(p):
    """
    RelChild : Relation
    """
    p[0] = p[1]


def p_Relation(p):
    """
    Relation : RELATION '{' Attributes '}' Relation_Next
    """
    """
    Returns:
        < edge_attributes node
    """
    p[0] = (p[1], p[3], p[5])


def p_Relation_Next(p):
    """
    Relation_Next : ModNode
                  | '(' SubNode ')'
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_ModNode(p):
    """
    ModNode : Child
    """
    p[0] = p[1]


def p_Child(p):
    """
    Child : Description
    """
    p[0] = p[1]


def p_Description(p):
    """
    Description : '{' Attributes '}'
                | '{' Attributes '}' '=' IDENTIFIER
    """
    if len(p) == 4:
        p[0] = pattern.NodePattern(p[2])
    else:
        p[0] = pattern.NodePattern(p[2], p[5])

def p_Attributes(p):
    """
    Attributes : IDENTIFIER ':' REGEX
               | IDENTIFIER ':' REGEX ',' Attributes
               | empty
    """
    if len(p) == 4:
        p[0] = {p[1]: p[3]}
    elif len(p) == 6:
        p[0] = {p[1]: p[3]}
        p[0].update(p[5])
    else:
        p[0] = {}


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    raise TypeError("Syntax error at '%s'" % p.value)

parser = yacc.yacc()

