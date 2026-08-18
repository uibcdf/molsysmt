from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all
from molsysmt._private.lists import sorted_list_of_pairs
from molsysmt.element.bond import max_expected_bond_length
import numpy as np
import warnings

@arg_digest()
def get_disulfide_bonds(molecular_system, selection='all', structure_index=0, max_bond_length=None,
                        group_names=None, pbc=True, syntax='MolSysMT', engine='MolSysMT', sorted=True,
                        skip_digestion=False):
    """
    Identifying disulfide bonds between sulfur atoms.

    This function detects disulfide bonds in a molecular system by finding pairs of sulfur atoms
    that belong to specified residue types (e.g., `CYS`) and lie within a covalent bond distance.
    These S–S bridges are returned as atom index pairs.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_index : object, default=0
        Argument structure_index.
    max_bond_length : object, default=None
        Argument max_bond_length.
    group_names : object, default=None
        Argument group_names.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : object, default='MolSysMT'
        Argument engine.
    sorted : bool, default=True
        Whether to sort the returned bonded atom pairs.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray of shape (n, 2)
        Array of atom index pairs (each a disulfide bond) detected in the selected atoms and structure.


    Raises
    ------
    NotSupportedFormError
        If the molecular system format is not supported.

    ArgumentError
        If input values do not meet required conditions.


    Notes
    -----
    - Sulfur atoms are identified based on element type and filtered by group name (e.g., `'CYS'`).
    - This function assumes that disulfide bonds are formed between SG atoms of cysteines or equivalent residues.
    - Distance units are internally standardized to nanometers.


    See Also
    --------
    :meth:`molsysmt.Topology.add_bonds`
        Add identified bonds directly to a native topology.

    :func:`molsysmt.structure.get_neighbors`
        Find neighboring atoms within a distance or bond limit.

    :func:`molsysmt.build.get_missing_bonds`
        Automatically infer missing covalent bonds.


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert('5XJH')
    >>> s_s_pairs = msm.build.get_disulfide_bonds(molsys, max_bond_length='2.15 angstroms')
    >>> s_s_pairs.shape
    (2, 2)


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Build > Get disulfide bonds <Tutorial_Get_disulfide_bonds>`

    .. versionadded:: 1.0.0
    """

    if group_names is None:
        group_names = ['CYS']

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
                        from molsysmt._private.smonitor import warn
                        for ii in pair:
                            if tmp_group_names[ii] not in group_names:
                                message=(f"Atom index {S_indices[ii]} in group {tmp_group_names[ii]} with index "
                                          f"{tmp_group_indices[ii]} cannot be part of a disulfide bond because it is not in the list "
                                          f"of your input argument `group_names`.")
                                warn(message)

    if sorted:

        bonds = sorted_list_of_pairs(bonds)

    return bonds
