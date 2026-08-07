from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest
import pandas as pd


def _openmm_element(atom_type, app):
    """Resolve direct symbols and unambiguous dotted Tripos atom types."""

    if atom_type is None or pd.isna(atom_type):
        return None
    value = str(atom_type).strip()
    candidates = [value]
    if '.' in value:
        candidates.append(value.split('.', maxsplit=1)[0])
    for candidate in candidates:
        try:
            return app.Element.getBySymbol(candidate)
        except KeyError:
            continue
    return None

@arg_digest(form='molsysmt.Topology')
@dep_digest('openmm')
def to_openmm_Topology(item, box=None, atom_indices='all', skip_digestion=False):

    import openmm as mm
    import openmm.app as app

    if not is_all(atom_indices):
        from .extract import extract
        item = extract(item, atom_indices=atom_indices, skip_digestion=True)

    tmp_item = app.Topology()

    list_new_atoms = []
    list_new_residues = []
    list_new_chains = []

    for chain in item.chains.itertuples(index=True):
        tmp_chain = tmp_item.addChain(id=str(chain.chain_id))
        list_new_chains.append(tmp_chain)

    if len(list_new_chains) == 0:
        tmp_chain = tmp_item.addChain(id=' ')
        list_new_chains.append(tmp_chain)

    group_chain_mapping = item.atoms.groupby('group_index')['chain_index'].agg('first').to_dict()

    for group in item.groups.itertuples(index=True):
        chain_idx = group_chain_mapping.get(group.Index, 0)
        if chain_idx is None or pd.isna(chain_idx):
            chain_idx = 0
        
        tmp_residue = tmp_item.addResidue(group.group_name, list_new_chains[int(chain_idx)],
                                          id=str(group.group_id))
        list_new_residues.append(tmp_residue)

    formal_charges = item._get_chemical_state_atom_attribute('formal_charge')
    for atom in item.atoms.itertuples(index=True):
        tmp_element = _openmm_element(atom.atom_type, app)
        formal_charge = None
        if formal_charges is not None and not pd.isna(formal_charges.iloc[atom.Index]):
            formal_charge = int(formal_charges.iloc[atom.Index])
        tmp_atom = tmp_item.addAtom(
            atom.atom_name, tmp_element, list_new_residues[int(atom.group_index)],
            id=str(atom.atom_id), formalCharge=formal_charge,
        )
        list_new_atoms.append(tmp_atom)

    bonds = item._get_chemical_state_bonds()
    type_by_order = {1: app.Single, 2: app.Double, 3: app.Triple}
    for bond in bonds.itertuples(index=True):
        order = None
        bond_type = None
        if hasattr(bond, 'bond_order') and not pd.isna(bond.bond_order):
            order = int(bond.bond_order)
            bond_type = type_by_order.get(order)
        if hasattr(bond, 'is_aromatic') and not pd.isna(bond.is_aromatic) and bond.is_aromatic:
            bond_type = app.Aromatic
        tmp_item.addBond(
            list_new_atoms[int(bond.atom1_index)],
            list_new_atoms[int(bond.atom2_index)],
            type=bond_type,
            order=order,
        )

    del list_new_atoms, list_new_residues, list_new_chains

    if box is not None:
        from molsysmt.form.openmm_Topology.set import set_box_to_system
        set_box_to_system(tmp_item, value=box, skip_digestion=True)

    return tmp_item
