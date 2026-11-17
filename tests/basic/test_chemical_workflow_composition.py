"""Protect chemistry, maps and selective invalidation across public boundaries."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from tests.form.file_sdf.test_native_contract import V2000, V3000


@pytest.mark.parametrize("source_text", [V2000, V3000], ids=["V2000", "V3000"])
def test_declared_sdf_permutation_storage_export_and_scoped_coordinate_edit(
    source_text, tmp_path
):
    puw = msm.pyunitwizard
    source_path = tmp_path / "declared.sdf"
    source_path.write_text(source_text)
    order = [4, 2, 0, 3, 1]
    original_nm = np.array(
        [[0, 0, 0], [0.12, 0, 0], [-0.12, 0, 0], [0.4, 0, 0], [0, 0.1, 0]]
    )
    expected_nm = np.stack([original_nm + [shift, 0, 0] for shift in [0, 1, 2]])
    with puw.context(standard_units=["pm", "fs", "elementary_charge"]):
        source = msm.convert(source_path, to_form="molsysmt.MolSys")
        source.structures.append(
            coordinates=puw.quantity(expected_nm[1:] * 10, "angstrom")
        )
        source.interactions = {
            "declared-observation": msm.Interactions.from_records(
                [
                    dict(
                        structure_index=0,
                        interaction_type="synthetic",
                        participants=[
                            dict(role="first", atom_indices=[0]),
                            dict(role="second", atom_indices=[4]),
                        ],
                        measurements={"distance": 0.1},
                    )
                ],
                n_atoms=5,
                n_structures=3,
                evaluated_structure_indices=[0, 1],
                measure_units={"distance": "nm"},
                method="declared-test-record",
                software={"fixture": "1"},
            )
        }
        transformed = msm.permute_atoms(source, order, return_report=True)
        np.testing.assert_array_equal(
            transformed["report"]["source_to_output_atom_indices"], [2, 4, 1, 3, 0]
        )
        selected = msm.extract(
            transformed["molecular_system"], structure_indices=[2, 0, 1]
        )
        path = tmp_path / "permuted.h5msm"
        msm.h5msm.write(selected, path)
        stored_bytes = path.read_bytes()
        loaded = msm.h5msm.read(path)
        np.testing.assert_allclose(
            puw.get_value(loaded.structures.coordinates, to_unit="nm"),
            expected_nm[[2, 0, 1]][:, order],
            rtol=0,
            atol=1e-15,
        )
        assert msm.get(loaded, element="atom", atom_type=True) == [
            "H",
            "O",
            "C",
            "Na",
            "O",
        ]
        assert msm.get(loaded, element="atom", formal_charge=True) == [0, -1, 0, 1, 0]
        assert msm.get(loaded, selection=[0, 2], isotope=True) == [2, 13]
        bonds = loaded.chemical_states.get_bonds()
        assert sorted(
            (int(row.atom1_index), int(row.atom2_index), float(row.bond_order))
            for row in bonds.itertuples()
        ) == [(0, 2, 1.0), (1, 2, 1.0), (2, 4, 2.0)]
        analysis = loaded.interactions["declared-observation"]
        assert analysis.atom_source_indices.tolist() == order
        assert analysis.structure_source_indices.tolist() == [2, 0, 1]
        assert analysis.evaluated_structure_indices.tolist() == [1, 2]
        assert analysis.query(structure_indices=[1]).n_interactions == 1
        assert analysis.query(structure_indices=[2]).n_interactions == 0
        assert (
            analysis.query(structure_indices=[0])
            .to_dict()["evaluated_structure_indices"]
            .tolist()
            == []
        )

        output_path = tmp_path / "exported.sdf"
        msm.convert(loaded, to_form=output_path, structure_indices=[1])
        exported = msm.convert(output_path)
        assert msm.get(exported, element="atom", formal_charge=True) == [0, -1, 0, 1, 0]
        assert msm.get(exported, selection=[0, 2], isotope=True) == [2, 13]
        np.testing.assert_allclose(
            puw.get_value(exported.structures.coordinates, to_unit="nm"),
            expected_nm[[0]][:, order],
            rtol=0,
            atol=1e-5,
        )
        before = puw.get_value(loaded.structures.coordinates, to_unit="nm").copy()
        with pytest.raises(ArgumentError):
            msm.set(
                loaded,
                selection=[0],
                structure_indices=[1],
                coordinates=puw.quantity([[[0, 200, 0]]], "ps"),
            )
        np.testing.assert_array_equal(
            puw.get_value(loaded.structures.coordinates, to_unit="nm"), before
        )
        assert loaded.interactions["declared-observation"] is analysis
        msm.set(
            loaded,
            selection=[0],
            structure_indices=[1],
            coordinates=puw.quantity([[[0, 200, 0]]], "pm"),
        )
        assert loaded.interactions[
            "declared-observation"
        ].evaluated_structure_indices.tolist() == [2]
        assert analysis.evaluated_structure_indices.tolist() == [1, 2]
        np.testing.assert_allclose(
            puw.get_value(source.structures.coordinates, to_unit="nm"), expected_nm
        )
        assert source.interactions["declared-observation"].n_interactions == 1
        assert path.read_bytes() == stored_bytes
    assert source_path.read_text() == source_text
