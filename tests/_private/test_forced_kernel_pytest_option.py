"""Regression tests for forcing one CPU backend across an xdist session."""

import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("backend", ["numba", "rust"])
def test_forced_kernel_option_reaches_xdist_worker(tmp_path, backend):
    """The command-line choice must govern code executed inside a worker."""
    if backend == "rust":
        import molsysmt._rust  # noqa: F401

    probe = tmp_path / "test_forced_kernel_probe.py"
    probe.write_text(
        "import molsysmt as msm\n"
        "from molsysmt._private import rust_backend\n"
        "\n"
        "def test_forced_backend():\n"
        f"    assert msm.configure.kernel == {backend!r}\n"
        f"    assert rust_backend._use_rust(None) is {backend == 'rust'!r}\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-n",
            "2",
            "--rootdir",
            str(REPO_ROOT),
            "-p",
            "conftest",
            "--molsysmt-kernel",
            backend,
            "-p",
            "no:cacheprovider",
            "-q",
            str(probe),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"forced {backend} subprocess failed:\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
