import numpy as np

import molsysmt as msm


def test_get_per_atom_mechanical_attributes(builder_pdb_molsys):
    mechanics = builder_pdb_molsys.molecular_mechanics
    msm.set(builder_pdb_molsys, element='atom', formal_charge=[0, 1, -1, 0])
    mechanics.partial_charge = [0.1, 0.2, -0.3, 0.0]
    mechanics.atom_ff_type = ['N', 'CT', 'C', 'O']

    formal_charge, partial_charge, atom_ff_type = msm.get(
        builder_pdb_molsys,
        element='atom',
        selection=[1, 2],
        formal_charge=True,
        partial_charge=True,
        atom_ff_type=True,
    )

    assert np.array_equal(formal_charge, [1, -1])
    assert np.allclose(partial_charge.astype(float), [0.2, -0.3])
    assert np.array_equal(atom_ff_type, ['CT', 'C'])


def test_get_mechanical_attributes_from_system(builder_pdb_molsys):
    mechanics = builder_pdb_molsys.molecular_mechanics
    msm.set(builder_pdb_molsys, element='atom', formal_charge=[0, 1, -1, 0])
    mechanics.partial_charge = [0.1, 0.2, -0.3, 0.0]
    mechanics.atom_ff_type = ['N', 'CT', 'C', 'O']

    formal_charge, partial_charge, atom_ff_type = msm.get(
        builder_pdb_molsys,
        element='system',
        formal_charge=True,
        partial_charge=True,
        atom_ff_type=True,
    )

    assert np.array_equal(formal_charge, [0, 1, -1, 0])
    assert np.allclose(partial_charge.astype(float), [0.1, 0.2, -0.3, 0.0])
    assert np.array_equal(atom_ff_type, ['N', 'CT', 'C', 'O'])
