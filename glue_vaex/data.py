import sys

import vaex
from glue.core.data import BaseCartesianData
from glue.core.component_id import ComponentID, ComponentIDDict

from .subset import translate_subset_state


class DataVaex(BaseCartesianData):
    def __init__(self, ds):
        super(DataVaex, self).__init__()
        self.ds = ds
        self.id = ComponentIDDict(self)
        self._main_components = [ComponentID(label=str(k), parent=self) for k in self.ds.get_column_names(strings=False, virtual=True)]

    @property
    def label(self):
        return self.ds.name

    @property
    def shape(self):
        return (len(self.ds),)

    @property
    def main_components(self):
        return self._main_components

    def get_kind(self, cid):
        column = self.ds[cid.label]
        return 'numerical'

    def get_data(self, cid, view=None):
        print('get_data', cid, view)
        expr = cid.label
        return self.ds[expr].evaluate(0, 10000)

    def get_mask(self, subset_state, view=None):
        print('get mask', subset_state, view)
        return subset_state.to_mask(self, view=view)

    def compute_statistic(self, statistic, cid,
                          axis=None, finite=True,
                          positive=False, subset_state=None,
                          percentile=None, random_subset=None):
        # print('compute_statistic', statistic, cid, axis, finite, positive, subset_state)
        if subset_state is not None:
            selection = translate_subset_state(self.ds, subset_state)
        expr = cid.label
        if axis is None:
            if statistic == 'minimum':
                return self.ds.min(expr).item()
            elif statistic == 'maximum':
                return self.ds.max(expr).item()
            elif statistic == 'mean':
                return self.ds.mean(exor)
            elif statistic == 'median':
                raise ValueError('not supported')
            elif statistic == 'percentile':
                raise ValueError('not supported')
            elif statistic == 'sum':
                return self.ds.sum(expr)
        else:
            final_shape = tuple(self.shape[i] for i in range(self.ndim)
                                if i not in axis)
            return np.random.random(final_shape)

    def compute_histogram(self, cid,
                          range=None, bins=None, log=False, weights=None,
                          subset_state=None, subset_group=None):
        # expressions = [k.label for k in cid]
        # print('compute_histogram', cid, range, bins, log, subset_state)
        selection = None
        if subset_state is not None:
            selection = translate_subset_state(self.ds, subset_state)
        expressions = [k.label for k in cid]
        return self.ds.count(binby=expressions, limits=range, shape=bins, selection=selection)




