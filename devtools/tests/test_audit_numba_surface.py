from pathlib import Path

from devtools.scripts import audit_numba_surface as audit


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_inventory_finds_stable_runtime_identities_and_broad_surfaces(tmp_path):
    _write(
        tmp_path / "molsysmt/lib/kernel.py",
        "from molsysmt._private.jit import lazy_njit\n"
        "@lazy_njit('sig', parallel=True)\n"
        "def distance(values):\n"
        "    return values\n",
    )
    _write(
        tmp_path / "molsysmt/lib/distance_cuda.py",
        "try:\n"
        "    from numba import cuda\n"
        "    @cuda.jit\n"
        "    def distance_cuda(values):\n"
        "        return values\n"
        "except ImportError:\n"
        "    cuda = None\n",
    )
    _write(
        tmp_path / "molsysmt/consumer.py",
        "from molsysmt.lib.kernel import distance\n",
    )
    _write(tmp_path / "molsysmt/_private/jit.py", "import numba as nb\n")
    _write(tmp_path / "tests/test_kernel.py", "# numba parity\n")
    _write(tmp_path / "docs/guide.md", "Numba migration.\n")
    _write(tmp_path / "devguide/current.md", "lazy_njit inventory.\n")
    _write(tmp_path / "devguide/archive/old.md", "numba history.\n")
    _write(tmp_path / "pyproject.toml", 'dependencies = ["numba"]\n')

    inventory = audit.collect_inventory(tmp_path)

    assert inventory["guarded"]["cpu_jit_sites"] == [
        "molsysmt/lib/kernel.py::distance::lazy_njit",
    ]
    assert inventory["guarded"]["cuda_jit_sites"] == [
        "molsysmt/lib/distance_cuda.py::distance_cuda::cuda.jit",
    ]
    assert inventory["guarded"]["numba_imports"] == [
        "molsysmt/_private/jit.py::numba",
        "molsysmt/lib/distance_cuda.py::numba",
    ]
    assert inventory["guarded"]["cuda_modules"] == [
        "molsysmt/lib/distance_cuda.py"
    ]
    assert inventory["guarded"]["direct_lib_consumers"] == [
        "molsysmt/consumer.py::molsysmt.lib.kernel"
    ]
    assert inventory["surfaces"]["dependency_files"] == ["pyproject.toml"]
    assert inventory["surfaces"]["runtime_reference_files"] == [
        "molsysmt/_private/jit.py",
        "molsysmt/lib/distance_cuda.py",
        "molsysmt/lib/kernel.py",
    ]
    assert inventory["surfaces"]["test_files"] == ["tests/test_kernel.py"]
    assert inventory["surfaces"]["active_documentation_files"] == [
        "docs/guide.md"
    ]
    assert inventory["surfaces"]["active_devguide_files"] == [
        "devguide/current.md"
    ]


def test_guarded_comparison_allows_removal_and_rejects_addition():
    baseline = {
        "guarded": {
            category: [] for category in audit.GUARDED_CATEGORIES
        }
    }
    baseline["guarded"]["cpu_jit_sites"] = ["old.py::old::lazy_njit"]
    current = {
        "guarded": {
            category: [] for category in audit.GUARDED_CATEGORIES
        }
    }
    current["guarded"]["cpu_jit_sites"] = ["new.py::new::lazy_njit"]

    added, resolved = audit.compare_guarded(current, baseline)

    assert added == {"cpu_jit_sites": ["new.py::new::lazy_njit"]}
    assert resolved == {"cpu_jit_sites": ["old.py::old::lazy_njit"]}


def test_line_movement_does_not_change_a_jit_identity(tmp_path):
    kernel = tmp_path / "molsysmt/lib/kernel.py"
    source = (
        "from molsysmt._private.jit import lazy_njit\n"
        "@lazy_njit('sig')\n"
        "def kernel(values):\n"
        "    return values\n"
    )
    _write(kernel, source)
    before = audit.collect_inventory(tmp_path)["guarded"]["cpu_jit_sites"]
    _write(kernel, "\n\n" + source)
    after = audit.collect_inventory(tmp_path)["guarded"]["cpu_jit_sites"]

    assert before == after
