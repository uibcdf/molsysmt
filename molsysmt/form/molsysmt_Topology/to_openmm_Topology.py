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

    for atom in item.atoms.itertuples(index=True):

        new_group = (former_group_index!=atom.group_index)
        new_chain = (former_chain_index!=atom.chain_index)

        if new_chain:
            former_chain_index = atom.chain_index
            chain_id = item.chains.iloc[atom.chain_index,0]
            chain = tmp_item.addChain(id=str(chain_id))

        if new_group:
            former_group_index = atom.group_index
            residue_id, residue_name = item.groups.iloc[atom.group_index,0:2]
            residue = tmp_item.addResidue(residue_name, chain, id=str(residue_id))

        element = app.Element.getBySymbol(atom.atom_type)
        new_atom = tmp_item.addAtom(atom.atom_name, element, residue)
        new_atom.id = atom.atom_id
        list_new_atoms.append(new_atom)

    for bond in item.bonds.itertuples(index=False):

        tmp_item.addBond(list_new_atoms[bond.atom1_index], list_new_atoms[bond.atom2_index])

    if box is not None:

        from ..openmm_Topology import set_box_to_system

        set_box_to_system(tmp_item, value=box)

    return tmp_item

