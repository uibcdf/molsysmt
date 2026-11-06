"""Distinguish unavailable verification from invalid molecular input."""

import subprocess
import sys

import pytest

import molsysmt as msm
from molsysmt._private.argdigest.argument.item import digest_item
from molsysmt._private.argdigest.argument.molecular_system import (
    digest_molecular_system,
)
from molsysmt._private.molecular_system_validation import (
    ValidationStatus,
    assess_molecular_system,
    validate_molecular_system_argument,
)
from molsysmt._private.smonitor import (
    ArgumentError,
    MolecularSystemVerificationError,
    NotSupportedFormError,
)


def test_operational_discovery_failure_is_undetermined_unverified_and_retains_cause(
    monkeypatch,
):
    original = RuntimeError("blocked uname")

    def blocked(_):
        raise original

    monkeypatch.setattr(msm.basic, "get_form", blocked)
    assessment = assess_molecular_system("existing.cif")
    assert assessment.validation is ValidationStatus.UNVERIFIED
    assert assessment.kind.value == "undetermined"
    assert assessment.cause is original
    assert "blocked uname" in assessment.reason
    with pytest.raises(MolecularSystemVerificationError) as caught:
        validate_molecular_system_argument("existing.cif", "molecular_system")
    assert caught.value.__cause__ is original


def test_operational_item_discovery_error_is_not_recast_as_argument_error(monkeypatch):
    original = RuntimeError("adapter initialization failed")

    def blocked(_):
        raise original

    monkeypatch.setattr(msm.basic, "get_form", blocked)
    with pytest.raises(RuntimeError) as caught:
        digest_item("existing.cif", form="file:cif")
    assert caught.value is original


def test_unsupported_item_keeps_argument_error_and_its_original_reason(monkeypatch):
    original = NotSupportedFormError(form=object, caller="test")

    def unsupported(_):
        raise original

    monkeypatch.setattr(msm.basic, "get_form", unsupported)
    with pytest.raises(ArgumentError) as caught:
        digest_item(object(), caller="test")
    assert caught.value.__cause__ is original


def test_valid_empty_append_target_is_not_sent_to_detectors(monkeypatch):
    calls = []

    def blocked(value):
        calls.append(value)
        raise RuntimeError("unrelated adapter cannot load")

    monkeypatch.setattr(msm.basic, "get_form", blocked)
    assert digest_item(None, caller="molsysmt.form.file_pdb.append_structures") is None
    assert calls == []


def test_existing_cross_form_append_targets_keep_their_contract(monkeypatch):
    target = object()
    monkeypatch.setattr(msm.basic, "get_form", lambda value: "molsysmt.Structures")
    assert (
        digest_item(
            target, form="file:trr", caller="molsysmt.form.file_trr.append_structures"
        )
        is target
    )


def test_regular_argument_validation_probes_once_and_preserves_operational_failure(
    monkeypatch,
):
    calls = []
    original = RuntimeError("reader initialization failed")

    def blocked(value):
        calls.append(value)
        raise original

    monkeypatch.setattr(msm.basic, "get_form", blocked)
    with pytest.raises(MolecularSystemVerificationError) as caught:
        digest_molecular_system("existing.cif", caller="molsysmt.basic.convert.convert")
    assert caught.value.__cause__ is original
    assert calls == ["existing.cif"]


def test_genuinely_unsupported_inputs_remain_invalid_argument_failures():
    value = object()
    assessment = assess_molecular_system(value)
    assert assessment.kind.value == "unsupported"
    assert assessment.validation is ValidationStatus.INVALID
    with pytest.raises(ArgumentError) as caught:
        validate_molecular_system_argument(value, "molecular_system", caller="test")
    assert isinstance(caught.value.__cause__, NotSupportedFormError)


def test_cold_declared_adapter_failure_survives_public_boundaries_and_explicit_retry(
    hp35_cif_file,
):
    script = r"""
from pathlib import Path
import sys
import depdigest.core.registry as registry_module
from depdigest import DeclaredRegistry
import molsysmt as msm
from molsysmt._private.smonitor import MolecularSystemVerificationError
from molsysmt.form import _dict_modules, current_dir

path = Path(sys.argv[1])
before = path.read_bytes()
original = RuntimeError("blocked uname")
actual_import = registry_module.import_module
def blocked(name, *args, **kwargs):
    if name == "molsysmt.form.file_cif":
        raise original
    return actual_import(name, *args, **kwargs)
registry_module.import_module = blocked
assert "file:cif" not in _dict_modules.loaded_keys()

# The published provider already retains the cause; host translation must keep it.
plain = DeclaredRegistry("molsysmt.form", current_dir,
    {"file:cif":"file_cif"}, attr_name="form_name", load_policy="adapter")
try:
    plain["file:cif"]
except KeyError as error:
    assert error.__cause__ is original
else:
    raise AssertionError("Injected adapter load was not reached")

def root_cause(error):
    while error.__cause__ is not None:
        error = error.__cause__
    return error
for action in (
    lambda: msm.get_form(path),
    lambda: msm.convert(path, to_form="mmcif.PdbxContainers.DataContainer"),
    lambda: getattr(msm.form, "file_cif"),
    lambda: _dict_modules.get("file:cif"),
):
    try:
        action()
    except MolecularSystemVerificationError as error:
        assert root_cause(error) is original
        assert "blocked uname" in str(error)
    else:
        raise AssertionError("A failed declared adapter was treated as available/absent")
assert path.read_bytes() == before
assert _dict_modules.get("no:such-form") is None
registry_module.import_module = actual_import
_dict_modules.retry("file:cif")
assert msm.get_form(path) == "file:cif"
result = msm.convert(path, get_missing_bonds=False)
assert result.topology.n_atoms > 0
assert result.structures.structure_id.tolist() == ["1"]
assert path.read_bytes() == before
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(hp35_cif_file)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
