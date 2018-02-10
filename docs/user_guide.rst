NegBio User Guide
=================

Run the pipeline step-by-step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. ``pipeline/text2bioc.py`` combines text into a BioC XML file.
#. ``pipeline/ssplit.py`` splits text into sentences.
#. ``pipeline/dner_mm.py`` detects UMLS concepts using MetaMap.
#. ``pipeline/parse.py`` parses sentence using the `Bllip parser <https://github.com/BLLIP/bllip-parser>`_.
#. ``pipeline/ptb2ud.py`` converts the parse tree to universal dependencies using `Stanford converter <https://github.com/dmcc/PyStanfordDependencies>`_.
#. ``pipeline/negdetect.py`` detects negative and uncertain findings.


Customize patterns
^^^^^^^^^^^^^^^^^^

By default, the program uses the negation and uncertainty patterns in the ``patterns`` folder.
However, you are free to create your own patterns.
The pattern is a `semgrex-type <https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/semgraph/semgrex/SemgrexPattern.html>`_ pattern for matching node in the dependency graph.
Currently, we only support ``<`` and ``>`` operations.
A detailed grammar specification (using PLY, Python Lex-Yacc) can be found in ``ngrex/parser.py``.