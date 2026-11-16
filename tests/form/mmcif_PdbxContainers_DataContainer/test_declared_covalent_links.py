"""Join deposited covalent endpoints through their source namespaces."""

from copy import deepcopy

import pytest
from mmcif.api.DataCategory import DataCategory

import molsysmt as msm
from molsysmt._private.smonitor import FormatError

from .test_primary_occupancy import _as_file, _container


def source_with_link(*, models=1, different_names=False, insertion=False):
    source = _container([[1.0, 1.0]] * models)
    atoms = source.getObj("atom_site")
    for index, row in enumerate(atoms.data):
        if different_names:
            row[atoms.getAttributeList().index("auth_atom_id")] = ["CAUTH", "OAUTH"][
                index % 2
            ]
        if insertion:
            row[atoms.getAttributeList().index("pdbx_PDB_ins_code")] = "A"
    source.append(
        DataCategory(
            "struct_conn",
            attributeNameList=[
                "conn_type_id",
                "ptnr1_label_asym_id",
                "ptnr1_auth_seq_id",
                "ptnr1_label_atom_id",
                "ptnr2_label_asym_id",
                "ptnr2_auth_seq_id",
                "ptnr2_label_atom_id",
                "pdbx_ptnr1_PDB_ins_code",
                "pdbx_ptnr2_PDB_ins_code",
            ],
            rowList=[
                [
                    "covale",
                    "A",
                    "1",
                    "C1",
                    "A",
                    "1",
                    "O1",
                    "A" if insertion else "?",
                    "A" if insertion else "?",
                ]
            ],
        )
    )
    return source


def test_numeric_native_group_ids_do_not_lose_declared_covalent_links():
    result = msm.convert(source_with_link(), get_missing_bonds=False)
    bonds = result.chemical_states.get_bonds()
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[0, 1]]
    assert bonds.evidence.tolist() == ["explicit"]


@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
@pytest.mark.parametrize("models", [1, 2])
@pytest.mark.parametrize("variant", ["numeric", "label-not-author", "insertion"])
def test_declared_endpoints_preserve_source_labels_and_model_membership(
    tmp_path, form, models, variant
):
    source = source_with_link(
        models=models,
        different_names=variant == "label-not-author",
        insertion=variant == "insertion",
    )
    before = deepcopy(source.getObj("atom_site").getRowList())
    item = source if form == "container" else _as_file(source, tmp_path, form)
    original_bytes = None if form == "container" else item.read_bytes()
    result = msm.convert(item, get_missing_bonds=False)
    assert result.structures.coordinates.shape == (models, 2, 3)
    bonds = result.chemical_states.get_bonds()
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[0, 1]]
    assert bonds.evidence.tolist() == ["explicit"]
    if variant == "label-not-author":
        assert result.topology.atoms.atom_name.tolist() == ["CAUTH", "OAUTH"]
    if variant == "insertion":
        assert result.topology.groups.group_id.tolist() == ["1A"]
    assert source.getObj("atom_site").getRowList() == before
    if original_bytes is not None:
        assert item.read_bytes() == original_bytes


def test_unrepresented_covalent_endpoint_fails_clearly_without_guessing():
    source = source_with_link()
    category = source.getObj("struct_conn")
    category.data[0][category.getAttributeList().index("ptnr2_label_atom_id")] = (
        "missing"
    )
    before = deepcopy(category.getRowList())
    with pytest.raises(FormatError, match="struct_conn"):
        msm.convert(source, get_missing_bonds=False)
    assert category.getRowList() == before
