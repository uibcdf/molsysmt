from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.variables import is_all
from molsysmt._private.lists import sorted_list_of_pairs
from molsysmt.element.bond import max_expected_bond_length
import numpy as np
import warnings

@digest()
def get_disulfide_bonds(molecular_system, selection='all', structure_index=0, max_bond_length=None,
                        group_names=['CYS'], pbc=True, syntax='MolSysMT', engine='MolSysMT', sorted=True,
                        skip_digestion=False):
    """
    """

    if max_bond_length is None:
        max_bond_length = max_expected_bond_length['protein']['S']['S']

    bonds = []

    if engine=="MolSysMT":

        from molsysmt import select, get
        from molsysmt.structure import get_contacts

        if is_all(selection):
            mask = None
        else:
            mask= select(molecular_system, selection=selection, syntax=syntax)

        S_indices = select(molecular_system, element='atom', selection='atom_type=="S"',
                           mask=mask, syntax='MolSysMT')

        if len(S_indices)>1:

            tmp_group_indices, tmp_group_names = get(molecular_system, element='atom', selection=S_indices,
                                                     group_index=True, group_name=True)

            contacts = get_contacts(molecular_system, selection=S_indices, structure_indices=structure_index,
                                    threshold=max_bond_length, output_type='pairs', output_indices='selection',
                                    pbc=pbc, skip_digestion=True)

            for pair in contacts[0]:
                at1, at2 = pair
                if tmp_group_indices[at1]!=tmp_group_indices[at2]:
                    if tmp_group_names[at1] in group_names and tmp_group_names[at2] in group_names:
                        bonds.append([S_indices[at1], S_indices[at2]])
                    else:
                        for ii in pair:
                            if aux_group_names[ii] not in group_names:
                                message=(f"Warning: atom index {S_indices[ii]} in group {aux_group_names[ii]} with index"
                                          f"{aux_group_indices[ii]} can not be part of a disulfide bond because it is not in the list"
                                          f"of your input argument `group_names`")
                                warnings.warn(message)

    if sorted:

        bonds = sorted_list_of_pairs(bonds)

    return bonds

