"""Regression tests for the single-artifact Conda ABI3 experiment."""

from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "test_conda_abi3.yaml"
RECIPE = REPO / "devtools" / "conda-build" / "meta.yaml"


def _workflow():
    payload = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_experiment_builds_all_native_release_platforms():
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
    assert job["strategy"]["matrix"] == (
        "${{ fromJSON(needs.prepare.outputs.matrix) }}"
    )
    assert job["strategy"]["fail-fast"] is False
    assert "continue-on-error" not in job


def test_experiment_builds_once_and_tests_one_artifact_three_times():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "action-build-and-upload-conda-packages@v2.0.3" in text
    assert 'MOLSYSMT_CONDA_ABI3: "true"' in text
    assert "--exclusive-config-file conda_build_config_abi3.yaml" in text
    assert '[[ "${#built_paths[@]}" -ne 1 ]]' in text
    assert "for python_version in 3.11 3.12 3.13" in text
    assert "validate_conda_abi3_artifact.py" in text
    assert "validate_installed_rust_extension.py" in text
    assert "upload: false" in text


def test_recipe_uses_the_cep20_abi3_contract_conditionally():
    text = RECIPE.read_text(encoding="utf-8")

    assert "python_version_independent: true" in text
    assert 'string: "pyabi3h{{ PKG_HASH }}_{{ PKG_BUILDNUM }}"' in text
    assert "python-abi3 3.11.*" in text
    assert "python >=3.11,<3.14" in text
    assert "MOLSYSMT_CONDA_ABI3" in text
    assert "python 3.12.14 *_1_cpython" in text
