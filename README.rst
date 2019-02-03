.. image:: https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true
   :target: https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true
   :alt: NegBio

-----------------------

.. image:: https://img.shields.io/travis/yfpeng/NegBio/master.svg
   :target: https://travis-ci.org/yfpeng/NegBio
   :alt: Build status

.. image:: https://img.shields.io/pypi/v/negbio.svg
   :target: https://pypi.python.org/pypi/negbio
   :alt: PyPI version

.. image:: https://img.shields.io/readthedocs/negbio.svg
   :target: http://negbio.readthedocs.io
   :alt: RTD version



NegBio is a high-performance NLP tool for negation and uncertainty detection in clinical texts (e.g. radiology reports).


Get started
===========

Install NegBio
~~~~~~~~~~~~~~

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

   $ python negbio/main_chexpert.py text --output=examples \
        examples/00000086.txt examples/00019248.txt

.. code-block:: bash

   $ python negbio/main_chexpert.py bioc --output=examples examples/1.xml


Using MetaMap
_____________

If you want to use MetaMap, run the following command by replacing ``<METAMAP_BINARY>`` with the actual **ABSOLUTE**
path, such as **META_MAP_HOME/bin/metamap16**

.. code-block:: bash

   $ python negbio/main_mm.py text \
        --metamap=<METAMAP_BINARY> \
        --output=examples \
        examples/00000086.txt examples/00019248.txt

.. code-block:: bash

   $ python negbio/main_mm.py bioc \
        --metamap=<METAMAP_BINARY> \
        --output=examples \
        examples/1.xml


Documentation
=============

negbio `documentation <http://negbio.readthedocs.io/en/latest/>`_ is available on Read The Docs.

See `Getting Started <http://negbio.readthedocs.io/en/latest/getting_started.html>`_ for installation and basic
information. To contribute to negbio, read our `contribution guide </CONTRIBUTING.md>`_.

Citing NegBio
=============

If you're running the NegBio pipeline, please cite:

*  Peng Y, Wang X, Lu L, Bagheri M, Summers RM, Lu Z. `NegBio: a high-performance tool for negation and uncertainty
   detection in radiology reports <https://arxiv.org/abs/1712.05898>`_. *AMIA 2018 Informatics Summit*. 2018.
*  Wang X, Peng Y, Lu L, Bagheri M, Lu Z, Summers R. `ChestX-ray8: Hospital-scale Chest X-ray database and benchmarks
   on weakly-supervised classification and localization of common thorax diseases <https://arxiv.org/abs/1705.02315>`_.
   *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*. 2017, 2097-2106.

Disclaimer
==========
This tool shows the results of research conducted in the Computational Biology Branch, NCBI. The information produced
on this website is not intended for direct diagnostic use or medical decision-making without review and oversight
by a clinical professional. Individuals should not change their health behavior solely on the basis of information
produced on this website. NIH does not independently verify the validity or utility of the information produced
by this tool. If you have questions about the information produced on this website, please see a health care
professional. More information about NCBI's disclaimer policy is available.
