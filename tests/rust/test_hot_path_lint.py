"""The Rust hot-path lint must pass, and must actually detect a regression.

Rationale: the optimisations in `devguide/rust_kernel_optimization_guide.md` are invisible
to every other test — reintroducing `f64::floor()` in an inner loop leaves the results
correct and only makes them 1.4x slower. Nothing else in the suite would notice.

The second test guards the guard: a lint that cannot fail is worthless.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "devtools" / "scripts" / "check_rust_hot_paths.py"
SRC = REPO / "rust" / "src"

pytestmark = pytest.mark.skipif(
    not SRC.is_dir(), reason="the Rust kernel sources are not present in this checkout"
)


def run_lint(script=None):
    """Run the lint. The script locates the sources relative to its own path, so the
    second test must invoke the *copy* it planted, not this repo's original."""
    return subprocess.run(
        [sys.executable, str(script or SCRIPT)],
        capture_output=True,
        text=True,
    )


def test_rust_kernels_have_no_libm_rounding_in_hot_paths():
    result = run_lint()
    assert result.returncode == 0, (
        "the Rust hot-path lint failed — a rounding call that lowers to libm on the "
        f"x86-64 baseline reached a kernel:\n{result.stdout}\n{result.stderr}"
    )


def test_the_lint_detects_a_reintroduced_libm_call(tmp_path):
    """Copy the tree, plant the exact regression that cost 1.4x, and require a failure."""
    import shutil

    fake_repo = tmp_path / "repo"
    (fake_repo / "rust").mkdir(parents=True)
    (fake_repo / "devtools" / "scripts").mkdir(parents=True)
    shutil.copytree(SRC, fake_repo / "rust" / "src")
    planted_script = fake_repo / "devtools" / "scripts" / SCRIPT.name
    shutil.copy(SCRIPT, planted_script)

    target = fake_repo / "rust" / "src" / "mic.rs"
    text = target.read_text()
    needle = "fast_floor(v[0] / cell[0][0] + 0.5)"
    assert needle in text, "the orthogonal wrap no longer looks as expected; update this test"
    target.write_text(text.replace(needle, "(v[0] / cell[0][0] + 0.5).floor()"))

    result = run_lint(planted_script)
    assert result.returncode != 0, (
        "the lint passed on a tree with a libm floor() call in the minimum-image wrap; "
        "it is not guarding anything"
    )
    assert "mic.rs" in result.stdout
