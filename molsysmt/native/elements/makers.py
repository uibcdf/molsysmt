def make_atom(index=None, id=None, name=None, type=None):

    from .atom import Atom

    return Atom(index=index, id=id, name=name, type=type)


def make_group(index=None, id=None, name=None, type=None,
               atom_indices=[]):

    from .groups import *

    atom_indices=atom_indices.copy()

    if type is None:

        return Group(index=index, id=id, name=name,
                     chemical_type=chemical_type, formal_charge=formal_charge,
                     atom_indices=atom_indices)

    elif type == 'aminoacid':

        return AminoAcid(index=index, id=id, name=name,
                         chemical_type=chemical_type, formal_charge=formal_charge,
                         atom_indices=atom_indices)

    elif type == 'nucleotide':

        return Nucleotide(index=index, id=id, name=name,
                          chemical_type=chemical_type, formal_charge=formal_charge,
                          atom_indices=atom_indices)

    elif type == 'ion':

        return Ion(index=index, id=id, name=name,
                        chemical_type=chemical_type, formal_charge=formal_charge,
                        atom_indices=atom_indices)

    elif type == 'water':

        return Water(index=index, id=id, name=name,
                     chemical_type=chemical_type, formal_charge=formal_charge,
                     atom_indices=atom_indices)

    elif type == 'cosolute':

        return Cosolute(index=index, id=id, name=name,
                        chemical_type=chemical_type, formal_charge=formal_charge,
                        atom_indices=atom_indices)

    elif type == 'small_molecule':

        return SmallMolecule(index=index, id=id, name=name,
                             chemical_type=chemical_type, formal_charge=formal_charge,
                             atom_indices=atom_indices)

    else:

        raise ValueError("Group type not recognized")


def make_component(index=None, id=None, name=None, type=None,
                  atom_indices=[], group_indices=[]):

    from .component import Component

    atom_indices=atom_indices.copy()
    group_indices=group_indices.copy()

    return Component(index=index, id=id, name=name, type=type,
                     atom_indices=atom_indices, group_indices=group_indices)


def make_molecule(index=None, id=None, name=None, type=None,
                 atom_indices=[], group_indices=[], component_indices=[]):

    atom_indices=atom_indices.copy()
    group_indices=group_indices.copy()
    component_indices=component_indices.copy()

    from .molecules import *

    if type is None:

        return Molecule(index=index, id=id, name=name,
                        atom_indices=atom_indices, group_indices=group_indices,
                        component_indices=component_indices)

    elif type is "ion":

        return Ion(index=index, id=id, name=name,
                   atom_indices=atom_indices, group_indices=group_indices,
                   component_indices=component_indices)

    elif type is "water":

        return Water(index=index, id=id, name=name,
                     atom_indices=atom_indices, group_indices=group_indices,
                     component_indices=component_indices)

    elif type is "cosolute":

        return Cosolute(index=index, id=id, name=name,
                        atom_indices=atom_indices, group_indices=group_indices,
                        component_indices=component_indices)

    elif type is "small_molecule":

        return SmallMolecule(index=index, id=id, name=name,
                             atom_indices=atom_indices, group_indices=group_indices,
                             component_indices=component_indices)

    elif type is "peptide":

        return Peptide(index=index, id=id, name=name,
                       atom_indices=atom_indices, group_indices=group_indices,
                       component_indices=component_indices)

    elif type is "dna":

        return DNA(index=index, id=id, name=name,
                   atom_indices=atom_indices, group_indices=group_indices,
                   component_indices=component_indices)

    elif type is "rna":

        return RNA(index=index, id=id, name=name,
                   atom_indices=atom_indices, group_indices=group_indices,
                   component_indices=component_indices)

    elif type is "protein":

        return Protein(index=index, id=id, name=name,
                       atom_indices=atom_indices, group_indices=group_indices,
                       component_indices=component_indices)

    else:

        raise ValueError("Entity type not recognized.")


def make_chain(index=None, id=None, name=None, type=None,
               atom_indices=[], group_indices=[], component_indices=[]):

    from .chain import Chain

    atom_indices=atom_indices.copy()
    group_indices=group_indices.copy()
    component_indices=component_indices.copy()

    return Chain(index=index, id=id, name=name, type=type,
                 atom_indices=atom_indices, group_indices=group_indices,
                 component_indices=component_indices)

def make_entity(index=None, id=None, name=None, type=None,
                atom_indices=[], group_indices=[], component_indices=[],
                chain_indices=[], molecule_indices=[]):

    atom_indices=atom_indices.copy()
    group_indices=group_indices.copy()
    component_indices=component_indices.copy()
    chain_indices=chain_indices.copy()
    molecule_indices=molecule_indices.copy()

    from .entities import *

    if type is None:

        return Entity(index=index, id=id, name=name,
                      atom_indices=atom_indices, group_indices=group_indices,
                      component_indices=component_indices,
                      chain_indices=chain_indices, molecule_indices=molecule_indices)

    elif type is "ion":

        return Ion(index=index, id=id, name=name,
                   atom_indices=atom_indices, group_indices=group_indices,
                   component_indices=component_indices,
                   chain_indices=chain_indices, molecule_indices=molecule_indices)

    elif type is "water":

        return Water(index=index, id=id, name=name,
                     atom_indices=atom_indices, group_indices=group_indices,
                     component_indices=component_indices,
                     chain_indices=chain_indices, molecule_indices=molecule_indices)

    elif type is "cosolute":

        return Cosolute(index=index, id=id, name=name,
                        atom_indices=atom_indices, group_indices=group_indices,
                        component_indices=component_indices,
                        chain_indices=chain_indices, molecule_indices=molecule_indices)

    elif type is "small_molecule":

        return SmallMolecule(index=index, id=id, name=name,
                             atom_indices=atom_indices, group_indices=group_indices,
                             component_indices=component_indices,
                             chain_indices=chain_indices, molecule_indices=molecule_indices)

    elif type is "peptide":

        return Peptide(index=index, id=id, name=name,
                       atom_indices=atom_indices, group_indices=group_indices,
                       component_indices=component_indices,
                       chain_indices=chain_indices, molecule_indices=molecule_indices)

    elif type is "dna":

        return DNA(index=index, id=id, name=name,
                   atom_indices=atom_indices, group_indices=group_indices,
                   component_indices=component_indices,
                   chain_indices=chain_indices, molecule_indices=molecule_indices)

    elif type is "rna":

        return RNA(index=index, id=id, name=name,
                   atom_indices=atom_indices, group_indices=group_indices,
                   component_indices=component_indices,
                   chain_indices=chain_indices, molecule_indices=molecule_indices)

    elif type is "protein":

        return Protein(index=index, id=id, name=name,
                       atom_indices=atom_indices, group_indices=group_indices,
                       component_indices=component_indices,
                       chain_indices=chain_indices, molecule_indices=molecule_indices)

    else:

        raise ValueError("Entity type not recognized.")

def make_bond(index=None, atoms=None, order=None):

    from .bond import Bond

    return Bond(index=index, atoms=atoms, order=order)



