def make_atom(index=None, id=None, name=None, type=None):

    from .atom import Atom

    return Atom(index=index, id=id, name=name, type=type)


def make_group(index=None, id=None, name=None, type=None, atoms=[]):

    from .groups import Group, AminoAcid, Nucleotide, Ion, Water, Cosolute, SmallMolecule

    if type is None:

        return Group(index=index, id=id, name=name, atoms=atoms)

    elif type == 'aminoacid':

        return AminoAcid(index=index, id=id, name=name, atoms=atoms)

    elif type == 'nucleotide':

        return Nucleotide(index=index, id=id, name=name, atoms=atoms)

    elif type == 'ion':

        return Ion(index=index, id=id, name=name, atoms=atoms)

    elif type == 'water':

        return Water(index=index, id=id, name=name, atoms=atoms)

    elif type == 'cosolute':

        return Cosolute(index=index, id=id, name=name, atoms=atoms)

    elif type == 'small_molecule':

        return SmallMolecule(index=index, id=id, name=name, atoms=atoms)

    else:

        raise ValueError("Group type not recognized")


def make_component(index=None, id=None, name=None, type=None,
                  atoms=[], groups=[]):

    from .component import Component

    return Component(index=index, id=id, name=name, type=type,
                     atoms=atoms, groups=groups)


def make_molecule(index=None, id=None, name=None, type=None,
                 atoms=[], groups=[], components=[]):

    from .molecules import Molecule, Ion, Water, Cosolute, SmallMolecule,\
    Peptide, DNA, RNA, Protein

    if type is None:

        return Molecule(index=index, id=id, name=name, atoms=atoms,
                        groups=groups, components=components)

    elif type is "ion":

        return Ion(index=index, id=id, name=name, atoms=atoms,
                   groups=groups, components=components)

    elif type is "water":

        return Water(index=index, id=id, name=name, atoms=atoms,
                     groups=groups, components=components)

    elif type is "cosolute":

        return Cosolute(index=index, id=id, name=name, atoms=atoms,
                        groups=groups, components=components)

    elif type is "small_molecule":

        return SmallMolecule(index=index, id=id, name=name, atoms=atoms,
                             groups=groups, components=components)

    elif type is "peptide":

        return Peptide(index=index, id=id, name=name, atoms=atoms,
                       groups=groups, components=components)

    elif type is "dna":

        return DNA(index=index, id=id, name=name, atoms=atoms,
                   groups=groups, components=components)

    elif type is "rna":

        return RNA(index=index, id=id, name=name, atoms=atoms,
                   groups=groups, components=components)

    elif type is "protein":

        return Protein(index=index, id=id, name=name, atoms=atoms,
                       groups=groups, components=components)

    else:

        raise ValueError("Entity type not recognized.")


def make_chain(index=None, id=None, name=None, type=None,
               atoms=[], groups=[], components=[]):

    from .chain import Chain

    return Chain(index=index, id=id, name=name, type=type,
                 atoms=atoms, groups=groups,
                 components=components)

def make_entity(index=None, id=None, name=None, type=None,
                atoms=[], groups=[], components=[],
                chains=[], molecules=[]):

    from .entities import Ion, Water, Cosolute, SmallMolecule, Peptide, DNA, RNA,\
            Protein

    if type is None:

        return Entity(index=index, id=id, name=name,
                      atoms=atoms, groups=groups,
                      components=components,
                      chains=chains, molecules=molecules)

    elif type is "ion":

        return Ion(index=index, id=id, name=name,
                   atoms=atoms, groups=groups,
                   components=components,
                   chains=chains, molecules=molecules)

    elif type is "water":

        return Water(index=index, id=id, name=name,
                     atoms=atoms, groups=groups,
                     components=components,
                     chains=chains, molecules=molecules)

    elif type is "cosolute":

        return Cosolute(index=index, id=id, name=name,
                        atoms=atoms, groups=groups,
                        components=components,
                        chains=chains, molecules=molecules)

    elif type is "small_molecule":

        return SmallMolecule(index=index, id=id, name=name,
                             atoms=atoms, groups=groups,
                             components=components,
                             chains=chains, molecules=molecules)

    elif type is "peptide":

        return Peptide(index=index, id=id, name=name,
                       atoms=atoms, groups=groups,
                       components=components,
                       chains=chains, molecules=molecules)

    elif type is "dna":

        return DNA(index=index, id=id, name=name,
                   atoms=atoms, groups=groups,
                   components=components,
                   chains=chains, molecules=molecules)

    elif type is "rna":

        return RNA(index=index, id=id, name=name,
                   atoms=atoms, groups=groups,
                   components=components,
                   chains=chains, molecules=molecules)

    elif type is "protein":

        return Protein(index=index, id=id, name=name,
                       atoms=atoms, groups=groups,
                       components=components,
                       chains=chains, molecules=molecules)

    else:

        raise ValueError("Entity type not recognized.")

def make_bond(index=None, atoms=None, order=None):

    from .bond import Bond

    return Bond(index=index, atoms=atoms, order=order)


