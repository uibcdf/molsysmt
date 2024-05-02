import numpy as np
from .group_names import group_names

def small_molecule_is_amino_acid(molecular_system, group_name):

    output = False

    if group_name in group_names:

        from molsysmt import get

        atom_names = get(molecular_system, element='atom', selection=f'group_name=="{group_name}"', atom_name=True)
        unique_atom_names = np.unique(atom_names)

        if 'CA' in unique_atom_names:
            if 'CB' in unique_atom_names:
                if 'C' in unique_atom_names:
                    if 'O' in unique_atom_names:
                        if 'N' in unique_atom_names:
                            output = True
                            warning_message = f"Warning! The group name {group_name} is reserved in the Protein Data "
                            warning_message += "Bank for a small molecule, not for an amino acid."
                            print(warning_message)

    return output

