from json import dump as jsondump
from json import load as jsonload

from .__json import Decoder, Encoder


def dump(obj, fp, indent=2):
    jsondump(obj=obj, fp=fp, cls=Encoder, indent=indent)

def load(fp):
    return jsonload(fp, cls=Decoder)
