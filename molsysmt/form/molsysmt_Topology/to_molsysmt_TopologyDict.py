from molsysmt._private.argdigest import arg_digest
from molsysmt.form._serialization import normalize_scalar as _normalize_scalar
from molsysmt.native import TopologyDict


@arg_digest(form="molsysmt.Topology")
def to_molsysmt_TopologyDict(item, skip_digestion=False):
    """
    Converting from molsysmt.Topology to molsysmt.TopologyDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.TopologyDict
        Resulting object in molsysmt.TopologyDict form.


    Notes
    -----
    Nullable table fields become Python scalars or None, including typed isotope
    and bond-order numbers. The emitted record schema is 0.1; primitive scalar
    transport does not imply preservation of every native chemical assignment.
    Independent atom/molecule declarations that schema 0.1 cannot represent
    are rejected. Use H5MSM 0.5 to preserve them.

    Examples
    --------
    >>> import json
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys(n_atoms=1)
    >>> molsys.topology.atoms.loc[0, "isotope"] = 13
    >>> records = msm.convert(molsys.topology, to_form="molsysmt.TopologyDict").to_dict()
    >>> json.loads(json.dumps(records))["atoms"][0]["isotope"]
    13

    .. versionadded:: 1.0.0
    """

    from molsysmt.native._legacy_molecule_membership import validate_record_export

    validate_record_export(item)

    atoms = []
    for atom_index in range(item.n_atoms):
        row = item.atoms.iloc[atom_index]
        atoms.append(
            {
                "atom_id": None
                if _normalize_scalar(row["atom_id"]) is None
                else str(_normalize_scalar(row["atom_id"])),
                "atom_name": _normalize_scalar(row["atom_name"]),
                "atom_type": _normalize_scalar(row["atom_type"]),
                "isotope": _normalize_scalar(row["isotope"]),
            }
        )

    atom_group_index = item.atoms["group_index"].to_numpy(dtype=object)
    groups = []
    for group_index in range(item.n_groups):
        row = item.groups.iloc[group_index]
        groups.append(
            {
                "group_id": None
                if _normalize_scalar(row["group_id"]) is None
                else str(_normalize_scalar(row["group_id"])),
                "group_name": _normalize_scalar(row["group_name"]),
                "group_type": _normalize_scalar(row["group_type"]),
                "atom_indices": [
                    int(ii)
                    for ii in range(item.n_atoms)
                    if atom_group_index[ii] == group_index
                ],
            }
        )

    bonds = []
    bonds_df = item._get_chemical_state_bonds()
    for bond_index in range(bonds_df.shape[0]):
        row = bonds_df.iloc[bond_index]
        bond = {
            "atom_index_1": int(row["atom1_index"]),
            "atom_index_2": int(row["atom2_index"]),
        }
        if (
            "bond_order" in bonds_df.columns
            and _normalize_scalar(row.get("bond_order", None)) is not None
        ):
            bond["bond_order"] = _normalize_scalar(row["bond_order"])
        elif (
            "is_aromatic" in bonds_df.columns
            and _normalize_scalar(row.get("is_aromatic", None)) is not None
            and bool(row["is_aromatic"])
        ):
            bond["bond_order"] = "aromatic"
        if (
            "bond_type" in bonds_df.columns
            and _normalize_scalar(row.get("bond_type", None)) is not None
        ):
            bond["bond_type"] = _normalize_scalar(row["bond_type"])
        bonds.append(bond)

    chains = []
    if item.n_chains > 0:
        from molsysmt.native._chain_groups import by_chain

        chain_group_indices = by_chain(item)
        for chain_index in range(item.n_chains):
            row = item.chains.iloc[chain_index]
            chains.append(
                {
                    "chain_id": None
                    if _normalize_scalar(row["chain_id"]) is None
                    else str(_normalize_scalar(row["chain_id"])),
                    "chain_name": _normalize_scalar(row["chain_name"]),
                    "chain_type": _normalize_scalar(row["chain_type"]),
                    "group_indices": chain_group_indices[chain_index].tolist(),
                }
            )

    molecules = []
    if item.n_molecules > 0:
        group_molecule_index = item.groups["molecule_index"].to_numpy(dtype=object)
        for molecule_index in range(item.n_molecules):
            row = item.molecules.iloc[molecule_index]
            molecules.append(
                {
                    "molecule_id": None
                    if _normalize_scalar(row["molecule_id"]) is None
                    else str(_normalize_scalar(row["molecule_id"])),
                    "molecule_name": _normalize_scalar(row["molecule_name"]),
                    "molecule_type": _normalize_scalar(row["molecule_type"]),
                    "group_indices": [
                        int(ii)
                        for ii in range(item.n_groups)
                        if group_molecule_index[ii] == molecule_index
                    ],
                }
            )

    entities = []
    if item.n_entities > 0:
        molecule_entity_index = item.molecules["entity_index"].to_numpy(dtype=object)
        for entity_index in range(item.n_entities):
            row = item.entities.iloc[entity_index]
            entities.append(
                {
                    "entity_id": None
                    if _normalize_scalar(row["entity_id"]) is None
                    else str(_normalize_scalar(row["entity_id"])),
                    "entity_name": _normalize_scalar(row["entity_name"]),
                    "entity_type": _normalize_scalar(row["entity_type"]),
                    "molecule_indices": [
                        int(ii)
                        for ii in range(item.n_molecules)
                        if molecule_entity_index[ii] == entity_index
                    ],
                }
            )

    return TopologyDict(
        data={
            "format": "molsysmt",
            "kind": "topology",
            "version": "0.1",
            "metadata": {},
            "atoms": atoms,
            "groups": groups,
            "bonds": bonds,
            "chains": chains,
            "molecules": molecules,
            "entities": entities,
        }
    )
