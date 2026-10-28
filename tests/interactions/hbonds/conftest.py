"""Small declared role graph, without geometry or implicit hydrogen preparation."""

import pytest

import molsysmt as msm


@pytest.fixture
def role_system():
    builder = msm.MolSysBuilder()
    for name, kind in [
        ("N0", "N"),
        ("H1", "H"),
        ("N2", "N"),
        ("H3", "H"),
        ("O4", "O"),
        ("S5", "S"),
        ("NE2", "N"),
        ("H7", "H"),
        ("ND1", "N"),
        ("H9", "H"),
        ("NE2", "N"),
        ("C11", "C"),
    ]:
        builder.add_atom(atom_name=name, atom_type=kind)
    for atoms, name in [
        ([0, 1, 2, 3, 4, 5], "LIG"),
        ([6, 7], "GLN"),
        ([8, 9, 10], "HIS"),
        ([11], "LIG"),
    ]:
        builder.add_group(atoms, group_name=name)
    for first, second in [(0, 3), (2, 1), (6, 7), (8, 9)]:
        builder.add_bond(first, second)
    return builder.build()
