NegBio User Guide
=================

Run the pipeline step-by-step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The step-by-step pipeline generates all intermediate documents. You can easily rerun one step if it makes errors.
The whole steps are

1. ``text2bioc`` combines text into a BioC XML file.
2. ``normalize`` removes noisy text such as ``[**Patterns**]``.
3. ``section_split`` splits the report into sections based on titles at ``patterns/section_titles.txt``
4. ``ssplit`` splits text into sentences.
5. Named entity recognition

   a. ``dner_mm`` detects UMLS concepts using MetaMap.
   b. ``dner_chexpert`` detects concepts using the CheXpert vocabularies at ``negbio/chexpert/phrases``.

6. ``parse`` parses sentence using the `Bllip parser <https://github.com/BLLIP/bllip-parser>`_.
7. ``ptb2ud`` converts the parse tree to universal dependencies using `Stanford converter <https://github.com/dmcc/PyStanfordDependencies>`_.
8. Negation detection

   a. ``neg`` detects negative and uncertain findings.
   b. ``neg_chexpert`` detects positive, negative and uncertain findings (recommended)

9. ``cleanup`` removes intermediate information.

Steps 2-10 will process the input files one-by-one and generate the results in the output directory.
The 2nd and 3rd can be skipped. You can chose either step 5 or 6 for named entity recognition.

1. Convert text files to BioC format
------------------------------------

You can skip this step if the reports are already in the `BioC <http://bioc.sourceforge.net/>`_ format.
**If you have lots of reports, it is recommended to put them into several BioC files, for example, 100 reports per BioC file.**

.. code-block:: bash

   $ export BIOC_DIR=/path/to/bioc
   $ export TEXT_DIR=/path/to/text
   $ negbio_pipeline text2bioc --output=$BIOC_DIR/test.xml $TEXT_DIR/*.txt

Another most commonly used command is:

.. code-block:: bash

   $ find $TEXT_DIR -type f | negbio_pipeline text2bioc --output=$BIOC_DIR

2. Normalize reports
--------------------

This step removes the noisy text such as ``[**Patterns**]`` in the MIMIC-III reports.

.. code-block:: bash

   $ negbio_pipeline normalize --output=$OUTPUT_DIR $INPUT_DIR/*.xml

3. Split each report into sections
-----------------------------------

This step splits the report into sections.
The default section titles is at ``patterns/section_titles.txt``.
You can specify customized section titles using the option ``--pattern=<file>``.

.. code-block:: bash

   $ negbio_pipeline section_split --output=$OUTPUT_DIR $INPUT_DIR/*.xml


4. Splits each report into sentences
------------------------------------

This step splits the report into sentences using the NLTK splitter
(`nltk.tokenize.sent_tokenize <https://www.nltk.org/api/nltk.tokenize.html>`_).

.. code-block:: bash

   $ negbio_pipeline ssplit --output=$OUTPUT_DIR $INPUT_DIR/*.xml


5. Named entity recognition
---------------------------

This step recognizes named entities (e.g., findings, diseases, devices) from the reports.
The first version of NegBio uses MetaMap to detect UMLS concepts.

MetaMap can be can be downloaded from `https://metamap.nlm.nih.gov/MainDownload.shtml <https://metamap.nlm.nih.gov/MainDownload.shtml>`_.
Installation instructions can be found at `https://metamap.nlm.nih.gov/Installation.shtml <https://metamap.nlm.nih.gov/Installation.shtml>`_.
Before using MetaMap, please make sure that both ``skrmedpostctl`` and ``wsdserverctl`` are started.

MetaMap intends to extract all UMLS concepts.
Many of them are not irrelevant to radiology.
Therefore, it is better to specify the UMLS concepts of interest via ``--cuis=<file>``

.. code-block:: bash

   $ export METAMAP_BIN=META_MAP_HOME/bin/metamap16
   $ negbio_pipeline dner_mm --metamap=$METAMAP_BIN --output=$OUTPUT_DIR $INPUT_DIR/*.xml

NegBio also integrates the CheXpert vocabularies to recognize the presence of 14 observations.
All vocabularies can be found at ``negbio/chexpert/phrases``.
Each file in the folder represents one type of named entities with various text expressions.
So far, NegBio does not support adding more types in the folder, but you can add more text expressions of the type.

.. code-block:: bash

   $ negbio_pipeline dner_chexpert --output=$OUTPUT_DIR $INPUT_DIR/*.xml


In general, MetaMap is more comprehensive while CheXpert is more accurate on 14 types of findings.
MetaMap is also slower and easier to break than CheXpert.


6. Parse the sentence
---------------------

This step parses sentence using the `Bllip parser <https://github.com/BLLIP/bllip-parser>`_.

.. code-block:: bash

   $ negbio_pipeline parse --output=$OUTPUT_DIR $INPUT_DIR/*.xml


7. Convert the parse tree to UD
-------------------------------

This step converts the parse tree to universal dependencies using `Stanford converter <https://github.com/dmcc/PyStanfordDependencies>`_.

.. code-block:: bash

   $ negbio_pipeline ptb2ud --output=$OUTPUT_DIR $INPUT_DIR/*.xml


8. Detect negative and uncertain findings
-----------------------------------------

This step detects negative and uncertain findings using patterns.
By default, the program uses the negation and uncertainty patterns in the ``negbio/patterns`` folder.
However, you are free to create your own patterns via ``--neg-patterns=<file>`` and ``--uncertainty-patterns=<file>``.
The pattern is a `semgrex-type <https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/semgraph/semgrex/SemgrexPattern.html>`_
pattern for matching node in the dependency graph.
Currently, we only support ``<`` and ``>`` operations.
A detailed grammar specification (using PLY, Python Lex-Yacc) can be found in ``ngrex/parser.py``.

.. code-block:: bash

   $ negbio_pipeline neg --output=$OUTPUT_DIR $INPUT_DIR/*.xml

NegBio also integrates the CheXpert algorithms.
Different from the original NegBio, CheXpert utilizes a 3-phase pipeline consisting of pre-negation uncertainty,
negation, and post-negation uncertainty (`Irvin et al., 2019 <https://arxiv.org/abs/1901.07031>`_).
Each phase consists of rules which are matched against the mention; if a match is found, then the mention is classified
accordingly (as uncertain in the first or third phase, and as negative in the second phase).
If a mention is not matched in any of the phases, it is classified as positive.

Generally, the CheXpert contains more rules and is more accurate than the original NegBio.

.. code-block:: bash

   $ negbio_pipeline neg_chexpert --output=$OUTPUT_DIR $INPUT_DIR/*.xml

Similarly, you are free to create patterns via ``--neg-patterns=<file>``, ``--pre-uncertainty-patterns=<file>``, and
``--post-uncertainty-patterns=<file>``.

9. Cleans intermediate information
----------------------------------

This step removes intermediate information (sentence annotations) from the BioC files.

.. code-block:: bash

   $ negbio_pipeline cleanup --output=$OUTPUT_DIR $INPUT_DIR/*.xml

