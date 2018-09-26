import numbers

import glue.core.subset
import glue.core.roi

from glue.core.data import ComponentID


class ViewAdapter(object):
    def __init__(self, ds):
        self.ds = ds

    def __getitem__(self, arg):
        attr, view = arg
        if view is not None:
            raise ValueError('view is not None: %r' % view)
        #
        # print(attr, type(attr))
        # import pdb
        # pdb.set_trace() 
        # expr = getattr(self.ds, str(attr))
        # print(expr)
        return self.ds[str(attr)]

def translate_subset_state(ds, state):
    if isinstance(state, (ComponentID, numbers.Number)):
        return state
    elif isinstance(state, glue.core.subset.RangeSubsetState):
        return state.to_mask(ViewAdapter(ds))#, ds[state.att.label])
    elif isinstance(state, glue.core.subset.RoiSubsetState):
        roi = state.roi
        x = ds[state.xatt.label]
        y = ds[state.yatt.label]
        if isinstance(roi, glue.core.roi.RectangularROI):
            return state.roi.contains(x, y)
        elif isinstance(roi, glue.core.roi.PolygonalROI):
            name = 'selection_' + str(id(state))
            ds.select_lasso(x, y, roi.vx, roi.vy, name=name)
            return name
        else:
            raise 'not supported'
    elif isinstance(state, glue.core.subset.InvertState):
        name = 'selection_' + str(id(state))
        selection = translate_subset_state(ds, state.state1)
        ds.select('~({selection})'.format(selection=selection), name=name)
        return name
    elif isinstance(state, glue.core.subset.InequalitySubsetState):
        name = 'selection_' + str(id(state))
        left = translate_subset_state(ds, state.left)
        right = translate_subset_state(ds, state.right)
        op = glue.core.subset.OPSYM.get(state.operator)
        # import pdb
        # pdb.set_trace()
        print(name, '{left} {op} {right}'.format(left=left, op=op, right=right))
        ds.select('{left} {op} {right}'.format(left=left, op=op, right=right), name=name)
        return name
    elif isinstance(state, (glue.core.subset.AndState, glue.core.subset.OrState, glue.core.subset.XorState)):
        name = 'selection_' + str(id(state))
        left = translate_subset_state(ds, state.state1)
        right = translate_subset_state(ds, state.state2)
        op = glue.core.subset.OPSYM.get(state.op)
        print(name, '{left} {op} {right}'.format(left=left, op=op, right=right))
        ds.select('{left} {op} {right}'.format(left=left, op=op, right=right), name=name)
        return name
    else:
        # import pdb
        # pdb.set_trace()
        raise TypeError('not supported: %r' % state)

