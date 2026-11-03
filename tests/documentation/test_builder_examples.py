"""Executing documented staging with absent chemical and structural domains."""

import re
from pathlib import Path

import numpy as np

import molsysmt as msm


def test_missing_domain_example_preserves_absence_and_source():
    path = (
        Path(__file__).resolve().parents[2]
        / "docs/content/user/foundations/native_world/classes/molsysmt_MolSysBuilder.md"
    )
    section = (
        path.read_text().split("### Missing Domains\n", 1)[1].split("\n### ", 1)[0]
    )
    blocks = re.findall(r"```python\n(.*?)\n```", section, re.DOTALL)
    assert len(blocks) == 1
    namespace = {}
    exec(compile(blocks[0], str(path), "exec"), namespace)
    source = namespace["molsys"]
    builder = namespace["builder"]
    result = namespace["new_molsys"]
    assert (
        source.chemical_states
        is builder.chemical_states
        is result.chemical_states
        is None
    )
    assert source.structures is None
    assert result.structures.coordinates is None
    assert result.structures.n_structures == 0
    assert len(source.topology.atoms) == len(result.topology.atoms) == 2
    assert result.topology is not source.topology


def test_builder_foundation_examples_preserve_declared_graph_and_geometry():
    path = (
        Path(__file__).resolve().parents[2]
        / "docs/content/user/foundations/native_world/classes/molsysmt_MolSysBuilder.md"
    )
    blocks = re.findall(r"```python\n(.*?)\n```", path.read_text(), re.DOTALL)
    assert len(blocks) == 3
    namespace = {
        "molsys": msm.convert(msm.systems["Met-enkephalin"]["met_enkephalin.h5msm"])
    }
    for block in blocks:
        exec(compile(block, str(path), "exec"), namespace)
    result = namespace["molsys"]
    assert result.get(n_atoms=True, n_groups=True, n_bonds=True) == [3, 1, 2]
    assert result.topology.groups["group_type"].tolist() == ["amino acid"]
    assert result.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1], [1, 2]]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
        [[[0.0, 0.0, 0.0], [0.145, 0.0, 0.0], [0.245, 0.12, 0.0]]],
    )
