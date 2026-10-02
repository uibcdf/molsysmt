"""Testing public preflight without writes or source mutation."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, FormatError
from molsysmt.native import Structures


def test_public_exports_and_exhaustive_structures_audit():
    molsys = Structures()
    molsys.append(coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm"))
    before = molsys.coordinates.copy()
    assert msm.get_conversion_report is msm.basic.get_conversion_report
    report = msm.get_conversion_report(
        molsys, to_form="molsysmt.StructuresDict", structure_indices=[1]
    )
    assert isinstance(report, msm.ConversionReport)
    assert report.is_exhaustive and not report.is_lossy
    _, converted_report = msm.convert(
        molsys,
        to_form="molsysmt.StructuresDict",
        structure_indices=[1],
        return_report=True,
    )
    assert report == converted_report
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.coordinates),
        msm.pyunitwizard.get_value(before),
    )


@pytest.mark.parametrize("existing", [False, True])
def test_preflight_never_creates_or_overwrites_destination(tmp_path, existing):
    molsys = msm.convert(msm.systems["caffeine"]["caffeine.sdf"])
    before_atoms = molsys.topology.atoms.copy(deep=True)
    before_bonds = molsys.topology.bonds.copy(deep=True)
    before_coordinates = molsys.structures.coordinates.copy()
    target = tmp_path / "audit.sdf"
    if existing:
        target.write_bytes(b"preserve this destination")
    report = msm.get_conversion_report(molsys, to_form=target, selection=[4, 0, 2])
    assert report.to_form == "file:sdf" and not report.is_exhaustive
    assert target.exists() is existing
    if existing:
        assert target.read_bytes() == b"preserve this destination"
    assert molsys.topology.atoms.equals(before_atoms)
    assert molsys.topology.bonds.equals(before_bonds)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.structures.coordinates),
        msm.pyunitwizard.get_value(before_coordinates),
    )
    _, converted_report = msm.convert(
        molsys, to_form=tmp_path / "actual.sdf", selection=[4, 0, 2], return_report=True
    )
    assert report == converted_report


def test_source_file_metadata_can_be_inspected_without_authorizing_discard(tmp_path):
    source = tmp_path / "properties.sdf"
    original = Path(msm.systems["caffeine"]["caffeine.sdf"]).read_text()
    source.write_text(original.replace("$$$$", ">  <LABEL>\nsample\n\n$$$$"))
    before = source.read_bytes()
    report = msm.get_conversion_report(source)
    assert report.is_lossy and not report.is_exhaustive
    assert "sdf_properties" in {issue.attribute for issue in report.issues}
    assert source.read_bytes() == before
    with pytest.raises(FormatError, match="property blocks"):
        msm.convert(source)
    _, converted_report = msm.convert(
        source, discard_properties=True, return_report=True
    )
    assert report == converted_report


def test_target_lists_and_single_source_compositions_preserve_order(tmp_path):
    molsys = msm.convert(msm.systems["caffeine"]["caffeine.sdf"])
    targets = ["molsysmt.Topology", tmp_path / "target.sdf", "molsysmt.Structures"]
    reports = msm.get_conversion_report([molsys], to_form=targets)
    assert [r.to_form for r in reports] == [
        "molsysmt.Topology",
        "file:sdf",
        "molsysmt.Structures",
    ]
    assert not targets[1].exists()
    assert msm.get_conversion_report(molsys, to_form=[]) == []
    assert msm.get_conversion_report(
        molsys, skip_digestion=True
    ) == msm.get_conversion_report(molsys)


def test_multiple_source_forms_use_same_conservative_audit_as_convert():
    molsys = msm.convert(msm.systems["caffeine"]["caffeine.sdf"])
    sources = [molsys.topology, molsys.structures]
    report = msm.get_conversion_report(sources)
    assert not report.is_exhaustive
    _, converted_report = msm.convert(sources, return_report=True)
    assert report == converted_report


@pytest.mark.parametrize("target", [None, "not:a:form", [["molsysmt.MolSys"]]])
def test_invalid_targets_are_rejected(target):
    with pytest.raises(ArgumentError):
        msm.get_conversion_report(Structures(), to_form=target)


@pytest.mark.parametrize("indices", [[-1], [2], [0.5], np.array([[0]])])
def test_invalid_structure_indices_are_rejected(indices):
    molsys = Structures()
    molsys.append(coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm"))
    with pytest.raises(ArgumentError):
        msm.get_conversion_report(molsys, structure_indices=indices)
