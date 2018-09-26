import vaex
from glue.core import DataCollection
from glue.app.qt.application import GlueApplication

from .data import DataVaex

def main(argv):
    datasets = [DataVaex(vaex.open(k)) for k in argv[1:]]
    dc = DataCollection(datasets)
    ga = GlueApplication(dc)
    ga.start()

if __name__ == '__main__':
    import sys
    main(sys.argv)