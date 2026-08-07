"""
The semantics decided by the atom-axis `add()` audit, and the defects it found.

These were written in Phase 2 as `xfail(strict=True)` against an implementation that did
not have them yet, and Phase 3 made them pass. The strict marker is what forced each one
to be examined as it flipped instead of being assumed correct.

Audit: `devguide/pending_proposals/atom_axis_add_semantic_audit.md`, sections
"Accepted Decisions" (D1-D7) and `atom_axis_add_phase1_findings.md`, section 5.

Each test states the decision it guards, not the behaviour that preceded it.
"""

import warnings

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt import systems
from molsysmt._private.smonitor import (
    BioassemblyIdentifierCollisionWarning,
    IncompatibleBoxWarning,
    NotImplementedMethodError,
    StructuralAttributeDropWarning,
)

def _cubic_box(edge_nm, n_structures=1):
    return puw.quantity(
        np.tile(np.eye(3) * edge_nm, (n_structures, 1, 1)),
        'nm',
    )


# =====================================================================================
# Defects found by Phase 1, independent of any policy choice
# =====================================================================================

def test_a_composite_source_list_is_assembled_before_being_added(proline_molsys):
    # `convert` reads [prmtop, inpcrd] as one 5207-atom system with one structure.
    # `add` must read the same list the same way, instead of iterating the two
    # complementary items as if they were independent sources. Findings, defect 5.
    prmtop = systems['pentalanine']['pentalanine.prmtop']
    inpcrd = systems['pentalanine']['pentalanine.inpcrd']
    composite = msm.convert([prmtop, inpcrd], to_form='molsysmt.MolSys')
    expected = msm.get(proline_molsys, n_atoms=True) + msm.get(composite, n_atoms=True)

    msm.add(proline_molsys, [prmtop, inpcrd])

    assert msm.get(proline_molsys, n_atoms=True) == expected
    assert msm.get(proline_molsys, n_structures=True) == 1


def test_a_composite_target_list_is_assembled_before_receiving(valine_molsys):
    # As a target the same list currently tries to convert the source back into
    # file:prmtop. Findings, defect 5.
    prmtop = systems['pentalanine']['pentalanine.prmtop']
    inpcrd = systems['pentalanine']['pentalanine.inpcrd']
    target = [prmtop, inpcrd]

    result = msm.add(target, valine_molsys, in_place=False)

    assert msm.get(result, n_atoms=True) == 5207 + msm.get(valine_molsys, n_atoms=True)


def test_adding_a_topology_to_a_system_with_coordinates_reports_the_real_cause(
        proline_molsys, valine_molsys):
    # Today this raises ArgumentLengthError naming `structures`, an argument the caller
    # never passed. Whatever the policy, the diagnostic must name the attribute that
    # cannot be built. Findings, defect 6.
    source = valine_molsys
    source.structures.coordinates = None

    with pytest.warns(StructuralAttributeDropWarning, match='coordinates'):
        msm.add(proline_molsys, source)


def test_the_topology_adapter_raises_the_catalogued_error(proline_molsys):
    # molsysmt.Topology's add raises a bare NotImplementedError, escaping the error
    # policy every other stub follows. Findings, defect 7.
    from molsysmt.form.molsysmt_Topology.add import add as topology_add

    with pytest.raises(NotImplementedMethodError):
        topology_add(proline_molsys.topology, proline_molsys.topology)


# =====================================================================================
# D1 - the target's periodic box prevails, and a mismatch is reported
# =====================================================================================

def test_incompatible_boxes_keep_the_targets_and_warn(proline_molsys, valine_molsys):
    proline_molsys.structures.box = _cubic_box(2.0)
    valine_molsys.structures.box = _cubic_box(9.0)

    with pytest.warns(IncompatibleBoxWarning):
        msm.add(proline_molsys, valine_molsys)

    box = puw.get_value(proline_molsys.structures.box, to_unit='nm')
    np.testing.assert_allclose(np.diag(box[0]), [2.0, 2.0, 2.0])


def test_compatible_boxes_do_not_warn(proline_molsys, valine_molsys):
    proline_molsys.structures.box = _cubic_box(3.0)
    valine_molsys.structures.box = _cubic_box(3.0)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        msm.add(proline_molsys, valine_molsys)

    assert not [w for w in caught if issubclass(w.category, IncompatibleBoxWarning)]


@pytest.mark.parametrize('side', ['target', 'source'])
def test_a_one_sided_box_warns(proline_molsys, valine_molsys, side):
    # Mixing a periodic fragment with a non-periodic one is the same class of event as
    # two disagreeing cells.
    holder = proline_molsys if side == 'target' else valine_molsys
    other = valine_molsys if side == 'target' else proline_molsys
    holder.structures.box = _cubic_box(3.0)
    other.structures.box = None

    with pytest.warns(IncompatibleBoxWarning):
        msm.add(proline_molsys, valine_molsys)


# =====================================================================================
# D2 - system-level observables are dropped; the structure axis identity is kept
# =====================================================================================

@pytest.mark.parametrize('attribute,unit', [
    ('temperature', 'K'),
    ('potential_energy', 'kJ/mol'),
    ('kinetic_energy', 'kJ/mol'),
])
def test_system_level_observables_are_dropped_when_the_system_grows(
        proline_molsys, valine_molsys, attribute, unit):
    setattr(proline_molsys.structures, attribute, puw.quantity(np.array([1.0]), unit))

    with pytest.warns(StructuralAttributeDropWarning, match=attribute):
        msm.add(proline_molsys, valine_molsys)

    assert getattr(proline_molsys.structures, attribute) is None


def test_the_structure_axis_identity_survives(proline_molsys, valine_molsys):
    # Already true today. It is here because D2 must not take it away while dropping the
    # observables: time and structure_id describe the structure axis, which add() does
    # not touch.
    proline_molsys.structures.time = puw.quantity(np.array([7.0]), 'ps')
    proline_molsys.structures.structure_id = np.array([42])

    msm.add(proline_molsys, valine_molsys)

    np.testing.assert_allclose(
        puw.get_value(proline_molsys.structures.time, to_unit='ps'), [7.0])
    np.testing.assert_array_equal(proline_molsys.structures.structure_id, [42])


def test_an_empty_selection_keeps_the_observables(proline_molsys, valine_molsys):
    # Passes today only because nothing is ever dropped. It is the guard that D2's drop
    # must not fire when no atom was actually added and the system did not change.
    proline_molsys.structures.potential_energy = puw.quantity(np.array([-100.0]), 'kJ/mol')
    n_atoms = msm.get(proline_molsys, n_atoms=True)

    msm.add(proline_molsys, valine_molsys, selection=[])

    assert msm.get(proline_molsys, n_atoms=True) == n_atoms
    np.testing.assert_allclose(
        puw.get_value(proline_molsys.structures.potential_energy, to_unit='kJ/mol'),
        [-100.0])


# =====================================================================================
# D3 and D7 - attribute_policy
# =====================================================================================

def test_attribute_policy_is_a_real_parameter_of_add():
    # `add()` currently has no such parameter, and passing one is silently ignored
    # rather than rejected, so asserting on behaviour alone would pass for the wrong
    # reason. The parameter itself is what D3 adds.
    import inspect

    parameters = inspect.signature(msm.add).parameters
    assert 'attribute_policy' in parameters
    assert parameters['attribute_policy'].default == 'intersection'


def test_strict_refuses_instead_of_discarding_the_targets_data(proline_molsys, valine_molsys):
    from molsysmt._private.smonitor import StructuralInconsistencyError

    n_atoms = msm.get(proline_molsys, n_atoms=True)
    proline_molsys.structures.b_factor = np.ones((1, n_atoms))

    with pytest.raises(StructuralInconsistencyError):
        msm.add(proline_molsys, valine_molsys, attribute_policy='strict')

    # Refusing must not mutate: the atom axis and the column are both intact.
    assert msm.get(proline_molsys, n_atoms=True) == n_atoms
    assert proline_molsys.structures.b_factor.shape == (1, n_atoms)


# =====================================================================================
# D4 - state add() does not currently traverse
# =====================================================================================

def test_the_targets_time_step_survives(proline_molsys, valine_molsys):
    # Already true today; D4 only makes it explicit.
    proline_molsys.structures.time_step = puw.quantity(2.0, 'ps')
    valine_molsys.structures.time_step = puw.quantity(5.0, 'ps')

    msm.add(proline_molsys, valine_molsys)

    assert puw.get_value(proline_molsys.structures.time_step, to_unit='ps') == 2.0


def test_bioassemblies_are_merged_with_chain_indices_remapped(proline_molsys, valine_molsys):
    n_target_chains = msm.get(proline_molsys, n_chains=True)
    proline_molsys.structures.bioassembly = {
        'A': {'chain_indices': [0], 'rotations': np.eye(3)[None, ...],
              'translations': np.zeros((1, 3))}}
    valine_molsys.structures.bioassembly = {
        'B': {'chain_indices': [0], 'rotations': np.eye(3)[None, ...],
              'translations': np.zeros((1, 3))}}

    msm.add(proline_molsys, valine_molsys)

    assemblies = proline_molsys.structures.bioassembly
    assert set(assemblies) == {'A', 'B'}
    assert assemblies['A']['chain_indices'] == [0]
    # The source's chain 0 became chain n_target_chains in the combined system.
    assert assemblies['B']['chain_indices'] == [n_target_chains]


def test_a_colliding_bioassembly_identifier_is_renamed_with_a_warning(
        proline_molsys, valine_molsys):
    for molsys in (proline_molsys, valine_molsys):
        molsys.structures.bioassembly = {
            '1': {'chain_indices': [0], 'rotations': np.eye(3)[None, ...],
                  'translations': np.zeros((1, 3))}}

    with pytest.warns(BioassemblyIdentifierCollisionWarning):
        msm.add(proline_molsys, valine_molsys)

    assemblies = proline_molsys.structures.bioassembly
    assert len(assemblies) == 2
    assert '1' in assemblies


def test_a_one_sided_force_field_clears_the_molecular_mechanics(proline_molsys, valine_molsys):
    # A merged atoms_ff would cover only the target's atoms, which the fixed invariants
    # forbid. Under the default policy it goes, with a warning.
    pytest.importorskip('pandas')
    import pandas as pd

    n_atoms = msm.get(proline_molsys, n_atoms=True)
    proline_molsys.molecular_mechanics.atoms_ff = pd.DataFrame(
        {'atom_type': ['CT'] * n_atoms})

    with pytest.warns(StructuralAttributeDropWarning):
        msm.add(proline_molsys, valine_molsys)

    assert proline_molsys.molecular_mechanics.atoms_ff is None


# =====================================================================================
# D5 - add() is one-to-one
# =====================================================================================

def test_a_list_of_independent_systems_is_still_refused(proline_molsys, valine_molsys):
    # Already true, and D5 must keep it true: deleting the loop must not turn a list of
    # independent systems into a silently accepted sequence of additions.
    from molsysmt._private.smonitor import MultipleMolecularSystemsError

    with pytest.raises(MultipleMolecularSystemsError):
        msm.add(proline_molsys, [valine_molsys, valine_molsys.copy()])


def test_the_dispatcher_has_no_target_by_source_loop():
    # D5 deletes the Cartesian loop. Its absence is the observable contract: the
    # dispatcher must not iterate a target sequence against a source sequence.
    import inspect

    from molsysmt.basic import add as add_module

    source = inspect.getsource(getattr(add_module, '__wrapped__', add_module))
    assert 'for to_item' not in source


# =====================================================================================
# D6 - alternate_location is atom-aligned in meaning
# =====================================================================================

def test_alternate_locations_are_merged_with_atom_indices_remapped(
        proline_molsys, valine_molsys):
    n_target = msm.get(proline_molsys, n_atoms=True)
    proline_molsys.structures.alternate_location = [{0: 'A'}]
    valine_molsys.structures.alternate_location = [{3: 'B'}]

    msm.add(proline_molsys, valine_molsys)

    assert proline_molsys.structures.alternate_location == [{0: 'A', n_target + 3: 'B'}]
