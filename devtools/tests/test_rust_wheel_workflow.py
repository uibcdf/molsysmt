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


def test_workflow_enforces_rust_quality_and_dependency_policy():
    workflow = _workflow()
    quality = workflow["jobs"]["rust-quality"]
    assert quality["runs-on"] == "ubuntu-24.04"

    text = WORKFLOW.read_text(encoding="utf-8")
    assert "cargo fmt --manifest-path rust/Cargo.toml --check" in text
    assert "cargo clippy --manifest-path rust/Cargo.toml" in text
    assert "cargo test --manifest-path rust/Cargo.toml" in text
    assert "EmbarkStudios/cargo-deny-action@v2" in text
    assert "manifest-path: rust/Cargo.toml" in text
    assert "--component rustfmt --component clippy" in text


def test_workflow_builds_a_wheel_from_the_validated_sdist():
    workflow = _workflow()
    sdist = workflow["jobs"]["source-distribution"]
    assert sdist["runs-on"] == "ubuntu-24.04"

    text = WORKFLOW.read_text(encoding="utf-8")
    assert "python -m build --sdist --outdir dist" in text
    assert "validate_rust_sdist.py dist" in text
    assert "python -m pip wheel dist/*.tar.gz --no-deps" in text
    assert "validate_rust_wheel.py sdist-wheelhouse" in text
    assert "name: molsysmt-source-distribution" in text


def test_workflow_validates_every_wheel_on_all_supported_pythons():
    workflow = _workflow()
    installed = workflow["jobs"]["test-full"]
    targets = installed["strategy"]["matrix"]["target"]
    assert {target["name"] for target in targets} == {
        "linux-x86_64",
        "linux-aarch64",
        "macos-x86_64",
        "macos-arm64",
        "windows-x86_64",
    }
    assert installed["strategy"]["matrix"]["python"] == ["3.11", "3.12", "3.13"]
    assert installed["needs"] == "build-full"

    pull_request = workflow["jobs"]["test-pull-request"]
    assert pull_request["strategy"]["matrix"]["python"] == [
        "3.11",
        "3.12",
        "3.13",
    ]
    assert pull_request["needs"] == "build-pull-request"


def test_workflow_validates_the_declared_numpy_floor():
    workflow = _workflow()
    floor = workflow["jobs"]["test-numpy-floor"]
    observed = {
        (entry["python"], entry["numpy"])
        for entry in floor["strategy"]["matrix"]["include"]
    }
    assert observed == {
        ("3.11", "numpy==1.26.4"),
        ("3.12", "numpy==1.26.4"),
        ("3.13", "numpy==2.1.3"),
    }
    assert floor["needs"] == "build-full"


def test_workflow_runs_installed_public_smoke_with_pinned_siblings():
    workflow = _workflow()
    smoke = workflow["jobs"]["test-public-smoke"]
    assert smoke["strategy"]["matrix"]["python"] == ["3.11", "3.12", "3.13"]
    assert smoke["needs"] == "build-full"

    text = WORKFLOW.read_text(encoding="utf-8")
    for commit in (
        "4fccafda4aa37b4c152d6b7d887ee665c7adc443",
        "df86d5d33de23724a819c2cb883198522a0c0c47",
        "0ff6656abfbd9f1ebc7575bc3f67fb263f52bf4f",
        "8df5bfee6bbb22bc2cd40aa744f04f1fc1c76ade",
        "28ebc4a9b624d81c1a09d27ffb91e96c63d2cfc4",
    ):
        assert commit in text
    assert "validate_installed_molsysmt.py" in text
    assert "python -m pip install --no-deps" in text
    assert '"anywidget>=0.9.15"' in text


def test_cibuildwheel_contract_is_single_cp311_abi3_build():
    config = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    cibw = config["tool"]["cibuildwheel"]
    assert cibw["build"] == "cp311-*"
    assert cibw["skip"] == "*-musllinux*"
    assert cibw["linux"]["manylinux-x86_64-image"] == "manylinux_2_28"
    assert cibw["linux"]["manylinux-aarch64-image"] == "manylinux_2_28"
    assert cibw["linux"]["environment"]["RUSTUP_TOOLCHAIN"] == "1.97.1"
    assert (
        cibw["macos"]["environment"]["MACOSX_DEPLOYMENT_TARGET"]
        == "11.0"
    )
    assert config["tool"]["distutils"]["bdist_wheel"]["py-limited-api"] == (
        "cp311"
    )
    assert "numpy>=1.26,<3" in config["project"]["dependencies"]
    assert config["tool"]["setuptools"]["packages"]["find"]["include"] == [
        "molsysmt*",
        "molsysviewer_molsysmt*",
    ]


def test_rust_toolchain_is_pinned():
    config = tomllib.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    assert config["toolchain"]["channel"] == "1.97.1"
    assert config["toolchain"]["profile"] == "minimal"
