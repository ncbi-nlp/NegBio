NegBio User Guide
=================

Install Environment
^^^^^^^^^^^^^^^^^^^

1. Copy the project on your local machine

.. code-block:: bash

   git clone https://github.com/ncbi-nlp/NegBio.git

2. Install `conda <https://conda.io>`_

.. code-block:: bash

   wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
   chmod 777 Miniconda2-latest-Linux-x86_64.sh
   ./Miniconda2-latest-Linux-x86_64.sh
   conda update conda # By default the version 4.3 is installed

3. Install or update the conda environment specified in ``environment2.7.yml`` by running:

.. code-block:: bash

   # If the negbio2.7 environment already exists, remove it first
   conda env remove --name negbio2.7

   # Install the environment
   conda env create --file environment2.7.yml

4. Activate with ``conda activate negbio2.7`` (assumes ``conda`` version of `at least <https://github.com/conda/conda/blob/9d759d8edeb86569c25f6eb82053f09581013a2a/CHANGELOG.md#440-2017-12-20>`_ 4.4).

5. Add the code directory to ``PYTHONPATH``.

.. code-block:: bash

   export PYTHONPATH=.:$PYTHONPATH

6. Install NLTK data.

.. code-block:: bash

   python -m nltk.downloader universal_tagset punkt wordnet


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