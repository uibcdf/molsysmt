def mutate (molecular_system, residue_indices=None, to_residue_names=None, engine='PDBFixer', verbose=False):


    if engine=="PDBFixer":

        from molsysmt.basic import get, convert, get_form

        if not hasattr(residue_indices, '__iter__'):
            residue_indices = [residue_indices]
        if not hasattr(to_residue_names, '__iter__'):
            to_residue_names = [to_residue_names]

        to_residue_names = [name.upper() for name in to_residue_names]

        form_in = get_form(molecular_system)
        tmp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")

        from_residue_names, residue_ids, in_chain_ids = get(tmp_molecular_system, target='group', indices=residue_indices,
                                             group_name=True, group_id=True, chain_id=True)

        for residue_id, from_residue_name, to_residue_name, in_chain_id in zip(residue_ids, from_residue_names, to_residue_names, in_chain_ids):
            mutation_string = "-".join([from_residue_name,str(residue_id),to_residue_name])
            if verbose: print(mutation_string)
            tmp_molecular_system.applyMutations([mutation_string], in_chain_id)

        tmp_molecular_system = convert(tmp_molecular_system, to_form=form_in)

        return tmp_molecular_system

    else:
        raise NotImplementedError

