"""Distinguish imported package versions from unrelated installation metadata.

Bootstrap controls execute the actual root initializer in fresh Python processes.
Small diagnostics/unit stubs isolate version selection; real scientific and
provider-policy integration is exercised separately on the complete package.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def bootstrap(
    tmp_path,
    *,
    embedded=None,
    own_metadata=False,
    record=True,
    metadata=True,
    broken_version=False,
):
    active = tmp_path / "active"
    package = active / "molsysmt"
    package.mkdir(parents=True)
    (package / "__init__.py").write_bytes((ROOT / "molsysmt/__init__.py").read_bytes())
    resolver = ROOT / "molsysmt/_runtime_version.py"
    if resolver.exists():
        (package / resolver.name).write_bytes(resolver.read_bytes())
    (package / "_pyunitwizard.py").write_text("")
    (package / "_private/smonitor").mkdir(parents=True)
    (package / "_private/__init__.py").write_text("")
    (package / "_private/smonitor/__init__.py").write_text(
        "PACKAGE_ROOT = 'isolated-bootstrap'\n"
    )
    (active / "smonitor").mkdir()
    (active / "smonitor/__init__.py").write_text("")
    (active / "smonitor/integrations.py").write_text(
        "def ensure_configured(root):\n    pass\n"
    )
    if embedded is not None:
        (package / "_version.py").write_text(f"__version__ = {embedded!r}\n")
    if broken_version:
        (package / "_version.py").write_text(
            "import missing_generated_version_dependency\n"
        )
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    metadata_root = active if own_metadata else foreign
    if metadata:
        info = metadata_root / "molsysmt-9.8.7.dist-info"
        info.mkdir()
        (info / "METADATA").write_text(
            "Metadata-Version: 2.1\nName: molsysmt\nVersion: 9.8.7\n"
        )
        if record:
            (info / "RECORD").write_text("molsysmt/__init__.py,,\n")
    script = """
import json, subprocess
def no_process(*args, **kwargs):
    raise AssertionError('Version bootstrap must not start a process')
subprocess.run = subprocess.check_output = subprocess.Popen = no_process
import molsysmt
print(json.dumps({'version': molsysmt.__version__, 'origin': molsysmt.__file__}))
"""
    result = subprocess.run(
        [sys.executable, "-S", "-c", script],
        cwd=tmp_path,
        env={
            **os.environ,
            "PYTHONPATH": os.pathsep.join(map(str, [active, foreign])),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        text=True,
        capture_output=True,
        timeout=20,
    )
    if broken_version:
        return result
    assert result.returncode == 0, result.stdout + result.stderr
    observed = json.loads(result.stdout)
    assert Path(observed["origin"]) == package / "__init__.py"
    return observed["version"]


def test_source_overlay_does_not_borrow_another_installation_version(tmp_path):
    assert bootstrap(tmp_path) == "0+unknown"


def test_embedded_package_version_precedes_foreign_distribution(tmp_path):
    assert bootstrap(tmp_path, embedded="1.2.3+package") == "1.2.3+package"


def test_embedded_package_version_precedes_matching_metadata(tmp_path):
    assert (
        bootstrap(tmp_path, embedded="1.2.3+package", own_metadata=True)
        == "1.2.3+package"
    )


def test_owned_legacy_distribution_can_supply_a_missing_build_stamp(tmp_path):
    assert bootstrap(tmp_path, own_metadata=True) == "9.8.7"


def test_unrecorded_metadata_does_not_prove_package_ownership(tmp_path):
    assert bootstrap(tmp_path, own_metadata=True, record=False) == "0+unknown"


def test_no_build_or_installation_metadata_is_explicitly_unknown(tmp_path):
    assert bootstrap(tmp_path, metadata=False) == "0+unknown"


def test_embedded_version_works_without_distribution_metadata(tmp_path):
    assert (
        bootstrap(tmp_path, embedded="1.2.3+package", metadata=False) == "1.2.3+package"
    )


def test_broken_embedded_module_is_not_silently_relabelled(tmp_path):
    result = bootstrap(tmp_path, broken_version=True)
    assert result.returncode != 0
    assert "missing_generated_version_dependency" in result.stderr


@pytest.mark.parametrize("embedded", [17, False, "", "   "])
def test_invalid_embedded_versions_are_explicitly_unknown(tmp_path, embedded):
    assert bootstrap(tmp_path, embedded=embedded) == "0+unknown"


def test_scientific_results_use_the_cached_imported_package_version(monkeypatch):
    from importlib import metadata

    import molsysmt as msm

    # Different distribution metadata must not replace the actual bootstrap
    # decision at each calculation; existing readers preserve producer strings.
    expected = msm.__version__
    original = metadata.version
    monkeypatch.setattr(
        metadata,
        "version",
        lambda name: "9.8.7+unrelated" if name == "molsysmt" else original(name),
    )
    distances = msm.pyunitwizard.quantity([[0.0, 1.0], [1.0, 0.0]], "nm")
    result = msm.structure.get_distance_clusters(distances, "1 nm")
    assert result["software"]["molsysmt"] == expected
    software = [
        item
        for item in result["attribution"]["items"]
        if item["id"] == f"software:molsysmt:{expected}"
    ]
    assert len(software) == 1 and software[0]["version"] == expected
