"""Adding atoms must not leave a structural series describing the old system.

Guard for `uibcdf/molsysmt#175`. The three `molsysmt.build` functions that add atoms
grew `coordinates` and nothing else, so `b_factor`, `occupancy` and `velocities` kept
the old atom axis and the system-level observables survived unchanged.

The energies are why this test exists in this shape. They have no atom axis, so
`Structures._payload_dimensions` cannot catch them: a system that has just gained 1311
hydrogens would still report its old kinetic energy, and nothing downstream would ever
contradict it. The stale atom-aligned arrays do raise eventually — far away, inside
`solvate` — but a wrong number that never raises is the worse failure, so every case
here asserts on the energies too.

`alternate_location` is asserted separately because it fails differently. It is a sparse
mapping keyed by atom index, so it survives the operation intact and silently points at
the wrong atoms once the placers reorder: on 181L, the key 500 named `OE2` of group 63
before the call and `N` of group 30 after it.
"""

import numpy as np
import pyunitwizard as puw
import pytest

import molsysmt as msm

ATOM_ALIGNED_BESIDES_COORDINATES = ('velocities', 'b_factor', 'occupancy')
SYSTEM_LEVEL_OBSERVABLES = ('temperature', 'potential_energy', 'kinetic_energy')


def _loaded(system, filename):
    """A single structure carrying every attribute this guard is about."""
    molecular_system = msm.extract(
        msm.convert(msm.systems[system][filename], to_form='molsysmt.MolSys'),
        structure_indices=[0],
    )
    n_atoms = int(msm.get(molecular_system, element='system', n_atoms=True))
    structures = molecular_system.structures
    structures.velocities = puw.quantity(np.full((1, n_atoms, 3), 0.7), 'nm/ps')
    structures.occupancy = puw.quantity(np.ones((1, n_atoms)), 'dimensionless')
    structures.temperature = puw.quantity(np.array([300.0]), 'K')
    structures.potential_energy = puw.quantity(np.array([-567.8]), 'kJ/mol')
    structures.kinetic_energy = puw.quantity(np.array([123.4]), 'kJ/mol')
    return molecular_system, n_atoms


def _atom_axis(structures, name):
    value = getattr(structures, name)
    return None if value is None else np.asarray(puw.get_value(value)).shape[1]


@pytest.mark.parametrize(
    ('function', 'keywords', 'system', 'filename'),
    [
        (msm.build.add_missing_heavy_atoms, {}, 'Barnase-Barstar', '1brs.bcif.gz'),
        (msm.build.add_missing_terminal_cappings, {}, 'T4 lysozyme L99A', '181l.h5msm'),
        (msm.build.add_missing_hydrogens, {'pH': 7.4}, 'T4 lysozyme L99A', '181l.h5msm'),
    ],
    ids=['heavy_atoms', 'terminal_cappings', 'hydrogens'],
)
def test_no_structural_series_survives_describing_the_old_atom_axis(
        function, keywords, system, filename):
    molecular_system, n_before = _loaded(system, filename)

    result = function(molecular_system, engine='MolSysMT', **keywords)

    n_after = int(msm.get(result, element='system', n_atoms=True))
    assert n_after > n_before, 'the case must actually add atoms to be a test'

    structures = result.structures
    assert _atom_axis(structures, 'coordinates') == n_after

    for name in ATOM_ALIGNED_BESIDES_COORDINATES:
        size = _atom_axis(structures, name)
        assert size is None or size == n_after, (
            f'{name} has {size} atoms in a system of {n_after}; a series that cannot '
            f'cover the atom axis must be dropped, not carried over'
        )

    for name in SYSTEM_LEVEL_OBSERVABLES:
        assert getattr(structures, name) is None, (
            f'{name} describes the system, and the system just changed; it has no atom '
            f'axis, so nothing downstream can detect that it is now wrong'
        )


def test_alternate_location_keys_follow_their_atoms():
    """The labels stay valid when atoms move; the keys have to move with them."""
    molecular_system = msm.extract(
        msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys'),
        structure_indices=[0],
    )
    names = msm.get(molecular_system, element='atom', atom_name=True)
    group_indices = msm.get(molecular_system, element='atom', group_index=True)

    marked = {0: 'A', 500: 'A', 1000: 'B', 1440: 'B'}
    molecular_system.structures.alternate_location = [dict(marked)]

    result = msm.build.add_missing_hydrogens(molecular_system, pH=7.4, engine='MolSysMT')

    series = result.structures.alternate_location
    assert series is not None, 'the labels are still valid data and must not be dropped'

    produced = dict(series[0])
    assert len(produced) == len(marked)
    assert sorted(produced.values()) == sorted(marked.values())

    names_after = msm.get(result, element='atom', atom_name=True)
    groups_after = msm.get(result, element='atom', group_index=True)
    for old_index, new_index in zip(sorted(marked), sorted(produced)):
        assert names_after[new_index] == names[old_index]
        assert groups_after[new_index] == group_indices[old_index]
        assert produced[new_index] == marked[old_index]


def test_the_drop_is_reported_rather_than_silent():
    """Losing a series the caller supplied is a fact they need, not an implementation detail."""
    from molsysmt._private.smonitor import StructuralAttributeDropWarning

    molecular_system, _ = _loaded('T4 lysozyme L99A', '181l.h5msm')

    with pytest.warns(StructuralAttributeDropWarning) as recorded:
        msm.build.add_missing_hydrogens(molecular_system, pH=7.4, engine='MolSysMT')

    reported = ' '.join(str(record.message) for record in recorded)
    for name in ('b_factor', 'occupancy', 'velocities', 'kinetic_energy'):
        assert name in reported, f'{name} was dropped without saying so'
