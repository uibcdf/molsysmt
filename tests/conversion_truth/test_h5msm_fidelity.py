import h5py
import numpy as np
import pandas as pd

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _roundtrip_h5msm(molsys, filename, float_precision):
    msm.convert(
        molsys,
        to_form="file:h5msm",
        output_filename=str(filename),
        float_precision=float_precision,
        int_precision=float_precision,
    )
    return msm.convert(str(filename), to_form="molsysmt.MolSys")


def test_h5msm_preserves_missing_bond_metadata_as_missing(rich_molsys, tmp_path):
    filename = tmp_path / "missing.h5msm"
    output = _roundtrip_h5msm(rich_molsys, filename, "single")

    assert output.topology.bonds["bond_order"].tolist()[0] == 1
    assert pd.isna(output.topology.bonds["bond_order"].tolist()[1])
    assert pd.isna(output.topology.bonds["bond_type"].tolist()[0])
    assert output.topology.bonds["bond_type"].tolist()[2] == "covalent"
    assert msm.get(str(filename), element="system", n_polysaccharides=True) == 0


def test_h5msm_04_preserves_normalized_bond_fields(
    rich_molsys, tmp_path
):
    molsys = rich_molsys.copy()
    bonds = molsys.topology._get_chemical_state_bonds().copy()
    bonds['is_conjugated'] = pd.array([True, pd.NA, pd.NA], dtype='boolean')
    molsys.topology._set_chemical_state_bonds(bonds)

    filename = tmp_path / 'rich-bond.h5msm'
    msm.convert(molsys, to_form='file:h5msm', output_filename=str(filename))
    restored = msm.convert(filename, to_form='molsysmt.Topology')

    assert restored.bonds['is_conjugated'].tolist() == [True, pd.NA, pd.NA]


def test_h5msm_single_and_double_precision_have_explicit_numeric_contracts(rich_molsys, tmp_path):
    single = _roundtrip_h5msm(rich_molsys, tmp_path / "single.h5msm", "single")
    double = _roundtrip_h5msm(rich_molsys, tmp_path / "double.h5msm", "double")
    expected_coordinates = puw.get_value(rich_molsys.structures.coordinates, to_unit="nm")
    expected_box = puw.get_value(rich_molsys.structures.box, to_unit="nm")

    np.testing.assert_allclose(
        puw.get_value(single.structures.coordinates, to_unit="nm"),
        expected_coordinates,
        rtol=1e-6,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        puw.get_value(single.structures.box, to_unit="nm"),
        expected_box,
        rtol=1e-6,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        puw.get_value(double.structures.coordinates, to_unit="nm"),
        expected_coordinates,
        rtol=0.0,
        atol=1e-14,
    )
    np.testing.assert_allclose(
        puw.get_value(double.structures.box, to_unit="nm"),
        expected_box,
        rtol=0.0,
        atol=1e-14,
    )


def test_h5msm_writer_reads_component_membership_through_native_seam(
    rich_molsys, tmp_path, monkeypatch
):
    topology = rich_molsys.topology.copy()
    expected = pd.Series(
        np.arange(topology.n_atoms, dtype=np.int64) % topology.n_components,
        dtype="Int64",
    )
    monkeypatch.setattr(
        type(topology),
        "_get_component_indices",
        lambda self: expected,
    )
    filename = tmp_path / "component-seam-write.h5msm"

    msm.convert(
        topology,
        to_form="file:h5msm",
        output_filename=str(filename),
    )

    with h5py.File(filename, "r") as file:
        np.testing.assert_array_equal(
            file["topology"]["atoms"]["component_index"][:],
            expected.to_numpy(dtype=np.int64),
        )


def test_h5msm_reader_restores_component_membership(rich_molsys, tmp_path):
    filename = tmp_path / "component-seam-read.h5msm"
    msm.convert(
        rich_molsys,
        to_form="file:h5msm",
        output_filename=str(filename),
    )
    restored = msm.convert(str(filename), to_form="molsysmt.Topology")

    np.testing.assert_array_equal(
        restored._get_component_indices().to_numpy(dtype=np.int64),
        rich_molsys.topology._get_component_indices().to_numpy(dtype=np.int64),
    )
    assert restored.bonds is restored._reference_chemical_state.bonds
    assert restored.components is restored._reference_chemical_state.components
