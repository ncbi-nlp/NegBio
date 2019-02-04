Getting Started with NegBio
===========================

These instructions will get you a copy of the project up and run on your local machine for development and testing
purposes. The package should successfully install on Linux (and possibly macOS).

Installing
----------

Prerequisites
~~~~~~~~~~~~~

*  python >2.4
*  Linux
*  Java

Note: since v1.0, MetaMap is not required. You can use the CheXpert vocabularies (``negbio/chexpert/phrases``) instead.
If you want to use MetaMap, it can be downloaded from `https://metamap.nlm.nih.gov/MainDownload.shtml <https://metamap.nlm.nih.gov/MainDownload.shtml>`_.
Installation instructions can be found at `https://metamap.nlm.nih.gov/Installation.shtml <https://metamap.nlm.nih.gov/Installation.shtml>`_.
Please make sure that both ``skrmedpostctl`` and ``wsdserverctl`` are started.

Installing from source
~~~~~~~~~~~~~~~~~~~~~~

1. Download the source code from GitHub

   .. code-block:: bash

      $ git clone https://github.com/ncbi-nlp/NegBio.git

2. Change to the directory of ``NegBio``
3. Install required packages.

   If you use ``pip``,

   .. code-block:: bash

      $ pip install -r requirements.txt

   If you use `Conda <https://conda.io>`_


   .. code-block:: bash

      $ conda env create -f environment2.7.yml


4. Install NLTK data

   .. code-block:: bash

      $ python -m nltk.downloader universal_tagset punkt wordnet


5. Add the code directory to ``PYTHONPATH``: ``export PYTHONPATH=.:$PYTHONPATH``


Using NegBio
------------

Prepare the dataset
~~~~~~~~~~~~~~~~~~~

The inputs can be in either plain text or `BioC <http://bioc.sourceforge.net/>`_ format. If the reports are in plain
text, each report needs to be in a single file. Some examples can be found in the ``examples`` folder.

Run the script
~~~~~~~~~~~~~~

There are two ways to run the pipeline.

Using CheXpert algorithm
________________________

If you want to use the CheXpert method, run one of the following lines

.. code-block:: bash

   $ python negbio/main_chexpert.py text --output=examples/test.neg.xml \
        examples/00000086.txt examples/00019248.txt

.. code-block:: bash

   $ python negbio/main_chexpert.py bioc --output=examples/test.neg.xml examples/1.xml

The script will

1. [Optional] Combine ``examples/00000086.txt`` and ``examples/00019248.txt`` into one BioC XML file
2. Detect concepts using CheXpert pre-defined vocabularies (by default using the list ``negbio\chexpert\phrases``)
3. Detect positive, negative and uncertain concepts using rules in  ``negbio\chexpert\patterns``
4. Save the results in ``examples/test.neg.xml``

More options (e.g., setting the CUI list or rules) can be obtained by running

.. code-block:: bash

   $ python negbio/main_chexpert.py --help

Using MetaMap
_____________

If you want to use MetaMap, run the following command by replacing ``<METAMAP_BIN>`` with the actual **ABSOLUTE**
path, such as **META_MAP_HOME/bin/metamap16**

.. code-block:: bash

   $ export METAMAP_BIN=META_MAP_HOME/bin/metamap16
   $ python negbio/main_mm.py text \
        --metamap=$METAMAP_BIN \
        --output=examples/test.neg.xml \
        examples/00000086.txt examples/00019248.txt

.. code-block:: bash

   $ export METAMAP_BIN=META_MAP_HOME/bin/metamap16
   $ python negbio/main_mm.py bioc \
        --metamap=$METAMAP_BIN \
        --output=examples/test.neg.xml \
        examples/1.xml

The script will

1. [Optional] Combine ``examples/00000086.txt`` and ``examples/00019248.txt`` into one BioC XML file
2. Detect UMLS concepts (CUIs) using MetaMap (by default using the CUI list ``examples\cuis-cvpr2017.txt``
3. Detect negative and uncertain CUIs using rules in  ``patterns``
4. Save the results in ``examples/test.neg.xml``

More options (e.g., setting the CUI list or rules) can be obtained by running

.. code-block:: bash

   $ python negbio/main_mm.py --help


Next Steps
----------

To start learning how to use NegBio, see the :doc:`user_guide`.
