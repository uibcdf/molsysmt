"""Public returns must carry native Python scalars inside Python containers.

`devguide/INTERFACES.md`, *Scalar types in returned values*: the nature of the datum
decides the container, and the container decides the scalar type. Numeric magnitudes
come back as `ndarray` or `Quantity` and keep their `dtype`; identifiers, labels,
relations and bare counts come back with native Python scalars.

This is the guard for uibcdf/molsysmt#165. It sweeps the whole attribute catalogue
rather than the attributes known to have been affected, because the defect it
protects against is precisely an attribute nobody remembered to normalise: the
measured surface grew from 9 to 30 to 45 combinations as the sweep widened.
"""

import warnings

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.attribute.attributes import attributes

try:
    from molsysmt import pyunitwizard as puw
except Exception:                                    # pragma: no cover
    puw = None

ELEMENTS = ['atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system', 'bond']


def _numpy_scalars(value, path='', found=None, depth=0):
    """Report NumPy scalars that are not inside an ndarray or a Quantity."""
    if found is None:
        found = []
    if depth > 8:
        return found
    if puw is not None and puw.is_quantity(value):
        return found
    if isinstance(value, np.ndarray):
        if value.dtype == object:                    # object arrays hold Python objects
            for index, item in enumerate(value.ravel()[:200]):
                _numpy_scalars(item, f'{path}[{index}]', found, depth + 1)
        return found                                 # typed array: correct, keeps its dtype
    if isinstance(value, np.generic):
        found.append((path, type(value).__name__))
        return found
    if isinstance(value, dict):
        for key, item in list(value.items())[:50]:
            _numpy_scalars(item, f'{path}.{key}', found, depth + 1)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for index, item in enumerate(list(value)[:200]):
            _numpy_scalars(item, f'{path}[{index}]', found, depth + 1)
    return found


@pytest.fixture(scope='module')
def molecular_system():
    return msm.convert(msm.systems['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')


@pytest.mark.parametrize('attribute', sorted(attributes))
def test_attribute_delivers_native_scalars(attribute, molecular_system):
    """No public attribute delivers a NumPy scalar outside an ndarray or a Quantity."""
    offenders = []
    for element in ELEMENTS:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            try:
                value = msm.get(molecular_system, element=element, **{attribute: True})
            except Exception:
                continue                             # attribute not available at this level
        for path, kind in _numpy_scalars(value):
            offenders.append(f'{attribute} on {element}: {kind} at value{path}')

    assert not offenders, (
        'NumPy scalars delivered outside an ndarray or a Quantity:\n  '
        + '\n  '.join(offenders[:10])
        + '\n\nSee devguide/INTERFACES.md, *Scalar types in returned values*. If this is a '
          'new attribute assembling a Python container from arrays, add it to '
          '`_ATTRIBUTES_WITH_NUMPY_SCALARS` in molsysmt/basic/get.py.'
    )


def test_covalent_blocks_sets_hold_native_ints(molecular_system):
    """`get_covalent_blocks` builds its sets from delivered bond pairs, so it inherits this.

    The mixture it used to return — some `int`, some `np.int64` in one set — came from
    NetworkX using the delivered pair objects as adjacency keys. It has no
    normalisation of its own and must not need one.
    """
    blocks = msm.topology.get_covalent_blocks(molecular_system)
    kinds = {type(index).__name__ for block in blocks for index in block}
    assert kinds == {'int'}, f'covalent blocks hold {sorted(kinds)}'


def test_numeric_magnitudes_keep_their_dtype(molecular_system):
    """The other half of the rule: arrays and quantities are not converted."""
    coordinates = msm.get(molecular_system, element='system', coordinates=True)
    assert puw.is_quantity(coordinates)
    assert puw.get_value(coordinates).dtype == np.float64

    occupancy = msm.get(molecular_system, element='atom', occupancy=True)
    assert isinstance(occupancy, np.ndarray)
    assert occupancy.dtype == np.float64
