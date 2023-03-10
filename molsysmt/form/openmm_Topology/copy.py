from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='openmm.Topology')
def copy(item):

    from openmm.app import Topology

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

    return tmp_item

