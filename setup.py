# Always prefer setuptools over distutils
# To use a consistent encoding
from __future__ import print_function
from codecs import open
import os
from subprocess import check_call

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install

here = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def readme():
    # Get the long description from the README file
    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()


def read_requirements():
    """parses requirements from requirements.txt"""
    reqs_path = os.path.join(here, 'requirements.txt')
    with open(reqs_path, encoding='utf8') as f:
        reqs = [line.strip() for line in f if not line.strip().startswith('#')]

    names = []
    links = []
    for req in reqs:
        if '://' in req:
            links.append(req)
        else:
            names.append(req)
    return {'install_requires': names, 'dependency_links': links}


def custom_command():
    check_call("python -m nltk.downloader universal_tagset punkt wordnet".split())


class CustomInstallCommand(install):
    def run(self):
        custom_command()
        install.run(self)


class CustomDevelopCommand(develop):
    def run(self):
        custom_command()
        develop.run(self)


class CustomEggInfoCommand(egg_info):
    def run(self):
        custom_command()
        egg_info.run(self)


setup(
    name='negbio',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.9.4',

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

    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': CustomEggInfoCommand
    },

    entry_points = {
        'console_scripts': ['negbio_pipeline=negbio.negbio_pipeline:main',
                            'main_chexpert=negbio.main_chexpert:main',
                            'main_mm=negbio.main_mm:main'],
    },

    **read_requirements()
)
