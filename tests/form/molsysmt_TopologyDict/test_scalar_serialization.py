"""Protecting transport of typed chemical scalars through declarative forms."""

import json

import pandas as pd
import pytest

import molsysmt as msm


@pytest.mark.parametrize("source_form", ["Topology", "MolSys", "MolSysBuilder"])
@pytest.mark.parametrize("field", ["isotope", "bond_order"])
@pytest.mark.parametrize("encoding", ["json", "yaml"])
def test_typed_scalars_are_serializable_and_restore_values(
    builder_pdb_molsys, source_form, field, encoding
):
    molsys = builder_pdb_molsys
    if field == "isotope":
        molsys.topology.atoms.loc[0, "isotope"] = 13
    else:
        molsys.chemical_states._resolve_chemical_state().bonds["bond_order"] = pd.array(
            [1, 1], dtype="UInt8"
        )
    source = {
        "Topology": molsys.topology,
        "MolSys": molsys,
        "MolSysBuilder": msm.MolSysBuilder(molsys),
    }[source_form]
    target_form = "TopologyDict" if source_form == "Topology" else "MolSysDict"
    declared = msm.convert(source, to_form="molsysmt." + target_form)
    data = declared.to_dict()
    topology = data if target_form == "TopologyDict" else data["topology"]
    if field == "isotope":
        assert type(topology["atoms"][0][field]) is int
    elif target_form == "TopologyDict":
        assert "bonds" not in topology
    else:
        assert data["chemical_states"] is not None
    if encoding == "json":
        restored = json.loads(json.dumps(data, allow_nan=False))
    else:
        yaml = pytest.importorskip("yaml")
        restored = yaml.safe_load(yaml.safe_dump(data))
    assert restored == data
    dictionary = type(declared)(data=restored)
    rebuilt = msm.convert(
        dictionary,
        to_form="molsysmt.Topology"
        if target_form == "TopologyDict"
        else "molsysmt.MolSys",
    )
    if field == "isotope":
        assert msm.get(rebuilt, element="atom", selection=[0], isotope=True) == [13]
    elif target_form == "TopologyDict":
        assert msm.get(rebuilt, element="bond", bond_order=True) is None
        assert not hasattr(rebuilt, "bonds")
    else:
        assert [
            int(value) for value in msm.get(rebuilt, element="bond", bond_order=True)
        ] == [1, 1]
