"""Reject ineffective global precision requests before modular output is written."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentConflictError
from molsysmt.native import MolSys, Structures


def _source(kind="molsys"):
    values = np.arange(18, dtype=np.float64).reshape(3, 2, 3) + 2**-40
    structures = Structures(coordinates=msm.pyunitwizard.quantity(values, "nm"))
    if kind == "structures":
        return structures, values
    molsys = MolSys(n_atoms=2)
    molsys.structures = structures
    if kind == "complementary":
        return [molsys.topology, molsys.chemical_states, structures], values
    return molsys, values


@pytest.mark.parametrize("version", ["0.5", "0.6"])
@pytest.mark.parametrize("name", ["float_precision", "int_precision"])
@pytest.mark.parametrize("value", ["single", "double"])
@pytest.mark.parametrize("kind", ["molsys", "structures", "complementary"])
def test_explicit_global_precision_requests_refuse_before_publication(
    tmp_path, version, name, value, kind
):
    source, original = _source(kind)
    path = tmp_path / "refused.h5msm"
    with pytest.raises(ArgumentConflictError, match="field-specific"):
        msm.convert(
            source,
            to_form="file:h5msm",
            output_filename=path,
            format_version=version,
            **{name: value},
        )
    assert not path.exists()
    structures = (
        source[-1]
        if kind == "complementary"
        else source
        if kind == "structures"
        else source.structures
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(structures.coordinates, to_unit="nm"), original
    )


@pytest.mark.parametrize("version", ["0.5", "0.6"])
@pytest.mark.parametrize("flags", [{}, {"strict": True, "return_report": True}])
def test_default_modular_storage_preserves_double_geometry_and_declared_dtypes(
    tmp_path, version, flags
):
    source, values = _source()
    assert np.any(values != values.astype(np.float32).astype(np.float64))
    if version == "0.6":
        source.molecular_mechanics.partial_charge = np.array(
            [0.25, -0.25], dtype=np.float32
        )
    path = tmp_path / "stored.h5msm"
    msm.convert(
        source,
        to_form="file:h5msm",
        output_filename=path,
        format_version=version,
        **flags,
    )
    with h5py.File(path, "r") as file:
        assert file["structures/coordinates"].dtype == np.dtype("float64")
        np.testing.assert_array_equal(file["structures/coordinates"][:], values)
    restored = msm.h5msm.read(path)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        values,
    )
    if version == "0.6":
        assert restored.molecular_mechanics.atoms_ff[
            "partial_charge"
        ].dtype == np.dtype("float32")


@pytest.mark.parametrize("version", ["0.5", "0.6"])
@pytest.mark.parametrize("skip_digestion", [False, True])
def test_refusal_preserves_existing_destination_even_with_trusted_delegation(
    tmp_path, version, skip_digestion
):
    source, _ = _source()
    path = tmp_path / "existing.h5msm"
    original = b"Existing destination must remain unchanged."
    path.write_bytes(original)
    with pytest.raises(ArgumentConflictError, match="field-specific"):
        msm.convert(
            source,
            to_form="file:h5msm",
            output_filename=path,
            format_version=version,
            float_precision="single",
            skip_digestion=skip_digestion,
        )
    assert path.read_bytes() == original
