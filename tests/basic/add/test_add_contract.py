"""
The behaviour of `add()` that the Phase 1 audit confirmed as contract.

These tests pin what the atom-axis audit found already correct, so that Phase 3 cannot
regress it while implementing decisions D1-D7. The decisions themselves, and the
defects the audit found, are in `test_add_audit_decisions.py`.

Audit: `devguide/pending_proposals/atom_axis_add_phase1_findings.md`, section 5,
"Confirmed contract".
"""

import warnings

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentLengthError, StructuralAttributeDropWarning


def _atom_aligned(molsys, name):
    return getattr(molsys.structures, f'_{name}', None) is not None


# --- 1. one-sided atom-aligned attributes are dropped, in both directions -------------

@pytest.mark.parametrize('attribute', ['b_factor', 'occupancy', 'velocities'])
@pytest.mark.parametrize('donor', ['target', 'source'])
def test_a_one_sided_atom_aligned_attribute_is_dropped_with_a_warning(
        proline_molsys, valine_molsys, attribute, donor):
    target, source = proline_molsys, valine_molsys
    giver, other = (target, source) if donor == 'target' else (source, target)
    n_atoms = giver.structures.coordinates.shape[1]
    shape = (1, n_atoms, 3) if attribute == 'velocities' else (1, n_atoms)
    value = np.ones(shape, dtype=float)
    if attribute == 'velocities':
        value = puw.quantity(value, 'nm/ps')
    setattr(giver.structures, attribute, value)
    setattr(other.structures, attribute, None)
    expected_atoms = (target.structures.coordinates.shape[1]
                      + source.structures.coordinates.shape[1])

    with pytest.warns(StructuralAttributeDropWarning):
        msm.add(target, source)

    # The column cannot cover only part of the atom axis, so it goes entirely.
    assert not _atom_aligned(target, attribute)
    assert msm.get(target, n_atoms=True) == expected_atoms


def test_an_attribute_present_on_both_sides_is_concatenated(proline_molsys, valine_molsys):
    target, source = proline_molsys, valine_molsys
    n_target = target.structures.coordinates.shape[1]
    n_source = source.structures.coordinates.shape[1]
    target.structures.b_factor = np.zeros((1, n_target), dtype=float)
    source.structures.b_factor = np.ones((1, n_source), dtype=float)

    with warnings.catch_warnings():
        warnings.simplefilter('error', StructuralAttributeDropWarning)
        msm.add(target, source)

    b_factor = target.structures.b_factor
    assert b_factor.shape == (1, n_target + n_source)
    np.testing.assert_allclose(b_factor[0, :n_target], 0.0)
    np.testing.assert_allclose(b_factor[0, n_target:], 1.0)


def test_an_attribute_absent_on_both_sides_stays_absent(proline_molsys, valine_molsys):
    target, source = proline_molsys, valine_molsys
    target.structures.velocities = None
    source.structures.velocities = None

    with warnings.catch_warnings():
        warnings.simplefilter('error', StructuralAttributeDropWarning)
        msm.add(target, source)

    assert not _atom_aligned(target, 'velocities')


# --- 2. the operation is transactional ------------------------------------------------

def test_a_structure_count_mismatch_leaves_the_target_untouched(proline_molsys, valine_molsys):
    source = valine_molsys
    coordinates = puw.get_value(source.structures.coordinates, to_unit='nm')
    source.structures.coordinates = puw.quantity(np.repeat(coordinates, 2, axis=0), 'nm')
    n_atoms = msm.get(proline_molsys, n_atoms=True)

    with pytest.raises(ArgumentLengthError):
        msm.add(proline_molsys, source)

    assert msm.get(proline_molsys, n_atoms=True) == n_atoms


def test_a_drop_warning_raised_as_an_error_leaves_the_target_untouched(
        proline_molsys, valine_molsys):
    target, source = proline_molsys, valine_molsys
    target.structures.b_factor = np.ones((1, target.structures.coordinates.shape[1]))
    n_atoms = msm.get(target, n_atoms=True)

    with warnings.catch_warnings():
        warnings.simplefilter('error', StructuralAttributeDropWarning)
        with pytest.raises(StructuralAttributeDropWarning):
            msm.add(target, source)

    # Atomicity has to survive the warning filter, not only a raised exception.
    assert msm.get(target, n_atoms=True) == n_atoms
    assert target.structures.b_factor.shape == (1, n_atoms)


# --- 3. in_place=False ----------------------------------------------------------------

def test_in_place_false_returns_a_new_system_and_leaves_the_original_alone(
        proline_molsys, valine_molsys):
    n_atoms = msm.get(proline_molsys, n_atoms=True)
    expected = n_atoms + msm.get(valine_molsys, n_atoms=True)

    result = msm.add(proline_molsys, valine_molsys, in_place=False)

    assert result is not proline_molsys
    assert msm.get_form(result) == 'molsysmt.MolSys'
    assert msm.get(result, n_atoms=True) == expected
    assert msm.get(proline_molsys, n_atoms=True) == n_atoms


def test_in_place_true_returns_none_and_mutates_the_target(proline_molsys, valine_molsys):
    expected = msm.get(proline_molsys, n_atoms=True) + msm.get(valine_molsys, n_atoms=True)

    assert msm.add(proline_molsys, valine_molsys) is None
    assert msm.get(proline_molsys, n_atoms=True) == expected


# --- 4. source selection happens before the atom-axis concatenation --------------------

def test_the_source_selection_is_applied_before_concatenating(proline_molsys, valine_molsys):
    n_target = msm.get(proline_molsys, n_atoms=True)

    msm.add(proline_molsys, valine_molsys, selection=[0, 1, 2])

    assert msm.get(proline_molsys, n_atoms=True) == n_target + 3


def test_a_string_selection_applies_to_the_assembled_composite_source(proline_molsys):
    # There is no longer such a thing as a selection "over multiple sources": a list is
    # one system, so the selection is evaluated against the system it assembles to.
    from molsysmt import systems

    prmtop = systems['pentalanine']['pentalanine.prmtop']
    inpcrd = systems['pentalanine']['pentalanine.inpcrd']
    composite = msm.convert([prmtop, inpcrd], to_form='molsysmt.MolSys')
    selected = len(msm.select(composite, selection='atom_type=="C"'))
    n_target = msm.get(proline_molsys, n_atoms=True)

    result = msm.add(proline_molsys, [prmtop, inpcrd], selection='atom_type=="C"',
                     in_place=False)

    assert selected > 0
    assert msm.get(result, n_atoms=True) == n_target + selected


def test_structure_indices_select_structures_of_the_source(proline_molsys, valine_molsys):
    source = valine_molsys
    coordinates = puw.get_value(source.structures.coordinates, to_unit='nm')
    source.structures.coordinates = puw.quantity(np.repeat(coordinates, 3, axis=0), 'nm')
    n_target = msm.get(proline_molsys, n_atoms=True)

    msm.add(proline_molsys, source, structure_indices=[0])

    assert msm.get(proline_molsys, n_structures=True) == 1
    assert msm.get(proline_molsys, n_atoms=True) == n_target + coordinates.shape[1]


# --- 5. scope: which target forms can be added into at all ----------------------------

def test_only_two_forms_implement_add():
    from molsysmt.form import _dict_modules
    import inspect

    implemented = []
    for name, module in sorted(_dict_modules.items()):
        function = getattr(module, 'add', None)
        if function is None:
            continue
        target = getattr(function, '__wrapped__', function)
        try:
            source = inspect.getsource(target)
        except (OSError, TypeError):
            continue
        if 'NotImplemented' not in source:
            implemented.append(name)

    # Phase 1 measured exactly these two. Adding a third is a contract change that must
    # come with its own delivery tests, not an accident.
    assert implemented == ['molsysmt.MolSys', 'molsysmt.Structures']
