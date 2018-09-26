from __future__ import absolute_import, division, print_function

import os
import glob

from glue.logger import logger
from glue.core.data import Data
from glue.config import data_factory
import vaex.hdf5.dataset

from .data import DataVaex

def is_vaex_file(source):
    return vaex.hdf5.dataset.Hdf5MemoryMapped.can_open(source)


@data_factory(
    label='vaex file or directory',
    identifier=is_vaex_file,
    priority=1000,
)
def vaex_reader(source):
    """
    Read a vaex hdf5 file
    """

    if os.path.isdir(source):

        arrays = {}
        for filename in glob.glob(os.path.join(source, '*')):
            if is_vaex_file(filename):
                logger.info("Reading vaex data from {0}".format(filename))
                ds = vaex.open(filename)
            else:
                logger.info("Not a vaex file: {0}".format(filename))

        # If there are no vaex files, we raise an error, and if there is one
        # then we are done!

        if len(arrays) == 0:
            raise Exception("No vaex files found in directory: {0}".format(source))
        elif len(arrays) == 1:
            label = list(arrays.keys())[0]
            return [Data(array=arrays[label], label=label)]

        # We now check whether all the shapes of the vaex files are the same,
        # and if so, we merge them into a single file.

        labels = sorted(arrays)
        ref_shape = arrays[labels[0]].shape

        for label in labels[1:]:

            if arrays[label].shape != ref_shape:
                break

        else:

            # Since we are here, the shapes of all the vaex files match, so
            # we can construct a higher-dimensional array.

            # Make sure arrays are sorted while constructing array
            array = np.array([arrays[label] for label in labels])

            # We flip the array here on that in most cases we expect that the
            # scan will start at the top of e.g. the body and move downwards.
            array = array[::-1]

            return [Data(array=array, label=dicom_label(source))]

        # If we are here, the shapes of the vaex files didn't match, so we
        # simply return one Data object per vaex file.
        return [Data(array=arrays[label], label=label) for label in labels]

    else:

        ds = vaex.open(source)
        data = [DataVaex(ds)]

    return data