"""Checking declared CTAB valence without inferring ordinary implicit hydrogen."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError, NotCompatibleConversionError
from tests.form.file_sdf.test_native_contract import V2000, V3000


def _payload(version, valence):
    if version == "V2000":
        lines = V2000.splitlines()
        # Isolated sodium has no drawn valence: only declared virtual H counts.
        lines[7] = (
            lines[7][:48] + f"{15 if valence == 0 else valence:3d}" + lines[7][51:]
        )
        return "\n".join(lines) + "\n"
    return V3000.replace(
        "80 Na 4 0 0 0 CHG=1",
        f"80 Na 4 0 0 0 CHG=1 VAL={-1 if valence == 0 else valence}",
    )


@pytest.mark.parametrize("version", ["V2000", "V3000"])
@pytest.mark.parametrize("valence", [0, 1, 4, 14])
def test_declared_valence_retains_virtual_counts_not_atoms(tmp_path, version, valence):
    source = tmp_path / "source.sdf"
    source.write_text(_payload(version, valence))
    native = msm.convert(source, to_form="molsysmt.MolSys")
    assert native.topology.n_atoms == 5
    assert native.structures.coordinates.shape == (1, 5, 3)
    for item in [source, native]:
        assert msm.get(item, selection=[3], n_explicit_hydrogens=True) == [valence]
        assert msm.get(item, selection=[3], n_implicit_hydrogens=True) == [0]
        assert msm.get(item, selection=[3], allows_implicit_hydrogens=True) == [False]
    # No field supplied for carbon: its ordinary implicit count stays unknown.
    assert pd.isna(
        native.chemical_states._states[0].atom_attributes.loc[0, "n_implicit_hydrogens"]
    )
    for output_version in ["V2000", "V3000"]:
        output = tmp_path / f"{output_version}.sdf"
        msm.convert(native, to_form=output, ctfile_version=output_version)
        assert msm.get(output, selection=[3], n_explicit_hydrogens=True) == [valence]
        assert msm.get(output, selection=[3], allows_implicit_hydrogens=True) == [False]
    h5msm = tmp_path / "state.h5msm"
    msm.convert(native, to_form=h5msm)
    restored = msm.convert(h5msm, to_form="molsysmt.MolSys")
    assert msm.get(restored, selection=[3], n_explicit_hydrogens=True) == [valence]
    subset = msm.extract(restored, selection=[3])
    assert msm.get(subset, n_explicit_hydrogens=True) == [valence]


@pytest.mark.parametrize("version", ["V2000", "V3000"])
def test_valence_subtracts_drawn_bond_orders_including_indexed_hydrogen(
    tmp_path, version
):
    if version == "V2000":
        lines = V2000.splitlines()
        lines[4] = lines[4][:48] + "  4" + lines[4][51:]
        payload = "\n".join(lines) + "\n"
    else:
        payload = V3000.replace("MASS=13", "MASS=13 VAL=4")
    source = tmp_path / "indexed.sdf"
    source.write_text(payload)
    native = msm.convert(source, to_form="molsysmt.MolSys")
    assert msm.get(native, selection=[0], n_explicit_hydrogens=True) == [0]
    inventory = msm.physchem.get_hydrogen_inventory(native, selection=[0])
    assert inventory["indexed_hydrogen_counts"].tolist() == [1]
    assert inventory["total_hydrogen_counts"].tolist() == [1]


@pytest.mark.parametrize("version", ["V2000", "V3000"])
def test_valence_does_not_guess_an_aromatic_or_conflicting_assignment(
    tmp_path, version
):
    if version == "V2000":
        lines = V2000.splitlines()
        lines[4] = lines[4][:48] + "  3" + lines[4][51:]
        payload = "\n".join(lines) + "\n"
    else:
        payload = V3000.replace("MASS=13", "MASS=13 VAL=3")
    source = tmp_path / "conflict.sdf"
    source.write_text(payload)
    with pytest.raises(FormatError, match="smaller than drawn"):
        msm.convert(source, to_form="molsysmt.MolSys")
    source.write_text(
        payload.replace("  1  2  2", "  1  2  4")
        if version == "V2000"
        else payload.replace("12 2 10 30", "12 4 10 30")
    )
    with pytest.raises(FormatError, match="aromatic and coordination"):
        msm.convert(source, to_form="molsysmt.MolSys")


def test_unencodable_hydrogen_metadata_remains_a_reported_loss(tmp_path):
    source = tmp_path / "source.sdf"
    source.write_text(V2000)
    native = msm.convert(source, to_form="molsysmt.MolSys")
    native.topology._set_chemical_state_atom_attribute(
        "n_implicit_hydrogens", [2, None, None, None, None]
    )
    native.topology._set_chemical_state_atom_attribute(
        "allows_implicit_hydrogens", [True, None, None, None, None]
    )
    output = tmp_path / "preserved.sdf"
    output.write_text("existing contents")
    report = msm.get_conversion_report(native, to_form=output)
    assert {"n_implicit_hydrogens", "allows_implicit_hydrogens"} <= {
        issue.attribute for issue in report.issues
    }
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(native, to_form=output, strict=True)
    assert output.read_text() == "existing contents"


@pytest.mark.parametrize("marker", ["", "   "])
def test_legacy_blank_marker_is_v2000_and_does_not_relax_unknown_versions(
    tmp_path, marker
):
    source = tmp_path / "legacy.sdf"
    source.write_text(V2000.replace(" V2000", marker))
    assert msm.get(source, n_atoms=True) == 5
    source.write_text(V2000.replace("V2000", "V4000"))
    with pytest.raises(FormatError, match="Unsupported CTAB version"):
        msm.convert(source, to_form="molsysmt.MolSys")
    source.write_text(V2000.replace("V2000", "V200"))
    with pytest.raises(FormatError, match="Unsupported CTAB version"):
        msm.convert(source, to_form="molsysmt.MolSys")


def test_declared_valence_compares_with_an_independent_reader(tmp_path):
    Chem = pytest.importorskip("rdkit.Chem")
    for version in ["V2000", "V3000"]:
        source = tmp_path / "source.sdf"
        source.write_text(_payload(version, 2))
        reference = Chem.SDMolSupplier(str(source), sanitize=False, removeHs=False)[0]
        assert reference is not None
        atom = reference.GetAtomWithIdx(3)
        assert atom.GetNoImplicit()
        assert atom.GetNumExplicitHs() == 2
        native = msm.convert(source, to_form="molsysmt.MolSys")
        output = tmp_path / "out.sdf"
        msm.convert(native, to_form=output, ctfile_version=version)
        restored = Chem.SDMolSupplier(str(output), sanitize=False, removeHs=False)[0]
        assert restored.GetAtomWithIdx(3).GetNumExplicitHs() == 2
        assert restored.GetAtomWithIdx(3).GetNoImplicit()


@pytest.mark.parametrize("version", ["V2000", "V3000"])
def test_optional_stereo_writer_retains_an_explicit_default_valence(tmp_path, version):
    pytest.importorskip("rdkit.Chem")
    # Methane with four virtual H, no indexed H, and no stereocenter. The
    # reference writer normally omits VAL=4 because carbon has default valence 4.
    source = tmp_path / "methane.sdf"
    source.write_text(
        "methane\n  Independent       2D\n\n"
        "  1  0  0  0  0  0  0  0  0  0999 V2000\n"
        "    0.0000    0.0000    0.0000 C   0  0  0  0  0  4  0  0  0  0  0  0\n"
        "M  END\n$$$$\n"
    )
    native = msm.convert(source, to_form="molsysmt.MolSys", stereo_engine="rdkit")
    output = tmp_path / "stereo.sdf"
    msm.convert(native, to_form=output, ctfile_version=version, stereo_engine="rdkit")
    restored = msm.convert(output, to_form="molsysmt.MolSys", stereo_engine="rdkit")
    assert msm.get(restored, n_explicit_hydrogens=True) == [4]
    assert msm.get(restored, n_implicit_hydrogens=True) == [0]
    assert msm.get(restored, allows_implicit_hydrogens=True) == [False]
    assert restored.topology.n_atoms == 1


def test_virtual_and_indexed_hydrogens_are_counted_once(tmp_path):
    source = tmp_path / "ammonium.sdf"
    source.write_text(
        "ammonium\n  Independent       3D\n\n"
        "  4  3  0  0  0  0  0  0  0  0999 V2000\n"
        "    0.0000    0.0000    0.0000 N   0  0  0  0  0  4  0  0  0  0  0  0\n"
        "    1.0000    0.0000    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0\n"
        "    0.0000    1.0000    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0\n"
        "    0.0000    0.0000    1.0000 H   0  0  0  0  0  0  0  0  0  0  0  0\n"
        "  1  2  1  0  0  0  0\n  1  3  1  0  0  0  0\n  1  4  1  0  0  0  0\n"
        "M  CHG  1   1   1\nM  END\n$$$$\n"
    )
    native = msm.convert(source, to_form="molsysmt.MolSys")
    inventory = msm.physchem.get_hydrogen_inventory(native, selection=[0])
    assert inventory["indexed_hydrogen_counts"].tolist() == [3]
    assert inventory["missing_hydrogen_counts"].tolist() == [1]
    assert inventory["total_hydrogen_counts"].tolist() == [4]
    assert native.topology.n_atoms == 4
    output = tmp_path / "virtual.sdf"
    msm.convert(native, to_form=output, ctfile_version="V3000")
    assert msm.get(output, selection=[0], n_explicit_hydrogens=True) == [1]


@pytest.mark.parametrize(
    "version,bad_code", [("V2000", -1), ("V2000", 16), ("V3000", -2), ("V3000", 15)]
)
def test_out_of_range_valence_is_not_a_default(tmp_path, version, bad_code):
    payload = _payload(version, 1)
    if version == "V2000":
        lines = payload.splitlines()
        lines[7] = lines[7][:48] + f"{bad_code:3d}" + lines[7][51:]
        payload = "\n".join(lines) + "\n"
    else:
        payload = payload.replace("VAL=1", f"VAL={bad_code}")
    source = tmp_path / "bad.sdf"
    source.write_text(payload)
    with pytest.raises(FormatError, match="valence"):
        msm.convert(source, to_form="molsysmt.MolSys")
