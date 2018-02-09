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
*  MetaMap >2016

MetaMap installation instructions can be found at `https://metamap.nlm.nih.gov/Installation.shtml <https://metamap.nlm.nih.gov/Installation.shtml>`_.
Please make sure that both ``skrmedpostctl`` and ``wsdserverctl`` are started.


Installing using pip
~~~~~~~~~~~~~~~~~~~~

negbio can be installed at the command line:

.. code-block:: bash

   $ pip install --pre negbio


Installing from source
~~~~~~~~~~~~~~~~~~~~~~

1. Download the source code from GitHub ``git clone https://github.com/ncbi-nlp/NegBio.git``
2. Change to the directory with the ``setup.py`` file
3. Run ``python setup.py install``


Using NegBio
------------

Prepare the dataset
~~~~~~~~~~~~~~~~~~~

The program inputs are reports in plain text. Each report needs to be in a single file.
Some examples can be found in the ``examples`` folder.

Run the script
~~~~~~~~~~~~~~

The easiest way is to run the following commend by replacing `<METAMAP_BINARY>` with the actual path, such as `/opt/public_mm/bin/metamap16`

.. code-block:: bash
   :linenos:

   $ python -m negbio.main_text \
        --out=examples/test.neg.xml \
        --metamap=<METAMAP_BINARY> \
        examples/00000086.txt examples/00019248.txt

The script will

1. Combine ``examples/00000086.txt`` and ``examples/00019248.txt`` into one BioC XML file
2. Detect UMLS concepts (CUIs) using MetaMap (by default using the CUI list ``examples\cuis-cvpr2017.txt``
3. Detect negative and uncertain CUIs using rules in  ``patterns/neg_patterns.txt`` and ``patterns/uncertainty_patterns.txt``
4. Save the results in ``examples/test.neg.xml``


More options (e.g., setting the CUI list or rules) can be obtained by running

.. code-block:: bash

   $ python -m negbio.main --help


Next Steps
----------

To start learning how to use pydicom, see the :doc:`user_guide`.
