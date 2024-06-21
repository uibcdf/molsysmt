import numpy as np

def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True):

    from .get_group_type import get_group_type_from_group_name
    from .amino_acid import get_bonded_atom_pairs as get_bonded_atom_pairs_from_amino_acid
    from .ion import get_bonded_atom_pairs as get_bonded_atom_pairs_from_ion
    from .small_molecule import get_bonded_atom_pairs as get_bonded_atom_pairs_from_small_molecule
    from .terminal_capping import get_bonded_atom_pairs as get_bonded_atom_pairs_from_terminal_capping
    from .water import get_bonded_atom_pairs as get_bonded_atom_pairs_from_water

    group_type = get_group_type_from_group_name(group_name)

    bonds = None

    if group_type=='amino acid': # Replace by match-case whenever Python 3.9 is deprecated

        bonds = get_bonded_atom_pairs_from_amino_acid(group_name, atom_names, atom_indices=atom_indices,
                                                      sorted=sorted)
    
    elif group_type=='ion':

        bonds = get_bonded_atom_pairs_from_ion(group_name, atom_names, atom_indices=atom_indices, sorted=sorted)

    elif group_type=='lipid':

        pass

    elif group_type=='nucleotide':

        pass

    elif group_type=='oligosaccharide':

        pass

    elif group_type=='saccharide':

        pass

    elif group_type=='small molecule':

        bonds = get_bonded_atom_pairs_from_small_molecule(group_name, atom_names, atom_indices=atom_indices,
                                                          sorted=sorted)

    elif group_type=='terminal capping':

        bonds = get_bonded_atom_pairs_from_terminal_capping(group_name, atom_names, atom_indices=atom_indices,
                                                            sorted=sorted)

    elif group_type=='water':

        bonds = get_bonded_atom_pairs_from_water(atom_names, atom_indices=atom_indices, sorted=sorted)


    if bonds is None:
        print(f'Warning! The amino acid {group_name} has no template.')

    return bonds

