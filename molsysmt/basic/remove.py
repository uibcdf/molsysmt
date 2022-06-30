from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.structure_indices import complementary_structure_indices
from molsysmt._private.atom_indices import complementary_atom_indices

def remove(molecular_system, selection=None, structure_indices=None, to_form=None,
        syntaxis='MolSysMT', check=True):

    """remove(item, selection=None, structure_indices=None, syntaxis='MolSysMT')

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

    structure_indices: str, list, tuple or np.ndarray, default=None
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
    >>> m3t.get(system,n_chains=True)
    8
    Remove chains 0 and 1
    >>> new_system = m3t.remove(system, 'chainid 0 1')
    Check the number of chains of the new molecular model
    >>> m3t.get(new_system,n_chains=True)
    6

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----
    There is a specific method to remove solvent atoms: molsysmt.remove_solvent and another one to
    remove hydrogens: molsysmt.remove_hydrogens.

    """

    from . import select, extract, is_molecular_system

    if check:

        if not is_molecular_system(molecular_system):
            raise SingleMolecularSystemNeededError()

        try:
            syntaxis = digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)

        try:
            selection = digest_selection(selection, syntaxis)
        except:
            raise WrongSelectionError()

        if structure_indices is not None:
            try:
                structure_indices = digest_structure_indices(structure_indices)
            except:
                raise WrongStructureIndicesError()

        try:
            to_form = digest_to_form(to_form)
        except:
            raise WrongToFormErro(to_form)

    atom_indices_to_be_kept = 'all'
    structure_indices_to_be_kept = 'all'

    if selection is not None:
        atom_indices_to_be_removed = select(molecular_system, selection=selection, syntaxis=syntaxis, check=False)
        atom_indices_to_be_kept = complementary_atom_indices(molecular_system, atom_indices_to_be_removed)

    if structure_indices is not None:
        structure_indices_to_be_kept = complementary_structure_indices(molecular_system, structure_indices)

    tmp_item = extract(molecular_system, selection=atom_indices_to_be_kept,
                       structure_indices=structure_indices_to_be_kept, to_form=to_form, copy_if_all=False)
    tmp_item = digest_output(tmp_item)

    return tmp_item

