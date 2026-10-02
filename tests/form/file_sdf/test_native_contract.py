"""Checking explicit native SDF chemistry with independent inputs and readers."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    ArgumentError,
    FormatError,
    NotCompatibleConversionError,
)
from molsysmt.native import MolSys

# Independent hand-written isotope-labelled sodium formate: no toolkit is needed
# to establish the atom order, coordinates, graph, isotope or charge expectations.
V2000 = """labelled formate
  Independent       2D

  5  3  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    4.0000    0.0000    0.0000 Na  0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    1.0000    0.0000 D   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0  0  0  0
  1  3  1  0  0  0  0
  1  5  1  0  0  0  0
M  CHG  2   3  -1   4   1
M  ISO  2   1  13   5   2
M  END
$$$$
"""

V3000 = """labelled formate
  Independent       2D

  0  0  0     0  0            999 V3000
M  V30 BEGIN CTAB
M  V30 COUNTS 5 3 0 0 0
M  V30 BEGIN ATOM
M  V30 10 C 0 0 0 0 -
M  V30 MASS=13
M  V30 30 O 1.2 0 0 0
M  V30 50 O -1.2 0 0 0 CHG=-1
M  V30 80 Na 4 0 0 0 CHG=1
M  V30 100 H 0 1 0 0 MASS=2
M  V30 END ATOM
M  V30 BEGIN BOND
M  V30 12 2 10 30
M  V30 14 1 10 50
M  V30 16 1 10 100
M  V30 END BOND
M  V30 END CTAB
M  END
$$$$
"""


@pytest.fixture(params=[V2000, V3000], ids=["V2000", "V3000"])
def source(tmp_path, request):
    path = tmp_path / "formate.sdf"
    path.write_text(request.param)
    return path


def test_public_native_domains_and_direct_getters(source):
    assert msm.get_form(source) == "file:sdf"
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert isinstance(molsys, MolSys)
    assert molsys.topology.n_atoms == 5
    assert molsys.topology.n_bonds == 3
    assert molsys.topology.n_groups == 0
    assert molsys.topology.n_components == 2
    assert molsys.topology.atoms.atom_type.tolist() == ["C", "O", "O", "Na", "H"]
    assert all(isinstance(i, str) for i in molsys.topology.atoms.atom_id)
    assert msm.get(source, formal_charge=True) == [0, 0, -1, 1, 0]
    isotope = molsys.topology.atoms.isotope
    assert isotope.iloc[0] == 13 and isotope.iloc[4] == 2
    assert isotope.iloc[1:4].isna().all()
    pairs = msm.get(source, element="bond", bonded_atom_pairs=True)
    np.testing.assert_array_equal(pairs, [[0, 1], [0, 2], [0, 4]])
    np.testing.assert_array_equal(
        msm.get(source, element="bond", bond_order=True), [2, 1, 1]
    )
    coordinates = msm.get(source, coordinates=True)
    assert coordinates.shape == (1, 5, 3)
    assert msm.pyunitwizard.check(coordinates, unit="nm")
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(coordinates, to_unit="nm")[0, :, 0],
        [0, 0.12, -0.12, 0.4, 0],
    )
    assert not msm.has_attribute(source, "partial_charge")
    assert not msm.has_attribute(source, "n_implicit_hydrogens")
    assert not msm.has_attribute(source, "atom_is_aromatic")


@pytest.mark.parametrize("version", ["V2000", "V3000"])
def test_round_trip_preserves_explicit_chemistry_and_coordinates(
    source, tmp_path, version
):
    before = msm.convert(source, to_form="molsysmt.MolSys")
    target = tmp_path / "roundtrip.sdf"
    assert msm.convert(before, to_form=target, ctfile_version=version) == target
    after = msm.convert(target, to_form="molsysmt.MolSys")
    assert (
        after.topology.atoms.atom_type.tolist()
        == before.topology.atoms.atom_type.tolist()
    )
    assert after.topology.atoms.isotope.equals(before.topology.atoms.isotope)
    assert msm.get(after, formal_charge=True) == [0, 0, -1, 1, 0]
    np.testing.assert_array_equal(
        msm.get(after, element="bond", bond_order=True), [2, 1, 1]
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(after.structures.coordinates, to_unit="angstrom"),
        msm.pyunitwizard.get_value(before.structures.coordinates, to_unit="angstrom"),
        atol=5e-5,
    )


def test_selection_remaps_bonds_in_native_extraction_order_without_mutation(
    source, tmp_path
):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    original_ids = molsys.topology.atoms.atom_id.tolist()
    target = tmp_path / "selection.sdf"
    msm.convert(molsys, selection=[4, 0, 2], to_form=target)
    after = msm.convert(target, to_form="molsysmt.MolSys")
    assert after.topology.atoms.atom_type.tolist() == ["C", "O", "H"]
    assert after.topology.atoms.atom_id.tolist() == ["1", "2", "3"]
    np.testing.assert_array_equal(
        msm.get(after, element="bond", bonded_atom_pairs=True), [[0, 1], [0, 2]]
    )
    assert msm.get(after, formal_charge=True) == [0, -1, 0]
    assert molsys.topology.atoms.atom_id.tolist() == original_ids
    direct = msm.convert(source, selection=[4, 0, 2], to_form="molsysmt.MolSys")
    assert direct.topology.atoms.atom_id.tolist() == [
        original_ids[i] for i in [0, 2, 4]
    ]


def test_properties_require_explicit_discard_and_strict_conversion_rejects(
    source, tmp_path
):
    text = source.read_text().replace(
        "$$$$", ">  <SAMPLE>\nfirst line\nsecond line\n\n$$$$"
    )
    source.write_text(text)
    with pytest.raises(FormatError, match="property blocks"):
        msm.convert(source, to_form="molsysmt.MolSys")
    molsys, report = msm.convert(
        source, to_form="molsysmt.MolSys", discard_properties=True, return_report=True
    )
    assert molsys.topology.n_atoms == 5
    assert report.is_lossy and not report.is_exhaustive
    assert "sdf_properties" in {issue.attribute for issue in report.issues}
    assert "source_metadata" in report.audited_scopes
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(
            source, to_form="molsysmt.MolSys", discard_properties=True, strict=True
        )
    copied = tmp_path / "copied.sdf"
    msm.convert(source, to_form=copied)
    assert copied.read_bytes() == source.read_bytes()


def test_multiple_records_are_rejected_without_taking_first(source):
    source.write_text(source.read_text() * 2)
    with pytest.raises(FormatError, match="Multiple SDF records"):
        msm.convert(source, to_form="molsysmt.MolSys")


def test_frame_selection_rejects_invalid_indices_and_unselected_multiple_frames(
    source, tmp_path
):
    with pytest.raises(Exception) as error:
        msm.convert(source, structure_indices=[1], to_form="molsysmt.MolSys")
    assert "structure" in str(error.value).lower()
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    molsys.structures.append(
        coordinates=molsys.structures.coordinates, skip_digestion=True
    )
    target = tmp_path / "frames.sdf"
    target.write_text("previous valid file")
    with pytest.raises(FormatError, match="exactly one selected structure"):
        msm.convert(molsys, to_form=target)
    assert target.read_text() == "previous valid file"
    msm.convert(molsys, structure_indices=[1], to_form=target)
    assert msm.convert(target, to_form="molsysmt.MolSys").structures.n_structures == 1


@pytest.mark.parametrize(
    "replacement",
    [
        ("  1  2  2  0", "  1  2  2  3"),
        ("  1  2  2  0", "  1  2  5  0"),
        ("  1  2  2  0", "  1 99  2  0"),
        ("  1  3  1  0", "  1  2  1  0"),
        (" C   0  0", " *   0  0"),
        ("M  END", "M  ALS  1  1 F C\nM  END"),
        ("M  END\n", ""),
        ("$$$$", ""),
        ("    1.2000", "       nan"),
        ("M  CHG  2   3  -1   4   1", "M  CHG  2   3  -1"),
    ],
)
def test_malformed_and_unsupported_v2000_are_rejected(tmp_path, replacement):
    source = tmp_path / "invalid.sdf"
    source.write_text(V2000.replace(*replacement))
    with pytest.raises(FormatError):
        msm.convert(source, to_form="molsysmt.MolSys")


@pytest.mark.parametrize(
    "replacement",
    [
        ("CHG=-1", "CFG=1"),
        ("CHG=-1", "HCOUNT=2"),
        ("10 C", "30 C"),
        ("12 2 10 30", "12 2 10 999"),
        ("12 2 10 30", "12 2 10 30 CFG=1"),
        ("END CTAB", "BEGIN SGROUP\nM  V30 END SGROUP\nM  V30 END CTAB"),
        ("COUNTS 5 3 0 0 0", "COUNTS 6 3 0 0 0"),
    ],
)
def test_unsupported_v3000_is_rejected(tmp_path, replacement):
    source = tmp_path / "invalid.sdf"
    source.write_text(V3000.replace(*replacement))
    with pytest.raises(FormatError):
        msm.convert(source, to_form="molsysmt.MolSys")


def test_v3000_accepts_explicit_inactive_defaults_without_guessing_chemistry(tmp_path):
    source = tmp_path / "defaults.sdf"
    atom_defaults = (
        " CFG=0 VAL=0 HCOUNT=0 STBOX=0 INVRET=0 EXACHG=0 SUBST=0 UNSAT=0 RBCNT=0"
    )
    source.write_text(
        V3000.replace("30 O 1.2 0 0 0", "30 O 1.2 0 0 0" + atom_defaults).replace(
            "12 2 10 30", "12 2 10 30 CFG=0 TOPO=0 RXCTR=0 STBOX=0"
        )
    )
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert molsys.topology.n_bonds == 3
    assert msm.get(molsys, formal_charge=True) == [0, 0, -1, 1, 0]
    assert not msm.has_attribute(molsys, "n_implicit_hydrogens")
    assert not msm.has_attribute(molsys, "atom_stereochemistry")


@pytest.mark.parametrize(
    "property", ["VAL=-1", "CFG=3", "HCOUNT=-1", "UNKNOWN=0", "CFG=0 CFG=0", "VAL=bad"]
)
def test_v3000_default_support_does_not_swallow_active_unknown_or_repeated_atom_fields(
    tmp_path, property
):
    source = tmp_path / "invalid-default.sdf"
    source.write_text(V3000.replace("30 O 1.2 0 0 0", "30 O 1.2 0 0 0 " + property))
    with pytest.raises(FormatError):
        msm.convert(source, to_form="molsysmt.MolSys")


@pytest.mark.parametrize(
    "property",
    ["CFG=2", "TOPO=1", "RXCTR=4", "UNKNOWN=0", "STBOX=0 STBOX=0", "DISP=COORD"],
)
def test_v3000_default_support_does_not_swallow_active_unknown_or_repeated_bond_fields(
    tmp_path, property
):
    source = tmp_path / "invalid-default.sdf"
    source.write_text(V3000.replace("12 2 10 30", "12 2 10 30 " + property))
    with pytest.raises(FormatError):
        msm.convert(source, to_form="molsysmt.MolSys")


def test_v2000_coordination_extension_requires_supported_v3000_syntax(tmp_path):
    source = tmp_path / "nonstandard.sdf"
    source.write_text(V2000.replace("  1  2  2  0", "  1  2  9  0"))
    with pytest.raises(FormatError, match="require.*V3000"):
        msm.convert(source, to_form="molsysmt.MolSys")


def test_native_reader_writer_work_when_rdkit_import_is_blocked(tmp_path):
    target = tmp_path / "without-rdkit.sdf"
    script = r"""
import importlib.abc
import sys
class NoRDKit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'rdkit' or fullname.startswith('rdkit.'):
            raise ImportError('RDKit deliberately unavailable')
sys.meta_path.insert(0, NoRDKit())
import molsysmt as msm
molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='molsysmt.MolSys')
assert molsys.topology.n_atoms == 24
msm.convert(molsys, to_form=sys.argv[1], ctfile_version='V3000')
assert msm.convert(sys.argv[1], to_form='molsysmt.MolSys').topology.n_bonds == 25
assert not any(name == 'rdkit' or name.startswith('rdkit.') for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(target)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(
    importlib.util.find_spec("rdkit") is None, reason="optional RDKit reference reader"
)
def test_against_independent_rdkit_reader(source, tmp_path):
    from rdkit import Chem

    reference = Chem.SDMolSupplier(
        str(source), sanitize=False, removeHs=False, strictParsing=True
    )[0]
    assert reference is not None
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert molsys.topology.atoms.atom_type.tolist() == [
        atom.GetSymbol() for atom in reference.GetAtoms()
    ]
    assert msm.get(molsys, formal_charge=True) == [
        atom.GetFormalCharge() for atom in reference.GetAtoms()
    ]
    assert molsys.topology.atoms.isotope.fillna(0).tolist() == [
        atom.GetIsotope() for atom in reference.GetAtoms()
    ]
    output = tmp_path / "independent.sdf"
    msm.convert(molsys, to_form=output, ctfile_version="V3000")
    recovered = Chem.SDMolSupplier(
        str(output), sanitize=False, removeHs=False, strictParsing=True
    )[0]
    assert recovered is not None
    assert recovered.GetNumAtoms() == 5 and recovered.GetNumBonds() == 3
    assert [atom.GetFormalCharge() for atom in recovered.GetAtoms()] == [0, 0, -1, 1, 0]
    assert [atom.GetIsotope() for atom in recovered.GetAtoms()] == [13, 0, 0, 0, 2]
    np.testing.assert_allclose(
        recovered.GetConformer().GetPositions(), reference.GetConformer().GetPositions()
    )


def test_caffeine_keeps_source_hydrogens_and_connectivity():
    source = msm.systems["caffeine"]["caffeine.sdf"]
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert molsys.topology.n_atoms == 24 and molsys.topology.n_bonds == 25
    assert sum(molsys.topology.atoms.atom_type == "H") == 10
    assert msm.get_form(Path(str(source).upper())) == "file:sdf"


@pytest.mark.parametrize("version", ["V2000", "V3000"])
def test_nondefault_length_units_at_read_write_boundary(source, tmp_path, version):
    puw = msm.pyunitwizard
    puw.configure.set_standard_units(
        [
            "angstrom",
            "ps",
            "K",
            "mole",
            "dalton",
            "e",
            "kJ/mol",
            "kJ/(mol*nm)",
            "kJ/(mol*nm**2)",
            "radians",
        ]
    )
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    # Structures.append stores canonical nm even under a different session
    # policy. Compare physical values through explicit units at both boundaries.
    assert puw.get_unit(molsys.structures.coordinates) == puw.unit("nm")
    np.testing.assert_allclose(
        puw.get_value(molsys.structures.coordinates, to_unit="angstrom")[0, :, 0],
        [0, 1.2, -1.2, 4, 0],
    )
    molsys.structures.coordinates = puw.quantity(
        puw.get_value(molsys.structures.coordinates, to_unit="angstrom"), "angstrom"
    )
    target = tmp_path / "units.sdf"
    msm.convert(molsys, to_form=target, ctfile_version=version)
    recovered = msm.convert(target, to_form="molsysmt.MolSys")
    np.testing.assert_allclose(
        puw.get_value(recovered.structures.coordinates, to_unit="nm")[0, :, 0],
        [0, 0.12, -0.12, 0.4, 0],
    )


def test_aromatic_bonds_are_explicit_and_do_not_require_kekulization(tmp_path):
    # A planar regular hexagon with explicit aromatic order 4.
    lines = [
        "benzene",
        "  Independent       2D",
        "",
        "  6  6  0  0  0  0  0  0  0  0999 V2000",
    ]
    for angle in np.arange(6) * np.pi / 3:
        lines.append(
            f"{1.4 * np.cos(angle):10.4f}{1.4 * np.sin(angle):10.4f}    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0"
        )
    for i in range(6):
        lines.append(f"{i + 1:3d}{(i + 1) % 6 + 1:3d}  4  0  0  0  0")
    source = tmp_path / "aromatic.sdf"
    source.write_text("\n".join([*lines, "M  END", "$$$$", ""]))
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert msm.get(molsys, atom_is_aromatic=True) == [True] * 6
    np.testing.assert_allclose(
        msm.get(molsys, element="bond", fractional_bond_order=True), [1.5] * 6
    )
    for version in ("V2000", "V3000"):
        target = tmp_path / f"{version}.sdf"
        msm.convert(molsys, to_form=target, ctfile_version=version)
        assert msm.get(target, element="bond", bond_is_aromatic=True) == [True] * 6
        if importlib.util.find_spec("rdkit") is not None:
            from rdkit import Chem

            reference = Chem.SDMolSupplier(str(target), removeHs=False)[0]
            assert reference is not None
            assert all(atom.GetIsAromatic() for atom in reference.GetAtoms())


def test_charge_and_radical_properties_override_atom_block(tmp_path):
    source = tmp_path / "override.sdf"
    lines = V2000.splitlines()
    lines[4] = lines[4][:36] + "  3" + lines[4][39:]
    lines[5] = lines[5][:36] + "  4" + lines[5][39:]
    source.write_text(
        "\n".join(lines).replace("M  END", "M  RAD  1   1   2\nM  END") + "\n"
    )
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert msm.get(molsys, formal_charge=True) == [0, 0, -1, 1, 0]
    assert msm.get(molsys, n_unpaired_electrons=True) == [1, 0, 0, 0, 0]
    target = tmp_path / "radical.sdf"
    msm.convert(molsys, to_form=target)
    assert msm.get(target, n_unpaired_electrons=True) == [1, 0, 0, 0, 0]


def test_writer_rejects_stereo_and_missing_chemistry_before_opening_file(
    source, tmp_path
):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    target = tmp_path / "preserved.sdf"
    target.write_text("keep existing contents")
    molsys.topology._set_chemical_state_atom_attribute(
        "stereochemistry",
        ["R", "unspecified", "unspecified", "unspecified", "unspecified"],
    )
    with pytest.raises(FormatError, match="stereochemistry"):
        msm.convert(molsys, to_form=target)
    assert target.read_text() == "keep existing contents"
    molsys.topology._set_chemical_state_atom_attribute(
        "stereochemistry", ["unspecified"] * 5
    )
    molsys.topology._set_chemical_state_atom_attribute("formal_charge", [None] * 5)
    with pytest.raises(FormatError, match="formal charges"):
        msm.convert(molsys, to_form=target)
    assert target.read_text() == "keep existing contents"


def test_option_digest_rejects_invalid_variants_and_discard_policy(source, tmp_path):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    with pytest.raises(ArgumentChoiceError):
        msm.convert(molsys, to_form=tmp_path / "invalid.sdf", ctfile_version="invalid")
    with pytest.raises(ArgumentError):
        msm.convert(source, to_form="molsysmt.MolSys", discard_properties="yes")


def test_reporting_catches_native_identity_loss_before_writing(source, tmp_path):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    molsys.topology.atoms["atom_id"] = [f"original-{i}" for i in range(5)]
    target = tmp_path / "strict.sdf"
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(molsys, to_form=target, strict=True)
    assert not target.exists()
    _, report = msm.convert(molsys, to_form=target, return_report=True)
    assert report.is_lossy and not report.is_exhaustive
    assert "atom_id" in {issue.attribute for issue in report.issues}


def test_empty_record_has_defined_native_shapes_and_can_be_written(tmp_path):
    source = tmp_path / "empty.sdf"
    source.write_text(
        "empty\n\n\n  0  0  0  0  0  0  0  0  0  0999 V2000\nM  END\n$$$$\n"
    )
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert molsys.topology.n_atoms == 0 and molsys.topology.n_bonds == 0
    assert molsys.structures.coordinates.shape == (1, 0, 3)
    assert molsys.chemical_states.n_chemical_states == 1
    target = tmp_path / "empty-v3000.sdf"
    msm.convert(molsys, to_form=target, ctfile_version="V3000")
    assert msm.convert(
        target, to_form="molsysmt.MolSys"
    ).structures.coordinates.shape == (1, 0, 3)


def test_v3000_supports_counts_beyond_v2000_limit(tmp_path):
    source = tmp_path / "large.sdf"
    atoms = [f"M  V30 {i + 1} He {i} 0 0 0" for i in range(1000)]
    source.write_text(
        "\n".join(
            [
                "helium",
                "  Independent       3D",
                "",
                "  0  0  0     0  0            999 V3000",
                "M  V30 BEGIN CTAB",
                "M  V30 COUNTS 1000 0 0 0 0",
                "M  V30 BEGIN ATOM",
                *atoms,
                "M  V30 END ATOM",
                "M  V30 END CTAB",
                "M  END",
                "$$$$",
                "",
            ]
        )
    )
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    target = tmp_path / "large-out.sdf"
    with pytest.raises(FormatError, match="999"):
        msm.convert(molsys, to_form=target)
    assert not target.exists()
    msm.convert(molsys, to_form=target, ctfile_version="V3000")
    assert msm.get(target, n_atoms=True) == 1000


def test_copy_and_native_extract_are_available_without_source_mutation(
    source, tmp_path
):
    original = source.read_bytes()
    target = tmp_path / "copy.sdf"
    msm.copy(source, output_filename=target)
    assert target.read_bytes() == original
    selected = msm.extract(source, selection=[2, 0], to_form="molsysmt.MolSys")
    assert selected.topology.n_atoms == 2
    assert selected.topology.atoms.atom_type.tolist() == ["C", "O"]
    assert selected.topology.n_bonds == 1
    assert source.read_bytes() == original


def test_numeric_syntax_and_absolute_isotope_precedence(tmp_path):
    source = tmp_path / "absolute.sdf"
    lines = V2000.splitlines()
    lines[4] = lines[4][:31] + "Fe " + " 1" + lines[4][36:]
    source.write_text("\n".join(lines).replace("   1  13", "   1  57") + "\n")
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert molsys.topology.atoms.isotope.iloc[0] == 57
    assert molsys.topology.atoms.atom_type.iloc[0] == "Fe"
    source.write_text(V3000.replace("CHG=-1", "CHG=1_0"))
    with pytest.raises(FormatError, match="Invalid integer"):
        msm.convert(source, to_form="molsysmt.MolSys")
    source.write_text(V3000.replace("O 1.2", "O 1_2"))
    with pytest.raises(FormatError, match="Invalid coordinates"):
        msm.convert(source, to_form="molsysmt.MolSys")


def test_v3000_writer_wraps_long_lines_without_changing_geometry(tmp_path):
    source = tmp_path / "long-lines.sdf"
    source.write_text(
        "\n".join(
            [
                "oxide",
                "  Independent       3D",
                "",
                "  0  0  0     0  0            999 V3000",
                "M  V30 BEGIN CTAB",
                "M  V30 COUNTS 1 0 0 0 0",
                "M  V30 BEGIN ATOM",
                "M  V30 1 O -0.123456789123 -0.123456789123 -0.123456789123 0 CHG=-1 MASS=18 RAD=2",
                "M  V30 END ATOM",
                "M  V30 END CTAB",
                "M  END",
                "$$$$",
                "",
            ]
        )
    )
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    target = tmp_path / "wrapped.sdf"
    msm.convert(molsys, to_form=target, ctfile_version="V3000")
    lines = [
        line for line in target.read_text().splitlines() if line.startswith("M  V30")
    ]
    assert max(map(len, lines)) <= 80
    assert any(line.endswith("-") for line in lines)
    result = msm.convert(target, to_form="molsysmt.MolSys")
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="angstrom"),
        [[[-0.123456789123] * 3]],
    )
    assert msm.get(result, formal_charge=True) == [-1]
    assert msm.get(result, n_unpaired_electrons=True) == [1]


def test_file_subset_reports_serial_reassignment_and_strictly_rejects_it(
    source, tmp_path
):
    target = tmp_path / "file-subset.sdf"
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(source, selection=[2, 4], to_form=target, strict=True)
    assert not target.exists()
    _, report = msm.convert(
        source, selection=[2, 4], to_form=target, return_report=True
    )
    assert report.is_lossy and not report.is_exhaustive
    assert "atom_id" in {issue.attribute for issue in report.issues}
    assert "identity" in report.audited_scopes
    assert msm.get(target, element="atom", atom_type=True) == ["O", "H"]


def test_writer_does_not_drop_unencodable_positive_atom_aromaticity(source, tmp_path):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    molsys.topology._set_chemical_state_atom_attribute(
        "is_aromatic", [True, False, False, False, False]
    )
    target = tmp_path / "unencodable.sdf"
    with pytest.raises(FormatError, match="aromaticity cannot be retained"):
        msm.convert(molsys, to_form=target)
    assert not target.exists()
