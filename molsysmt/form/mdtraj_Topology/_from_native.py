from depdigest import dep_digest


@dep_digest("mdtraj")
def export_native(
    item, atom_indices="all", skip_digestion=False, *, chemical_states=None
):
    """
    Converting from molsysmt.Topology to mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Independent target preserving selected atom order, declared hierarchy,
        available formal charges and bonds. Missing source groups/chains use
        temporary target-only parents, never new native assignments.

    Raises
    ------
    StructuralInconsistencyError
        If a group spans several declared chains or parent indices are invalid.

    Notes
    -----
    MDTraj requires every atom to belong to a residue and chain. Existing native
    groups retain their target order. Ungrouped atoms use UNL placeholders per
    known source molecule and chain; when molecule ownership is absent, each
    ungrouped atom receives its own placeholder. Missing chains share one target
    fallback chain. A partially assigned group's one known chain is used for
    that whole target group; conflicting known chains fail explicitly.

    These external residue/chain indices are not missing native group/chain
    indices. MDTraj selectors such as resid or protein operate on the target's
    available metadata, including placeholders. Atom-index selections remain
    aligned with the selected source atom order. No source hierarchy, chemistry
    or coordinates are changed, and no physical group identity is inferred.


    .. versionadded:: 1.0.0
    """
    import numpy as np

    from molsysmt._private.variables import is_all

    if chemical_states is not None and not is_all(atom_indices):
        chemical_states = chemical_states._extract_atoms(
            np.sort(np.asarray(atom_indices, dtype=np.int64))
        )
    import pandas as pd
    from mdtraj import Aromatic, Double, Single, Topology, Triple
    from mdtraj.core import element

    from molsysmt.form.molsysmt_Topology.extract import extract

    item = extract(
        item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True
    )
    tmp_item = Topology()
    list_new_atoms = []
    from molsysmt.form.molsysmt_Topology._mdtraj_hierarchy import (
        target_residues_for_atoms,
    )

    residues_for_atoms = target_residues_for_atoms(item, tmp_item)
    formal_charges = (
        None
        if chemical_states is None
        else chemical_states._get_chemical_state_atom_attribute("formal_charge")
    )
    for atom in item.atoms.itertuples(index=True):
        elem = element.get_by_symbol(atom.atom_type)
        formal_charge = None
        if formal_charges is not None and (
            not pd.isna(formal_charges.iloc[atom.Index])
        ):
            formal_charge = int(formal_charges.iloc[atom.Index])
        tmp_atom = tmp_item.add_atom(
            atom.atom_name,
            elem,
            residues_for_atoms[atom.Index],
            atom.atom_id,
            formal_charge=formal_charge,
        )
        list_new_atoms.append(tmp_atom)
    from molsysmt.native._chemical_state import Bonds_DataFrame

    bonds = (
        Bonds_DataFrame()
        if chemical_states is None
        else chemical_states._resolve_chemical_state().bonds
    )
    type_by_order = {1: Single, 2: Double, 3: Triple}
    for bond in bonds.itertuples(index=False):
        order = None
        bond_type = None
        if hasattr(bond, "bond_order") and (not pd.isna(bond.bond_order)):
            order = int(bond.bond_order)
            bond_type = type_by_order.get(order)
        if (
            hasattr(bond, "is_aromatic")
            and (not pd.isna(bond.is_aromatic))
            and bond.is_aromatic
        ):
            bond_type = Aromatic
        tmp_item.add_bond(
            list_new_atoms[bond.atom1_index],
            list_new_atoms[bond.atom2_index],
            type=bond_type,
            order=order,
        )
    del list_new_atoms, residues_for_atoms
    return tmp_item
