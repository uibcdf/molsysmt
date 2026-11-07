"""Execute documented placement workflows with local molecular inputs."""

import json
import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]


def test_center_cookbook_places_rigid_atoms():
    source = (
        ROOT / "docs/content/user/cookbook/placing_selected_centers.md"
    ).read_text()
    namespace = {}
    for code in re.findall(r"```python\n(.*?)```", source, re.S):
        exec(compile(code, "placing_selected_centers.md", "exec"), namespace)
    np.testing.assert_allclose(namespace["xyz"][0, :, 0], [2.0, 4.0, 1.0, 3.0])


def test_antiviral_geometric_course_moves_only_inhibitor_chain(
    monkeypatch, headless_plotting
):
    """A peptide inhibitor must be selected by identity rather than small-molecule type."""
    seed = msm.build.build_peptide("AlaGlyPro")
    count = msm.get(seed, n_atoms=True)
    source = msm.merge([seed, seed.copy()])
    msm.set(
        source,
        element="chain",
        selection=[0, 1],
        chain_id=["A", "B"],
        chain_name=["A", "C"],
    )
    assert msm.get(source, element="molecule", molecule_type=True) == [
        "peptide",
        "peptide",
    ]
    assert msm.select(source, 'molecule_type=="small molecule"') == []
    before = msm.pyunitwizard.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    original_convert = msm.convert

    def local_convert(molecular_system, *args, **kwargs):
        if isinstance(molecular_system, str) and molecular_system == "pdb:6LU7":
            return source
        return original_convert(molecular_system, *args, **kwargs)

    monkeypatch.setattr(msm, "convert", local_convert)
    path = (
        ROOT / "docs/content/course/Path_Antiviral/46_Geometric_Transformations.ipynb"
    )
    namespace = {}
    for cell in json.loads(path.read_text())["cells"]:
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
    assert namespace["inhibitor_atom_indices"] == list(range(count, 2 * count))
    after = msm.pyunitwizard.get_value(msm.get(source, coordinates=True), to_unit="nm")
    center = before[:, count:].mean(axis=1, keepdims=True)
    relative = before[:, count:] - center
    expected = (
        np.stack(
            (
                (relative[..., 0] - relative[..., 1]) / np.sqrt(2),
                (relative[..., 0] + relative[..., 1]) / np.sqrt(2),
                relative[..., 2],
            ),
            axis=-1,
        )
        + center
    )
    np.testing.assert_allclose(after[:, count:], expected, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(after[:, :count], before[:, :count])
    assert np.any(np.abs(after[:, count:] - before[:, count:]) > 1e-8)
    assert headless_plotting


@pytest.mark.parametrize("domain", ["Alzheimer", "Enzyme"])
def test_geometric_course_executes_with_local_source_substitutions(
    domain, monkeypatch, headless_plotting
):
    """Replace only remote input identifiers; run actual public scientific tools."""
    if domain == "Enzyme":
        pytest.importorskip("rdkit")
    original_convert = msm.convert

    def local_convert(molecular_system, *args, **kwargs):
        if isinstance(molecular_system, str):
            if molecular_system == "pdb:6EQE":
                molecular_system = msm.systems["T4 lysozyme L99A"]["181l.bcif.gz"]
            elif molecular_system == "pdb:2BEG":
                molecular_system = msm.systems["pentalanine"]["traj_pentalanine.h5msm"]
        return original_convert(molecular_system, *args, **kwargs)

    monkeypatch.setattr(msm, "convert", local_convert)
    path = (
        ROOT / f"docs/content/course/Path_{domain}/46_Geometric_Transformations.ipynb"
    )
    namespace = {}
    for cell in json.loads(path.read_text())["cells"]:
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
    center = namespace["center" if domain == "Alzheimer" else "new_center"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(center, to_unit="nm"), 0.0, atol=1e-12
    )
    if domain == "Alzheimer":
        assert msm.get(namespace["molsys"], n_structures=True) == 1
        assert namespace["fibril_atom_indices"]
        assert namespace["peptide_atom_indices"]
        assert set(namespace["fibril_atom_indices"]).isdisjoint(
            namespace["peptide_atom_indices"]
        )
    assert headless_plotting
