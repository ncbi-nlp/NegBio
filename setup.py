# Always prefer setuptools over distutils
# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup, find_packages


here = path.abspath(path.dirname((__file__)))


def readme():
    # Get the long description from the README file
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()


def requirements():
    reqs = []
    with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        for line in f:
            reqs.append(line.strip())
    print(reqs)


setup(
    name='negbio',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.9.dev1',

    description='NegBio: a tool for negation and uncertainty detection',
    long_description=readme(),

    # The project's main homepage.
    url='https://github.com/ncbi-nlp/NegBio.git',

    # Author details
    author='Yifan Peng',
    author_email='yifan.peng@nih.gov',

    license='Public Domain',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',

        # Pick your license as you wish (should match "license" above)
        'License :: Public Domain',

        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',

        # Specify the Python versions you support here.
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    keywords='negbio',

    packages=find_packages(exclude=["tests.*", "tests", "backup", "docs"]),
    include_package_data=True,

    install_requires=requirements()
)
