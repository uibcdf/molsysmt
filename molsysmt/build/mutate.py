from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest()
def mutate(molecular_system, mutations=None, keys='group_index', selection="all", syntax='MolSysMT', engine='PDBFixer'):
    """
    To be written soon...
    """

    if engine=="PDBFixer":

        from molsysmt.basic import get, convert, get_form, contains, select

        if isinstance(mutations, (tuple, list)):

            group_indices = []
            to_group_names = []

            for mutation_string in mutations:
                old_group_name, group_id, new_group_name = mutation_string.split('-')
                aux_index, group_name = get(molecular_system, element='group',
                        selection='group_id=='+group_id, mask=selection,
                        group_index=True, group_name=True)
                if group_name[0].lower()!=old_group_name.lower():
                    raise ValueError(f'The group with id {group_id} is {group_name} and not {old_group_name}')
                group_indices.append(aux_index[0])
                to_group_names.append(new_group_name)


        elif isinstance(mutations, dict):
            if keys=='group_index':
                group_indices = list(mutations.keys())
                to_group_names = list(mutations.values())
            elif keys=='group_id':
                group_ids = list(mutations.keys())
                to_group_names = list(mutations.values())
                group_indices = []
                for ii in group_ids:
                    aux_indices = get(molecular_system, element='group',
                            selection='group_id==@ii', mask=selection,
                            group_index=True)
                    if aux_indices.shape[0]>1:
                        raise ValueError(f'There are multiple groups with the group_id: {ii}')
                    else:
                        group_indices.append(aux_indices[0])
            elif keys=='group_name':
                group_indices = []
                to_group_names = []
                for from_name, to_name in mutations.items():
                    aux_indices = get(molecular_system, element='group',
                            selection='group_name==@from_name', mask=selection, group_index=True)
                    for aux_index in aux_indices:
                        group_indices.append(aux_index)
                        to_group_names.append(to_name)

        to_group_names = [name.upper() for name in to_group_names]

        form_in = get_form(molecular_system)
        tmp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")

        from_group_names, group_ids, in_chain_ids = get(tmp_molecular_system, element='group',
                                                        selection=group_indices, group_name=True, group_id=True,
                                                        chain_id=True)

        for group_id, from_group_name, to_group_name, in_chain_id in zip(group_ids, from_group_names, to_group_names, in_chain_ids):
            mutation_string = "-".join([from_group_name,str(group_id),to_group_name])
            tmp_molecular_system.applyMutations([mutation_string], in_chain_id)

        tmp_molecular_system.findMissingResidues()
        tmp_molecular_system.findMissingAtoms()
        tmp_molecular_system.addMissingAtoms()

        if contains(tmp_molecular_system, selection='atom_type=="H"'):
            tmp_molecular_system.addMissingHydrogens(7.4)

        tmp_molecular_system = convert(tmp_molecular_system, to_form=form_in)

        return tmp_molecular_system

    else:
        raise NotImplementedMethodError

