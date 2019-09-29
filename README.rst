.. image:: https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true
   :target: https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true
   :alt: NegBio

-----------------------


NegBio is a high-performance NLP tool for negation and uncertainty detection in clinical texts (e.g. radiology reports).


Note
====

This is a NegBio branch to construct the labels from the MIMIC-III-CXR reports. To use the order version, please see `v0.9.4 <https://github.com/ncbi-nlp/NegBio/tree/v0.9.4>`_.


Run NegBio
==========

1. Sectioned report CSVs. See the https://github.com/MIT-LCP/mimic-cxr for details.

2. Download NegBio

.. code-block:: bash

   git clone --single-branch --branch MIMIC-CXR https://github.com/ncbi-nlp/NegBio.git
   cd path/to/NegBio


3. Prepare virtual environment

.. code-block:: bash

   conda create --name negbio python=3.6
   source activate negbio


or

.. code-block:: bash

   python3 -m venv negbio
   source negbio/bin/activate


4. Install required packages

.. code-block:: bash

   pip install --upgrade pip setuptools
   pip install -r requirements3.txt


5. Setup enviroments

.. code-block:: bash

   export OUTPUT=mimic_cxr
   export OUTPUT_LABELS=$OUTPUT/mimic_cxr_negbio_labels.csv
   export INPUT_FILES=mimic_cxr_000.csv


6. Run the script

.. code-block:: bash

   bash run_negbio_on_files.sh


The output folder will contains final results and intermediated files such as sentences (in the ``ssplit`` folder), parse trees (in the ``parse`` folder), and universal dependendy graphs (in the ``ud`` folder). For each findings, you can which rule was used to extract the findings, and which rule was used to detect if it is negative or uncertain.

More details of running ``NegBio`` step-by-step, such as how to set the number of CPUs for parallel processing, can be found at https://github.com/ncbi-nlp/NegBio


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

Acknowledgments
===============

This work was supported by the Intramural Research Programs of the National Institutes of Health, National Library of
Medicine and Clinical Center.

We are grateful to the authors of NegEx, MetaMap, Stanford CoreNLP, Bllip parser, and CheXpert labeler for making
their software tools publicly available.

We thank Dr. Alexis Allot for the helpful discussion.

Disclaimer
==========
This tool shows the results of research conducted in the Computational Biology Branch, NCBI. The information produced
on this website is not intended for direct diagnostic use or medical decision-making without review and oversight
by a clinical professional. Individuals should not change their health behavior solely on the basis of information
produced on this website. NIH does not independently verify the validity or utility of the information produced
by this tool. If you have questions about the information produced on this website, please see a health care
professional. More information about NCBI's disclaimer policy is available.
