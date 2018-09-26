import numpy as np
import vaex
import pytest
import glue.core.subset
import glue.core.roi
from glue.core.component_id import ComponentID

from .subset import translate_subset_state
from .data import DataVaex

@pytest.fixture
def ds():
    x = np.arange(5)
    y = np.arange(5)
    ds = vaex.from_arrays(x=x, y=y)
    return ds

@pytest.fixture
def data(ds):
    return DataVaex(ds)

def test_range(ds):
    state = glue.core.subset.RangeSubsetState(lo=2, hi=3, att=ComponentID('x'))
    selection = translate_subset_state(ds, state)
    assert ds.evaluate_selection_mask(selection).tolist() == [0, 0, 1, 1, 0]

def test_and(data):
    ds = data.ds
    state = (data.id['x'] > 1) & (data.id['y'] < 4)
    selection = translate_subset_state(ds, state)
    assert ds.evaluate_selection_mask(selection).tolist() == [0, 0, 1, 1, 0]

def test_or(data):
    ds = data.ds
    state = (data.id['x'] < 1) | (data.id['y'] > 3)
    selection = translate_subset_state(ds, state)
    assert ds.evaluate_selection_mask(selection).tolist() == [1, 0, 0, 0, 1]

def test_invert(data):
    ds = data.ds
    state = ~(data.id['x'] < 2)
    selection = translate_subset_state(ds, state)
    assert ds.evaluate_selection_mask(selection).tolist() == [0, 0, 1, 1, 1]

def test_xor(data):
    ds = data.ds
    state = (data.id['x'] > 2) ^ (data.id['y'] < 4)
    selection = translate_subset_state(ds, state)
    assert ds.evaluate_selection_mask(selection).tolist() == [1, 1, 1, 0, 1]

def test_rect(ds):
    roi = glue.core.roi.RectangularROI(xmin=1, xmax=4, ymin=0, ymax=3)
    state = glue.core.subset.RoiSubsetState(roi=roi, xatt=ComponentID('x'), yatt=ComponentID('y'))
    selection = translate_subset_state(ds, state)
    assert ds.evaluate_selection_mask(selection).tolist() == [0, 0, 1, 0, 0]

def test_polygon(ds):
    xmin=1; xmax=4; ymin=0; ymax=3
    vx = [xmin, xmax, xmax, xmin, xmin]
    vy = [ymin, ymin, ymax, ymax, ymin]
    roi = glue.core.roi.PolygonalROI(vx=vx, vy=vy)
    state = glue.core.subset.RoiSubsetState(roi=roi, xatt=ComponentID('x'), yatt=ComponentID('y'))
    selection = translate_subset_state(ds, state)
    assert ds.evaluate_selection_mask(selection).tolist() == [0, 1, 1, 0, 0]
