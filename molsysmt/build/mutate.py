def mutate (item, residue_indices=None, to_residue_names=None, engine='PDBFixer', verbose=False):

    if engine=="PDBFixer":
        if syntaxis=="PDBFixer":

            if not hasattr(residue_indices, '__iter__'):
                residue_indices = [residue_indices]
            if not hasattr(to_residue_names, '__iter__'):
                to_residue_names = [to_residue_names]

            form_in = get_form(item)
            tmp_item = _convert(item, to_form="pdbfixer.PDBFixer")

            for residue_index, to_residue_name in zip(residue_indices, to_residue_names):

                from_residue_name = _get(tmp_item, target='residue', index=residue_index,
                                         residue_name=True)

                in_chain_id = _get(tmp_item, target='residue', index=residue_index,
                                         chain_id=True)

                mutation_string = "-".join([from_residue_name,str(residue_index),to_residue_name])
                if verbose: print(mutation_string)
                tmp_item.applyMutations([mutation_string], in_chain_id)

            tmp_item = _convert(tmp_item, to_form=form_in)

            return tmp_item

        else:
            raise NotImplementedError
    else:
        raise NotImplementedError

