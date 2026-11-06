"""Retain deposited model labels on their existing coordinate-model axis."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError, MolecularSystemMismatchWarning
from tests.form.mmcif_PdbxContainers_DataContainer.test_primary_occupancy import (
    _as_file,
    _container,
)


def source_with_labels(labels):
    source = _container([[0.8, 1.0]] * len(labels))
    category = source.getObj("atom_site")
    column = category.getAttributeList().index("pdbx_PDB_model_num")
    for row, label in zip(category.data, np.repeat(labels, 2), strict=True):
        row[column] = label
    return source


@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Structures"])
def test_deposited_model_labels_follow_numeric_model_axis_and_repeated_selection(
    form, target, tmp_path
):
    source = source_with_labels(["017", "2", "51"])
    before = deepcopy(source.getObj("atom_site").getRowList())
    item = source if form == "container" else _as_file(source, tmp_path, form)
    original_bytes = None if form == "container" else item.read_bytes()
    result = msm.convert(item, to_form=target, structure_indices=[2, 0, 2])
    structures = result.structures if target == "molsysmt.MolSys" else result
    assert structures.structure_id is not None
    assert structures.structure_id.tolist() == ["51", "2", "51"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(structures.coordinates, to_unit="angstrom")[:, :, 0],
        [[30, 31], [20, 21], [30, 31]],
    )
    observed = msm.get(item, structure_id=True)
    assert observed is not None
    assert list(observed) == ["2", "017", "51"]
    selected = msm.get(item, structure_indices=[1, 0, 1], structure_id=True)
    assert list(selected) == ["017", "2", "017"]
    combined = msm.get(
        item,
        structure_indices=[2, 0, 2],
        coordinates=True,
        structure_id=True,
        output_type="dictionary",
    )
    assert list(combined["structure_id"]) == ["51", "2", "51"]
    assert source.getObj("atom_site").getRowList() == before
    if original_bytes is not None:
        assert item.read_bytes() == original_bytes


def test_direct_getter_retains_exact_labels_and_detaches_selected_values():
    from molsysmt.form.mmcif_PdbxContainers_DataContainer import (
        get_structure_id_from_system,
    )

    source = source_with_labels(["009", "2", "51"])
    ids = get_structure_id_from_system(source, structure_indices=[1, 0, 1])
    assert ids is not None
    assert list(ids) == ["009", "2", "009"]
    ids[0] = "edited"
    assert list(get_structure_id_from_system(source)) == ["2", "009", "51"]


@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
def test_single_model_id_remains_a_label_through_h5msm_and_extraction(form, tmp_path):
    source = source_with_labels(["071"])
    item = source if form == "container" else _as_file(source, tmp_path, form)
    result = msm.convert(item, to_form="molsysmt.MolSys")
    assert result.structures.structure_id is not None
    assert result.structures.structure_id.tolist() == ["071"]
    selected = msm.extract(result, structure_indices=[0, 0])
    assert selected.structures.structure_id.tolist() == ["071", "071"]
    path = tmp_path / "selected.h5msm"
    msm.convert(selected, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert loaded.structures.structure_id.tolist() == ["071", "071"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(selected.structures.coordinates, to_unit="nm"),
    )


@pytest.mark.parametrize("missing", ["?", ".", "column_absent"])
@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
def test_unavailable_model_labels_remain_unavailable(missing, form, tmp_path):
    source = source_with_labels(["1"])
    category = source.getObj("atom_site")
    if missing == "column_absent":
        category.removeAttribute("pdbx_PDB_model_num")
    else:
        column = category.getAttributeList().index("pdbx_PDB_model_num")
        for row in category.data:
            row[column] = missing
    item = source if form == "container" else _as_file(source, tmp_path, form)
    assert msm.get(item, structure_id=True) is None
    result = msm.convert(item, to_form="molsysmt.MolSys")
    assert result.structures.structure_id is None
    assert result.structures.coordinates.shape == (1, 2, 3)
    assert msm.get(item, n_structures=True) == 1


@pytest.mark.parametrize("labels", [["?", "1"], ["1", "01"], ["1", "1.5"]])
def test_ambiguous_or_invalid_model_labels_fail_without_mutating_source(labels):
    source = source_with_labels(labels)
    before = deepcopy(source.getObj("atom_site").getRowList())
    with pytest.raises(FormatError, match="model|MODEL"):
        msm.convert(source, to_form="molsysmt.MolSys")
    assert source.getObj("atom_site").getRowList() == before


def test_incompatible_model_inventories_keep_each_label_and_the_existing_warning():
    source = source_with_labels(["5", "17"])
    category = source.getObj("atom_site")
    for name in ("auth_atom_id", "label_atom_id"):
        category.data[-1][category.getAttributeList().index(name)] = "O2"
    with pytest.warns(MolecularSystemMismatchWarning):
        result = msm.convert(source, to_form="molsysmt.MolSys")
    assert isinstance(result, list) and len(result) == 2
    assert [m.structures.structure_id.tolist() for m in result] == [["5"], ["17"]]


def test_bundled_nmr_labels_remain_aligned_with_selected_deposited_coordinates():
    filename = msm.systems["Trp-Cage"]["1l2y.bcif.gz"]
    source = msm.convert(filename, to_form="mmcif.PdbxContainers.DataContainer")
    category = source.getObj("atom_site")
    columns = {name: i for i, name in enumerate(category.getAttributeList())}
    labels = sorted(
        {str(r[columns["pdbx_PDB_model_num"]]) for r in category.data}, key=int
    )
    assert len(labels) > 10
    selected = [len(labels) - 1, 0, 9, len(labels) - 1]
    result = msm.convert(source, structure_indices=selected, get_missing_bonds=False)
    assert result.structures.structure_id.tolist() == [labels[i] for i in selected]
    assert result.topology.atoms.atom_name.iloc[0] == "N"
    expected = []
    for index in selected:
        first = next(
            r
            for r in category.data
            if str(r[columns["pdbx_PDB_model_num"]]) == labels[index]
        )
        assert first[columns["auth_atom_id"]] == "N"
        expected.append(
            [float(first[columns[name]]) for name in ("Cartn_x", "Cartn_y", "Cartn_z")]
        )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="angstrom")[
            :, 0
        ],
        expected,
        rtol=0,
        atol=1e-12,
    )
