"""Keep receiver provenance observation passive at cold initialization."""

import hashlib
import json
import subprocess
import sys
from types import ModuleType

from tests.molsysviewer_molsysmt import system_panel_jupyter as launcher


def test_snapshot_keeps_scientific_providers_unimported_in_a_fresh_process(tmp_path):
    output = tmp_path / "cold.json"
    code = """
import sys
from tests.molsysviewer_molsysmt.system_panel_jupyter import _record_molecular_imports
names = {'molsysmt', 'molsysmt._rust', 'molsysviewer',
         'molsysviewer_molsysmt', 'pyunitwizard', 'smonitor',
         'argdigest', 'depdigest'}
assert not names.intersection(sys.modules), 'The probe must start cold'
record = _record_molecular_imports(sys.argv[1])
assert set(record['modules']) == names
assert not names.intersection(sys.modules), 'The observer imported a provider'
assert all(row['loaded'] is False for row in record['modules'].values())
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(output)],
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert output.is_file()


def test_snapshot_records_loaded_file_bytes_without_lazy_attribute_access(
    tmp_path, monkeypatch
):
    origin = tmp_path / "provider.py"
    origin.write_text("# Deliberately loaded provider bytes.\n")
    module = ModuleType("depdigest")
    module.__file__ = str(origin)
    module.__version__ = "observed-test-version"

    def reject_lazy_access(name):
        raise AssertionError(f"Observation triggered a lazy attribute: {name}")

    module.__getattr__ = reject_lazy_access
    monkeypatch.setitem(sys.modules, "depdigest", module)
    output = tmp_path / "loaded.json"
    record = launcher._record_molecular_imports(output)
    assert json.loads(output.read_text()) == record
    assert record["modules"]["depdigest"] == {
        "loaded": True,
        "origin": str(origin.resolve()),
        "sha256": hashlib.sha256(origin.read_bytes()).hexdigest(),
        "module_version": "observed-test-version",
    }


def test_snapshot_reports_loaded_modules_without_file_metadata(tmp_path, monkeypatch):
    module = ModuleType("depdigest")
    monkeypatch.setitem(sys.modules, "depdigest", module)
    row = launcher._record_molecular_imports(tmp_path / "no-file.json")["modules"][
        "depdigest"
    ]
    assert row == {
        "loaded": True,
        "origin": None,
        "sha256": None,
        "module_version": None,
    }
