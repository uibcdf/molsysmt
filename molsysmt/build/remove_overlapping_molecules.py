from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.atom_indices import complementary_atom_indices
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest()
def remove_overlapping_molecules(molecular_system, selection, selection_2=None,
                                structure_index=0, threshold='3 angstroms', pbc=True,
                                syntax='MolSysMT'):
    """
    Removing molecules that overlap a reference selection within a distance threshold.

    Given a reference selection (and optionally a second selection), this function finds
    contacts closer than `threshold` and removes the molecules containing the overlapping atoms.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray
        Selection string or boolean/integer array specifying elements.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    structure_index : object, default=0
        Argument structure_index.
    threshold : float or quantity, default='3 angstroms'
        Distance cutoff threshold quantity.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').

    Returns
    -------
    molecular system
        The pruned molecular system with overlapping molecules removed.
    """

    from molsysmt import select, get, remove
    from molsysmt.pbc import has_pbc
    from molsysmt.structure import get_contacts

    if pbc:
        pbc=has_pbc(molecular_system)

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if selection_2 is None:
        atom_indices_2 = complementary_atom_indices(molecular_system, atom_indices)
    else:
        atom_indices_2 = select(molecular_system, selection=selection_2, syntax=syntax)

    contact_map = get_contacts(molecular_system, selection=atom_indices, selection_2=atom_indices_2,
                               structure_indices=structure_index, threshold=threshold, pbc=pbc,
                               output_type='numpy.ndarray')

    mask = np.any(contact_map[0], axis=1)
    atoms_to_be_removed = np.array(atom_indices)[mask].tolist()
    molecules_to_be_removed = get(molecular_system, element='atom', selection=atoms_to_be_removed, molecule_index=True)
    molecules_to_be_removed = np.unique(molecules_to_be_removed)
    atoms_to_be_removed = select(molecular_system, selection='molecule_index==@molecules_to_be_removed')
    if len(atoms_to_be_removed):
        output = remove(molecular_system, selection=atoms_to_be_removed)
    else:
        output = molecular_system

    return output
