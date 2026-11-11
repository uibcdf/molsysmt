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


def test_documentation_build_validates_stored_schemas_before_publishing():
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["sphinx_docs_to_gh-pages"]["steps"]
    validation = next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Validate stored notebook schemas"
    )
    build = next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Running the Sphinx to gh-pages Action"
    )
    assert validation < build
    step = steps[validation]
    assert step["run"] == "python devtools/scripts/validate_notebook_schemas.py"
    assert not step.get("continue-on-error", False)
    assert "if" not in step
