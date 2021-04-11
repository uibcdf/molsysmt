import numpy as np
from molsysmt.forms import dict_get, dict_select
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.selection import selection_is_all
from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.selection import indices_to_selection # basic_selection, within_selection, bonded_to_selection, parenthesis_substitution_in_selection

#def _select_within(molecular_system, selection_1, selection_2, threshold, pbc, syntaxis):
#
#    from molsysmt.distances import neighbors_lists
#
#    output = neighbors_lists(molecular_system, selection_1=selection_1, selection_2=selection_2,
#                             threshold=threshold, pbc=pbc, engine='MolSysMT', syntaxis=syntaxis)
#    return output
#
#def _select_bonded_to(molecular_system, selection_1, selection_2, syntaxis):
#
#    pass

def select(molecular_system, selection='all', target='atom', mask=None, syntaxis='MolSysMT', to_syntaxis=None):

    # to_syntaxis: 'NGLView', 'MDTraj', ...

    """select(item, selection='all', target='atom', syntaxis='MolSysMT')

    Get the atom indices corresponding to a selection criterion.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any supported form (see: :doc:`/Forms`). The object being acted on by the method.

    selection: str, default='all'
       Selection criterion given by means of a string following any of the selection syntaxis parsable by MolSysMT.

    mask: list, tuple, numpy array or None. default=None
       XXX

    target: str, default='atom'
       The output indices list can correspond to 'atom', 'group', 'component', 'molecule', 'chain',
       'entity' or 'bond' indices.

    syntaxis: str, default='MolSysMT'
       Syntaxis used to write the argument `selection`. The current options supported by MolSysMt
       can be found in :doc:`/Atoms_Selection`.

    Returns
    -------

    Numpy array of integers
        List of indices in agreement with the selection criterion applied over `item`. The nature
        of the indices is chosen with the input argument 'output_indices': 'atom' (default),
        'group', 'component', 'molecule', 'chain' or 'entity'.

    Examples
    --------

    :doc:`/Atoms_Selection`

    See Also
    --------

    Notes
    -----

    """

    molecular_system = digest_molecular_system(molecular_system)
    target = digest_target(target)
    syntaxis = digest_syntaxis(syntaxis)
    selection = digest_selection(selection, syntaxis)
    to_syntaxis = digest_to_syntaxis(to_syntaxis)

    #if 'within' in selection or 'bonded to' in selection:

    #    from molsysmt._private_tools.selection import parenthesis_substitution_in_selection



    #    pass

    #if 'within' in selection:

    #    selection_1, selection_2, threshold, pbc = parse_within_selection(selection)


    if mask is 'all':
        mask=None

    if type(selection)==str:
        if selection in ['all', 'All', 'ALL']:
            n_atoms = dict_get[molecular_system.elements_form]['system']['n_atoms'](molecular_system.elements_item)
            atom_indices = np.arange(n_atoms, dtype='int64')
        else:
            selection = digest_selection(selection, syntaxis)
            atom_indices = dict_select[molecular_system.elements_form][syntaxis](molecular_system.elements_item, selection)
    elif type(selection) in [int, np.int64, np.int]:
        atom_indices = np.array([selection], dtype='int64')
    elif hasattr(selection, '__iter__'):
        atom_indices = np.array(selection, dtype='int64')
    else :
        atom_indices = None

    output_indices = []

    if target=='atom':
        output_indices = atom_indices
    elif target in ['group', 'component', 'chain', 'molecule', 'entity']:
        output_indices = dict_get[molecular_system.elements_form]['atom'][target+'_index'](molecular_system.elements_item, indices=atom_indices)
        output_indices = np.unique(output_indices)
    elif target=='bond':
        output_indices = dict_get[molecular_system.elements_form]['atom']['inner_bond_index'](molecular_system.elements_item, indices=atom_indices)
    else:
        raise NotImplementedError()

    if mask is not None:
        output_indices = np.intersect1d(output_indices, mask, assume_unique=True)

    if to_syntaxis is None:
        return output_indices
    else:
        return indices_to_selection(molecular_system, output_indices, target=target, syntaxis=to_syntaxis)

