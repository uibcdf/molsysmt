def to_openmm_Topology(item, atom_indices='all', check=True):

    if check:

        try:
            is_file_prmtop(item)
        except:
            raise WrongFormError('file:prmtop')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_openmm_AmberPrmtopFile
    from ..openmm_AmberPrmtopFile import to_openmm_Topology as openmm_AmberPrmtopFile_to_openmm_Topology

    tmp_item = to_openmm_AmberPrmtopFile(item, check=False)
    tmp_item = openmm_AmberPrmtopFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, check=False)

    return tmp_item

