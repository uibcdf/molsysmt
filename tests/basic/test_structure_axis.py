"""
Regression tests for the structure axis of a composite molecular system.

A molecular system spread over complementary items need not have the same number of
structures in each: a topology file holding one reference conformation beside a
trajectory file is ordinary. The axis is a property of the system, so no result may
depend on the order the items were listed in.
"""

import warnings

import molsysmt as msm
import pytest
from molsysmt import systems
from molsysmt._private.smonitor import (
    StructuralAttributeOffAxisWarning,
    StructuralInconsistencyError,
)


@pytest.fixture
def villin_items():
    return (systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm'],
            systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'])


def test_n_structures_does_not_depend_on_item_order(villin_items):
    h5msm, dcd = villin_items
    # One reference structure in the H5MSM, twenty in the DCD.
    assert msm.get(h5msm, n_structures=True) == 1
    assert msm.get(dcd, n_structures=True) == 20

    assert msm.get([h5msm, dcd], n_structures=True) == 20
    assert msm.get([dcd, h5msm], n_structures=True) == 20


@pytest.mark.parametrize('reversed_order', [False, True])
def test_conversion_does_not_discard_the_trajectory(villin_items, reversed_order):
    # Listing the trajectory first used to make the reference conformation win the
    # tie-break, and nineteen structures were dropped without a diagnostic.
    h5msm, dcd = villin_items
    items = [dcd, h5msm] if reversed_order else [h5msm, dcd]

    molecular_system = msm.convert(items, to_form='molsysmt.MolSys')

    assert msm.get(molecular_system, n_structures=True) == 20
    assert msm.get(molecular_system, n_atoms=True) == 4369


def test_structural_series_of_one_system_share_a_length(villin_items):
    h5msm, dcd = villin_items
    coordinates = msm.get([h5msm, dcd], element='atom', coordinates=True)
    assert len(coordinates) == msm.get([h5msm, dcd], n_structures=True)

    # 'time' exists only on the reference conformation, so it is absent rather than
    # returned with a length that contradicts the structure axis.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        time = msm.get([h5msm, dcd], element='system', time=True)

    assert time is None
    assert any(issubclass(entry.category, StructuralAttributeOffAxisWarning)
               for entry in caught)


def test_a_topology_without_structures_does_not_define_the_axis():
    # A PSF carries no structural data at all, so it neither defines nor constrains the
    # axis. This is the most common composite and must be untouched.
    psf = systems['POPC membrane']['popc_membrane.psf']
    dcd = systems['POPC membrane']['popc_membrane.dcd']

    assert msm.get([psf, dcd], n_structures=True) == 5
    assert msm.get([dcd, psf], n_structures=True) == 5


def _axis_with_counts(monkeypatch, counts):
    """Exercising the rule itself, with the per-item counts supplied directly."""

    from molsysmt._private import structure_axis as module

    supplied = iter(counts)
    monkeypatch.setattr(module, 'item_n_structures', lambda item, form: next(supplied))
    items = [f'item_{index}' for index in range(len(counts))]
    forms = ['file:dcd']*len(counts)
    return module.structure_axis(items, forms, caller='test')


@pytest.mark.parametrize('counts,axis', [
    ([None, 5], 5),      # a topology carrying no structures at all
    ([1, 20], 20),       # a reference conformation beside a trajectory
    ([20, 1], 20),       # the same, listed the other way round
    ([20, 20], 20),      # both span the axis; the tie-break decides
    ([None, None], None),  # no structural data anywhere
])
def test_structure_axis_rule(monkeypatch, counts, axis):
    assert _axis_with_counts(monkeypatch, counts)[0] == axis


def test_two_trajectories_of_different_lengths_are_rejected(monkeypatch):
    # Nothing in the data says which one defines the axis, so choosing silently is what
    # this whole contract exists to prevent. The message points at the function that does
    # join structures on purpose.
    with pytest.raises(StructuralInconsistencyError, match='concatenate_structures'):
        _axis_with_counts(monkeypatch, [20, 10])
