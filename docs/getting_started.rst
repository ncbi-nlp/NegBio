Getting Started with NegBio
===========================

These instructions will get you a copy of the project up and run on your local machine for development and testing purposes.
The package should successfully install on Linux (and possibly macOS).

Installing
----------

Prerequisites
~~~~~~~~~~~~~

*  python >2.4
*  Linux

Note: since v1.0, MetaMap is not required. You can use the CheXpert vocabularies (``negbio/``) instead.


*  MetaMap >2016 (if you need

MetaMap can be downloaded from `https://metamap.nlm.nih.gov/MainDownload.shtml <https://metamap.nlm.nih.gov/MainDownload.shtml>`_.
Installation instructions can be found at `https://metamap.nlm.nih.gov/Installation.shtml <https://metamap.nlm.nih.gov/Installation.shtml>`_.
Please make sure that both ``skrmedpostctl`` and ``wsdserverctl`` are started.

Installing from source
~~~~~~~~~~~~~~~~~~~~~~

1. Download the source code from GitHub ``git clone https://github.com/ncbi-nlp/NegBio.git``
2. Change to the directory of ``NegBio``
3. Install required packages: ``pip install -r requirements.txt``
4. Install NLTK data: ``python -m nltk.downloader universal_tagset punkt wordnet``
5. Add the code directory to ``PYTHONPATH``: ``export PYTHONPATH=.:$PYTHONPATH``


Using NegBio
------------

Prepare the dataset
~~~~~~~~~~~~~~~~~~~

The program inputs are reports in plain text. Each report needs to be in a single file.
Some examples can be found in the ``examples`` folder.

Run the script
~~~~~~~~~~~~~~

The easiest way is to run the following command by replacing ``<METAMAP_BINARY>`` with the actual **ABSOLUTE** path, such as **META_MAP_HOME/bin/metamap16**

.. code-block:: bash
   :linenos:

   $ python negbio/main_text.py --metamap=<METAMAP_BINARY> --out=examples/test.neg.xml examples/00000086.txt examples/00019248.txt

The script will

1. Combine ``examples/00000086.txt`` and ``examples/00019248.txt`` into one BioC XML file
2. Detect UMLS concepts (CUIs) using MetaMap (by default using the CUI list ``examples\cuis-cvpr2017.txt``
3. Detect negative and uncertain CUIs using rules in  ``patterns/neg_patterns.txt`` and ``patterns/uncertainty_patterns.txt``
4. Save the results in ``examples/test.neg.xml``


More options (e.g., setting the CUI list or rules) can be obtained by running

.. code-block:: bash

   $ python negbio/main.py --help


Next Steps
----------

To start learning how to use NegBio, see the :doc:`user_guide`.
