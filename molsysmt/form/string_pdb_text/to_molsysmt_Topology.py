from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdb_text")
def to_molsysmt_Topology(
    item,
    atom_indices="all",
    get_missing_bonds=True,
    skip_digestion=False,
    *,
    bond_inference_engine=None,
    from_naming_scheme=None,
):
    """
    Converting from string:pdb_text to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    get_missing_bonds : bool, default=True
        Request connectivity inference when True; otherwise retain only
        declared PDB edges. Defaults to True for this topology projection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    bond_inference_engine : str or None, default=None
        Explicit 'MolSysMT' or 'OpenMM' engine, requiring get_missing_bonds=True.
        None retains this form's existing connectivity default.

    from_naming_scheme : str or None, default=None
        Source group-name convention declared before classification and native
        inference. None leaves it undeclared; no chemical state is translated.

    Returns
    -------
    molsysmt.Topology
        Stable source inventory and naming metadata. This pure Topology has
        no ChemicalStates graph or preparation-history facade.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import (
        to_molsysmt_PDBFileHandler,
    )
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_Topology import (
        to_molsysmt_Topology as molsysmt_PDBFileHandler_to_molsysmt_Topology,
    )

    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    try:
        return molsysmt_PDBFileHandler_to_molsysmt_Topology(
            tmp_item,
            atom_indices=atom_indices,
            get_missing_bonds=get_missing_bonds,
            bond_inference_engine=bond_inference_engine,
            from_naming_scheme=from_naming_scheme,
            skip_digestion=True,
        )
    finally:
        tmp_item.close()
