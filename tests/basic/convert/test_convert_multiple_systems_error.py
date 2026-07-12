"""
Error reporting when a molecular_system argument holds several molecular systems.

A list of items is read as one molecular system split across complementary items
(a topology plus its coordinates, say). When the items are instead several
distinct systems, the digestion used to raise a bare ArgumentError telling the
user to "check the API for the expected argument format", which says nothing
about what was wrong. It now raises MultipleMolecularSystemsError (MSM-ERR-SYS-003),
which names the situation and points at merge().

The error is raised by digest_molecular_system, so every public function taking a
molecular_system inherits it, not only convert.
"""

import pytest

import molsysmt as msm
from molsysmt import systems
from molsysmt._private.smonitor import ArgumentError, MultipleMolecularSystemsError


@pytest.fixture()
def two_systems():
    """Two unrelated systems: 1441 atoms and 304 atoms."""
    return [systems['T4 lysozyme L99A']['181l.pdb'],
            systems['Trp-Cage']['1l2y.h5msm']]


def test_two_systems_are_not_one_molecular_system(two_systems):
    assert msm.basic.is_a_molecular_system(two_systems) is False
    assert msm.are_multiple_molecular_systems(two_systems) is True


def test_convert_reports_how_many_systems_were_seen(two_systems):
    with pytest.raises(MultipleMolecularSystemsError, match='2 separate molecular systems'):
        msm.convert(two_systems)


def test_convert_points_the_user_at_merge(two_systems):
    with pytest.raises(MultipleMolecularSystemsError, match='molsysmt.merge'):
        msm.convert(two_systems)


def test_error_is_driven_by_the_catalog(two_systems):
    # the message must be hydrated from MSM-ERR-SYS-003, not hardcoded at the raise site
    with pytest.raises(MultipleMolecularSystemsError) as excinfo:
        msm.convert(two_systems)
    assert excinfo.value.catalog_key == 'MultipleMolecularSystemsError'


def test_exception_is_public(two_systems):
    assert msm.MultipleMolecularSystemsError is MultipleMolecularSystemsError


@pytest.mark.parametrize('function, kwargs', [
    (msm.get, {'n_atoms': True}),
    (msm.select, {'selection': 'all'}),
])
def test_error_is_inherited_by_other_functions(function, kwargs, two_systems):
    with pytest.raises(MultipleMolecularSystemsError, match='molsysmt.merge'):
        function(two_systems, **kwargs)


def test_merge_is_the_documented_way_out(two_systems):
    # The two systems hold a different number of structures (1 and 38), so merge
    # needs to be told which ones to align. That choice is exactly what convert
    # has no argument to express, and why it points at merge instead of guessing.
    molsys = msm.merge(two_systems, structure_indices=0, to_form='molsysmt.MolSys')
    assert msm.get(molsys, n_atoms=True) == 1441 + 304


def test_a_genuinely_invalid_input_keeps_the_generic_argument_error():
    with pytest.raises(ArgumentError) as excinfo:
        msm.convert(42)
    assert not isinstance(excinfo.value, MultipleMolecularSystemsError)
