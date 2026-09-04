"""Regression tests for the experimental Rattler Build workflow."""

from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "test_conda_rattler.yaml"
RECIPE = REPO / "devtools" / "rattler-build" / "recipe.yaml"


def _workflow():
    payload = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_rattler_experiment_covers_each_native_release_platform():
    workflow = _workflow()
    prepare = workflow["jobs"]["prepare"]
    job = workflow["jobs"]["build-and-test"]
    matrix_script = prepare["steps"][0]["run"]

    for platform, runner in {
        "linux-64": "ubuntu-24.04",
        "linux-aarch64": "ubuntu-24.04-arm",
        "osx-64": "macos-15-intel",
        "osx-arm64": "macos-15",
        "win-64": "windows-2025",
    }.items():
        assert f'"platform":"{platform}","runner":"{runner}"' in matrix_script
    assert job["needs"] == "prepare"
    assert job["strategy"]["fail-fast"] is False


def test_rattler_experiment_builds_and_tests_one_exact_artifact():
    text = WORKFLOW.read_text(encoding="utf-8")
    workflow = _workflow()
    lto_input = workflow[True]["workflow_dispatch"]["inputs"]["lto"]

    assert lto_input["options"] == ["true", "thin"]
    assert "rattler-build=0.72.2" in text
    assert "--compression-threads 4" in text
    assert "--package-format conda" in text
    assert '[[ "${#packages[@]}" -ne 1 ]]' in text
    assert "for python_version in 3.11 3.12 3.13" in text
    assert "validate_conda_abi3_artifact.py" in text
    assert "validate_installed_rust_extension.py" in text
    assert "--no-deps" in text


def test_rattler_recipe_declares_one_platform_abi3_artifact():
    text = RECIPE.read_text(encoding="utf-8")

    assert "version_independent: true" in text
    assert "string: pyabi3h${{ hash }}_${{ build_number }}" in text
    assert "python-abi3 3.11.*" in text
    assert "python >=3.11,<3.14" in text
    assert "use_gitignore: true" in text
    assert "python_abi" not in text
