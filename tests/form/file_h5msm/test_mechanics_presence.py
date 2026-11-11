"""Refuse unrepresented mechanics before a complete-system transport loses it."""

import h5py
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolecularMechanics, MolSys, Structures, Topology


def _system(domain):
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    )
    if domain == "complete":
        source = MolSys(n_atoms=2)
        source.structures = structures
        return source
    if domain == "topology_free":
        source = MolSys(n_atoms=2)
        return MolSys._from_partial_domains(
            chemical_states=source.chemical_states, structures=structures
        )
    if domain == "no_chemistry":
        return MolSys._from_partial_domains(
            topology=Topology(n_atoms=2), structures=structures
        )
    if domain == "no_structures":
        source = MolSys(n_atoms=2)
        source.structures = None
        return source
    return MolSys._from_partial_domains(
        interactions={
            "empty": msm.Interactions.from_records(
                [],
                n_atoms=2,
                n_structures=1,
                evaluated_structure_indices=[0],
                method="presence_guard",
            )
        }
    )


@pytest.mark.parametrize(
    "domain",
    ["complete", "topology_free", "no_chemistry", "no_structures", "interactions"],
)
@pytest.mark.parametrize("field", ["partial_charge_assignment", "atom_type_assignment"])
@pytest.mark.parametrize("strict", [False, True])
def test_report_only_mechanics_is_refused_before_transport(
    tmp_path, domain, field, strict
):
    source = _system(domain)
    assert (source.structures is None) == (domain in {"no_structures", "interactions"})
    assert (source.topology is None) == (domain in {"topology_free", "interactions"})
    assert (source.chemical_states is None) == (
        domain in {"no_chemistry", "interactions"}
    )
    report = {"schema": "synthetic-negative-fixture", "status": "stale"}
    setattr(source.molecular_mechanics, field, report)
    # This remains a parameter projection, not the complete stored domain.
    assert all(value is None for value in source.molecular_mechanics.to_dict().values())
    path = tmp_path / "refused.h5msm"
    for route in ("direct", "converted", "dictionary"):
        with pytest.raises(
            ValueError, match="[Mm]olecular[Mm]echanics|molecular mechanics"
        ):
            if route == "direct":
                msm.h5msm.write(source, path, format_version="0.5")
            elif route == "converted":
                msm.convert(
                    source,
                    to_form="file:h5msm",
                    output_filename=path,
                    strict=strict,
                    format_version="0.5",
                )
            else:
                msm.convert(source, to_form="molsysmt.MolSysDict", strict=strict)
        assert not path.exists()
        assert getattr(source.molecular_mechanics, field) is report


@pytest.mark.parametrize("route", ["direct", "converted"])
def test_refused_mechanics_never_replaces_existing_file(tmp_path, route):
    source = _system("complete")
    path = tmp_path / "existing.h5msm"
    msm.h5msm.write(source, path, format_version="0.5")
    original = path.read_bytes()
    source.molecular_mechanics.partial_charge_assignment = {}
    with pytest.raises(ValueError, match="molecular mechanics"):
        if route == "direct":
            msm.h5msm.write(source, path, format_version="0.5")
        else:
            msm.convert(
                source, to_form="file:h5msm", output_filename=path, format_version="0.5"
            )
    assert path.read_bytes() == original


@pytest.mark.parametrize(
    "stored", ["empty_report", "empty_table", "null_table", "extension", "subclass"]
)
def test_unprojected_mechanics_storage_cannot_masquerade_as_absent(tmp_path, stored):
    source = _system("complete")
    mechanics = source.molecular_mechanics
    if stored == "empty_report":
        mechanics.atom_type_assignment = {}
    elif stored == "empty_table":
        mechanics.atoms_ff = pd.DataFrame()
    elif stored == "null_table":
        mechanics.atoms_ff = pd.DataFrame({"partial_charge": [None, None]})
    elif stored == "extension":
        mechanics.unrepresented = None
    else:

        class ExtendedMechanics(MolecularMechanics):
            __slots__ = ("unrepresented",)

        source.molecular_mechanics = ExtendedMechanics()
        source.molecular_mechanics.unrepresented = None
    path = tmp_path / "refused.h5msm"
    with pytest.raises(ValueError, match="molecular mechanics"):
        msm.h5msm.write(source, path, format_version="0.5")
    with pytest.raises(ValueError, match="MolecularMechanics"):
        msm.convert(source, to_form="molsysmt.MolSysDict")
    assert not path.exists()


@pytest.mark.parametrize("mechanics", ["default", "none"])
def test_absent_mechanics_keeps_supported_transport_working(tmp_path, mechanics):
    source = _system("complete")
    if mechanics == "none":
        source.molecular_mechanics = None
    path = tmp_path / "supported.h5msm"
    msm.h5msm.write(source, path, format_version="0.5")
    with h5py.File(path, "r") as file:
        assert file.attrs["version"] == "0.5"
        assert "molecular_mechanics" not in file
    assert msm.h5msm.read(path).get_n_atoms() == 2
    wire = msm.convert(source, to_form="molsysmt.MolSysDict")
    assert msm.convert(wire, to_form="molsysmt.MolSys").get_n_atoms() == 2
