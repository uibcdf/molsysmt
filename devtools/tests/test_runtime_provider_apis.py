"""Executing provider operations used by the core runtime dependency contract.

Run this module with exact minimum providers to receive those versions. Passing
with a newer environment alone does not qualify declared minima or optional engines.
"""

import io
import subprocess
import sys
import tomllib
from pathlib import Path

import h5py
import networkx as nx
import numpy as np
import pandas as pd
from packaging.requirements import Requirement
from packaging.version import Version


def test_default_styler_renderer_is_a_declared_runtime_requirement():
    root = Path(__file__).resolve().parents[2]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    requirements = {
        r.name.lower(): r for r in map(Requirement, project["dependencies"])
    }
    assert "jinja2" in requirements, (
        "Default basic/native info() needs pandas Styler's renderer."
    )
    requirement = requirements["jinja2"]
    # pandas 2.2.2's published compat/_optional.py requires Jinja2 >=3.1.2.
    assert any(
        s.operator == ">=" and Version(s.version) >= Version("3.1.2")
        for s in requirement.specifier
    )
    import jinja2

    assert requirement.specifier.contains(jinja2.__version__)


def test_numpy_arrays_cross_native_bridge():
    # Keep this ABI probe independent of the remaining MolSysMT runtime. A
    # separate process also avoids initializing one extension under two names.
    subprocess.run(
        [
            sys.executable,
            "-c",
            """
from importlib.machinery import PathFinder
from importlib.util import find_spec, module_from_spec
from pathlib import Path
import numpy as np
root = Path(find_spec('molsysmt').origin).parent
spec = PathFinder.find_spec('_rust', [str(root)])
assert spec is not None, 'The bundled native extension is required.'
backend = module_from_spec(spec)
spec.loader.exec_module(backend)
coordinates = np.array([[[0., 0., 0.], [0.3, 0., 0.]]])
observed = backend.get_distances_single_system(coordinates, 1)
assert observed.shape == (1, 2, 2)
np.testing.assert_allclose(observed, [[[0., 0.3], [0.3, 0.]]])
""",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def test_h5msm_string_and_extendable_dataset_operations(tmp_path):
    path = tmp_path / "provider.h5msm"
    with h5py.File(path, "w") as file:
        names = file.create_dataset(
            "names", shape=(0,), maxshape=(None,), dtype=h5py.string_dtype()
        )
        names.resize(2, axis=0)
        names[:] = ["alpha", "β"]
        assert h5py.check_string_dtype(names.dtype).encoding == "utf-8"
    with h5py.File(path, "r") as file:
        assert file["names"].asstr()[:].tolist() == ["alpha", "β"]


def test_nullable_inventory_mapping_and_styler_operations():
    data = pd.DataFrame({"index": pd.array([1, None, 3], dtype="Int64")})
    mapped = data.map(lambda value: value, na_action="ignore")
    assert pd.isna(mapped.loc[1, "index"])
    assert data["index"].dropna().astype(int).tolist() == [1, 3]
    html = (
        data.style.hide(axis="index")
        .set_table_attributes('class="dataframe"')
        .to_html()
    )
    assert 'class="dataframe"' in html


def test_state_graph_components_bridges_and_ring_basis():
    graph = nx.Graph([(0, 1), (1, 2), (2, 3), (3, 0), (3, 4)])
    assert list(nx.connected_components(graph)) == [{0, 1, 2, 3, 4}]
    assert {frozenset(pair) for pair in nx.bridges(graph)} == {frozenset([3, 4])}
    assert {frozenset(block) for block in nx.biconnected_components(graph)} == {
        frozenset([3, 4]),
        frozenset([0, 1, 2, 3]),
    }
    assert {frozenset(ring) for ring in nx.minimum_cycle_basis(graph)} == {
        frozenset([0, 1, 2, 3])
    }


def test_colormap_registry_and_centered_normalization():
    from matplotlib.colors import CenteredNorm, TwoSlopeNorm, to_hex
    from matplotlib.pyplot import colormaps

    centered = CenteredNorm(vcenter=2.0, halfrange=1.0)
    split = TwoSlopeNorm(vmin=1.0, vcenter=2.0, vmax=4.0)
    assert centered(2.0) == split(2.0) == 0.5
    color = colormaps["viridis"](split(2.0))
    assert len(color) == 4 and np.isfinite(color).all()
    assert to_hex("red") == "#ff0000"


def test_standard_and_auto_progress_iterator_lifecycle():
    from tqdm import tqdm
    from tqdm.auto import tqdm as auto_tqdm

    for progress_type in (tqdm, auto_tqdm):
        with progress_type(total=2, file=io.StringIO()) as progress:
            progress.update(1)
            progress.set_description("structures")
            progress.update(1)
            assert progress.n == 2
