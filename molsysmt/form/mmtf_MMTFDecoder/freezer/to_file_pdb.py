from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError

def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None,
                check=True):

    if check:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check=check)

    if output_filename is None:
        raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.form.mmtf_MMTFDecoder.freezer.to_file_pdb")
    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = molsysmt_MolSys_to_file_pdb(tmp_item, output_filename=output_filename)

    return tmp_item

