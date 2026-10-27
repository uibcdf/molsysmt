"""Shared complete-ring fixtures with explicit hierarchy and structural axes."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import Structures, Topology


@pytest.fixture
def aromatic_system():
    topology = Topology(n_atoms=6)
    topology.atoms["atom_type"] = ["C"] * 6
    topology.atoms["atom_name"] = [f"C{i}" for i in range(6)]
    topology.atoms["atom_id"] = [str(100 + i) for i in range(6)]
    topology.bonds = pd.DataFrame(
        dict(
            atom1_index=np.arange(6),
            atom2_index=np.roll(np.arange(6), -1),
            bond_type=["covalent"] * 6,
            bond_order=[1, 2, 1, 2, 1, 2],
            is_aromatic=[True] * 6,
        )
    )
    state = topology._chemical_states_domain._states[0]
    state.connectivity_completeness = "complete"
    for name, values in dict(
        formal_charge=[0] * 6,
        n_unpaired_electrons=[0] * 6,
        n_implicit_hydrogens=[1] * 6,
        is_aromatic=[True] * 6,
    ).items():
        state.set_atom_attribute(name, values)
    builder = msm.MolSysBuilder(msm.convert(topology, to_form="molsysmt.MolSys"))
    group = builder.add_group(list(range(6)), group_name="BEN", group_id="1")
    builder.add_chain([group], chain_id="A")
    molsys = builder.build()
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(54, dtype=float).reshape(3, 6, 3) / 100, "nm"
        )
    )
    return molsys
