"""Regression tests for the documentation build environment."""

from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "sphinx_docs_to_gh_pages.yaml"


def test_documentation_build_uses_the_minimal_pinned_rust_toolchain():
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["sphinx_docs_to_gh-pages"]["steps"]
    by_name = {step.get("name"): step for step in steps if "name" in step}

    toolchain = by_name["Select the pinned minimal Rust toolchain"]
    assert "rustup toolchain install 1.97.1 --profile minimal" in toolchain["run"]

    install = by_name["Install package"]
    assert install["env"]["RUSTUP_TOOLCHAIN"] == "1.97.1"
    assert "python -m pip install . --no-deps" in install["run"]
