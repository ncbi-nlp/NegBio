

.. image:: https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true
   :target: https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true
   :alt: NegBio
----------------------

.. image:: https://img.shields.io/circleci/project/github/ncbi-nlp/NegBio.svg
   :alt: Build status
   :target: https://circleci.com/gh/ncbi-nlp/NegBio

.. image:: https://img.shields.io/pypi/v/negbio.svg
   :target: https://pypi.python.org/pypi/negbio
   :alt: Latest version on PyPI


NegBio is a high-performance NLP tool for negation and uncertainty detection in clinical texts (e.g. radiology reports).

Getting Started
---------------

These instructions will get you a copy of the project up and  run on your local machine for development and testing purposes.

Prerequisites
^^^^^^^^^^^^^

#. Copy the project on your local machine

.. code-block:: bash

   git clone https://github.com/ncbi-nlp/NegBio.git

Install environment
^^^^^^^^^^^^^^^^^^^

Install or update the `conda <https://conda.io>`_ environment specified in ``environment2.7.yml`` by running:

.. code-block:: bash

   # If the negbio2.7 environment already exists, remove it first
   conda env remove --name negbio2.7

   # Install the environment
   conda env create --file environment2.7.yml

Activate with ``conda activate negbio2.7`` (assumes ``conda`` version of `at least <https://github.com/conda/conda/blob/9d759d8edeb86569c25f6eb82053f09581013a2a/CHANGELOG.md#440-2017-12-20>`_ 4.4).
The environment should successfully install on both Linux and macOS.

Prepare the dataset
^^^^^^^^^^^^^^^^^^^

The program needs the reports with finding mentions annotated in `BioC format <http://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/BioC/>`_. 
Some examples can be found in the ``examples`` folder.

Run the script
^^^^^^^^^^^^^^

The easiest way is to run

.. code-block:: bash

   python negbio/main.py --out=examples examples/1.xml examples/2.xml

The script will detect negative and uncertain findings in files ``examples/1.xml`` and ``examples/2.xml``. 
It prints the results to the directory ``example``.
The dest file has the same basename as SOURCE and has 'neg.xml' as the suffix.

A more detailed usage can be obtained by running

.. code-block:: bash

   python negbio/main.py -h                                          
   Usage:
       negbio [options] --out=DIRECTORY SOURCE ...

   Options:
       --neg-patterns=FILE             negation rules [default: patterns/neg_patterns.txt]
       --uncertainty-patterns=FILE     uncertainty rules [default: patterns/uncertainty_patterns.txt]
       --model=MODEL_DIR               Bllip parser model directory

Alternatively, you can run the pipeline step-by-step.


#. ``pipeline/ssplit.py`` splits text into sentences.
#. ``pipeline/parse.py`` parse sentence using the `Bllip parser <https://github.com/BLLIP/bllip-parser>`_.
#. ``pipeline/ptb2ud.py`` convert the parse tree to universal dependencies using `Stanford converter <https://github.com/dmcc/PyStanfordDependencies>`_.
#. ``pipeline/negdetect.py`` detect negative and uncertain findings.

Customize patterns
^^^^^^^^^^^^^^^^^^

By default, the program uses the negation and uncertainty patterns in the ``patterns`` folder.
You can add more patterns if needed.
The pattern is a `semgrex-type <https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/semgraph/semgrex/SemgrexPattern.html>`_ pattern for matching node in the dependency graph.
Currently, we only support ``<`` and ``>`` operations.
A detailed grammar (using PLY, Python Lex-Yacc) can be found in ``ngrex/parser.py``.

Contributing
------------

Please read ``CONTRIBUTING.md`` for details on our code of conduct, and the process for submitting pull requests to us.

License
-------

see ``LICENSE.txt``.

Acknowledgments
---------------

This work was supported by the Intramural Research Programs of the National
Institutes of Health, National Library of Medicine.

Reference
---------


* Peng Y, Wang X, Lu L, Bagheri M, Summers RM, Lu Z. `NegBio: a high-performance tool for negation and uncertainty detection in radiology reports <https://arxiv.org/abs/1712.05898>`_. *AMIA 2018 Informatics Summit*. 2018.
