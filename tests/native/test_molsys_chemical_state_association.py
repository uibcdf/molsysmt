"""Testing MolSys structure-to-chemical-state association semantics."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentLengthError, StructuralInconsistencyError
from molsysmt.native import MolSys


def _multistate_molsys(state_indices=(0, 1, 1)):
    molsys = MolSys(n_atoms=2)
    molsys.topology.atoms['atom_id'] = ['0', '1']
    molsys.topology.atoms['atom_name'] = ['C', 'O']
    molsys.topology.atoms['atom_type'] = ['C', 'O']
    molsys.topology._set_chemical_state_atom_attribute('formal_charge', [0, -1])
    molsys.topology._append_chemical_state_bonds([[0, 1]], orders=1)
    product = molsys.topology._append_chemical_state(state_id='product')
    molsys.topology._set_chemical_state_atom_attribute(
        'formal_charge', [1, 0], state_index=product
    )
    molsys.topology._append_chemical_state_bonds(
        [[0, 1]], orders=2, state_index=product
    )
    molsys.topology._set_reference_chemical_state_index(None)
    molsys.structures.coordinates = msm.pyunitwizard.quantity(
        np.zeros((len(state_indices), 2, 3)), 'nm'
    )
    molsys._set_structure_chemical_state_indices(state_indices)
    return molsys


def test_public_get_set_and_capability_expose_resolved_structure_association():
    molsys = _multistate_molsys()

    assert msm.get(molsys, structure_chemical_state_index=True) == [0, 1, 1]
    assert msm.get(
        molsys,
        structure_indices=[2, 0],
        structure_chemical_state_index=True,
    ) == [1, 0]
    assert msm.has_attribute(molsys, 'structure_chemical_state_index')

    msm.set(
        molsys,
        element='system',
        structure_indices=[1],
        structure_chemical_state_index=0,
    )
    assert msm.get(molsys, structure_chemical_state_index=True) == [0, 0, 1]


def test_single_state_association_is_implicit_without_allocating_storage():
    molsys = MolSys(n_atoms=1)
    molsys.structures.coordinates = msm.pyunitwizard.quantity(
        np.zeros((2, 1, 3)), 'nm'
    )

    assert molsys._structure_chemical_state_indices is None
    assert msm.get(molsys, structure_chemical_state_index=True) == [0, 0]
    assert msm.has_attribute(molsys, 'structure_chemical_state_index')
    assert molsys._structure_chemical_state_indices is None


def test_legacy_structures_association_migrates_to_molsys_authority():
    legacy = _multistate_molsys()
    legacy.structures._chemical_state_indices = pd.array(
        [0, -1, pd.NA], dtype='Int64'
    )
    state = legacy.__dict__.copy()
    state.pop('_structure_chemical_state_indices')

    restored = MolSys.__new__(MolSys)
    restored.__setstate__(state)

    assert restored._structure_chemical_state_indices[0] == 0
    assert pd.isna(restored._structure_chemical_state_indices[1:]).all()
    assert not hasattr(restored.structures, '_chemical_state_indices')


def test_nullable_and_invalid_associations_fail_closed():
    molsys = _multistate_molsys()
    msm.set(
        molsys,
        element='system',
        structure_indices=[1],
        structure_chemical_state_index=pd.NA,
    )

    assert msm.get(molsys, structure_chemical_state_index=True) == [0, pd.NA, 1]
    assert not msm.has_attribute(molsys, 'structure_chemical_state_index')
    assert msm.has_attribute(
        molsys, 'structure_chemical_state_index', include_none=True
    )
    with pytest.raises(StructuralInconsistencyError, match='no chemical-state association'):
        msm.get(
            molsys,
            element='atom',
            structure_indices=[1],
            chemical_state='structure',
            formal_charge=True,
        )
    with pytest.raises(StructuralInconsistencyError, match='existing chemical-state'):
        molsys._set_structure_chemical_state_indices([0, 1, 2])
    with pytest.raises(ArgumentLengthError):
        molsys._set_structure_chemical_state_indices([0, 1])


def test_structure_resolver_drives_get_select_and_rejects_mixed_states():
    molsys = _multistate_molsys()

    assert msm.get(
        molsys,
        element='atom',
        structure_indices=[0],
        chemical_state='structure',
        formal_charge=True,
    ) == [0, -1]
    assert msm.get(
        molsys,
        element='bond',
        structure_indices=[1, 2],
        chemical_state='structure',
        bond_order=True,
    ) == [2]
    assert msm.select(
        molsys,
        'formal_charge==1',
        structure_indices=[2],
        chemical_state='structure',
    ) == [0]
    assert msm.has_attribute(
        molsys,
        'formal_charge',
        structure_indices=[2],
        chemical_state='structure',
    )
    with pytest.raises(StructuralInconsistencyError, match='span multiple chemical states'):
        msm.select(
            molsys,
            'formal_charge!=0',
            chemical_state='structure',
        )


def test_copy_extract_and_remove_preserve_aligned_association_independently():
    molsys = _multistate_molsys()

    copied = molsys.copy()
    extracted = molsys.extract(structure_indices=[2, 0], skip_digestion=True)
    removed = molsys.remove(structure_indices=[1], skip_digestion=True)
    copied._set_structure_chemical_state_indices(0, structure_indices=[2])

    assert msm.get(molsys, structure_chemical_state_index=True) == [0, 1, 1]
    assert msm.get(copied, structure_chemical_state_index=True) == [0, 1, 0]
    assert msm.get(extracted, structure_chemical_state_index=True) == [1, 0]
    assert msm.get(removed, structure_chemical_state_index=True) == [0, 1]


def test_native_append_preserves_exact_inventory_and_rejects_mismatch():
    target = _multistate_molsys((0,))
    source = _multistate_molsys((1, 1))

    target.append_structures(source, skip_digestion=True)
    assert msm.get(target, structure_chemical_state_index=True) == [0, 1, 1]

    incompatible = _multistate_molsys((1,))
    incompatible.topology._chemical_states[1].bonds.at[0, 'bond_order'] = 3
    with pytest.raises(StructuralInconsistencyError, match='inventories match exactly'):
        target.append_structures(incompatible, skip_digestion=True)


def test_public_concatenation_preserves_association_for_native_molsys():
    first = _multistate_molsys((0,))
    second = _multistate_molsys((1, 1))

    output = msm.concatenate_structures([first, second], to_form='molsysmt.MolSys')

    assert msm.get(output, structure_chemical_state_index=True) == [0, 1, 1]


def test_public_append_preserves_association_for_native_molsys():
    target = _multistate_molsys((0,))
    source = _multistate_molsys((1, 1))

    msm.append_structures(target, source)

    assert msm.get(target, structure_chemical_state_index=True) == [0, 1, 1]
