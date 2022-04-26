from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np
from molsysmt._private.selection import selection_is_all
from molsysmt._private.strings import get_parenthesis
from re import findall
from inspect import stack

def select_standard(molecular_system, selection, syntaxis):

    #from .is_molecular_system import is_molecular_system
    from . import where_is_attribute
    from molsysmt.api_forms import dict_get

    if type(selection)==str:
        if selection_is_all(selection):
            aux_item, aux_form = where_is_attribute(molecular_system, 'n_atoms')
            n_atoms = dict_get[aux_form]['system']['n_atoms'](aux_item)
            atom_indices = np.arange(n_atoms, dtype='int64')
        else:
            selection = digest_selection(selection, syntaxis)
            aux_item, aux_form = where_is_attribute(molecular_system, 'atom_index')
            if syntaxis=='MolSysMT':
                atom_indices = select_with_MolSysMT(aux_item, selection)
            elif syntaxis=='MDTraj':
                atom_indices = select_with_MDTraj(aux_item, selection)
            elif syntaxis=='Amber':
                atom_indices = select_with_Amber(aux_item, selection)
            elif syntaxis=='ParmEd':
                atom_indices = select_with_ParmEd(aux_item, selection)
            elif syntaxis=='MDAnalysis':
                atom_indices = select_with_MDAnalysis(aux_item, selection)
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

def select_within(molecular_system, selection, structure_index, syntaxis):

    from molsysmt.structure.get_contacts import get_contacts

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

    atom_indices_1, atom_indices_2, cmap = get_contacts(molecular_system, selection=selection_1, selection_2=selection_2,
                                           structure_indices=structure_index, threshold=threshold, pbc=pbc, engine='MolSysMT',
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

def select(molecular_system, selection='all', structure_index=0, target='atom', mask=None,
        syntaxis='MolSysMT', to_syntaxis=None, check=True):

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

    from . import get_form, where_is_attribute, is_molecular_system
    from molsysmt.api_forms import dict_get

    if check:

        if not is_molecular_system(molecular_system):
            raise MolecularSystemNeededError()

        try:
            target=digest_target(target)
        except:
            raise WrongTargetError(target)

        try:
            syntaxis=digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)
        try:
            to_syntaxis=digest_to_syntaxis(to_syntaxis)
        except:
            raise WrongSyntaxisError(to_syntaxis)

        try:
            selection=digest_selection(selection, syntaxis)
        except:
            raise WrongSelectionError(selection)

    if mask is 'all':
        mask=None

    if type(selection)==str:

        while selection_with_special_subsentences(selection):

            sub_selection = selection_with_special_subsentences(selection)
            sub_atom_indices = select(molecular_system, sub_selection, syntaxis=syntaxis, check=False)
            selection = selection.replace(sub_selection, 'atom_index==@sub_atom_indices')

        if 'within' in selection:
            atom_indices = select_within(molecular_system, selection, structure_index, syntaxis)
        elif 'bonded to' in selection:
            atom_indices = select_bonded_to(molecular_system, selection, syntaxis)
        else:
            atom_indices = select_standard(molecular_system, selection, syntaxis)

    else:

        atom_indices = select_standard(molecular_system, selection, syntaxis)

    if target=='atom':
        output_indices = atom_indices
    elif target in ['group', 'component', 'chain', 'molecule', 'entity']:
        aux_item, aux_form = where_is_attribute(molecular_system, target+'_index', check=False)
        output_indices = dict_get[aux_form]['atom'][target+'_index'](aux_item, indices=atom_indices)
        output_indices = np.unique(output_indices)
    elif target=='bond':
        aux_item, aux_form = where_is_attribute(molecular_system, 'inner_bond_index', check=False)
        output_indices = dict_get[aux_form]['atom']['inner_bond_index'](aux_item, indices=atom_indices)
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

    from . import convert, get_form

    form_in = get_form(item)

    if form_in == 'mdtraj.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='mdtraj.Topology')

    atom_indices = tmp_item.select(selection)

    return atom_indices

def select_with_MDAnalysis(item, selection):

    from . import convert, get_form

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

    from . import convert, get_form

    form_in = get_form(item)

    if form_in == 'molsysmt.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='molsysmt.Topology')

    if '@' in selection:

        var_names = [ii[1:] for ii in findall(r"@[\w']+", selection)]
        first_var_name = var_names[0]

        f_with_vars = None

        for stack_frame in stack():
            if first_var_name in stack_frame[0].f_globals.keys():
                f_with_vars = stack_frame[0].f_globals
                break
            elif first_var_name in stack_frame[0].f_locals.keys():
                f_with_vars = stack_frame[0].f_localsa

        if f_with_vars is None:
            raise ValueError("An @variable in a selection sentence was not found")

        for var_name in var_names:
            var_value = f_with_vars[var_name]
            if type(var_value) in [np.ndarray]:
                var_value = list(var_value)
            locals()[var_name]=var_value

    indices = tmp_item.atoms_dataframe.query(selection).index.to_numpy()

    return indices

def select_with_ParmEd(item, selection):

    from . import convert, get_form
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

    from . import convert, get_form

    if form_in == 'pytraj.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='pytraj.Topology')

    raise NotImplementedError()

def indices_to_selection(molecular_system, indices, target='atom', syntaxis=None):

    syntaxis = digest_syntaxis(syntaxis)
    target = digest_target(target)

    output_string = ''

    if syntaxis=='NGLView':

        if target=='atom':
            output_string = '@'+','.join([str(ii) for ii in indices])
        elif target=='group':
            from molsysmt import get
            group_ids, chain_ids = get(molecular_system, target='group', indices=indices, group_id=True, chain_id=True)
            output_string = ' '.join([str(ii)+':'+str(jj) for ii,jj in zip(group_ids, chain_ids)])
        elif target=='chain':
            from molsysmt import get
            chain_ids = get(molecular_system, target='chain', indices=indices, chain_id=True)
            output_string = ' '.join([':'+ii for ii in chain_ids])
        else:
            raise NotImplementedError

    elif syntaxis=='MDTraj':

        if target=='atom':
            output_string = 'index '+' '.join([str(ii) for ii in indices])
        elif target=='group':
            output_string = 'resid '+' '.join([str(ii) for ii in indices])
        elif target=='chain':
            output_string = 'chainid '+' '.join([str(ii) for ii in indices])
        else:
            raise NotImplementedError

    else:

        raise NotImplementedError

    return output_string

