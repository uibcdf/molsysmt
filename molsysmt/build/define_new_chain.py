from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np

@arg_digest()
def define_new_chain(molecular_system, selection='all', chain_id=None, chain_name=None, syntax='MolSysMT',
                     skip_digestion=False):
    """
    Defining a new chain from selected atoms.

    This function creates a new chain by assigning a unique `chain_id` and/or `chain_name` to a selection
    of atoms in a molecular system. The selected atoms are grouped into a new chain, which is appended
    to the existing list of chains in the system. This does not alter or remove any of the existing chains.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>` to be modified.

    selection : index, tuple, list, numpy.ndarray or str, default 'all'
        Selection of atoms to assign to the new chain. The selection can be given as a list, tuple,
        or NumPy array of atom indices (0-based integers), or as a string following one of the
        :ref:`supported selection syntaxes <Introduction_Selection>`.

    chain_id : str, optional
        Identifier of the new chain (e.g., 'A', 'B', 'C'). If not provided,
        a unique string `chain_id` will be automatically generated. Numeric inputs are
        converted to strings internally.

    chain_name : str, optional
        Descriptive name for the new chain. If not provided, the name will be left empty or
        automatically assigned.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case it is a string).

    Returns
    -------
    molecular system
        A modified molecular system with the selected atoms grouped into a newly defined chain.

    Raises
    ------
    NotSupportedFormError
        Raised if the molecular system has a non-supported form.

    ArgumentError
        Raised if any of the input values is invalid or incompatible.

    Notes
    -----
    - This function is useful when merging multiple molecules, redefining topology, or recovering
      proper chain segmentation after structural edits.
    - Chains are identified by their `chain_id` (unique identifier) and `chain_name` (optional descriptive label).
    - This explicit editing helper is part of the legacy editing path. New code
      should prefer `molsysmt.MolSysBuilder` or `molsysmt.build.editable(...)`
      for topology editing workflows targeting the `1.0` line.

    See Also
    --------
    :func:`molsysmt.basic.set`
        Setting attribute values in a molecular system.

    :func:`molsysmt.basic.info`
        Displaying a summary of elements and chain structure.

    :func:`molsysmt.build.merge`
        Merging multiple molecular systems, often requiring reassignment of chains.

    Examples
    --------
>>> import molsysmt as msm
>>> molsys = msm.convert('1TCD')
>>> msm.build.define_new_chain(molsys, selection='molecule_type=="water"', chain_name='C')
    >>> msm.get(molsys, element='chain', chain_name=True)
    ['A', 'B', 'C']

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:  
       :ref:`User Guide > Tools > Build > Define new chain <Tutorial_Define_new_chain>`

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, set, select, get_form
    from molsysmt.element.chain import all_chain_names
    from molsysmt._private.atom_indices import complementary_atom_indices
    from molsysmt._private.smonitor import ArgumentConflictError, InternalAlgorithmError

    chain_id = str(chain_id) if chain_id is not None else None
    chain_name = str(chain_name) if chain_name is not None else None

    if is_all(selection):

        if chain_id is None:
            chain_id = 'A'
        if chain_name is None:
            chain_name = 'A'

        set(molecular_system, element='atom', selection='all', chain_index=0, skip_digestion=True)
        set(molecular_system, element='chain', selection='all', chain_id=[chain_id], chain_name=[chain_name], skip_digestion=True)

    else:

        atom_indices = select(molecular_system, selection=selection)
        rest_atom_indices = complementary_atom_indices(molecular_system, atom_indices)

        former_chain_ids, former_chain_names = get(molecular_system, selection=rest_atom_indices, chain_id=True,
                                                   chain_name=True)
        former_chain_ids = np.array(former_chain_ids).astype(str)
        former_chain_names = np.array(former_chain_names).astype(str)

        aux_chain_ids = sorted(np.unique(former_chain_ids).tolist())
        aux_chain_names = sorted(np.unique(former_chain_names).tolist())

        if chain_id is None:
            for ii in all_chain_names:
                if ii not in aux_chain_ids:
                    chain_id = ii
                    break
            if chain_id is None:
                chain_id = str(len(aux_chain_ids))
        else:
            if chain_id in aux_chain_ids:
                raise ArgumentConflictError(
                    arg1="chain_id",
                    arg2="molecular_system",
                    reason=f"There is already a chain with chain_id={chain_id}.",
                    caller="molsysmt.build.define_new_chain"
                )

        if chain_name is None:
            for ii in all_chain_names:
                if ii not in aux_chain_names:
                    chain_name = ii
                    break
            if chain_name is None:
                raise InternalAlgorithmError(
                    reason="MolSysMT run out of chain names.",
                    caller="molsysmt.build.define_new_chain"
                )
        else:
            if chain_name in aux_chain_names:
                raise ArgumentConflictError(
                    arg1="chain_name",
                    arg2="molecular_system",
                    reason=f"There is already a chain with chain_name={chain_name}.",
                    caller="molsysmt.build.define_new_chain"
                )


        all_atom_indices = np.array(atom_indices+rest_atom_indices)
        all_chain_ids = np.array([chain_id for ii in atom_indices]+former_chain_ids.tolist()).astype(str)
        all_chain_names_array = np.array([chain_name for ii in atom_indices]+former_chain_names.tolist()).astype(str)
        sorted_indices = np.argsort(all_atom_indices)
        all_atom_indices = all_atom_indices[sorted_indices]
        all_chain_ids = all_chain_ids[sorted_indices]
        all_chain_names_array = all_chain_names_array[sorted_indices]

        chain_index=-1
        chain_ids_done=[]
        new_chain_indices=[]
        new_chain_ids=[]
        new_chain_names=[]
        aux_dict={}
        for ii,jj,kk in zip(all_atom_indices, all_chain_ids, all_chain_names_array):
            if jj not in chain_ids_done:
                chain_index+=1
                aux_dict[jj]=chain_index
                chain_ids_done.append(jj)
                new_chain_indices.append(chain_index)
                new_chain_ids.append(str(jj))
                new_chain_names.append(str(kk))
            else:
                new_chain_indices.append(aux_dict[jj])

        n_chains=chain_index+1

        form_in = get_form(molecular_system)
        if form_in=='molsysmt.MolSys':
            molecular_system.topology.reset_chains(n_chains=n_chains)
        elif form_in=='molsysmt.Topology':
            molecular_system.reset_chains(n_chains=n_chains)

        set(molecular_system, element='atom', selection='all', chain_index=new_chain_indices, skip_digestion=True)
        set(molecular_system, element='chain', selection='all', chain_id=new_chain_ids, chain_name=new_chain_names,
            skip_digestion=True)

        if form_in=='molsysmt.MolSys':
            molecular_system.topology.rebuild_chains(redefine_indices=False, redefine_ids=False, redefine_types=True, redefine_names=False)
        elif form_in=='molsysmt.Topology':
            molecular_system.rebuild_chains(redefine_indices=False, redefine_ids=False, redefine_types=True, redefine_names=False)

        del new_chain_indices, new_chain_ids, new_chain_names
        del all_atom_indices, all_chain_ids, all_chain_names
        del atom_indices, rest_atom_indices

    pass
