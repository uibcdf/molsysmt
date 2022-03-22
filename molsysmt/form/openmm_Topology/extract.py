from .is_openmm_Topology import is_openmm_Topology
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices
from molsysmt._private.step import digest_step
from molsysmt._private.time import digest_time
from molsysmt._private.coordinates import digest_coordinates
from molsysmt._private.box import digest_box

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from openmm.app import Topology

    if (atom_indices is 'all') and (structure_indices is 'all'):

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

