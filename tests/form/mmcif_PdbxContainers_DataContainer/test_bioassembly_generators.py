"""Retain every source generator without inventing common chain membership."""

import hashlib
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
from mmcif.api.DataCategory import DataCategory

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError


@pytest.fixture(scope="module")
def public_container():
    path = Path(msm.systems["Barnase-Barstar"]["1brs.bcif.gz"])
    original_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    container = msm.convert(str(path), to_form="mmcif.PdbxContainers.DataContainer")
    yield container
    assert hashlib.sha256(path.read_bytes()).hexdigest() == original_hash


def _container(public_container, rows):
    container = deepcopy(public_container)
    # Only assembly declarations are synthetic; the bundled coordinates are public.
    container.replace(
        DataCategory(
            "pdbx_struct_oper_list",
            attributeNameList=[
                "id",
                "matrix[1][1]",
                "matrix[1][2]",
                "matrix[1][3]",
                "matrix[2][1]",
                "matrix[2][2]",
                "matrix[2][3]",
                "matrix[3][1]",
                "matrix[3][2]",
                "matrix[3][3]",
                "vector[1]",
                "vector[2]",
                "vector[3]",
            ],
            rowList=[
                ["1", 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                ["2", 1, 0, 0, 0, 1, 0, 0, 0, 1, 10, 0, 0],
                ["3", 0, -1, 0, 1, 0, 0, 0, 0, 1, 0, 20, 0],
            ],
        )
    )
    container.replace(
        DataCategory(
            "pdbx_struct_assembly_gen",
            attributeNameList=["assembly_id", "asym_id_list", "oper_expression"],
            rowList=rows,
        )
    )
    return container


def _translations(operation):
    return np.asarray(
        [puw.get_value(value, to_unit="nm") for value in operation["translations"]]
    )


@pytest.mark.parametrize("reverse", [False, True])
def test_repeated_parent_rows_build_all_copies_in_source_order(
    public_container, reverse
):
    rows = [["1", "A", "1"], ["1", "A", "2"]]
    if reverse:
        rows.reverse()
    container = _container(public_container, rows)
    before = deepcopy(container.getObj("pdbx_struct_assembly_gen").getRowList())
    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        source = msm.convert(container, to_form="molsysmt.MolSys")
        operation = msm.get(source, bioassembly=True)["1"]
        assert len(operation["rotations"]) == 2
        chain = msm.get(source, element="chain", chain_id=True).index("A")
        assert operation["chain_indices"] == [chain]
        atoms = msm.select(source, selection=f"chain_index=={chain}")
        coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[
            :, atoms
        ]
        offsets = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
        if reverse:
            offsets.reverse()
        np.testing.assert_allclose(
            _translations(operation), offsets, rtol=0, atol=1e-14
        )
        assembled = msm.build.make_bioassembly(
            source, bioassembly="1", structure_indices=0
        )
        observed = puw.get_value(msm.get(assembled, coordinates=True), to_unit="nm")
        expected = np.concatenate([coordinates + offset for offset in offsets], axis=1)
        assert observed.shape == (1, 2 * len(atoms), 3)
        np.testing.assert_allclose(observed, expected, rtol=0, atol=1e-12)
    assert container.getObj("pdbx_struct_assembly_gen").getRowList() == before


def test_interleaved_parents_ranges_products_and_duplicates_remain_separate(
    public_container,
):
    source = msm.convert(
        _container(
            public_container,
            [
                ["1", "A", "(1-2)"],
                ["2", "B", "1"],
                ["1", "A", "(3)(2)"],
                ["1", "A", "1"],
            ],
        ),
        to_form="molsysmt.MolSys",
    )
    operations = msm.get(source, bioassembly=True)
    assert list(operations) == ["1", "2"]
    assert len(operations["1"]["rotations"]) == 4
    assert len(operations["2"]["rotations"]) == 1
    # Product (3)(2) applies translation 2 first, then rotation/translation 3.
    np.testing.assert_allclose(
        _translations(operations["1"]),
        [[0, 0, 0], [1, 0, 0], [0, 3, 0], [0, 0, 0]],
        rtol=0,
        atol=1e-14,
    )
    np.testing.assert_array_equal(
        operations["1"]["rotations"][2], [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    )
    chain_ids = msm.get(source, element="chain", chain_id=True)
    assert operations["1"]["chain_indices"] == [chain_ids.index("A")]
    assert operations["2"]["chain_indices"] == [chain_ids.index("B")]


def test_different_chain_scopes_persist_and_builder_refuses_them(
    public_container, tmp_path
):
    source = msm.convert(
        _container(
            public_container,
            [
                ["1", "A", "(1-2)"],
                ["1", "B,A", "3"],
                ["1", "A", "1"],
            ],
        ),
        to_form="molsysmt.MolSys",
    )
    chain_ids = msm.get(source, element="chain", chain_id=True)
    a, b = chain_ids.index("A"), chain_ids.index("B")
    expected = [[a], [a], [b, a], [a]]
    operation = msm.get(source, bioassembly=True)["1"]
    assert operation["chain_indices"] == expected
    assert len(operation["rotations"]) == 4
    filename = tmp_path / "generators.h5msm"
    msm.convert(source, to_form=str(filename))
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    np.testing.assert_allclose(
        _translations(msm.get(restored, bioassembly=True)["1"]),
        _translations(operation),
        rtol=0,
        atol=1e-14,
    )
    for item in (source, restored):
        assert msm.get(item, bioassembly=True)["1"]["chain_indices"] == expected
        with pytest.raises(NotImplementedError):
            msm.build.make_bioassembly(item, bioassembly="1", structure_indices=0)


@pytest.mark.parametrize("expression", ["(1)(2)(3)", "()", "(1)()", "", "(2-1)"])
def test_uninterpreted_generator_cannot_return_a_partial_assembly(
    public_container, expression
):
    container = _container(public_container, [["1", "A", "1"], ["1", "A", expression]])
    with pytest.raises(FormatError, match="operation expression"):
        msm.convert(container, to_form="molsysmt.MolSys")
