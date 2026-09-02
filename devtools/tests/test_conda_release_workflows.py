"""Regression tests for native Conda staging and release publication."""

from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[2]
RECIPE = REPO / "devtools" / "conda-build" / "meta.yaml"
PUBLISH_WORKFLOW = (
    REPO / ".github" / "workflows" / "build_and_upload_conda_packages.yaml"
)
STAGING_WORKFLOW = REPO / ".github" / "workflows" / "validate_conda_staging.yaml"

EXPECTED_TARGETS = {
    ("linux-64", "ubuntu-24.04"),
    ("linux-aarch64", "ubuntu-24.04-arm"),
    ("osx-64", "macos-15-intel"),
    ("osx-arm64", "macos-15"),
    ("win-64", "windows-2025"),
}


def _workflow(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _targets(job: dict) -> set[tuple[str, str]]:
    return {
        (target["platform"], target["runner"])
        for target in job["strategy"]["matrix"]["target"]
    }


def _step(job: dict, name: str) -> dict:
    return next(step for step in job["steps"] if step.get("name") == name)


def test_recipe_builds_and_tests_the_native_extension():
    recipe = RECIPE.read_text(encoding="utf-8")
    variant_config = (
        REPO / "devtools" / "conda-build" / "conda_build_config.yaml"
    ).read_text(encoding="utf-8")

    assert (
        "  - {{ compiler('c') }}  # [linux]\n"
        "  - {{ compiler('rust') }}\n"
        "  host:" in recipe
    )
    assert "rust_compiler_version:\n- 1.97.1" in variant_config
    assert "MOLSYSMT_CONDA_BUILD_NUMBER" in recipe
    assert "  - setuptools-rust >=1.10" in recipe
    assert "test:\n  imports:\n  - molsysmt\n  - molsysmt._rust" in recipe
    assert "PKG_VERSION" in recipe
    assert (REPO / "devtools" / "conda-build" / "bld.bat").is_file()
    assert "--no-build-isolation" in (
        REPO / "devtools" / "conda-build" / "build.sh"
    ).read_text(encoding="utf-8")


def test_publish_workflow_uses_native_runners_and_atomic_upload():
    workflow = _workflow(PUBLISH_WORKFLOW)
    prepare = workflow["jobs"]["prepare"]
    build = workflow["jobs"]["build"]
    publish = workflow["jobs"]["publish"]

    assert build["needs"] == "prepare"
    assert _targets(build) == EXPECTED_TARGETS
    assert build["strategy"]["matrix"]["python"] == ["3.11", "3.12", "3.13"]
    assert publish["needs"] == "build"

    validate_identity = _step(
        prepare, "Validate staging inputs or the release tag"
    )["run"]
    assert "^[0-9a-f]{40}$" in validate_identity
    assert validate_identity.count("^[0-9]+\\.[0-9]+\\.[0-9]+$") == 2

    staging_build = _step(
        build, "Build the staging package without its circular runtime test"
    )
    release_build = _step(build, "Build and test the release package")
    upload = _step(publish, "Upload to Anaconda.org")
    assert staging_build["if"] == "github.event_name == 'workflow_dispatch'"
    assert staging_build["env"]["MOLSYSMT_CONDA_BUILD_NUMBER"] == 0
    assert "--no-test" in staging_build["run"]
    assert release_build["if"] == "github.event_name == 'release'"
    assert release_build["env"]["MOLSYSMT_CONDA_BUILD_NUMBER"] == 1
    assert "--no-test" not in release_build["run"]
    assert upload["uses"] == "anaconda/actions/upload-package@v0"
    assert upload["with"]["labels"] == (
        "${{ github.event_name == 'workflow_dispatch' && 'staging' || 'main' }}"
    )

    text = PUBLISH_WORKFLOW.read_text(encoding="utf-8")
    assert "uibcdf/action-build-and-upload-conda-packages" not in text
    assert "platform_linux-64" not in text


def test_staging_workflow_installs_the_pair_on_the_native_matrix():
    workflow = _workflow(STAGING_WORKFLOW)
    prepare = workflow["jobs"]["prepare"]
    validate = workflow["jobs"]["validate"]

    assert validate["needs"] == "prepare"
    assert _targets(validate) == EXPECTED_TARGETS
    assert validate["strategy"]["matrix"]["python"] == ["3.11", "3.12", "3.13"]

    version_gate = _step(prepare, "Require stable package versions")["run"]
    assert version_gate.count("^[0-9]+\\.[0-9]+\\.[0-9]+$") == 2

    install = _step(validate, "Install the staged package pair")["with"]
    assert "uibcdf/label/staging" in install["condarc"]
    assert "molsysmt=${{ inputs.molsysmt_version }}" in install["create-args"]
    assert "molsysviewer=${{ inputs.molsysviewer_version }}" in install["create-args"]

    validation = _step(
        validate, "Validate versions, provenance, native code, and viewer resources"
    )["run"]
    assert "validate_conda_staging.py" in validation
    assert "--molsysmt-version" in validation
    assert "--molsysviewer-version" in validation

    environment_record = _step(validate, "Record the exact environment")["run"]
    assert environment_record.startswith("conda list --explicit")
