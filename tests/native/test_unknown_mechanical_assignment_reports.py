"""Keep unknown stored evidence distinct from a usable scientific assignment."""

from copy import deepcopy

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from tests.native.test_prepared_system_checkpoint import _prepared


@pytest.mark.parametrize("operation", ["project", "export"])
@pytest.mark.parametrize("field", ["partial_charge_assignment", "atom_type_assignment"])
@pytest.mark.parametrize("damage", ["future_schema", "empty", "missing_index"])
def test_unknown_reports_roundtrip_but_refuse_projection_and_scientific_export(
    tmp_path, field, damage, operation
):
    source = _prepared("complete")
    report = deepcopy(getattr(source.molecular_mechanics, field))
    if damage == "future_schema":
        report["schema"] = report["schema"].split("@")[0] + "@999"
    elif damage == "empty":
        report = {}
    else:
        del report["chemical_state_index"]
    setattr(source.molecular_mechanics, field, report)
    path = tmp_path / "evidence.h5msm"
    msm.h5msm.write(source, path, format_version="0.6")
    original = path.read_bytes()
    restored = msm.h5msm.read(path)
    # Full copies transport evidence; they do not interpret or repair it.
    copied = msm.copy(restored)
    copied_report = getattr(copied.molecular_mechanics, field)
    if report:
        assert copied_report["schema"] == report["schema"]
    else:
        assert copied_report == {}
    with pytest.raises(StructuralInconsistencyError, match="report|schema"):
        if operation == "project":
            msm.extract(restored, selection=[1])
        else:
            msm.convert(
                restored,
                to_form="string:pdbqt_text",
                typing_scheme="autodock4",
                structure_indices=[0],
            )
    assert path.read_bytes() == original
