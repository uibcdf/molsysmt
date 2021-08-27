import numpy as np
from molsysmt.forms import dict_get
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.selection import selection_is_all
from molsysmt._private_tools.lists_and_tuples import list_to_csv_string
from molsysmt._private_tools.strings import get_parenthesis
from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.selection import indices_to_selection # basic_selection, within_selection, bonded_to_selection, parenthesis_substitution_in_selection
from molsysmt._private_tools.get_arguments import where_get_argument

def select_standard(molecular_system, selection, syntaxis):

    if type(selection)==str:
        if selection_is_all(selection):
            n_atoms = None
            for where_attribute in where_get_argument['n_atoms']:
                aux_item = getattr(molecular_system, where_attribute+'_item')
                aux_form = getattr(molecular_system, where_attribute+'_form')
                if aux_item is not None:
                    n_atoms = dict_get[aux_form]['system']['n_atoms'](aux_item)
                if n_atoms is not None:
                    break
            atom_indices = np.arange(n_atoms, dtype='int64')
        else:
            selection = digest_selection(selection, syntaxis)
            if syntaxis=='MolSysMT':
                atom_indices = select_with_MolSysMT(molecular_system.elements_item, selection)
            elif syntaxis=='MDTraj':
                atom_indices = select_with_MDTraj(molecular_system.elements_item, selection)
            elif syntaxis=='Amber':
                atom_indices = select_with_Amber(molecular_system.elements_item, selection)
            elif syntaxis=='ParmEd':
                atom_indices = select_with_ParmEd(molecular_system.elements_item, selection)
            elif syntaxis=='MDAnalysis':
                atom_indices = select_with_MDAnalysis(molecular_system.elements_item, selection)
            else:
                raise NotImplementedSyntaxisError()

    elif type(selection) in [int, np.int64, np.int32]:
        atom_indices = np.array([selection], dtype='int64')
    elif type(selection)==set:
        atom_indices = np.array(list(selection), dtype='int64')
    elif hasattr(selection, '__iter__'):
        atom_indices = np.array(selection, dtype='int64')
    else :
        atom_indices = None

    return atom_indices

def select_within(molecular_system, selection, frame_index, syntaxis):

    from molsysmt.structure.get_contact_map import get_contact_map

    not_within = False

    if "not within " in selection:
        selection_1, tmp_selection = selection.split(" not within ")
        not_within = True
    else:
        selection_1, tmp_selection = selection.split(" within ")

    pbc = False

    if "with pbc " in tmp_selection:
        pbc = True
        tmp_selection = tmp_selection.replace("with pbc ","")
    elif "without pbc " in tmp_selection:
        tmp_selection = tmp_selection.replace("without pbc ","")

    threshold, selection_2 = tmp_selection.split(" of ")

    atom_indices_1, atom_indices_2, cmap = contact_map(molecular_system, selection=selection_1, selection_2=selection_2,
                                           frame_indices=frame_index, threshold=threshold, pbc=pbc, engine='MolSysMT',
                                           syntaxis=syntaxis, output_atom_indices=True)

    if not_within:
        output = atom_indices_1[np.where(cmap.all(axis=2)[0]==False)[0]]
    else:
        output = atom_indices_1[np.where(cmap.any(axis=2)[0]==True)[0]]

    return output

def select_bonded_to(molecular_system, selection, syntaxis):

    from molsysmt.basic import get

    not_bonded=False

    if "not bonded to" in selection:
        selection_1, selection_2 = selection.split(" not bonded to")
        not_bonded=True
    else:
        selection_1, selection_2 = selection.split(" bonded to")

    atom_indices_1 = select(molecular_system, selection=selection_1, syntaxis=syntaxis)
    atom_indices_2 = get(molecular_system, 'atom', selection=selection_2, bonded_atoms=True, syntaxis=syntaxis)
    atom_indices_2 = np.unique(np.concatenate(atom_indices_2).ravel())

    if not_bonded:
        output = np.setdiff1d(atom_indices_1, atom_indices_2, assume_unique=True)
    else:
        output = np.intersect1d(atom_indices_1, atom_indices_2, assume_unique=True)

    return output

def select(molecular_system, selection='all', frame_index=0, target='atom', mask=None, syntaxis='MolSysMT', to_syntaxis=None):

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

    if mask is 'all':
        mask=None

    if type(selection)==str:

        while selection_with_special_subsentences(selection):

            sub_selection = selection_with_special_subsentences(selection)
            sub_atom_indices = select(molecular_system, sub_selection, syntaxis=syntaxis)
            #selection = selection.replace(sub_selection, 'atom_index==('+list_to_csv_string(sub_atom_indices)+')')
            selection = selection.replace(sub_selection, 'atom_index==@sub_atom_indices')

        if 'within' in selection:
            atom_indices = select_within(molecular_system, selection, frame_index, syntaxis)
        elif 'bonded to' in selection:
            atom_indices = select_bonded_to(molecular_system, selection, syntaxis)
        else:
            atom_indices = select_standard(molecular_system, selection, syntaxis)

    else:

        atom_indices = select_standard(molecular_system, selection, syntaxis)

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


def selection_with_special_subsentences(selection):

    output = None
    parenthesis = get_parenthesis(selection)
    for subselection in parenthesis:
        if ('within ' in subselection) or ('bonded to ' in subselection):
            output = subselection
            break

    return output

def select_with_MDTraj(item, selection):

    from molsysmt.basic import convert, get_form

    form_in = get_form(item)

    if form_in == 'mdtraj.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='mdtraj.Topology')

    atom_indices = tmp_item.select(selection)

    return atom_indices

def select_with_MDAnalysis(item, selection):

    from molsysmt.basic import convert, get_form

    form_in = get_form(item)

    if form_in == 'mdanalysis.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='mdanalysis.Topology')

    tmp_atomgroup = tmp_item.select_atoms(selection)
    atom_indices = tmp_atomgroup.atoms.ids
    del(tmp_atomgroup)

    return atom_indices

def select_with_MolSysMT(item, selection):

    from molsysmt.basic import convert, get_form
    from molsysmt.native.selector import elements_select

    form_in = get_form(item)

    if form_in == 'molsysmt.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='molsysmt.Topology')

    atom_indices = elements_select(tmp_item.atoms_dataframe, selection)

    return atom_indices

def select_with_ParmEd(item, selection):

    from molsysmt.basic import convert, get_form
    from parmed.amber import AmberMask as _AmberMask

    form_in = get_form(item)

    if form_in == 'parmed.Structure':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='parmed.Structure')

    atom_indices = list(_AmberMask(item,selection).Selected())
    del(_AmberMask)

    return tmp_atom_indices

def select_with_Amber(item, selection):

    from molsysmt.basic import convert, get_form

    if form_in == 'pytraj.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='pytraj.Topology')

    raise NotImplementedError()

