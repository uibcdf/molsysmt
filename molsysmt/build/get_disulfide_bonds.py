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
    Identifying disulfide bonds between sulfur atoms.

    This function detects disulfide bonds in a molecular system by finding pairs of sulfur atoms
    that belong to specified residue types (e.g., `CYS`) and lie within a covalent bond distance.
    These S–S bridges are returned as atom index pairs.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>` to be analyzed.

    selection : index, tuple, list, numpy.ndarray or str, default 'all'
        Selection of atoms to be considered for disulfide bond detection. This can be a list, tuple, or array
        of atom indices (0-based), or a string parsed using the specified selection syntax.

    structure_index : int, default 0
        Index of the structure (frame) in which disulfide bonds will be searched.

    max_bond_length : float or str with units, optional
        Maximum distance between two sulfur atoms to be considered a disulfide bond. If not provided,
        a default threshold (typically 2.05 Å) will be used.

    group_names : list of str, default ['CYS']
        List of residue names to be considered as potential cysteine-like residues forming disulfide bonds.

    pbc : bool, default True
        Whether to apply periodic boundary conditions when computing distances.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used to parse the `selection` argument (if string).

    engine : {'MolSysMT'}, default 'MolSysMT'
        Engine used to perform the analysis. Currently only 'MolSysMT' is supported.

    sorted : bool, default True
        Whether to sort the indices in each pair (i.e., smaller index first).

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
    :func:`molsysmt.build.add_bonds`
        Manually add bonds between specific atom pairs.

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

