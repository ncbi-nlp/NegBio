
![NegBio](https://github.com/yfpeng/negbio/blob/master/images/negbio.png?raw=true)

NegBio is a high-performance NLP tool for negation and uncertainty detection in clinical texts (e.g. radiology reports).

The source code will be released before AMIA 2018 Informatics Summit (March 12).


See [`CONTRIBUTING.md`](/CONTRIBUTING.md) before filing an issue or creating a pull request.

## Getting Started

These instructions will get you a copy of the project up and  run on your
local machine for development and testing purposes.

#### Prerequisites

0. Copy the project on your local machine

```bash
git clone https://github.com/ncbi-nlp/NegBio.git
```

#### Install environment

Install or update the [conda](https://conda.io) environment specified in [`environment2.7.yml`](environment2.7.yml) by running:

```bash
# If the negbio2.7 environment already exists, remove it first
conda env remove --name negbio2.7

# Install the environment
conda env create --file environment2.7.yml
```

Activate with `conda activate negbio2.7` (assumes `conda` version of [at least](https://github.com/conda/conda/blob/9d759d8edeb86569c25f6eb82053f09581013a2a/CHANGELOG.md#440-2017-12-20) 4.4).
The environment should successfully install on both Linux and macOS (and possibly Windows).

#### Prepare the dataset

The program needs the reports with finding mentions annotated in [BioC format](http://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/BioC/). 
Some examples can be found in the `examples` folder.

#### Run the script

The easiest way is to run

```bash
python negbio/main.py --out=examples examples/1.xml examples/2.xml
```

The script will detect negative and uncertain findings in files `examples/1.xml` and `examples/2.xml`. 
It prints to the directory `example`.
The dest file has the same basename as SOURCE and has 'neg.xml' as the suffix.

A more detailed useage can be obtained by running

```bash
python negbio/main.py -h                                          
Usage:
    negbio [options] --out=DIRECTORY SOURCE ...

Options:
    --neg-patterns=FILE             negation rules [default: patterns/neg_patterns.txt]
    --uncertainty-patterns=FILE     uncertainty rules [default: patterns/uncertainty_patterns.txt]
    --model=MODEL_DIR               Bllip parser model directory
```

Alternatively, you can run the pipeline step-by-step.

1.  `pipeline/ssplit.py` splits text into sentences.
1.  `pipeline/parse.py` parse sentence using the [Bllip parser](https://github.com/BLLIP/bllip-parser).
1.  `pipeline/ptb2ud.py` convert the parse tree to universal dependencies using [Stanford converter](https://github.com/dmcc/PyStanfordDependencies).
1.  `pipeline/negdetect.py` detect negative and uncertain findings.

#### Customize patterns

By default, the program uses the negatition and uncertainty patterns in `patterns`.
You can add more patterns if needed.
The pattern is a [`semgrex-type`](https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/semgraph/semgrex/SemgrexPattern.html) pattern for matchig node in the dependency graph.
Currently, we only support `<` and `>` operations.
A detailed grammar (using PLY, Python Lex-Yacc) can be found at [ngrex/parser.py](ngrex/parser).

## Contributing

Please read
[CONTRIBUTING](/CONTRIBUTING.md) for
details on our code of conduct, and the process for submitting pull requests to
us.

## License

see `LICENSE.txt`.

## Acknowledgments

This work was supported by the Intramural Research Programs of the National
Institutes of Health, National Library of Medicine.

## Reference

* Peng Y, Wang X, Lu L, Bagheri M, Summers RM, Lu Z. 
[NegBio: a high-performance tool for negation and uncertainty detection in radiology reports](https://arxiv.org/abs/1712.05898). *AMIA 2018 Informatics Summit*. 2018.
