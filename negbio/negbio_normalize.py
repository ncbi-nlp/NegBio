"""
Usage:
    negbio normalize [options] --out=<directory> <source> ...

Options:
    --suffix=<str>  [default: .normalized.xml]
"""

import os
from pathlib import Path
import docopt
import tqdm
import bioc

from ext.normalize_mimiccxr import normalize_collection

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)

    for pathname in tqdm.tqdm(argv['<source>'], total=len(argv['<source>'])):
        src = Path(pathname)
        with open(str(src)) as fp:
            collection = bioc.load(fp)

        collection = normalize_collection(collection)

        dst = Path(argv['--out']) / src.with_suffix(argv['--suffix']).name
        with open(str(dst), 'w') as fp:
            bioc.dump(collection, fp)
