"""Regression tests for the multiplatform Rust-wheel CI contract."""

from pathlib import Path

import tomllib
import yaml


REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "ci-rust-wheels.yaml"
PYPROJECT = REPO / "pyproject.toml"
TOOLCHAIN = REPO / "rust-toolchain.toml"


def _workflow():
    payload = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_workflow_builds_every_declared_platform_architecture():
    workflow = _workflow()
    full = workflow["jobs"]["build-full"]
    targets = full["strategy"]["matrix"]["target"]
    observed = {
        (target["name"], target["runner"], target["arch"])
        for target in targets
    }
    expected = {
        ("linux-x86_64", "ubuntu-24.04", "x86_64"),
        ("linux-aarch64", "ubuntu-24.04-arm", "aarch64"),
        ("macos-x86_64", "macos-15-intel", "x86_64"),
        ("macos-arm64", "macos-15", "arm64"),
        ("windows-x86_64", "windows-2022", "AMD64"),
    }
    assert observed == expected
    assert full["if"] == "github.event_name == 'workflow_dispatch'"

    pull_request = workflow["jobs"]["build-pull-request"]
    assert pull_request["if"] == "github.event_name == 'pull_request'"
    assert pull_request["runs-on"] == "ubuntu-24.04"


def test_workflow_builds_validates_and_uploads_without_publish_credentials():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "cibuildwheel==3.4.1" in text
    assert "validate_installed_rust_wheel.py" in text
    assert "actions/upload-artifact@v4" in text
    assert "persist-credentials: false" in text
    assert "pypi" not in text.lower()
    assert "anaconda" not in text.lower()


def test_cibuildwheel_contract_is_single_cp311_abi3_build():
    config = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    cibw = config["tool"]["cibuildwheel"]
    assert cibw["build"] == "cp311-*"
    assert cibw["skip"] == "*-musllinux*"
    assert cibw["linux"]["manylinux-x86_64-image"] == "manylinux_2_28"
    assert cibw["linux"]["manylinux-aarch64-image"] == "manylinux_2_28"
    assert (
        cibw["macos"]["environment"]["MACOSX_DEPLOYMENT_TARGET"]
        == "11.0"
    )
    assert config["tool"]["distutils"]["bdist_wheel"]["py-limited-api"] == (
        "cp311"
    )


def test_rust_toolchain_is_pinned():
    config = tomllib.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    assert config["toolchain"]["channel"] == "1.97.1"
    assert config["toolchain"]["profile"] == "minimal"
