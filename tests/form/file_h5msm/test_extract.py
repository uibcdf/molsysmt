"""
Tests for file_h5msm/extract.py.

The form-level extract() function has four main code branches depending on
whether atom_indices and structure_indices are 'all' or a specific subset.

We call the form function directly (skip_digestion=True) so that output_filename
can be a different path — allowing non-destructive subset extraction without
touching the fixture file.

Builder fixture: 4 atoms, 2 groups, 2 bonds, 1 chain, 2 molecules, 2 entities,
1 structure.
"""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.form.file_h5msm.extract import extract as h5msm_extract


def _load(path):
    """Convert extracted h5msm file to MolSys for inspection."""
    return msm.convert(path, to_form="molsysmt.MolSys")


# ---------------------------------------------------------------------------
# Branch 1: is_all(atoms) and is_all(structures) — file copy
# ---------------------------------------------------------------------------


def test_extract_all_all_copy(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    result = h5msm_extract(
        builder_h5msm_file, output_filename=output, skip_digestion=True
    )
    assert result == output
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_atoms=True) == 4
    assert msm.get(molsys, element="system", n_groups=True) == 2


def test_extract_all_all_copy_preserves_structure_count(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(builder_h5msm_file, output_filename=output, skip_digestion=True)
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_structures=True) == 1


def test_extract_all_all_inplace_no_copy(builder_h5msm_file):
    """copy_if_all=False with all+all returns same path without copying."""
    result = h5msm_extract(builder_h5msm_file, copy_if_all=False, skip_digestion=True)
    assert result == builder_h5msm_file


@pytest.mark.parametrize("selection", ["atom_index<0", "atom_index==0"])
def test_public_subset_without_destination_preserves_source(
    builder_h5msm_file, tmp_path, selection
):
    source = tmp_path / "source.h5msm"
    source.write_bytes(Path(builder_h5msm_file).read_bytes())
    original = source.read_bytes()

    with pytest.raises(ArgumentError, match="output_filename"):
        msm.extract(source, selection=selection)

    assert source.read_bytes() == original


def test_subset_rejects_explicit_source_path_alias(builder_h5msm_file, tmp_path):
    source = tmp_path / "source.h5msm"
    source.write_bytes(Path(builder_h5msm_file).read_bytes())
    original = source.read_bytes()

    with pytest.raises(ArgumentError, match="output_filename"):
        h5msm_extract(
            source,
            atom_indices=np.array([0]),
            output_filename=tmp_path / "." / source.name,
            skip_digestion=True,
        )

    assert source.read_bytes() == original


def test_public_subset_rejects_explicit_source_destination(
    builder_h5msm_file, tmp_path
):
    source = tmp_path / "source.h5msm"
    source.write_bytes(Path(builder_h5msm_file).read_bytes())
    original = source.read_bytes()

    with pytest.raises(ArgumentError, match="output_filename"):
        msm.extract(
            source,
            selection="atom_index==0",
            output_filename=tmp_path / "." / source.name,
        )

    assert source.read_bytes() == original


def test_public_subset_writes_distinct_destination(builder_h5msm_file, tmp_path):
    source = tmp_path / "source.h5msm"
    destination = tmp_path / "subset.h5msm"
    source.write_bytes(Path(builder_h5msm_file).read_bytes())
    original = source.read_bytes()

    result = msm.extract(
        source,
        selection="atom_index==0",
        output_filename=destination,
    )

    assert Path(result) == destination
    assert source.read_bytes() == original
    assert msm.get(destination, n_atoms=True) == 1


def test_public_subset_can_return_molsys_without_writing(builder_h5msm_file, tmp_path):
    source = tmp_path / "source.h5msm"
    source.write_bytes(Path(builder_h5msm_file).read_bytes())
    original = source.read_bytes()

    subset = msm.extract(
        source,
        selection="atom_index==0",
        to_form="molsysmt.MolSys",
    )

    assert msm.get(subset, n_atoms=True) == 1
    assert source.read_bytes() == original


def test_subset_rejects_hard_link_to_source(builder_h5msm_file, tmp_path):
    source = tmp_path / "source.h5msm"
    source.write_bytes(Path(builder_h5msm_file).read_bytes())
    alias = tmp_path / "alias.h5msm"
    try:
        alias.hardlink_to(source)
    except OSError as exception:
        pytest.skip(f"Hard links are unavailable: {exception}")
    original = source.read_bytes()

    with pytest.raises(ArgumentError, match="output_filename"):
        h5msm_extract(
            source,
            atom_indices=np.array([0]),
            output_filename=alias,
            skip_digestion=True,
        )

    assert source.read_bytes() == original


def test_legacy_v03_subset_without_destination_preserves_source(tmp_path):
    legacy_fixture = Path(__file__).with_name("data") / "alanine_dipeptide_v03.h5msm"
    source = tmp_path / "legacy.h5msm"
    source.write_bytes(legacy_fixture.read_bytes())
    original = source.read_bytes()

    with pytest.raises(ArgumentError, match="output_filename"):
        h5msm_extract(source, atom_indices=np.array([0]), skip_digestion=True)

    assert source.read_bytes() == original


# ---------------------------------------------------------------------------
# Branch 2: atom subset, all structures
# ---------------------------------------------------------------------------


def test_extract_atom_subset_n_atoms(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(
        builder_h5msm_file,
        atom_indices=np.array([0, 1]),
        output_filename=output,
        skip_digestion=True,
    )
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_atoms=True) == 2


def test_extract_atom_subset_preserves_structure_count(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(
        builder_h5msm_file,
        atom_indices=np.array([0, 1]),
        output_filename=output,
        skip_digestion=True,
    )
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_structures=True) == 1


def test_extract_single_atom(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(
        builder_h5msm_file,
        atom_indices=np.array([0]),
        output_filename=output,
        skip_digestion=True,
    )
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_atoms=True) == 1


def test_extract_atom_subset_bonds_filtered(builder_h5msm_file, tmp_path):
    """Extracting both atoms of a bond preserves the bond; extracting one drops it."""
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(
        builder_h5msm_file,
        atom_indices=np.array([0, 1]),
        output_filename=output,
        skip_digestion=True,
    )
    molsys = _load(output)
    # atoms 0 and 1 share a bond in the builder fixture
    assert msm.get(molsys, element="system", n_bonds=True) >= 1


# ---------------------------------------------------------------------------
# Branch 3: all atoms, structure subset
# ---------------------------------------------------------------------------


def test_extract_structure_subset_preserves_atom_count(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(
        builder_h5msm_file,
        structure_indices=np.array([0]),
        output_filename=output,
        skip_digestion=True,
    )
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_atoms=True) == 4


def test_extract_structure_subset_count(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(
        builder_h5msm_file,
        structure_indices=np.array([0]),
        output_filename=output,
        skip_digestion=True,
    )
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_structures=True) == 1


# ---------------------------------------------------------------------------
# Branch 4: atom subset + structure subset
# ---------------------------------------------------------------------------


def test_extract_both_subsets_atom_count(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(
        builder_h5msm_file,
        atom_indices=np.array([0, 1]),
        structure_indices=np.array([0]),
        output_filename=output,
        skip_digestion=True,
    )
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_atoms=True) == 2


def test_extract_both_subsets_structure_count(builder_h5msm_file, tmp_path):
    output = str(tmp_path / "out.h5msm")
    h5msm_extract(
        builder_h5msm_file,
        atom_indices=np.array([0, 1]),
        structure_indices=np.array([0]),
        output_filename=output,
        skip_digestion=True,
    )
    molsys = _load(output)
    assert msm.get(molsys, element="system", n_structures=True) == 1
