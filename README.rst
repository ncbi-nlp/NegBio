

.. image:: https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true
   :target: https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true
   :alt: NegBio

----------------------

.. image:: https://travis-ci.com/yfpeng/negbio.svg?token=rpjX5A9sQziaNbzs65j6&branch=master
   :alt: Build status
   :target: https://travis-ci.com/yfpeng/negbio

.. image:: https://img.shields.io/pypi/v/negbio.svg
   :target: https://pypi.python.org/pypi/negbio
   :alt: Latest version on PyPI


NegBio is a high-performance NLP tool for negation and uncertainty detection in clinical texts (e.g. radiology reports).

Getting Started
---------------

These instructions will get you a copy of the project up and run on your local machine for development and testing purposes.
The package should successfully install on Linux (and possibly macOS).

Install environment
^^^^^^^^^^^^^^^^^^^

Copy the project on your local machine

.. code-block:: bash

   git clone https://github.com/ncbi-nlp/NegBio.git

Install or update the `conda <https://conda.io>`_ environment specified in ``environment2.7.yml`` by running:

.. code-block:: bash

   # If the negbio2.7 environment already exists, remove it first
   conda env remove --name negbio2.7

   # Install the environment
   conda env create --file environment2.7.yml

Activate with ``conda activate negbio2.7`` (assumes ``conda`` version of `at least <https://github.com/conda/conda/blob/9d759d8edeb86569c25f6eb82053f09581013a2a/CHANGELOG.md#440-2017-12-20>`_ 4.4).

Prepare the dataset
^^^^^^^^^^^^^^^^^^^

The program needs the reports with finding mentions annotated in `BioC format <http://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/BioC/>`_.
All finding mentions have to be specified on the passage level. For example:

.. code-block:: xml

   <document>
    <id>00000086</id>
    <passage>
      <offset>0</offset>
      <text>findings: pa and lat cxr at 7:34 p.m.. heart and mediastinum are stable. 
            lungs are unchanged. air- filled cystic changes. no pneumothorax. osseous structures 
            unchanged scoliosis impression: stable chest. dictating </text>
      <annotation id="24">
        <infon key="term">Pneumothorax</infon>
        <infon key="CUI">C0032326</infon>
        <infon key="annotator">MetaMap</infon>
        <infon key="semtype">dsyn</infon>
        <location length="12" offset="125"/>
        <text>pneumothorax</text>
      </annotation>
    </passage>
  </document>

More examples can be found in the ``examples`` folder.

Run the script
^^^^^^^^^^^^^^

The easiest way is to run

.. code-block:: bash

   python negbio/main.py --out=examples examples/1.xml examples/2.xml

The script will detect negative and uncertain findings in files ``examples/1.xml`` and ``examples/2.xml``. 
It saves the results (``1.neg.xml`` and ``2.neg.xml``) in the directory ``examples``. 

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

Contributing
------------

Please read ``CONTRIBUTING.md`` for details on our code of conduct, and the process for submitting pull requests to us.

License
-------

see ``LICENSE.txt``.

Acknowledgments
---------------

This work was supported by the Intramural Research Programs of the National Institutes of Health, National Library of Medicine.

Reference
---------


* Peng Y, Wang X, Lu L, Bagheri M, Summers RM, Lu Z. `NegBio: a high-performance tool for negation and uncertainty detection in radiology reports <https://arxiv.org/abs/1712.05898>`_. *AMIA 2018 Informatics Summit*. 2018.
