from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.frame_indices import complementary_frame_indices
from molsysmt._private_tools.atom_indices import complementary_atom_indices

def remove(molecular_system, selection=None, frame_indices=None, to_form=None, syntaxis='MolSysMT'):

    """remove(item, selection=None, frame_indices=None, syntaxis='MolSysMT')

    Remove atoms or frames from the molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    selection: str, list, tuple or np.ndarray, default=None
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    frame_indices: str, list, tuple or np.ndarray, default=None
        XXX

    syntaxis: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    item: molecular model
        The result is a new molecular model with the same form as the input item.

    Examples
    --------
    Remove chains 0 and 1 from the pdb: 1B3T.
    >>> import molsysmt as m3t
    >>> system = m3t.load('pdb:1B3T')
    Check the number of chains
    >>> m3t.get(system, n_chains=True)
    8
    Remove chains 0 and 1
    >>> new_system = m3t.remove(system, 'chainid 0 1')
    Check the number of chains of the new molecular model
    >>> m3t.get(new_system, n_chains=True)
    6

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----
    There is a specific method to remove solvent atoms: molsysmt.remove_solvent and another one to
    remove hydrogens: molsysmt.remove_hydrogens.

    """

    from molsysmt.basic import select, extract

    molecular_system = digest_molecular_system(molecular_system)
    frame_indices = digest_frame_indices(frame_indices)

    atom_indices_to_be_kept = 'all'
    frame_indices_to_be_kept = 'all'

    if selection is not None:
        atom_indices_to_be_removed = select(molecular_system, selection=selection, syntaxis=syntaxis)
        atom_indices_to_be_kept = complementary_atom_indices(molecular_system, atom_indices_to_be_removed)

    if frame_indices is not None:
        frame_indices_to_be_kept = complementary_frame_indices(molecular_system, frame_indices)

    tmp_item = extract(molecular_system, selection=atom_indices_to_be_kept, frame_indices=frame_indices_to_be_kept, to_form=to_form)
    tmp_item = digest_output(tmp_item)

    return tmp_item

