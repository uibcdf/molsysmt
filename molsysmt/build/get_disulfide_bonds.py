from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.variables import is_all
from molsysmt._private.lists import sorted_list_of_pairs
from molsysmt.element.bond import max_expected_bond_length
import numpy as np
import warnings


@digest()
def get_disulfide_bonds(molecular_system, selection='all', structure_index=0, max_bond_length='2.05 angstroms',
                        group_names=['CYS'], pbc=True, syntax='MolSysMT', engine='MolSysMT', sorted=True,
                        skip_digestion=False):
    """
    """

    if max_bond_length is None:
        max_bond_length = max_expected_bond_length['protein'][['S','S']]
    else:
        max_bond_length = puw.quantity(max_bond_length)

    bonds = []

    if engine=="MolSysMT":

        from molsysmt import select, get
        from molsysmt.structure import get_contacts

        S_indices = select(molecular_system, selection=selection, group_name=group_names, atom_type='S')

        if len(S_indices)>1:

            tmp_group_indices, tmp_group_names = get(molecular_system, target='atom', indices=S_indices,
                                                     group_index=True, group_name=True)

            aux_group_indices = {ii:jj for ii,jj in zip(S_indices, tmp_group_indices)}
            aux_group_names = {ii:jj for ii,jj in zip(S_indices, tmp_group_names)}

            contacts = get_contacts(molecular_system, selection=S_indices, structure_indices=structure_index,
                                    threshold=max_bond_length, output_type='pairs', pbc=pbc, skip_digestion=True)

            for pair in contacts[0]:
                if group_indices[pair[0]]!=group_indices[pair[1]]:
                    if aux_group_names[pair[0]] in group_names and aux_group_names[pair[1]] in group_names:
                        bonds.append(pair)
                    else:
                        for ii in pair:
                            if aux_group_names[ii] not in group_names:
                                message=(f"Warning: atom index {ii} in group {aux_group_names[ii]} with index"
                                          f"{aux_group_indices[ii]} can not be part of a disulfide bond not defined"
                                          f"with your input argument `group_names`")
                                warnings.warn(message)

    if sorted:

        bonds = sorted_list_of_pairs(bonds)

    return bonds

