
import bioc
from pynih import metamap


def metamap2bioc(src, dst):
    """
    Extract annotations from MetaMap src and place them in the passages
    """
    with open(src, 'rb') as fp, bioc.iterwrite(dst) as biocwriter:
        for i, document in enumerate(metamap.iterparse(fp)):
            biocwriter.writedocument(document)