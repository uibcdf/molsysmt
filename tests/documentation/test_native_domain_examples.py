"""Execute native-domain guidance against independent physical/index expectations."""

import json
import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]
FOUNDATION = (
    ROOT / "docs/content/user/foundations/native_world/classes/molsysmt_MolSys.md"
)


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_native_composition_example_keeps_separate_domains_and_physical_axes(
    length_unit, time_unit
):
    blocks = re.findall(r"^```python\n(.*?)^```", FOUNDATION.read_text(), re.M | re.S)
    assert len(blocks) == 3
    namespace = {}
    puw = msm.pyunitwizard
    expected = np.array(
        [[[0, 0, 0], [1, 0, 0], [2, 0, 0]], [[0, 0, 1], [1, 0, 1], [2, 0, 1]]],
        dtype=float,
    )
    with puw.context(
        standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
    ):
        for block in blocks:
            exec(compile(block, str(FOUNDATION), "exec"), namespace)
        molsys, copied, restored = (
            namespace[name] for name in ["molsys", "molsys_A", "molsys_B"]
        )
        assert not namespace["path"].exists()
        for system in [molsys, copied, restored]:
            assert system.topology.n_atoms == system.chemical_states.n_atoms == 3
            assert system.get(element="atom", atom_type=True) == ["C", "C", "O"]
            assert system.chemical_states.n_chemical_states == 1
            assert system.get(n_bonds=True) == 2
            assert system.get(connectivity_completeness=True) == "partial"
            assert not any(
                hasattr(system.topology, name)
                for name in ["bonds", "components", "chemical_states"]
            )
            selected = system.get(
                element="atom",
                selection=[2, 0, 2],
                structure_indices=[1, 0],
                coordinates=True,
            )
            assert selected.shape == (2, 3, 3)
            assert puw.get_unit(selected) == puw.unit(length_unit)
            np.testing.assert_allclose(
                puw.get_value(selected, to_unit="angstrom"),
                expected[[1, 0]][:, [2, 0, 2]],
            )
            time = system.get(time=True)
            assert puw.get_unit(time) == puw.unit(time_unit)
            np.testing.assert_allclose(puw.get_value(time, to_unit="fs"), [0, 2])
        restored.chemical_states.add_bonds([[0, 2]])
        assert restored.get(n_bonds=True) == 3
        assert molsys.get(n_bonds=True) == copied.get(n_bonds=True) == 2
        assert namespace["chemistry"].get(n_bonds=True) == 2
        for system in [molsys, copied, restored]:
            np.testing.assert_allclose(
                puw.get_value(
                    system.get(element="atom", coordinates=True), to_unit="angstrom"
                ),
                expected,
            )


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_current_h5msm_guide_keeps_mechanical_requests_as_declared(
    length_unit, time_unit
):
    page = ROOT / "docs/content/user/tools/form/file/h5msm_10.md"
    blocks = re.findall(r"^```python\n(.*?)^```", page.read_text(), re.M | re.S)
    assert len(blocks) == 1
    namespace = {}
    puw = msm.pyunitwizard
    with puw.context(
        standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
    ):
        exec(compile(blocks[0], str(page), "exec"), namespace)
        molsys, restored = namespace["molsys"], namespace["restored"]
        assert not namespace["path"].exists()
        assert restored.molecular_mechanics is not molsys.molecular_mechanics
        assert restored.molecular_mechanics.forcefield == "unresolved_model_request"
        np.testing.assert_array_equal(
            restored.molecular_mechanics.partial_charge, [0.25, -0.25]
        )
        assert restored.get(connectivity_completeness=True) == "unavailable"
        assert not hasattr(restored.topology, "bonds")
        coordinates = restored.get(element="atom", coordinates=True)
        assert coordinates.shape == (1, 2, 3)
        assert puw.get_unit(coordinates) == puw.unit(length_unit)
        np.testing.assert_array_equal(puw.get_value(coordinates, to_unit="nm"), 0)


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_existing_core_native_cells_keep_ownership_and_default_persistence(
    length_unit, time_unit
):
    page = ROOT / "docs/content/course/Common_Core/04_Native_Forms.ipynb"
    notebook = json.loads(page.read_text())
    namespace = {"systems": msm.systems}
    puw = msm.pyunitwizard
    with puw.context(
        standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
    ):
        for index in [10, 13, 15, 17, 19, 22]:
            cell = notebook["cells"][index]
            assert cell["cell_type"] == "code"
            exec(
                compile("".join(cell["source"]), f"{page}:cell-{index}", "exec"),
                namespace,
            )
        assembled, restored = namespace["assembled"], namespace["restored"]
        assert restored.get(element="atom", formal_charge=True) == [1, -1]
        assert assembled.topology is not namespace["molsys"].topology
        assert not hasattr(restored.topology, "chemical_states")
        np.testing.assert_array_equal(
            restored.molecular_mechanics.partial_charge, [1, -1]
        )
        np.testing.assert_allclose(
            puw.get_value(restored.get(element="atom", coordinates=True), to_unit="nm"),
            [[[0, 0, 0], [0.25, 0, 0]]],
        )
        states = namespace["chemical_states"]
        assert states.reference_chemical_state_index == 0
        assert [states.get(chemical_state=i, n_bonds=True) for i in [0, 1]] == [2, 0]
