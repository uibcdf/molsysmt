from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.TopologyDict")
def to_molsysmt_MolSys(item, atom_indices="all", skip_digestion=False):
    """Converting declared inventory, retaining chemistry only from legacy records.

    Parameters
    ----------
    item : molsysmt.TopologyDict
        Version 0.2 stable records or legacy 0.1 records with reference bonds.
    atom_indices : str or array-like of int, default='all'
        Atom positions to retain with their available domains.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    molsysmt.MolSys
        Independent native domains; 0.2 inventory does not create chemical states.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.variables import is_all
    from molsysmt.form._native_dict import decode_topology
    from molsysmt.native import MolSys, MolSysDict

    if item.data.get("version", "0.1") == "0.2":
        result = MolSys._from_partial_domains(topology=decode_topology(item.data))
    else:
        from molsysmt.form.molsysmt_MolSysDict._builder import (
            build_molsys_builder_from_molsys_dict,
        )

        payload = MolSysDict(
            {"version": "0.1", "topology": item.data, "structures": {}}
        )
        builder = build_molsys_builder_from_molsys_dict(payload)
        result = builder._build(preserve_absent_groups=builder._preserve_absent_groups)
    return (
        result
        if is_all(atom_indices)
        else result.extract(atom_indices=atom_indices, skip_digestion=True)
    )
