from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.Topology')
def to_openmm_Topology(item, box=None, atom_indices='all', skip_digestion=False):

    try:
        import openmm as mm
        import openmm.app as app
        import openmm.unit as unit
    except:
        raise LibraryNotFound('openmm')

    if not is_all(atom_indices):
        from . import extract
        item = extract(item, atom_indices=atom_indices)

    tmp_item = app.Topology()

    former_group_index = -1
    former_chain_index = -1

    list_new_atoms = []
    list_new_residues = []
    list_new_chains = []

    for chain in item.chains.itertuples(index=True):
        tmp_chain = tmp_item.addChain(id=str(chain.chain_id))
        list_new_chains.append(tmp_chain)

    group_chain_mapping = item.atoms.groupby('group_index')['chain_index'].agg('first').to_dict()

    for group in item.groups.itertuples(index=True):
        tmp_residue = tmp_item.addResidue(group.group_name, list_new_chains[group_chain_mapping[group.Index]],
                                      id=str(group.group_id))
        list_new_residues.append(tmp_residue)

    for atom in item.atoms.itertuples(index=True):

        element = app.Element.getBySymbol(atom.atom_type)
        tmp_atom = tmp_item.addAtom(atom.atom_name, element, list_new_residues[atom.group_index])
        tmp_atom.id = str(atom.atom_id)
        list_new_atoms.append(tmp_atom)

    for bond in item.bonds.itertuples(index=False):

        tmp_item.addBond(list_new_atoms[bond.atom1_index], list_new_atoms[bond.atom2_index])

    del list_new_atoms, list_new_residues, list_new_chains

    if box is not None:

        from ..openmm_Topology import set_box_to_system

        set_box_to_system(tmp_item, value=box)

    return tmp_item

