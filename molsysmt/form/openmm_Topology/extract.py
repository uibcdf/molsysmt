from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='openmm.Topology')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, digest=True):

    from openmm.app import Topology

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:

            new_item = Topology()
            newAtoms = {}
            for chain in item.chains():
                newChain = new_item.addChain(chain.id)
                for residue in chain.residues():
                    newResidue = new_item.addResidue(residue.name, newChain, residue.id, residue.insertionCode)
                    for atom in residue.atoms():
                        newAtom = new_item.addAtom(atom.name, atom.element, newResidue, atom.id)
                        newAtoms[atom] = newAtom
            for bond in item.bonds():
                new_item.addBond(newAtoms[bond[0]], newAtoms[bond[1]])
            del(newAtoms)
            new_item.setPeriodicBoxVectors(item.getPeriodicBoxVectors())
            tmp_item = new_item

        else:

            tmp_item = item
    else:

        new_item = Topology()
        atom_indices_to_be_kept = atom_indices
        newAtoms = {}
        set_atom_indices = set(atom_indices_to_be_kept)
        for chain in item.chains():
            needNewChain = True
            for residue in chain.residues():
                needNewResidue = True
                for atom in residue.atoms():
                    if atom.index in set_atom_indices:
                        if needNewChain:
                            newChain = new_item.addChain(chain.id)
                            needNewChain = False;
                        if needNewResidue:
                            newResidue = new_item.addResidue(residue.name, newChain, residue.id, residue.insertionCode)
                            needNewResidue = False;
                        newAtom = new_item.addAtom(atom.name, atom.element, newResidue, atom.id)
                        newAtoms[atom] = newAtom
        for bond in item.bonds():
            if bond[0].index in set_atom_indices and bond[1].index in set_atom_indices:
                new_item.addBond(newAtoms[bond[0]], newAtoms[bond[1]])
        del(newAtoms)
        new_item.setPeriodicBoxVectors(item.getPeriodicBoxVectors())
        tmp_item = new_item

    return tmp_item

