NegBio User Guide
=================

Run the pipeline step-by-step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Convert text file to BioC format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
   :linenos:

   $ python negbio/negbio_cli.py text2bioc --output examples/test.xml examples/00000086.txt examples/00019248.txt


Another most commonly used command is:


.. code-block:: bash
   :linenos:

   $ find /path -type f | python negbio/negbio_cli.py text2bioc --output examples/test.xml


Run the pipeline step-by-step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. ``text2bioc`` combines text into a BioC XML file.
#. ``normalize`` removes noisy text such as ``[**Patterns**]``.
#. ``section_split`` splits the report into sections based on titles.
#. ``ssplit`` splits text into sentences.
#. ``dner`` detects UMLS concepts using MetaMap.
#. ``parse`` parses sentence using the `Bllip parser <https://github.com/BLLIP/bllip-parser>`_.
#. ``ptb2ud`` converts the parse tree to universal dependencies using `Stanford converter <https://github.com/dmcc/PyStanfordDependencies>`_.
#. ``neg`` detects negative and uncertain findings.


Customize patterns
^^^^^^^^^^^^^^^^^^

By default, the program uses the negation and uncertainty patterns in the ``patterns`` folder.
However, you are free to create your own patterns.
The pattern is a `semgrex-type <https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/semgraph/semgrex/SemgrexPattern.html>`_ pattern for matching node in the dependency graph.
Currently, we only support ``<`` and ``>`` operations.
A detailed grammar specification (using PLY, Python Lex-Yacc) can be found in ``ngrex/parser.py``.


